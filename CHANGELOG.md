# Changelog: Hierarchical Multi-Task & Explainable Educational Recourse Framework

All notable changes, structural corrections, security remediations, and research enhancements applied to this repository are documented in this file.

---

## [2.0.0-RELEASE] - Final Comprehensive Verification & Remediation Release

### Phase 1 & 2: Architectural Cascade Leakage Prevention & Exposure Bias Elimination
- **Fixed Training-Inference Mismatch:**
  - Stage 2 (`AcademicForecaster`) and Stage 3 (`HybridPlacementPredictor`) previously trained on ground-truth intermediate labels (`recommended_branch` and `academic_performance`), but during inference operated on upstream predictions, causing distribution shift (exposure bias).
  - Implemented 5-Fold Stratified Out-of-Fold (OOF) cross-validation in [`HierarchicalMultiStagePipeline.train()`](file:///c:/Users/Methunraj%20A/Downloads/bro/src/pipeline.py#L95-L160) to generate realistic intermediate predictions (`oof_branch_preds`, `oof_acad_preds`) for all training records.
  - Downstream models are now trained strictly on intermediate out-of-fold predictions.
- **Fold-Isolated Preprocessing:**
  - Fold preprocessors ([`MultiModalPreprocessor`](file:///c:/Users/Methunraj%20A/Downloads/bro/src/data_preprocessing.py)) are fit exclusively on the $K-1$ training folds during OOF generation, preventing data leakage across validation folds.
- **Strict Ground-Truth Invariance at Inference:**
  - Modified [`predict_placement_probability()`](file:///c:/Users/Methunraj%20A/Downloads/bro/src/pipeline.py#L225-L255) and [`predict_student()`](file:///c:/Users/Methunraj%20A/Downloads/bro/src/pipeline.py#L275-L330) to explicitly strip any pre-existing `recommended_branch` or `academic_performance` keys from input dictionaries prior to sequential cascade evaluation.
  - Ground-truth intermediate label tampering has provably zero effect on inference outputs (verified by [`test_ground_truth_label_invariance`](file:///c:/Users/Methunraj%20A/Downloads/bro/tests/test_pipeline.py#L134-L148)).

### Phase 3: Research Benchmark Suite Overhaul & Publication Figures
- **Empirical Measurement Verification:**
  - Overhauled [`evaluation/reproduce_benchmarks.py`](file:///c:/Users/Methunraj%20A/Downloads/bro/evaluation/reproduce_benchmarks.py) to compute all benchmark metrics dynamically from live model predictions rather than synthetic hardcoded values.
  - Added Majority Class (Zero-R) dummy classifier baseline to Table II to establish a rigorous lower-bound benchmark.
  - Added Brier Score and PR-AUC tracking across baseline and proposed models.
  - Added publication-quality visualization generators for Figures 1, 2, 3a, 3b, and local waterfall SHAP plots.

### Phase 4 & 8: Data Pipeline, Input Validation & Security Hardening
- **Pydantic v2 Schema Hardening:**
  - Updated [`StudentProfileSchema`](file:///c:/Users/Methunraj%20A/Downloads/bro/src/schemas.py#L32-L75) with `model_config = ConfigDict(extra="forbid")` to immediately reject payloads containing unexpected or injected attributes (HTTP 422).
  - Enforced strict numerical bounds on all features (e.g., CGPA $\in [0.0, 10.0]$, Attendance $\in [0.0, 100.0]$).
- **OWASP Top 10 API Security Hardening:**
  - Configured `MAX_CONTENT_LENGTH = 1_048_576` (1MB limit) in [`web_app/app.py`](file:///c:/Users/Methunraj%20A/Downloads/bro/web_app/app.py#L48) to prevent denial-of-service payload attacks.
  - Implemented defense-in-depth path traversal prevention in `/api/export` using `os.path.basename()` and secure whitelist validation.
  - Injected complete OWASP HTTP security headers (`Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`, `Referrer-Policy`) on all responses.
  - Added `/ready` and `/api/ready` readiness probe endpoints verifying model artifact presence and operational readiness.

### Phase 5: Probability Calibration & Stage 3 Hybrid Predictor
- **Platt Calibration on Blended Logits:**
  - Implemented logistic calibration (`LogisticRegression`) in [`HybridPlacementPredictor`](file:///c:/Users/Methunraj%20A/Downloads/bro/src/models/placement_predictor.py#L110-L135) fitted on out-of-fold blended probabilities to correct uncalibrated ensemble outputs.
  - Added Expected Calibration Error (ECE) metric calculation ([`compute_expected_calibration_error`](file:///c:/Users/Methunraj%20A/Downloads/bro/src/models/placement_predictor.py#L22-L40)).
  - Supported dual-mode probability outputs: `predict_proba(X, calibrated=True)` and `predict_proba_uncalibrated(X)`.

### Phase 6: Constrained Algorithmic Counterfactual Recourse
- **Normalized L1 Cost Metric with Empirical MADs:**
  - Implemented Median Absolute Deviation (MAD) scaling across all numerical features calculated from training distributions and serialized into model artifacts.
  - Enforced strict immutable feature constraints: gender, age, parental education, family income bracket, and pre-college intermediate exam scores are locked ($\Delta = 0$).
  - Enforced directional feasibility bounds (e.g., CGPA and attendance cannot decrease; study hours $\le 45$).
  - Full multi-stage cascade recalculation: at every candidate counterfactual step, intermediate Stage 1 branch fit and Stage 2 academic performance are dynamically recomputed to reflect the perturbed student profile.

### Phase 7: Explainable & Responsible AI Enhancements
- **TreeExplainer Attribution & Consistency:**
  - Configured TreeExplainer on the dominant gradient boosted decision tree component ($\alpha = 0.55$).
  - Added [`validate_attribution_consistency()`](file:///c:/Users/Methunraj%20A/Downloads/bro/src/explainability/shap_explainer.py#L105-L130) to empirically verify that perturbing top-attributed features moves the output margin in the predicted direction.
  - Added local waterfall plot generator [`plot_waterfall()`](file:///c:/Users/Methunraj%20A/Downloads/bro/src/explainability/shap_explainer.py#L132-L157).
- **Fairness & Equity Audit:**
  - Expanded [`FairnessEvaluator`](file:///c:/Users/Methunraj%20A/Downloads/bro/src/explainability/fairness_evaluator.py) with Demographic Parity Ratio (DPR), Equal Opportunity Difference (EOD), and subgroup disaggregation audits across sensitive demographic cohorts.

### Phase 9 & 10: Testing & Verification Infrastructure
- **Comprehensive Automated Test Suite:**
  - Expanded test coverage from 15 to 21 automated pytest test cases across [`test_api_and_security.py`](file:///c:/Users/Methunraj%20A/Downloads/bro/tests/test_api_and_security.py), [`test_models.py`](file:///c:/Users/Methunraj%20A/Downloads/bro/tests/test_models.py), and [`test_pipeline.py`](file:///c:/Users/Methunraj%20A/Downloads/bro/tests/test_pipeline.py).
  - 100% test pass rate achieved (21/21 passed).
