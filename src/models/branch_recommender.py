"""
Stage 1: Post-Intermediate Academic Branch Recommendation (Random Forest Ensemble)
Implements Section III-B (Eq. 2) of the Research Article.
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Optional, List, Dict, Any
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score

from src.config import get_logger

logger = get_logger(__name__)


class BranchRecommender:
    """
    Random Forest discipline recommendation classifier.
    Operates on pre-college intermediate admissions data to recommend optimal engineering branch.
    """
    def __init__(self, n_estimators: int = 150, max_depth: int = 12, random_state: int = 42):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state
        self.model = RandomForestClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            min_samples_split=4,
            min_samples_leaf=2,
            class_weight='balanced',
            random_state=self.random_state
        )
        self.classes_: Optional[List[str]] = None
        self.feature_names_: Optional[List[str]] = None

    def fit(self, X: np.ndarray, y: np.ndarray, class_names: Optional[List[str]] = None,
            feature_names: Optional[List[str]] = None) -> "BranchRecommender":
        logger.info("Fitting BranchRecommender (Random Forest) on %d samples", len(X))
        self.model.fit(X, y)
        self.classes_ = class_names if class_names is not None else list(self.model.classes_)
        self.feature_names_ = feature_names
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)

    def get_feature_importances(self) -> pd.DataFrame:
        """Returns sorted impurity-based feature importances."""
        importances = self.model.feature_importances_
        if self.feature_names_ is not None and len(self.feature_names_) == len(importances):
            return pd.DataFrame({
                'feature': self.feature_names_,
                'importance': importances
            }).sort_values(by='importance', ascending=False)
        return pd.DataFrame({'importance': importances})

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
        logger.info("BranchRecommender saved to %s", filepath)

    @staticmethod
    def load(filepath: str) -> "BranchRecommender":
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        return joblib.load(filepath)
