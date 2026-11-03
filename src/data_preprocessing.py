"""
Multi-Modal Data Preprocessing Pipeline.
Implements Section III-A (Eq. 1) with strict temporal leakage prevention and SOLID principles.

Splits feature space into:
- Pre-College Academic Indicators (x_i^(acad))
- Socio-Economic & Demographic Indicators (x_i^(socio), F_imm)
- College Behavioral & Co-Curricular Indicators (x_i^(behav), F_mut)
- College Academic Longitudinal Indicators (x_i^(coll_acad), F_mut)
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import List, Tuple, Optional
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from src.config import (
    STAGE1_NUMERIC_FEATURES,
    STAGE1_CATEGORICAL_FEATURES,
    COLLEGE_ACADEMIC_FEATURES,
    BEHAVIORAL_FEATURES,
    TARGET_STAGE_1,
    TARGET_STAGE_2,
    TARGET_STAGE_3,
    ENGINEERING_BRANCHES,
    ACADEMIC_TIERS,
    get_logger
)

logger = get_logger(__name__)


class MultiModalPreprocessor:
    """
    Transforms multi-modal student tabular data into stage-specialized feature matrices.
    Enforces temporal integrity: Stage 1 does NOT access future college behavioral metrics.
    """
    def __init__(self):
        # Stage 1: Strictly Pre-College Admissions Data
        self.stage1_num = list(STAGE1_NUMERIC_FEATURES)
        self.stage1_cat = list(STAGE1_CATEGORICAL_FEATURES)

        # Stage 2: Admissions Data + Behavioral Habits + Midterm + Predicted Discipline
        self.stage2_num = self.stage1_num + list(BEHAVIORAL_FEATURES) + ['midterm_score']
        self.stage2_cat = self.stage1_cat + ['recommended_branch']

        # Stage 3: Complete Augmented Profile + Predicted Discipline + Predicted Academic Tier
        self.stage3_num = self.stage1_num + list(BEHAVIORAL_FEATURES) + list(COLLEGE_ACADEMIC_FEATURES)
        # Deduplicate while preserving order
        self.stage3_num = list(dict.fromkeys(self.stage3_num))
        self.stage3_cat = self.stage1_cat + ['recommended_branch', 'academic_performance']

        # Encoders & Transformers
        self.branch_encoder = LabelEncoder()
        self.academic_perf_encoder = LabelEncoder()

        self.stage1_transformer: Optional[ColumnTransformer] = None
        self.stage2_transformer: Optional[ColumnTransformer] = None
        self.stage3_transformer: Optional[ColumnTransformer] = None
        self.is_fitted: bool = False

    def _build_column_transformer(self, num_cols: List[str], cat_cols: List[str]) -> ColumnTransformer:
        num_pipeline = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        cat_pipeline = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])
        return ColumnTransformer(
            transformers=[
                ('num', num_pipeline, num_cols),
                ('cat', cat_pipeline, cat_cols)
            ],
            remainder='drop'
        )

    def fit(self, df: pd.DataFrame) -> "MultiModalPreprocessor":
        """Fits transformers on training data only to prevent data leakage."""
        logger.info("Fitting MultiModalPreprocessor transformers on %d samples", len(df))

        # Fit Stage 1 transformer
        self.stage1_transformer = self._build_column_transformer(self.stage1_num, self.stage1_cat)
        self.stage1_transformer.fit(df)

        # Fit Stage 2 transformer
        self.stage2_transformer = self._build_column_transformer(self.stage2_num, self.stage2_cat)
        self.stage2_transformer.fit(df)

        # Fit Stage 3 transformer
        self.stage3_transformer = self._build_column_transformer(self.stage3_num, self.stage3_cat)
        self.stage3_transformer.fit(df)

        # Fit Label Encoders with canonical classes to guarantee stable index mapping
        self.branch_encoder.fit(ENGINEERING_BRANCHES)
        self.academic_perf_encoder.fit(ACADEMIC_TIERS)

        self.is_fitted = True
        return self

    def transform_stage1(self, df: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted or self.stage1_transformer is None:
            raise RuntimeError("Preprocessor must be fitted before transforming.")
        return self.stage1_transformer.transform(df)

    def transform_stage2(self, df: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted or self.stage2_transformer is None:
            raise RuntimeError("Preprocessor must be fitted before transforming.")
        return self.stage2_transformer.transform(df)

    def transform_stage3(self, df: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted or self.stage3_transformer is None:
            raise RuntimeError("Preprocessor must be fitted before transforming.")
        return self.stage3_transformer.transform(df)

    def get_feature_names_stage3(self) -> List[str]:
        """Returns ordered feature names for Stage 3 matrix, utilized by SHAP."""
        if not self.is_fitted or self.stage3_transformer is None:
            raise RuntimeError("Preprocessor must be fitted before retrieving feature names.")
        cat_encoder = self.stage3_transformer.named_transformers_['cat'].named_steps['onehot']
        cat_names = cat_encoder.get_feature_names_out(self.stage3_cat)
        return list(self.stage3_num) + list(cat_names)

    def save(self, filepath: str) -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self, filepath)
        logger.info("Preprocessor successfully persisted to %s", filepath)

    @staticmethod
    def load(filepath: str) -> "MultiModalPreprocessor":
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Serialized preprocessor file not found: {filepath}")
        return joblib.load(filepath)
