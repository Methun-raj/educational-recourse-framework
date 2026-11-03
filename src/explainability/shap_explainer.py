"""
SHapley Additive exPlanations (SHAP) Module.
Implements Section III-C (Eq. 5) of the Research Article with mathematical feature attribution.

Decomposes model predictions into additive local attributions:
f(x_i) = φ_0 + Σ_{j=1..d} φ_j(x_i)
"""

import os
import shap
import numpy as np
import pandas as pd
from typing import Optional, List, Dict, Any
import matplotlib.pyplot as plt

from src.config import EXPORT_DIR, get_logger

logger = get_logger(__name__)


class MultimodalSHAPExplainer:
    """
    Computes local and global Shapley additive explanations for multi-modal student forecasts.
    Provides TreeExplainer on the dominant gradient-boosted tree meta-learner (alpha=0.55),
    with perturbation validation and visualization utilities (global summary, waterfall, dependence).
    """
    def __init__(self, model: Any, feature_names: Optional[List[str]] = None,
                 background_data: Optional[np.ndarray] = None):
        self.model = model
        self.feature_names = feature_names
        self.background_data = background_data
        self.target_tree = getattr(model, 'xgb_model', model)

        # Initialize TreeExplainer on tree component
        self.explainer = shap.TreeExplainer(self.target_tree)
        self.base_value_ = float(self.explainer.expected_value) if np.isscalar(self.explainer.expected_value) else float(self.explainer.expected_value[0])

    def explain_instance(self, X_sample: Any) -> pd.DataFrame:
        """
        Calculates local additive SHAP values for a single student profile.
        Returns sorted DataFrame of features, raw values, and φ_j attributions.
        """
        if isinstance(X_sample, pd.DataFrame):
            X_arr = X_sample.values
        else:
            X_arr = np.array(X_sample)

        if X_arr.ndim == 1:
            X_arr = X_arr.reshape(1, -1)

        shap_values = self.explainer.shap_values(X_arr)
        if isinstance(shap_values, list):
            sv = shap_values[1][0] if len(shap_values) > 1 else shap_values[0][0]
        elif shap_values.ndim == 2:
            sv = shap_values[0]
        else:
            sv = shap_values

        names = self.feature_names if self.feature_names is not None else [f"Feature_{i}" for i in range(len(sv))]

        df_local = pd.DataFrame({
            'feature': names,
            'feature_value': X_arr[0],
            'shap_value': sv,
            'abs_shap': np.abs(sv)
        }).sort_values(by='abs_shap', ascending=False)

        return df_local

    def explain_cohort(self, X_cohort: Any) -> pd.DataFrame:
        """
        Calculates global mean |SHAP| feature importance across an evaluation cohort.
        Replicates Figure 3(a) rankings based on empirical model outputs.
        """
        if isinstance(X_cohort, pd.DataFrame):
            X_arr = X_cohort.values
        else:
            X_arr = np.array(X_cohort)

        shap_values = self.explainer.shap_values(X_arr)
        if isinstance(shap_values, list) and len(shap_values) > 1:
            sv = shap_values[1]
        else:
            sv = shap_values

        mean_abs_shap = np.mean(np.abs(sv), axis=0)
        names = self.feature_names if self.feature_names is not None else [f"Feature_{i}" for i in range(len(mean_abs_shap))]

        df_global = pd.DataFrame({
            'feature': names,
            'mean_abs_shap': mean_abs_shap
        }).sort_values(by='mean_abs_shap', ascending=False)

        return df_global

    def validate_attribution_consistency(self, X_sample: Any) -> Dict[str, Any]:
        """
        Validates explanation fidelity via directional perturbation test:
        Perturbing the top positive feature upwards should increase or maintain model probability.
        """
        if isinstance(X_sample, pd.DataFrame):
            X_arr = X_sample.values.copy()
        else:
            X_arr = np.array(X_sample).copy()

        if X_arr.ndim == 1:
            X_arr = X_arr.reshape(1, -1)

        df_local = self.explain_instance(X_arr)
        top_row = df_local.iloc[0]
        top_feat_name = top_row['feature']
        top_idx = list(self.feature_names).index(top_feat_name) if self.feature_names else 0

        # Predict baseline probability using hybrid model
        p_base = float(self.model.predict_proba(X_arr)[:, 1][0]) if hasattr(self.model, 'predict_proba') else 0.5

        # Perturb feature upwards by 1.0 standard unit
        X_perturbed = X_arr.copy()
        X_perturbed[0, top_idx] += 1.0
        p_perturbed = float(self.model.predict_proba(X_perturbed)[:, 1][0]) if hasattr(self.model, 'predict_proba') else 0.5

        is_consistent = (p_perturbed >= p_base) if top_row['shap_value'] >= 0 else (p_perturbed <= p_base)
        return {
            'top_feature': top_feat_name,
            'top_shap': float(top_row['shap_value']),
            'baseline_prob': p_base,
            'perturbed_prob': p_perturbed,
            'delta_prob': p_perturbed - p_base,
            'is_consistent': bool(is_consistent)
        }

    def plot_waterfall(self, X_sample: Any,
                       output_path: str = os.path.join(EXPORT_DIR, "figure_waterfall_local.png"),
                       top_k: int = 7) -> str:
        """Renders and exports local waterfall SHAP explanation plot."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df_local = self.explain_instance(X_sample).head(top_k)
        df_plot = df_local.iloc[::-1]

        colors = ['#2a9d8f' if s >= 0 else '#e63946' for s in df_plot['shap_value']]
        plt.figure(figsize=(9, 5), dpi=300)
        bars = plt.barh(df_plot['feature'], df_plot['shap_value'], color=colors, edgecolor='black', linewidth=0.6)

        for bar, val in zip(bars, df_plot['shap_value']):
            x_pos = bar.get_width() + (0.01 if val >= 0 else -0.04)
            plt.text(x_pos, bar.get_y() + bar.get_height() / 2, f"{val:+.3f}",
                     va='center', ha='left' if val >= 0 else 'right',
                     fontsize=9, fontweight='bold')

        plt.axvline(0, color='black', linestyle='--', linewidth=0.8)
        plt.title("Local SHAP Attribution (Student-Level Explanation)", fontsize=12, fontweight='bold', pad=12)
        plt.xlabel("SHAP Attribution (φ_j to Placement Margin)", fontsize=10)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        logger.info("Local waterfall SHAP plot saved to %s", output_path)
        return output_path


    def plot_global_summary(self, X_cohort: Any,
                            output_path: str = os.path.join(EXPORT_DIR, "figure3a_shap_global.png"),
                            top_k: int = 8) -> str:
        """Renders and exports Figure 3(a) global SHAP attribution plot."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df_global = self.explain_cohort(X_cohort).head(top_k)
        df_plot = df_global.iloc[::-1]

        plt.figure(figsize=(9, 5), dpi=300)
        bars = plt.barh(df_plot['feature'], df_plot['mean_abs_shap'], color='#1d3557', edgecolor='#1d3557')

        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.005, bar.get_y() + bar.get_height() / 2, f"+{width:.3f}",
                     va='center', ha='left', fontsize=10, fontweight='bold', color='#1d3557')

        plt.title("(a) Global SHAP Feature Attribution (Cohort Analysis)", fontsize=13, fontweight='bold', pad=15)
        plt.xlabel("Mean |SHAP Value| (Global Impact)", fontsize=11, fontweight='medium')
        plt.xlim(0, max(df_plot['mean_abs_shap']) * 1.3)
        plt.grid(axis='x', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        logger.info("Figure 3(a) plot generated and saved to %s", output_path)
        return output_path
