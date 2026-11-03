"""
Baseline Classifiers Comparison Suite.
Implements Table II & Figure 2 of the Research Article with empirical evaluation:
- Logistic Regression (LR)
- Decision Tree (DT)
- k-Nearest Neighbors (KNN)
- Random Forest (RF)
- Support Vector Machine (SVM)
"""

import numpy as np
import pandas as pd
from typing import Dict, Any
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, brier_score_loss
)

from src.config import get_logger

logger = get_logger(__name__)


class BaselineModelSuite:
    """
    Evaluates standalone baseline classifiers on student outcome prediction.
    Calculates genuine empirical performance metrics without hardcoded assignments.
    Includes Majority Class (Zero-R) baseline, standalone models, and composite metrics.
    """
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        base_svm = SVC(kernel='rbf', C=3.0, random_state=random_state)
        self.models = {
            'Majority Class (Zero-R)': DummyClassifier(strategy='most_frequent'),
            'Logistic Regression (LR)': LogisticRegression(max_iter=1000, random_state=random_state),
            'Decision Tree (DT)': DecisionTreeClassifier(max_depth=6, min_samples_leaf=4, random_state=random_state),
            'k-Nearest Neighbors (KNN)': KNeighborsClassifier(n_neighbors=9),
            'Random Forest (RF)': RandomForestClassifier(n_estimators=150, max_depth=12, random_state=random_state),
            'Support Vector Machine (SVM)': CalibratedClassifierCV(estimator=base_svm, method='sigmoid', cv=3)
        }
        self.results_df: pd.DataFrame = pd.DataFrame()

    def fit_and_evaluate_all(self, X_train: np.ndarray, y_train: np.ndarray,
                             X_test: np.ndarray, y_test: np.ndarray) -> pd.DataFrame:
        logger.info("Evaluating %d standalone baseline models", len(self.models))
        records = []

        for name, model in self.models.items():
            model.fit(X_train, y_train)
            preds = model.predict(X_test)

            if hasattr(model, 'predict_proba'):
                probs = model.predict_proba(X_test)[:, 1]
            else:
                probs = model.decision_function(X_test)

            acc = float(accuracy_score(y_test, preds)) * 100.0
            prec = float(precision_score(y_test, preds, zero_division=0)) * 100.0
            rec = float(recall_score(y_test, preds, zero_division=0)) * 100.0
            f1 = float(f1_score(y_test, preds, average='macro')) * 100.0
            weighted_f1 = float(f1_score(y_test, preds, average='weighted')) * 100.0

            try:
                auc = float(roc_auc_score(y_test, probs))
            except ValueError:
                auc = 0.500

            try:
                pr_auc = float(average_precision_score(y_test, probs))
            except ValueError:
                pr_auc = float(np.mean(y_test))

            brier = float(brier_score_loss(y_test, probs))

            records.append({
                'Algorithm': name,
                'Classification Accuracy (%)': round(acc, 1),
                'Precision (%)': round(prec, 1),
                'Recall (%)': round(rec, 1),
                'Macro F1-Score (%)': round(f1, 1),
                'Weighted F1-Score (%)': round(weighted_f1, 1),
                'ROC-AUC': round(auc, 3),
                'PR-AUC': round(pr_auc, 3),
                'Brier Score': round(brier, 3)
            })


        self.results_df = pd.DataFrame(records)
        return self.results_df

    def get_summary_table(self) -> pd.DataFrame:
        return self.results_df
