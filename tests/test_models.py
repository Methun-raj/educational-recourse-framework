"""
Unit tests for preprocessing and individual stage models.
"""

import pytest
import numpy as np
import pandas as pd
import os
import sys

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.generate_dataset import generate_multimodal_student_dataset
from src.data_preprocessing import MultiModalPreprocessor
from src.models.branch_recommender import BranchRecommender
from src.models.academic_forecaster import AcademicForecaster
from src.models.placement_predictor import HybridPlacementPredictor
from src.models.baseline_models import BaselineModelSuite

@pytest.fixture(scope="module")
def sample_data():
    return generate_multimodal_student_dataset(n_samples=250, random_seed=42)

def test_preprocessor_fitting(sample_data):
    prep = MultiModalPreprocessor()
    prep.fit(sample_data)
    assert prep.is_fitted

    X1 = prep.transform_stage1(sample_data)
    X2 = prep.transform_stage2(sample_data)
    X3 = prep.transform_stage3(sample_data)

    assert X1.shape[0] == len(sample_data)
    assert X2.shape[0] == len(sample_data)
    assert X3.shape[0] == len(sample_data)
    # Stage 3 incorporates all features, so dimension is largest
    assert X3.shape[1] >= X2.shape[1] >= X1.shape[1]

def test_stage1_branch_recommender(sample_data):
    prep = MultiModalPreprocessor().fit(sample_data)
    X1 = prep.transform_stage1(sample_data)
    y1 = prep.branch_encoder.transform(sample_data['recommended_branch'].astype(str))

    model = BranchRecommender(n_estimators=30, random_state=42)
    model.fit(X1, y1, class_names=list(prep.branch_encoder.classes_))

    preds = model.predict(X1)
    probs = model.predict_proba(X1)

    assert len(preds) == len(X1)
    assert probs.shape == (len(X1), len(prep.branch_encoder.classes_))
    assert np.allclose(probs.sum(axis=1), 1.0)

def test_stage2_academic_forecaster(sample_data):
    prep = MultiModalPreprocessor().fit(sample_data)
    X2 = prep.transform_stage2(sample_data)
    y2 = prep.academic_perf_encoder.transform(sample_data['academic_performance'].astype(str))

    model = AcademicForecaster(random_state=42)
    model.fit(X2, y2, class_names=list(prep.academic_perf_encoder.classes_))

    preds = model.predict(X2)
    probs = model.predict_proba(X2)

    assert len(preds) == len(X2)
    assert probs.shape[1] == len(prep.academic_perf_encoder.classes_)
    assert np.allclose(probs.sum(axis=1), 1.0)

def test_stage3_hybrid_placement_predictor(sample_data):
    prep = MultiModalPreprocessor().fit(sample_data)
    X3 = prep.transform_stage3(sample_data)
    y3 = sample_data['placement_status'].values

    model = HybridPlacementPredictor(alpha=0.55, random_state=42)
    model.fit(X3, y3, feature_names=prep.get_feature_names_stage3())

    preds = model.predict(X3)
    probs_calib = model.predict_proba(X3, calibrated=True)
    probs_raw = model.predict_proba_uncalibrated(X3)
    eval_res = model.evaluate(X3, y3)

    assert len(preds) == len(X3)
    assert probs_calib.shape == (len(X3), 2)
    assert np.all((probs_calib >= 0.0) & (probs_calib <= 1.0))
    assert np.allclose(probs_calib.sum(axis=1), 1.0)
    assert 'pr_auc' in eval_res
    assert 'brier_score' in eval_res
    assert 'ece' in eval_res
    assert 'log_loss' in eval_res
    assert eval_res['ece'] >= 0.0

def test_baseline_models_suite(sample_data):
    prep = MultiModalPreprocessor().fit(sample_data)
    X3 = prep.transform_stage3(sample_data)
    y3 = sample_data['placement_status'].values

    suite = BaselineModelSuite(random_state=42)
    results_df = suite.fit_and_evaluate_all(X3[:180], y3[:180], X3[180:], y3[180:])

    assert len(results_df) >= 5
    assert 'Classification Accuracy (%)' in results_df.columns
    assert 'ROC-AUC' in results_df.columns
    assert 'Brier Score' in results_df.columns
    assert 'Weighted F1-Score (%)' in results_df.columns

def test_real_world_dataset_evaluation():
    from evaluation.evaluate_real_world import evaluate_college_placement_real
    res_df = evaluate_college_placement_real()
    assert len(res_df) >= 7
    assert 'Proposed Hybrid XGBoost + SVM' in res_df['Algorithm'].values
    hybrid_row = res_df[res_df['Algorithm'] == 'Proposed Hybrid XGBoost + SVM'].iloc[0]
    assert hybrid_row['Classification Accuracy (%)'] >= 80.0
    assert hybrid_row['ROC-AUC'] >= 0.85

