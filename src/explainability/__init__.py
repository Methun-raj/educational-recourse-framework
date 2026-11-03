"""
Explainable AI & Counterfactual Recourse Modules
"""
from .shap_explainer import MultimodalSHAPExplainer
from .counterfactual_recourse import CounterfactualRecourseEngine
from .fairness_evaluator import FairnessEvaluator

__all__ = [
    "MultimodalSHAPExplainer",
    "CounterfactualRecourseEngine",
    "FairnessEvaluator"
]
