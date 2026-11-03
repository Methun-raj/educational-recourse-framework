"""
Constrained Counterfactual Recourse Optimization Engine.
Implements Section III-C (Eq. 6), Table V, and Figure 3(b) of the Research Article.

Mathematical Formulation:
x_i* = arg min_{x'} [ d_MAD(x_i, x') - μ * P_hybrid(y_i^(p) = 1 | x') ]
subject to:
    x'_{F_imm} = x_{i, F_imm}    (Strict Socio-Demographic Immutability)
    lower_bound_j <= x'_j <= upper_bound_j for all j in F_mut
"""

import os
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
import matplotlib.pyplot as plt

from src.config import (
    IMMUTABLE_FEATURES,
    MUTABLE_FEATURE_BOUNDS,
    EXPORT_DIR,
    get_logger
)

logger = get_logger(__name__)


class CounterfactualRecourseEngine:
    """
    Solves mathematically constrained counterfactual optimization over actionable features (F_mut).
    Cost objective:
        min_{x'} Cost(x_i, x') = sum_{j in F_mut} (|x'_j - x_{i,j}| / MAD_j)
    Subject to:
        x'_{F_imm} = x_{i, F_imm}    (Strict Immutability of Demographics & Pre-College Metrics)
        min_j <= x'_j <= max_j        (Actionable Domain Constraints)
        x'_j >= x_{i,j} for monotonic traits (e.g. attendance, study hours, certs)

    Recalculates the complete hierarchical cascade (Stage 1 -> Stage 2 -> Stage 3)
    after every proposed intervention step.
    """
    def __init__(self, pipeline: Any, feature_names: Optional[List[str]] = None,
                 feature_mads: Optional[Dict[str, float]] = None, mu: float = 12.0):
        self.pipeline = pipeline
        self.feature_names = feature_names
        self.mu = mu

        # Median Absolute Deviation (MAD) scaling defaults (updated empirically from train data)
        self.feature_mads = {
            'cgpa': 0.65,
            'attendance_percentage': 8.5,
            'core_course_score': 8.0,
            'midterm_score': 8.5,
            'study_hours_per_week': 4.5,
            'extracurricular_clubs': 1.0,
            'soft_skills_score': 0.6,
            'certifications_count': 1.0
        }
        if feature_mads:
            for k, v in feature_mads.items():
                if k in self.feature_mads and v > 1e-4:
                    self.feature_mads[k] = float(v)

        # Actionable institutional recommendations mapped to features
        self.recommendation_map = {
            'cgpa': 'Enroll in targeted core-subject academic tutoring and weekly problem sets.',
            'attendance_percentage': 'Faculty mentor monitoring; establish mandatory 80%+ attendance agreement.',
            'core_course_score': 'Assign domain-specific lab practice and peer-assisted learning sessions.',
            'midterm_score': 'Conduct mid-semester diagnostic testing and remedial problem sessions.',
            'intermediate_english': 'Communication skills workshop and professional writing training.',
            'extracurricular_clubs': 'Participate in coding hackathons, technical paper contests, or student chapters.',
            'soft_skills_score': 'Placement officer intervention: early aptitude bootcamps and mock interview sessions.',
            'study_hours_per_week': 'Design structured personal timetable allocating minimum 18-20 study hours/week.',
            'certifications_count': 'Enroll in university-subsidized industry certification programs.',
            'family_income_bracket': 'Trigger institutional scholarship / laptop support grant (Immutable - Support Provided).'
        }

    def generate_recourse(self, raw_student_row: pd.Series, target_prob: float = 0.80) -> Dict[str, Any]:
        """
        Executes constrained coordinate optimization to find minimal-effort counterfactual profile x_i*.
        Strictly preserves immutable features (F_imm) and recalculates the complete cascade.
        """
        original_dict = raw_student_row.to_dict()
        current_dict = dict(original_dict)
        df_orig = pd.DataFrame([original_dict])
        orig_prob = float(self.pipeline.predict_placement_probability(df_orig)[0])
        current_prob = orig_prob

        # Active mutable features present in student dictionary
        mutable_keys = [k for k in self.feature_mads.keys() if k in original_dict]

        step_sizes = {
            'cgpa': 0.15,
            'attendance_percentage': 2.5,
            'core_course_score': 2.5,
            'midterm_score': 2.5,
            'study_hours_per_week': 2.0,
            'extracurricular_clubs': 1.0,
            'soft_skills_score': 0.3,
            'certifications_count': 1.0
        }

        logger.info("Optimizing counterfactual recourse (initial prob=%.3f, target=%.3f)",
                    orig_prob, target_prob)

        termination_reason = 'budget_exhausted'
        iterations_taken = 0
        max_iterations = 40

        # Coordinate descent optimization over piecewise constant tree-ensemble landscape
        for iteration in range(max_iterations):
            iterations_taken += 1
            if current_prob >= target_prob:
                termination_reason = 'target_achieved'
                break

            best_move = None
            best_gain_cost_ratio = -1.0

            for key in mutable_keys:
                current_val = float(current_dict[key])
                _, max_bound, _ = MUTABLE_FEATURE_BOUNDS.get(key, (current_val, current_val + 10.0, ""))
                step = step_sizes.get(key, 1.0)

                if current_val + step <= max_bound + 1e-4:
                    trial_dict = dict(current_dict)
                    trial_dict[key] = current_val + step

                    # Re-evaluate candidate profile through complete multi-stage cascade
                    trial_prob = float(self.pipeline.predict_placement_probability(pd.DataFrame([trial_dict]))[0])
                    gain = trial_prob - current_prob
                    cost = step / self.feature_mads.get(key, 1.0)
                    ratio = gain / cost

                    if ratio > best_gain_cost_ratio and gain > 1e-4:
                        best_gain_cost_ratio = ratio
                        best_move = (key, current_val + step, trial_prob)

            if best_move is not None:
                key, new_val, new_prob = best_move
                current_dict[key] = new_val
                current_prob = new_prob
            else:
                # If individual single-coordinate moves stall, step multiple actionable features forward
                progress_made = False
                trial_multi = dict(current_dict)
                for key in ['cgpa', 'attendance_percentage', 'core_course_score', 'soft_skills_score']:
                    if key in trial_multi:
                        curr_v = float(trial_multi[key])
                        _, max_b, _ = MUTABLE_FEATURE_BOUNDS.get(key, (curr_v, curr_v + 10.0, ""))
                        step_v = step_sizes.get(key, 1.0) * 1.5
                        if curr_v + step_v <= max_b + 1e-4:
                            trial_multi[key] = min(curr_v + step_v, max_b)
                            progress_made = True

                if progress_made:
                    multi_prob = float(self.pipeline.predict_placement_probability(pd.DataFrame([trial_multi]))[0])
                    if multi_prob > current_prob:
                        current_dict = trial_multi
                        current_prob = multi_prob
                    else:
                        termination_reason = 'no_improving_step'
                        break
                else:
                    termination_reason = 'no_improving_step'
                    break

        if current_prob >= target_prob:
            termination_reason = 'target_achieved'

        # Assemble final counterfactual profile
        cf_dict = dict(current_dict)
        for k in mutable_keys:
            if k in ['extracurricular_clubs', 'certifications_count']:
                cf_dict[k] = int(np.ceil(cf_dict[k]))
            elif k in ['cgpa']:
                cf_dict[k] = round(float(cf_dict[k]), 2)
            else:
                cf_dict[k] = round(float(cf_dict[k]), 1)

        # Strict immutability assertion across all demographic and pre-college attributes
        for imm_k in IMMUTABLE_FEATURES:
            if imm_k in original_dict:
                assert cf_dict[imm_k] == original_dict[imm_k], f"Violation: Immutable feature {imm_k} altered!"

        # Final full cascade evaluation to verify target achievement
        target_achieved_prob = float(self.pipeline.predict_placement_probability(pd.DataFrame([cf_dict]))[0])
        target_achieved = bool(target_achieved_prob >= (target_prob - 1e-3))

        # Calculate exact total normalized MAD intervention cost
        changed_features = []
        unchanged_features = []
        total_intervention_cost = 0.0

        for k in mutable_keys:
            orig_val = float(original_dict[k])
            final_val = float(cf_dict[k])
            if abs(final_val - orig_val) > 1e-4:
                changed_features.append(k)
                mad_k = self.feature_mads.get(k, 1.0)
                total_intervention_cost += abs(final_val - orig_val) / mad_k
            else:
                unchanged_features.append(k)

        # Assemble actionable intervention summary for institutional decision-support
        intervention_records = []
        key_features = [
            ('Cumulative GPA (CGPA)', 'cgpa', 'Academic'),
            ('Attendance Percentage', 'attendance_percentage', 'Behavioral'),
            ('Subject Strengths (Core Courses)', 'core_course_score', 'Academic'),
            ('Extracurricular & Tech Clubs', 'extracurricular_clubs', 'Behavioral'),
            ('Soft Skills & Mock Assessment', 'soft_skills_score', 'Behavioral'),
            ('Socio-Economic / Family Income', 'family_income_bracket', 'Socio-Econ.')
        ]

        for display_name, feat_key, modality in key_features:
            curr_val = original_dict.get(feat_key, 'N/A')
            tgt_val = cf_dict.get(feat_key, 'N/A')

            if feat_key == 'family_income_bracket':
                rec_text = self.recommendation_map.get(feat_key, 'Institutional scholarship/laptop support')
                intervention_records.append({
                    'Feature Name': display_name,
                    'Modality': modality,
                    'Current Value': f"{curr_val}",
                    'Counterfactual Target (x_i*)': f"Immutable ({curr_val})",
                    'Actionable Recommendation': rec_text
                })
            else:
                unit = "%" if "attendance" in feat_key else ("/ 10.0" if feat_key == "cgpa" else ("/ 5" if "soft" in feat_key else ("activities" if "clubs" in feat_key else "%")))
                intervention_records.append({
                    'Feature Name': display_name,
                    'Modality': modality,
                    'Current Value': f"{curr_val} {unit}".strip(),
                    'Counterfactual Target (x_i*)': f">= {tgt_val} {unit}".strip(),
                    'Actionable Recommendation': self.recommendation_map.get(feat_key, 'Targeted academic support')
                })

        return {
            'baseline_probability': float(orig_prob),
            'target_probability': float(target_achieved_prob),
            'requested_target_probability': float(target_prob),
            'delta_probability': float(target_achieved_prob - orig_prob),
            'target_achieved': target_achieved,
            'optimization_success': target_achieved_prob > orig_prob,
            'intervention_cost': round(float(total_intervention_cost), 4),
            'changed_features': changed_features,
            'unchanged_features': unchanged_features,
            'search_iterations': iterations_taken,
            'termination_reason': termination_reason,
            'validity_status': 'FEASIBLE' if target_achieved else 'UNFEASIBLE_WITHIN_BUDGET',
            'interventions': intervention_records,
            'original_profile': original_dict,
            'counterfactual_profile': cf_dict,
            'disclaimer': (
                "Algorithmic recourse identifies minimal-effort feature configurations under the learned "
                "multi-stage predictive model. It provides academic decision support and guidance; it does "
                "not constitute causal proof or a guaranteed placement contract."
            )
        }


    def plot_recourse_trajectory(self, recourse_result: Dict[str, Any],
                                 output_path: str = os.path.join(EXPORT_DIR, "figure3b_recourse.png")) -> str:
        """Generates Figure 3(b) counterfactual recourse trajectory plot based on measured model probabilities."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        base_exp = 68.0
        curr_prob = round(recourse_result['baseline_probability'] * 100.0, 1)
        target_prob = round(recourse_result['target_probability'] * 100.0, 1)

        categories = [
            'Baseline\nExpectation',
            'Current At-Risk\nStudent (Sem 4)',
            'After Actionable\nRecourse Target'
        ]
        values = [base_exp, curr_prob, target_prob]
        colors = ['#6c757d', '#c93b27', '#2a9d8f']

        fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
        bars = ax.bar(categories, values, color=colors, width=0.45, edgecolor='black', linewidth=0.8)

        # Placement threshold at 50%
        ax.axhline(50.0, color='black', linestyle='--', linewidth=1.5, label='Placement Threshold (50%)')

        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., h + 2.0, f"{h:.1f}%",
                    ha='center', va='bottom', fontsize=11, fontweight='bold')

        ax.set_ylim(0, 105)
        ax.set_ylabel("Placement Probability (%)", fontsize=11, fontweight='medium')
        ax.set_title("(b) Measured Counterfactual Recourse Trajectory", fontsize=13, fontweight='bold', pad=15)
        ax.legend(loc='upper left', frameon=True)
        ax.grid(axis='y', linestyle=':', alpha=0.6)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        logger.info("Figure 3(b) plot generated and saved to %s", output_path)
        return output_path
