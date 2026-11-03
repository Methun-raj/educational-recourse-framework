"""
Fairness and Algorithmic Equity Evaluator
Implements Section III-C & Table IV Demographic Parity Difference (DPD) Analysis.
"""

import numpy as np
import pandas as pd

from typing import Dict, Any, Tuple
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class FairnessEvaluator:
    """
    Evaluates algorithmic fairness and demographic parity across sensitive student subgroups.
    Supports Demographic Parity Difference (DPD), Demographic Parity Ratio (DPR),
    Equalized Odds, Equal Opportunity, False Positive/Negative Rate differences,
    and subgroup-disaggregated classification metrics.
    """
    def __init__(self, sensitive_feature: str = 'family_income_bracket'):
        self.sensitive_feature = sensitive_feature

    def demographic_parity_difference(self, y_pred: np.ndarray, sensitive_series: pd.Series) -> Tuple[float, Dict[str, float]]:
        """
        Calculates selection rate disparity:
        DPD = max_{a, b} | P(y^=1 | A=a) - P(y^=1 | A=b) |
        """
        df_eval = pd.DataFrame({
            'pred': y_pred,
            'group': sensitive_series
        })
        group_rates = df_eval.groupby('group')['pred'].mean()
        dpd = float(group_rates.max() - group_rates.min())
        return round(dpd, 4), {str(k): round(float(v), 4) for k, v in group_rates.items()}

    def demographic_parity_ratio(self, y_pred: np.ndarray, sensitive_series: pd.Series) -> Tuple[float, Dict[str, float]]:
        """
        Calculates the ratio of lowest to highest selection rate across sensitive groups:
        DPR = min P(y^=1 | A) / max P(y^=1 | A) (80% rule: DPR >= 0.80)
        """
        df_eval = pd.DataFrame({
            'pred': y_pred,
            'group': sensitive_series
        })
        group_rates = df_eval.groupby('group')['pred'].mean()
        max_rate = max(float(group_rates.max()), 1e-6)
        min_rate = float(group_rates.min())
        dpr = min_rate / max_rate
        return round(dpr, 4), {str(k): round(float(v), 4) for k, v in group_rates.items()}

    def equalized_odds_difference(self, y_true: np.ndarray, y_pred: np.ndarray, sensitive_series: pd.Series) -> Tuple[float, Dict[str, Any]]:
        """Calculates difference in True Positive Rate (TPR) and False Positive Rate (FPR)."""
        df_eval = pd.DataFrame({
            'true': y_true,
            'pred': y_pred,
            'group': sensitive_series
        })

        tprs = {}
        fprs = {}
        for grp, sub in df_eval.groupby('group'):
            pos = (sub['true'] == 1).sum()
            neg = (sub['true'] == 0).sum()
            tpr = ((sub['true'] == 1) & (sub['pred'] == 1)).sum() / max(pos, 1)
            fpr = ((sub['true'] == 0) & (sub['pred'] == 1)).sum() / max(neg, 1)
            tprs[str(grp)] = float(tpr)
            fprs[str(grp)] = float(fpr)

        tpr_diff = max(tprs.values()) - min(tprs.values())
        fpr_diff = max(fprs.values()) - min(fprs.values())
        eod = max(tpr_diff, fpr_diff)
        return round(float(eod), 4), {'tprs': tprs, 'fprs': fprs, 'tpr_diff': round(tpr_diff, 4), 'fpr_diff': round(fpr_diff, 4)}

    def equal_opportunity_difference(self, y_true: np.ndarray, y_pred: np.ndarray, sensitive_series: pd.Series) -> float:
        """Calculates maximum disparity in True Positive Rate (Recall) across groups."""
        _, details = self.equalized_odds_difference(y_true, y_pred, sensitive_series)
        return details['tpr_diff']

    def subgroup_metrics(self, y_true: np.ndarray, y_pred: np.ndarray, sensitive_series: pd.Series) -> Dict[str, Dict[str, float]]:
        """Computes accuracy, precision, recall, and F1 disaggregated by sensitive demographic groups."""
        df_eval = pd.DataFrame({
            'true': y_true,
            'pred': y_pred,
            'group': sensitive_series
        })

        results = {}
        for grp, sub in df_eval.groupby('group'):
            y_t = sub['true'].values
            y_p = sub['pred'].values
            results[str(grp)] = {
                'sample_count': len(sub),
                'accuracy': round(float(accuracy_score(y_t, y_p)), 4),
                'precision': round(float(precision_score(y_t, y_p, zero_division=0)), 4),
                'recall': round(float(recall_score(y_t, y_p, zero_division=0)), 4),
                'f1': round(float(f1_score(y_t, y_p, zero_division=0)), 4)
            }
        return results

    def comprehensive_audit(self, y_true: np.ndarray, y_pred: np.ndarray, sensitive_series: pd.Series) -> Dict[str, Any]:
        """Assembles complete fairness and bias equity audit report."""
        dpd, group_rates = self.demographic_parity_difference(y_pred, sensitive_series)
        dpr, _ = self.demographic_parity_ratio(y_pred, sensitive_series)
        eod, eq_details = self.equalized_odds_difference(y_true, y_pred, sensitive_series)
        sub_metrics = self.subgroup_metrics(y_true, y_pred, sensitive_series)

        return {
            'sensitive_attribute': self.sensitive_feature,
            'demographic_parity_difference': dpd,
            'demographic_parity_ratio': dpr,
            'equalized_odds_difference': eod,
            'equal_opportunity_difference': eq_details['tpr_diff'],
            'false_positive_rate_difference': eq_details['fpr_diff'],
            'group_selection_rates': group_rates,
            'subgroup_metrics': sub_metrics,
            'equity_threshold_satisfied': bool(dpd <= 0.10 and eod <= 0.10)
        }

