"""
Stage 2: Longitudinal Academic Performance Forecasting (XGBoost & Gradient Boosting)
Implements Section III-B (Eq. 3) of the Research Article.
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Optional, List, Dict, Any
from sklearn.ensemble import GradientBoostingClassifier
import xgboost as xgb
from sklearn.metrics import accuracy_score, f1_score, classification_report

from src.config import get_logger

logger = get_logger(__name__)


class AcademicForecaster:
    """
    Ensemble of extreme gradient boosted decision trees (XGBoost) and Gradient Boosting
    to forecast longitudinal semester academic performance tiers.
    """
    def __init__(self, xgb_weight: float = 0.6, random_state: int = 42):
        self.xgb_weight = float(xgb_weight)
        self.gb_weight = 1.0 - self.xgb_weight
        self.random_state = random_state

        self.xgb_model = xgb.XGBClassifier(
            n_estimators=160,
            max_depth=6,
            learning_rate=0.08,
            subsample=0.85,
            colsample_bytree=0.85,
            reg_alpha=0.1,
            reg_lambda=1.2,
            random_state=self.random_state,
            eval_metric='mlogloss'
        )

        self.gb_model = GradientBoostingClassifier(
            n_estimators=130,
            learning_rate=0.08,
            max_depth=5,
            subsample=0.85,
            random_state=self.random_state
        )

        self.classes_: Optional[List[str]] = None
        self.feature_names_: Optional[List[str]] = None

    def fit(self, X: np.ndarray, y: np.ndarray, class_names: Optional[List[str]] = None,
            feature_names: Optional[List[str]] = None) -> "AcademicForecaster":
        logger.info("Fitting AcademicForecaster (XGBoost + GradientBoosting) on %d samples", len(X))
        self.classes_ = class_names if class_names is not None else list(np.unique(y))
        self.feature_names_ = feature_names

        self.xgb_model.fit(X, y)
        self.gb_model.fit(X, y)
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        xgb_proba = self.xgb_model.predict_proba(X)
        gb_proba = self.gb_model.predict_proba(X)
        blended = self.xgb_weight * xgb_proba + self.gb_weight * gb_proba
        return blended

    def predict(self, X: np.ndarray) -> np.ndarray:
        proba = self.predict_proba(X)
        return np.argmax(proba, axis=1)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        preds = self.predict(X_test)
        acc = float(accuracy_score(y_test, preds))
        macro_f1 = float(f1_score(y_test, preds, average='macro'))
        target_names = [str(c) for c in self.classes_] if self.classes_ is not None else None
        report = classification_report(y_test, preds, target_names=target_names, output_dict=True)
        return {
            'accuracy': acc,
            'macro_f1': macro_f1,
            'report': report
        }

    def save(self, filepath: str) -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self, filepath)
        logger.info("AcademicForecaster saved to %s", filepath)

    @staticmethod
    def load(filepath: str) -> "AcademicForecaster":
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        return joblib.load(filepath)
