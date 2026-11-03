# Comprehensive Test Execution & Security Verification Report

**Project:** Hierarchical Multi-Task & Explainable Educational Recourse Framework  
**Document Version:** 2.3.0  
**Audit Date:** 2026-11-01  
**Status:** 100% Passed (25/25 Automated Tests)

---

## 1. Test Execution Environment & Configuration

| Parameter | Specification / Environment Value |
|---|---|
| **Operating System** | Microsoft Windows (x86_64) |
| **Python Runtime** | Python 3.14.6 (`C:\Users\Methunraj A\AppData\Local\Python\pythoncore-3.14-64\python.exe`) |
| **Test Runner** | `pytest` v9.1.1 (Pluggy v1.6.0, AnyIO v4.14.2) |
| **Execution Command** | `python -m pytest -v tests/` |
| **Total Test Cases** | 25 collected |
| **Pass Count** | 25 passed (0 failed, 0 skipped, 0 xfailed, 0 warnings) |
| **Test Duration** | ~43.7 seconds |

---

## 2. Test Execution Breakdown by Test Suite

### Suite 1: API Security, Input Validation & Reliability (`tests/test_api_and_security.py`)

| Test Identifier | Verified Capability / Security Control | Status | Evidence / Notes |
|---|---|---|---|
| `test_health_check_endpoint` | Verifies `/health` endpoint returns HTTP 200 with service status, version, and dependencies. | **PASSED** | Response payload contains `{"status": "healthy", "service": ...}`. |
| `test_security_headers_present` | OWASP Top 10 HTTP security headers injection on all Flask responses. | **PASSED** | Validates headers: `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security`, `Referrer-Policy: no-referrer`. |
| `test_api_predict_valid_payload` | Valid end-to-end prediction via `/api/predict` returns stage 1, stage 2, stage 3 outputs, SHAP, and recourse. | **PASSED** | JSON response contains valid probabilities, intermediate predictions, SHAP attributions, and recourse actions. |
| `test_api_predict_invalid_cgpa_boundary` | Pydantic v2 validation boundary enforcement on numerical inputs ($CGPA > 10.0$). | **PASSED** | Returns HTTP 422 Unprocessable Entity with specific field validation error. |
| `test_api_predict_missing_mandatory_fields` | Schema enforcement on missing required student fields (e.g., missing `intermediate_math`). | **PASSED** | Returns HTTP 422 with missing field breakdown. |
| `test_api_predict_non_json_rejection` | Content-Type checking rejecting malformed or non-JSON payloads. | **PASSED** | Returns HTTP 400 Bad Request. |
| `test_path_traversal_blocked_on_exports` | Defense-in-depth path traversal attack mitigation on `/api/export` (e.g. `../../etc/passwd`). | **PASSED** | Path traversal sequences blocked via `os.path.basename()` whitelist sanitization. Returns HTTP 400. |
| `test_readiness_probe_endpoint` | Kubernetes/container readiness probe endpoint at `/ready` and `/api/ready`. | **PASSED** | Returns HTTP 200 when models and preprocessors are loaded; returns HTTP 503 if artifacts are absent. |
| `test_api_predict_rejects_unauthorized_extra_fields` | Schema injection rejection via Pydantic `extra="forbid"`. | **PASSED** | Passing malicious unexpected field `{"admin_override": True}` triggers HTTP 422 rejection. |
| `test_datasets_endpoints` | Datasets explorer view and metadata/preview API endpoint verification. | **PASSED** | `/datasets` returns HTTP 200; `/api/datasets` returns metadata for all datasets; `/api/datasets/<name>` returns paginated records. |
| `test_api_sample_real_student` | Authentic student sampling from real-world cohort and end-to-end inference verification. | **PASSED** | `/api/sample/real_at_risk` returns valid student schema; passing through `/api/predict` returns valid 3-stage cascaded prediction and recourse. |
| `test_user_data_integration_endpoint` | Dynamic user-supplied student data integration, schema validation, and persistence. | **PASSED** | Validates `POST /api/datasets/integrate` (HTTP 201), verifies automatic cascade prediction filling, and confirms rejection on out-of-boundary values (HTTP 422). |

---

## 3. Machine Learning Models & Baseline Evaluation (`tests/test_models.py`)

| Test Identifier | Verified Capability / ML Component | Status | Evidence / Notes |
|---|---|---|---|
| `test_preprocessor_fitting` | MultiModalPreprocessor correctly imputes, one-hot encodes, and normalizes tabular features across all 3 stages. | **PASSED** | Output feature dimensions match expectations; no NaNs remain after transformation. |
| `test_stage1_branch_recommender` | Random Forest multi-class branch recommender fits, predicts, and outputs calibrated multi-class probabilities summing to 1.0. | **PASSED** | Matrix shape $(N, 4)$, probabilities sum to $1.0 \pm 1e-5$, classification accuracy $\ge 0.70$. |
| `test_stage2_academic_forecaster` | XGBoost + GradientBoosting ensemble predicts longitudinal academic performance categories and probability distributions. | **PASSED** | Matrix shape $(N, 3)$, probabilities sum to $1.0 \pm 1e-5$, classification accuracy $\ge 0.65$. |
| `test_stage3_hybrid_placement_predictor` | Hybrid XGBoost + RBF-SVM ensemble with Platt calibration outputs calibrated binary probabilities $\in [0.0, 1.0]$ and classification metrics. | **PASSED** | Calibration reduces Brier score; ECE calculated; metrics dictionary contains ROC-AUC, PR-AUC, F1, and Brier score. |
| `test_baseline_models_suite` | Baseline comparison suite evaluates 6 standalone models including Majority Class (Zero-R) lower-bound baseline. | **PASSED** | Evaluates Zero-R, Logistic Regression, Decision Tree, KNN, Random Forest, and SVM. Produces Weighted F1 and Macro F1. |
| `test_real_world_dataset_evaluation` | Ingestion, validation, and benchmarking on genuine real-world engineering student cohort ($N=2,966$). | **PASSED** | Verifies CSV structure, feature alignment, and hybrid model performance ($AUC \ge 0.85$) on real student placement data. |

---

## 3. Hierarchical Pipeline, Invariance, Recourse & Fairness (`tests/test_pipeline.py`)

| Test Identifier | Verified Capability / Algorithmic Guarantee | Status | Evidence / Notes |
|---|---|---|---|
| `test_pipeline_sequential_inference` | End-to-end cascading inference sequentially predicts Stage 1 branch $\to$ Stage 2 academic $\to$ Stage 3 placement. | **PASSED** | Intermediate predictions automatically flow into Stage 2 and Stage 3 inputs without user intervention. |
| `test_counterfactual_recourse_strict_immutability` | Recourse optimization strictly locks immutable characteristics ($\Delta = 0$). | **PASSED** | Features `gender`, `age`, `parental_status`, `parental_education`, `family_income_bracket`, and intermediate entrance marks remain strictly unchanged. |
| `test_shap_waterfall_attribution` | Multimodal TreeExplainer decomposes placement prediction into additive local feature attributions. | **PASSED** | Top features identified; waterfall plot generated without error. |
| `test_ground_truth_label_invariance` | Invariance to ground-truth intermediate label tampering during inference. | **PASSED** | Injecting conflicting ground-truth labels `recommended_branch="Mechanical Engineering"` and `academic_performance="Poor"` into an at-risk profile produces **identical** predictions ($P_{\text{tampered}} == P_{\text{original}}$). |
| `test_counterfactual_bounds_and_costs` | Algorithmic recourse adheres to directional bounds (e.g. CGPA non-decreasing) and returns finite normalized L1 MAD cost. | **PASSED** | Target probability $\ge 0.75$ achieved; counterfactual CGPA $\ge$ baseline CGPA; normalized cost $\in (0, \infty)$. |
| `test_fairness_evaluator_comprehensive` | Comprehensive demographic fairness evaluation across sensitive demographic cohorts. | **PASSED** | Calculates Demographic Parity Difference (DPD), Demographic Parity Ratio (DPR), and Equal Opportunity Difference (EOD). |
| `test_shap_perturbation_consistency` | Perturbation validation verifying that perturbing the highest-attributed SHAP feature moves the output margin in the predicted direction. | **PASSED** | Positive SHAP attribution increases placement probability when feature is increased. |

---

## 3. Boundary & Penetration Test Details

### 3.1 Pydantic v2 `extra="forbid"` Payload Injection Test
- **Payload:**
  ```json
  {
    "age": 19,
    "gender": "Female",
    "intermediate_math": 88.0,
    ...
    "malicious_injection_token": "DROP TABLE students;",
    "bypass_auth": true
  }
  ```
- **Response:** HTTP 422 Unprocessable Entity
- **Validation Message:** `"Extra inputs are not permitted [type=extra_forbidden, input_value='DROP TABLE students;']"`

### 3.2 Path Traversal Attack on Report Export
- **Request:** `GET /api/export?file=../../../../Windows/System32/drivers/etc/hosts`
- **Response:** HTTP 400 Bad Request
- **Log:** Security audit logged traversal attempt; sanitized via `os.path.basename()` whitelist.

### 3.3 Negative & Out-of-Bound Numerical Feature Checks
- **Input:** `cgpa = 11.5` (Valid scale: 0.0 to 10.0) $\to$ HTTP 422 Rejected.
- **Input:** `attendance_percentage = -5.0` (Valid scale: 0.0 to 100.0) $\to$ HTTP 422 Rejected.
- **Input:** `study_hours_per_week = 85.0` (Valid bound: $\le 60.0$) $\to$ HTTP 422 Rejected.

---

## 4. Test Conclusion

All 25 automated test cases executed cleanly with zero failures. The test suite verifies end-to-end mathematical correctness, architectural isolation of the hierarchical cascade, algorithmic recourse constraints, SHAP attribution consistency, OWASP API security hardening, real-world student dataset empirical validity, dataset registry/preview APIs, and dynamic user data integration.
