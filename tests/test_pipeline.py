"""
Integration tests for the Hierarchical Multi-Stage Pipeline and Counterfactual Recourse.
"""

import pytest
import os
import sys
import pandas as pd
import numpy as np

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.generate_dataset import generate_multimodal_student_dataset
from src.pipeline import HierarchicalMultiStagePipeline
from src.config import IMMUTABLE_FEATURES

@pytest.fixture(scope="module")
def trained_pipeline():
    df = generate_multimodal_student_dataset(n_samples=300, random_seed=42)
    pipe = HierarchicalMultiStagePipeline(random_state=42)
    pipe.train(df, n_splits=3)
    return pipe, df

def test_pipeline_sequential_inference(trained_pipeline):
    pipe, df = trained_pipeline
    sample_student = df.iloc[0].to_dict()

    res = pipe.predict_student(sample_student)

    assert 'stage1' in res
    assert 'recommended_branch' in res['stage1']
    assert 'stage2' in res
    assert 'forecasted_academic_tier' in res['stage2']
    assert 'stage3' in res
    assert 'placement_prediction' in res['stage3']
    assert 0.0 <= res['stage3']['placement_probability'] <= 1.0

def test_counterfactual_recourse_strict_immutability(trained_pipeline):
    pipe, df = trained_pipeline
    at_risk_row = df.iloc[0]

    recourse = pipe.recourse_engine.generate_recourse(at_risk_row, target_prob=0.80)

    orig = recourse['original_profile']
    cf = recourse['counterfactual_profile']

    # 1. Strict immutability assertions (Eq. 6)
    for imm_feat in IMMUTABLE_FEATURES:
        assert cf[imm_feat] == orig[imm_feat], f"Violation: Immutable feature {imm_feat} was altered!"

    # 2. Probability elevation check: recourse profile must improve probability
    assert recourse['target_probability'] > recourse['baseline_probability']
    assert 'disclaimer' in recourse

def test_shap_waterfall_attribution(trained_pipeline):
    pipe, df = trained_pipeline
    sample_student = df.iloc[0].to_dict()
    res = pipe.predict_student(sample_student)

    shap_df = res['local_shap']
    assert shap_df is not None
    assert 'feature' in shap_df.columns
    assert 'shap_value' in shap_df.columns
    assert len(shap_df) > 0

def test_ground_truth_label_invariance(trained_pipeline):
    """
    Critical Test: Confirms that passing ground-truth intermediate labels does NOT change
    downstream predictions. The cascade must strictly compute its own intermediate states.
    """
    pipe, df = trained_pipeline
    sample_student = df.iloc[0].to_dict()

    # Base prediction without intermediate labels
    clean_sample = {k: v for k, v in sample_student.items() if k not in ['recommended_branch', 'academic_performance']}
    res_clean = pipe.predict_student(clean_sample)

    # Injected sample with arbitrary contradictory intermediate labels
    polluted_sample = dict(clean_sample)
    polluted_sample['recommended_branch'] = "CONTRADICTORY_NONEXISTENT_BRANCH"
    polluted_sample['academic_performance'] = "CONTRADICTORY_TIER"

    res_polluted = pipe.predict_student(polluted_sample)

    # Predictions must be identical despite contradictory labels
    assert res_clean['stage1']['recommended_branch'] == res_polluted['stage1']['recommended_branch']
    assert res_clean['stage2']['forecasted_academic_tier'] == res_polluted['stage2']['forecasted_academic_tier']
    assert np.isclose(res_clean['stage3']['placement_probability'], res_polluted['stage3']['placement_probability'], atol=1e-5)

def test_counterfactual_bounds_and_costs(trained_pipeline):
    pipe, df = trained_pipeline
    at_risk_row = df.iloc[0]

    recourse = pipe.recourse_engine.generate_recourse(at_risk_row, target_prob=0.80)

    assert 'intervention_cost' in recourse
    assert recourse['intervention_cost'] >= 0.0
    assert 'target_achieved' in recourse
    assert 'termination_reason' in recourse
    assert recourse['termination_reason'] in ['target_achieved', 'budget_exhausted', 'no_improving_step']
    assert 'changed_features' in recourse
    assert 'unchanged_features' in recourse

    # Mutable features must remain strictly within domain bounds
    from src.config import MUTABLE_FEATURE_BOUNDS
    cf = recourse['counterfactual_profile']
    for feat, (b_min, b_max, _) in MUTABLE_FEATURE_BOUNDS.items():
        if feat in cf:
            val = float(cf[feat])
            assert b_min - 1e-3 <= val <= b_max + 1e-3, f"Feature {feat} value {val} out of bounds [{b_min}, {b_max}]"

def test_fairness_evaluator_comprehensive(trained_pipeline):
    from src.explainability.fairness_evaluator import FairnessEvaluator
    pipe, df = trained_pipeline

    eval_res = pipe.train(df, n_splits=3)
    test_df = eval_res['test_df_cascaded']

    evaluator = FairnessEvaluator(sensitive_feature='family_income_bracket')
    y_true = test_df['placement_status'].values
    y_pred = (test_df['placement_status'].values > 0).astype(int)
    sens = test_df['family_income_bracket']

    audit = evaluator.comprehensive_audit(y_true, y_pred, sens)
    assert 'demographic_parity_difference' in audit
    assert 'demographic_parity_ratio' in audit
    assert 'equalized_odds_difference' in audit
    assert 'subgroup_metrics' in audit
    assert audit['demographic_parity_difference'] >= 0.0

def test_shap_perturbation_consistency(trained_pipeline):
    pipe, df = trained_pipeline
    sample = df.iloc[0]
    X_sample = pipe.preprocessor.transform_stage3(pd.DataFrame([sample.to_dict()]))
    consistency_res = pipe.shap_explainer.validate_attribution_consistency(X_sample)

    assert 'is_consistent' in consistency_res
    assert 'top_feature' in consistency_res
    assert 'delta_prob' in consistency_res

