"""
Stage 3: Hybrid Campus Placement Prediction (XGBoost + RBF-SVM)
Implements Section III-B (Eq. 4) of the Research Article with mathematical calibration.

Mathematical Formulation:
P_hybrid(y_i^(p) = 1 | z_i) = α P_XGB(y_i^(p) = 1 | z_i) + (1 - α) σ(A * f_SVM(z_i) + B)
where σ(A * f_SVM(z_i) + B) is the Platt-scaled SVM margin probability.
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Optional, List, Dict, Any
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import StratifiedKFold
import xgboost as xgb
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, brier_score_loss, log_loss,
    classification_report
)

from src.config import get_logger

logger = get_logger(__name__)


def compute_expected_calibration_error(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> Dict[str, Any]:
    """
    Computes Expected Calibration Error (ECE) and reliability diagram bins:
    ECE = sum_{m=1}^M (|B_m| / N) * |acc(B_m) - conf(B_m)|
    """
    y_true = np.asarray(y_true).astype(int)
    y_prob = np.asarray(y_prob).astype(float)
    bin_boundaries = np.linspace(0.0, 1.0, n_bins + 1)
    
    bin_accs = []
    bin_confs = []
    bin_counts = []
    ece = 0.0
    n = len(y_true)

    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]
        if i == n_bins - 1:
            in_bin = (y_prob >= bin_lower) & (y_prob <= bin_upper)
        else:
            in_bin = (y_prob >= bin_lower) & (y_prob < bin_upper)

        count = int(np.sum(in_bin))
        bin_counts.append(count)
        if count > 0:
            acc = float(np.mean(y_true[in_bin]))
            conf = float(np.mean(y_prob[in_bin]))
            bin_accs.append(acc)
            bin_confs.append(conf)
            ece += (count / n) * abs(acc - conf)
        else:
            bin_accs.append(0.0)
            bin_confs.append((bin_lower + bin_upper) / 2.0)

    return {
        'ece': float(ece),
        'bin_accuracies': bin_accs,
        'bin_confidences': bin_confs,
        'bin_counts': bin_counts,
        'bin_boundaries': bin_boundaries.tolist()
    }


class HybridPlacementPredictor:
    """
    Hybrid calibrated ensemble combining extreme gradient boosted trees (XGBoost)
    with a maximum-margin Radial Basis Function Kernel SVM.
    Features end-to-end ensemble calibration and reliability metrics.
    """
    def __init__(self, alpha: float = 0.55, random_state: int = 42):
        self.alpha = float(alpha)
        self.random_state = random_state

        # XGBoost Classifier
        self.xgb_model = xgb.XGBClassifier(
            n_estimators=180,
            max_depth=5,
            learning_rate=0.06,
            subsample=0.85,
            colsample_bytree=0.85,
            reg_alpha=0.15,
            reg_lambda=1.5,
            random_state=self.random_state,
            eval_metric='logloss'
        )

        # Base RBF Kernel SVM with Component Platt Scaling
        base_svm = SVC(
            C=3.0,
            kernel='rbf',
            gamma='scale',
            decision_function_shape='ovr',
            random_state=self.random_state
        )
        self.calibrated_svm = CalibratedClassifierCV(
            estimator=base_svm,
            method='sigmoid',
            cv=3
        )

        # Final Ensemble-Level Calibrator
        self.ensemble_calibrator = LogisticRegression(C=1.0, solver='lbfgs', random_state=self.random_state)
        self.feature_names_: Optional[List[str]] = None
        self.is_fitted: bool = False

    def _get_raw_hybrid_proba(self, X: np.ndarray) -> np.ndarray:
        p_xgb = self.xgb_model.predict_proba(X)
        p_svm = self.calibrated_svm.predict_proba(X)
        return self.alpha * p_xgb + (1.0 - self.alpha) * p_svm

    def fit(self, X: np.ndarray, y: np.ndarray, feature_names: Optional[List[str]] = None) -> "HybridPlacementPredictor":
        """
        Fits XGBoost, SVM, and the ensemble-level calibrator using Out-of-Fold predictions.
        Guarantees that calibration is evaluated and fitted on proper validation folds.
        """
        logger.info("Fitting HybridPlacementPredictor (XGBoost + RBF-SVM) on %d samples", len(X))
        self.feature_names_ = feature_names

        # 1. Fit component models on full X, y
        self.xgb_model.fit(X, y)
        self.calibrated_svm.fit(X, y)

        # 2. Fit ensemble-level calibrator on stratified out-of-fold blended probabilities
        skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=self.random_state)
        oof_raw_probs = np.zeros(len(y), dtype=float)

        for trn_idx, val_idx in skf.split(X, y):
            fold_xgb = xgb.XGBClassifier(
                n_estimators=120, max_depth=5, learning_rate=0.06,
                subsample=0.85, colsample_bytree=0.85, random_state=self.random_state,
                eval_metric='logloss'
            )
            fold_svm = CalibratedClassifierCV(
                estimator=SVC(C=3.0, kernel='rbf', gamma='scale', random_state=self.random_state),
                method='sigmoid', cv=2
            )
            fold_xgb.fit(X[trn_idx], y[trn_idx])
            fold_svm.fit(X[trn_idx], y[trn_idx])

            p_x = fold_xgb.predict_proba(X[val_idx])[:, 1]
            p_s = fold_svm.predict_proba(X[val_idx])[:, 1]
            oof_raw_probs[val_idx] = self.alpha * p_x + (1.0 - self.alpha) * p_s

        # Fit logistic ensemble calibrator on OOF logit margins
        eps = 1e-6
        clipped_p = np.clip(oof_raw_probs, eps, 1.0 - eps)
        oof_logits = np.log(clipped_p / (1.0 - clipped_p)).reshape(-1, 1)
        self.ensemble_calibrator.fit(oof_logits, y)

        self.is_fitted = True
        return self

    def predict_proba_uncalibrated(self, X: np.ndarray) -> np.ndarray:
        """Returns raw blended probability before ensemble calibration."""
        if not self.is_fitted:
            raise RuntimeError("HybridPlacementPredictor must be fitted before predict_proba.")
        return self._get_raw_hybrid_proba(X)

    def predict_proba(self, X: np.ndarray, calibrated: bool = True) -> np.ndarray:
        """
        Calculates calibrated hybrid probability array [[P(y=0), P(y=1)]].
        Applies ensemble-level Platt calibration over the blended logits.
        """
        if not self.is_fitted:
            raise RuntimeError("HybridPlacementPredictor must be fitted before predict_proba.")
        raw_p = self._get_raw_hybrid_proba(X)
        if not calibrated or not hasattr(self, 'ensemble_calibrator') or self.ensemble_calibrator is None:
            return raw_p

        eps = 1e-6
        clipped_p = np.clip(raw_p[:, 1], eps, 1.0 - eps)
        logits = np.log(clipped_p / (1.0 - clipped_p)).reshape(-1, 1)
        return self.ensemble_calibrator.predict_proba(logits)


    def predict(self, X: np.ndarray, threshold: float = 0.50) -> np.ndarray:
        proba = self.predict_proba(X)[:, 1]
        return (proba >= threshold).astype(int)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray, threshold: float = 0.50) -> Dict[str, Any]:
        """Calculates comprehensive empirical metrics from actual predictions."""
        preds = self.predict(X_test, threshold=threshold)
        probs_calib = self.predict_proba(X_test, calibrated=True)[:, 1]
        probs_raw = self.predict_proba_uncalibrated(X_test)[:, 1]

        acc = float(accuracy_score(y_test, preds))
        prec = float(precision_score(y_test, preds, zero_division=0))
        rec = float(recall_score(y_test, preds, zero_division=0))
        macro_f1 = float(f1_score(y_test, preds, average='macro'))
        weighted_f1 = float(f1_score(y_test, preds, average='weighted'))
        roc_auc = float(roc_auc_score(y_test, probs_calib))
        pr_auc = float(average_precision_score(y_test, probs_calib))
        brier_calib = float(brier_score_loss(y_test, probs_calib))
        brier_raw = float(brier_score_loss(y_test, probs_raw))
        ll_calib = float(log_loss(y_test, probs_calib))
        ll_raw = float(log_loss(y_test, probs_raw))

        ece_calib_info = compute_expected_calibration_error(y_test, probs_calib)
        ece_raw_info = compute_expected_calibration_error(y_test, probs_raw)

        report = classification_report(y_test, preds, target_names=['Not Placed', 'Placed'], output_dict=True)

        return {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'macro_f1': macro_f1,
            'weighted_f1': weighted_f1,
            'roc_auc': roc_auc,
            'pr_auc': pr_auc,
            'brier_score': brier_calib,
            'brier_score_uncalibrated': brier_raw,
            'log_loss': ll_calib,
            'log_loss_uncalibrated': ll_raw,
            'ece': ece_calib_info['ece'],
            'ece_uncalibrated': ece_raw_info['ece'],
            'reliability_data': ece_calib_info,
            'report': report
        }


    def save(self, filepath: str) -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self, filepath)
        logger.info("HybridPlacementPredictor saved to %s", filepath)

    @staticmethod
    def load(filepath: str) -> "HybridPlacementPredictor":
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        return joblib.load(filepath)
