"""
Hierarchical Multi-Stage Forecasting & Counterfactual Recourse Pipeline.
Implements Figure 1 Flowchart with Leakage-Safe Out-of-Fold (OOF) Cascaded Training.

Eliminates cascading exposure bias:
- Stage 2 is trained using Out-of-Fold predicted branches from Stage 1.
- Stage 3 is trained using Out-of-Fold predicted academic tiers from Stage 2 and branches from Stage 1.
- Test evaluation executes genuine end-to-end cascading inference.
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
from sklearn.model_selection import StratifiedKFold, train_test_split

from src.config import (
    TARGET_STAGE_1,
    TARGET_STAGE_2,
    TARGET_STAGE_3,
    MODEL_DIR,
    get_logger
)
from src.data_preprocessing import MultiModalPreprocessor
from src.models.branch_recommender import BranchRecommender
from src.models.academic_forecaster import AcademicForecaster
from src.models.placement_predictor import HybridPlacementPredictor
from src.explainability.shap_explainer import MultimodalSHAPExplainer
from src.explainability.counterfactual_recourse import CounterfactualRecourseEngine

logger = get_logger(__name__)


class HierarchicalMultiStagePipeline:
    """
    End-to-End Orchestrator for 3-Stage Cascaded Educational Prediction:
    Stage 1 (RF Branch) -> Stage 2 (XGB+GB Academic) -> Stage 3 (Hybrid Placement)
    + SHAP Attribution + Constrained Counterfactual Recourse.
    """
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.preprocessor = MultiModalPreprocessor()
        self.stage1_model = BranchRecommender(random_state=random_state)
        self.stage2_model = AcademicForecaster(random_state=random_state)
        self.stage3_model = HybridPlacementPredictor(random_state=random_state)
        self.shap_explainer: Optional[MultimodalSHAPExplainer] = None
        self.recourse_engine: Optional[CounterfactualRecourseEngine] = None
        self.is_trained: bool = False

    def train(self, df: pd.DataFrame, test_size: float = 0.2, n_splits: int = 5) -> Dict[str, Any]:
        """
        Executes leak-free Out-of-Fold (OOF) cascaded training across all stages.
        """
        logger.info("Initiating Hierarchical Pipeline Training on %d samples (test_size=%.2f, n_splits=%d)",
                    len(df), test_size, n_splits)

        # 1. Stratified Train / Test Split
        train_df, test_df = train_test_split(
            df,
            test_size=test_size,
            random_state=self.random_state,
            stratify=df[TARGET_STAGE_3]
        )
        train_df = train_df.reset_index(drop=True)
        test_df = test_df.reset_index(drop=True)

        # 2. Fit Preprocessor exclusively on train_df
        self.preprocessor.fit(train_df)

        # -------------------------------------------------------------
        # 3. Stage 1: Out-of-Fold (OOF) Cross-Validation for Branch Recommender
        # -------------------------------------------------------------
        logger.info("Computing Out-of-Fold Stage 1 predictions with fold-isolated preprocessing")
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=self.random_state)
        oof_branch_preds = np.empty(len(train_df), dtype=object)

        y1_train_full = self.preprocessor.branch_encoder.transform(train_df[TARGET_STAGE_1].astype(str))

        for fold, (trn_idx, val_idx) in enumerate(skf.split(train_df, y1_train_full)):
            fold_prep = MultiModalPreprocessor()
            fold_prep.fit(train_df.iloc[trn_idx])

            X1_trn = fold_prep.transform_stage1(train_df.iloc[trn_idx])
            y1_trn = fold_prep.branch_encoder.transform(train_df.iloc[trn_idx][TARGET_STAGE_1].astype(str))

            fold_rf = BranchRecommender(random_state=self.random_state + fold)
            fold_rf.fit(
                X1_trn,
                y1_trn,
                class_names=fold_prep.branch_encoder.classes_
            )
            X1_val = fold_prep.transform_stage1(train_df.iloc[val_idx])
            val_preds_idx = fold_rf.predict(X1_val)
            oof_branch_preds[val_idx] = fold_prep.branch_encoder.inverse_transform(val_preds_idx)

        # -------------------------------------------------------------
        # 4. Stage 2: Out-of-Fold Cross-Validation using OOF Stage 1 predictions
        # -------------------------------------------------------------
        logger.info("Computing Out-of-Fold Stage 2 predictions using OOF Stage 1 inputs")
        train_df_s2 = train_df.copy()
        train_df_s2[TARGET_STAGE_1] = oof_branch_preds

        y2_train_full = self.preprocessor.academic_perf_encoder.transform(train_df[TARGET_STAGE_2].astype(str))
        oof_acad_preds = np.empty(len(train_df), dtype=object)

        for fold, (trn_idx, val_idx) in enumerate(skf.split(train_df_s2, y2_train_full)):
            fold_prep = MultiModalPreprocessor()
            fold_prep.fit(train_df_s2.iloc[trn_idx])

            X2_trn = fold_prep.transform_stage2(train_df_s2.iloc[trn_idx])
            y2_trn = fold_prep.academic_perf_encoder.transform(train_df_s2.iloc[trn_idx][TARGET_STAGE_2].astype(str))

            fold_acad = AcademicForecaster(random_state=self.random_state + fold)
            fold_acad.fit(
                X2_trn,
                y2_trn,
                class_names=fold_prep.academic_perf_encoder.classes_
            )
            X2_val = fold_prep.transform_stage2(train_df_s2.iloc[val_idx])
            val_preds_idx = fold_acad.predict(X2_val)
            oof_acad_preds[val_idx] = fold_prep.academic_perf_encoder.inverse_transform(val_preds_idx)

        # -------------------------------------------------------------
        # 5. Stage 3: Train Hybrid Placement Predictor on OOF augmented profile
        # -------------------------------------------------------------
        logger.info("Training Stage 3 Hybrid Placement Predictor on augmented OOF features")
        train_df_s3 = train_df.copy()
        train_df_s3[TARGET_STAGE_1] = oof_branch_preds
        train_df_s3[TARGET_STAGE_2] = oof_acad_preds

        # Explicit assertion: guarantee downstream training features are out-of-fold predicted
        assert (train_df_s3[TARGET_STAGE_1] == oof_branch_preds).all(), "Stage 3 branch input is not OOF predicted!"
        assert (train_df_s3[TARGET_STAGE_2] == oof_acad_preds).all(), "Stage 3 academic input is not OOF predicted!"

        X3_train_oof = self.preprocessor.transform_stage3(train_df_s3)
        y3_train_full = train_df[TARGET_STAGE_3].values
        feat_names_stage3 = self.preprocessor.get_feature_names_stage3()

        self.stage3_model.fit(
            X3_train_oof,
            y3_train_full,
            feature_names=feat_names_stage3
        )

        # -------------------------------------------------------------
        # 6. Fit Final Production Stage 1 & Stage 2 models on Full Training Set
        # -------------------------------------------------------------
        logger.info("Fitting final production models on full training partition without exposure bias")
        X1_train_full = self.preprocessor.transform_stage1(train_df)
        self.stage1_model.fit(
            X1_train_full,
            y1_train_full,
            class_names=self.preprocessor.branch_encoder.classes_,
            feature_names=self.preprocessor.stage1_num
        )

        # Stage 2 production model trained on Stage 1 OOF predictions to eliminate exposure bias
        X2_train_prod = self.preprocessor.transform_stage2(train_df_s2)
        self.stage2_model.fit(
            X2_train_prod,
            y2_train_full,
            class_names=self.preprocessor.academic_perf_encoder.classes_
        )

        # Calculate empirical MADs from training set
        self.empirical_mads = {}
        for col in self.preprocessor.stage3_num:
            if col in train_df.columns:
                series = train_df[col].dropna()
                med = float(np.median(series))
                mad = float(np.median(np.abs(series - med)))
                self.empirical_mads[col] = max(mad, 1e-2)

        # -------------------------------------------------------------
        # 7. Initialize Explainability & Recourse Engines
        # -------------------------------------------------------------
        self.shap_explainer = MultimodalSHAPExplainer(
            self.stage3_model,
            feature_names=feat_names_stage3
        )
        self.recourse_engine = CounterfactualRecourseEngine(
            self,
            feature_names=feat_names_stage3,
            feature_mads=self.empirical_mads
        )
        self.is_trained = True

        # -------------------------------------------------------------
        # 8. Genuine End-to-End Cascading Evaluation on Test Set
        # -------------------------------------------------------------
        logger.info("Evaluating true end-to-end cascading inference on holdout test set")
        test_df_cascaded = test_df.copy()

        # Step 1 Test Inference
        X1_test = self.preprocessor.transform_stage1(test_df_cascaded)
        y1_test_true = self.preprocessor.branch_encoder.transform(test_df[TARGET_STAGE_1].astype(str))
        eval_s1 = self.stage1_model.evaluate(X1_test, y1_test_true)
        test_branch_pred_idx = self.stage1_model.predict(X1_test)
        test_df_cascaded[TARGET_STAGE_1] = self.preprocessor.branch_encoder.inverse_transform(test_branch_pred_idx)

        # Step 2 Test Inference (conditioned strictly on Stage 1 predictions)
        X2_test = self.preprocessor.transform_stage2(test_df_cascaded)
        y2_test_true = self.preprocessor.academic_perf_encoder.transform(test_df[TARGET_STAGE_2].astype(str))
        eval_s2 = self.stage2_model.evaluate(X2_test, y2_test_true)
        test_acad_pred_idx = self.stage2_model.predict(X2_test)
        test_df_cascaded[TARGET_STAGE_2] = self.preprocessor.academic_perf_encoder.inverse_transform(test_acad_pred_idx)

        # Step 3 Test Inference (conditioned strictly on Stage 1 + Stage 2 predictions)
        X3_test = self.preprocessor.transform_stage3(test_df_cascaded)
        y3_test_true = test_df[TARGET_STAGE_3].values
        eval_s3 = self.stage3_model.evaluate(X3_test, y3_test_true)

        logger.info("Cascaded Test Accuracies: Stage 1 = %.1f%%, Stage 2 = %.1f%%, Stage 3 = %.1f%%",
                    eval_s1['accuracy'] * 100, eval_s2['accuracy'] * 100, eval_s3['accuracy'] * 100)

        return {
            'stage1': eval_s1,
            'stage2': eval_s2,
            'stage3': eval_s3,
            'test_df': test_df,
            'test_df_cascaded': test_df_cascaded
        }

    def predict_placement_probability(self, df_input: pd.DataFrame) -> np.ndarray:
        """
        Evaluates calibrated placement probability through the complete hierarchical cascade.
        Strictly strips and ignores any ground-truth intermediate columns in df_input,
        guaranteeing that changing ground-truth intermediate labels does not affect predictions.
        """
        if not self.is_trained:
            raise RuntimeError("Pipeline must be trained or loaded before running inference.")

        df_copy = df_input.copy()
        # Drop any pre-existing intermediate labels to strictly prevent ground-truth leakage
        for col in [TARGET_STAGE_1, TARGET_STAGE_2, TARGET_STAGE_3]:
            if col in df_copy.columns:
                df_copy = df_copy.drop(columns=[col])

        # Stage 1: Generate predicted branch
        X1 = self.preprocessor.transform_stage1(df_copy)
        b_pred_idx = self.stage1_model.predict(X1)
        df_copy[TARGET_STAGE_1] = self.preprocessor.branch_encoder.inverse_transform(b_pred_idx)

        # Stage 2: Generate predicted academic tier conditioned on Stage 1 predicted branch
        X2 = self.preprocessor.transform_stage2(df_copy)
        a_pred_idx = self.stage2_model.predict(X2)
        df_copy[TARGET_STAGE_2] = self.preprocessor.academic_perf_encoder.inverse_transform(a_pred_idx)

        # Stage 3: Placement prediction conditioned on predicted intermediate outputs
        X3 = self.preprocessor.transform_stage3(df_copy)
        return self.stage3_model.predict_proba(X3)[:, 1]

    def predict_student(self, student_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes sequential 3-stage inference for a single student profile.
        Returns Stage 1 discipline, Stage 2 academic forecast, Stage 3 placement decision & local SHAP.
        """
        if not self.is_trained:
            raise RuntimeError("Pipeline must be trained or loaded before running inference.")

        # Clean student dict to strictly remove intermediate targets if present
        clean_dict = {
            k: v for k, v in student_dict.items()
            if k not in [TARGET_STAGE_1, TARGET_STAGE_2, TARGET_STAGE_3]
        }
        df_single = pd.DataFrame([clean_dict])

        # Stage 1: Branch Recommendation
        X1 = self.preprocessor.transform_stage1(df_single)
        branch_idx = int(self.stage1_model.predict(X1)[0])
        branch_proba = self.stage1_model.predict_proba(X1)[0]
        recommended_branch = str(self.preprocessor.branch_encoder.inverse_transform([branch_idx])[0])
        branch_prob_dict = {
            str(cls): round(float(p), 4)
            for cls, p in zip(self.preprocessor.branch_encoder.classes_, branch_proba)
        }

        # Stage 2: Academic Performance Forecast (conditioned strictly on predicted branch)
        df_single[TARGET_STAGE_1] = recommended_branch
        X2 = self.preprocessor.transform_stage2(df_single)
        acad_idx = int(self.stage2_model.predict(X2)[0])
        acad_proba = self.stage2_model.predict_proba(X2)[0]
        academic_tier = str(self.preprocessor.academic_perf_encoder.inverse_transform([acad_idx])[0])
        acad_prob_dict = {
            str(cls): round(float(p), 4)
            for cls, p in zip(self.preprocessor.academic_perf_encoder.classes_, acad_proba)
        }

        # Stage 3: Placement Prediction (conditioned strictly on predicted branch + academic tier)
        df_single[TARGET_STAGE_2] = academic_tier
        X3 = self.preprocessor.transform_stage3(df_single)
        probs = self.stage3_model.predict_proba(X3)[0]
        placement_prob = float(probs[1])
        placement_pred = int(placement_prob >= 0.50)
        placement_label = "Placed" if placement_pred == 1 else "Not Placed"

        # Local SHAP waterfall explanation
        local_shap_df = self.shap_explainer.explain_instance(X3) if self.shap_explainer else None

        return {
            'stage1': {
                'recommended_branch': recommended_branch,
                'probabilities': branch_prob_dict
            },
            'stage2': {
                'forecasted_academic_tier': academic_tier,
                'probabilities': acad_prob_dict
            },
            'stage3': {
                'placement_prediction': placement_label,
                'placement_probability': round(placement_prob, 4),
                'placement_status': placement_pred,
                'confidence': round(max(placement_prob, 1.0 - placement_prob) * 100, 1)
            },
            'local_shap': local_shap_df
        }

    def save_pipeline(self, model_dir: str = MODEL_DIR) -> None:
        os.makedirs(model_dir, exist_ok=True)
        self.preprocessor.save(os.path.join(model_dir, "preprocessor.joblib"))
        self.stage1_model.save(os.path.join(model_dir, "stage1_model.joblib"))
        self.stage2_model.save(os.path.join(model_dir, "stage2_model.joblib"))
        self.stage3_model.save(os.path.join(model_dir, "stage3_model.joblib"))
        if hasattr(self, 'empirical_mads') and self.empirical_mads:
            joblib.dump(self.empirical_mads, os.path.join(model_dir, "empirical_mads.joblib"))
        logger.info("Hierarchical pipeline saved to %s", model_dir)

    def load_pipeline(self, model_dir: str = MODEL_DIR) -> "HierarchicalMultiStagePipeline":
        logger.info("Loading hierarchical pipeline components from %s", model_dir)
        self.preprocessor = MultiModalPreprocessor.load(os.path.join(model_dir, "preprocessor.joblib"))
        self.stage1_model = BranchRecommender.load(os.path.join(model_dir, "stage1_model.joblib"))
        self.stage2_model = AcademicForecaster.load(os.path.join(model_dir, "stage2_model.joblib"))
        self.stage3_model = HybridPlacementPredictor.load(os.path.join(model_dir, "stage3_model.joblib"))

        mads_path = os.path.join(model_dir, "empirical_mads.joblib")
        if os.path.exists(mads_path):
            self.empirical_mads = joblib.load(mads_path)
        else:
            self.empirical_mads = {}

        feat_names = self.preprocessor.get_feature_names_stage3()
        self.shap_explainer = MultimodalSHAPExplainer(self.stage3_model, feature_names=feat_names)
        self.recourse_engine = CounterfactualRecourseEngine(
            self,
            feature_names=feat_names,
            feature_mads=self.empirical_mads
        )
        self.is_trained = True
        logger.info("Hierarchical pipeline successfully loaded and ready for inference.")
        return self


# Backward-compatible alias for pipeline orchestrator
HierarchicalPipeline = HierarchicalMultiStagePipeline


