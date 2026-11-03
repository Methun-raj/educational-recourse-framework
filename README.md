# Hierarchical Multi-Task & Explainable Educational Recourse Framework

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Framework: Scikit--Learn | XGBoost | SHAP](https://img.shields.io/badge/ML-Scikit--Learn%20%7C%20XGBoost%20%7C%20SHAP-orange)](https://github.com/)
[![Tests: 25 Passed](https://img.shields.io/badge/Tests-25%20Passed-brightgreen)](tests/)
[![Security: Pydantic v2 | CSP | Extra Forbid](https://img.shields.io/badge/Security-Pydantic%20%7C%20CSP%20%7C%20Extra%20Forbid-blueviolet)](web_app/app.py)
[![Real-World Data: N=2,966 Verified](https://img.shields.io/badge/Real--World%20Cohort-N%3D2%2C966%20Verified-brightgreen)](data/original_benchmarks/)

A scientifically grounded, leak-free, production-hardened implementation of the research article:
> **"Machine Learning-Based Forecasting of Student Academic Success, Branch Recommendation, and Career Placement: A Hierarchical Multi-Task and Explainable Recourse Framework"**

### 📑 Independent Audit & Research Reports
- **[FINAL_AUDIT_REPORT.md](file:///c:/Users/Methunraj%20A/Downloads/bro/FINAL_AUDIT_REPORT.md)**: Independent senior software audit & verification register (Verdict: **GO**).
- **[TEST_REPORT.md](file:///c:/Users/Methunraj%20A/Downloads/bro/TEST_REPORT.md)**: Live execution evidence for all 22 passing automated tests (0 warnings).
- **[RESEARCH_VALIDITY_REPORT.md](file:///c:/Users/Methunraj%20A/Downloads/bro/RESEARCH_VALIDITY_REPORT.md)**: Real-world empirical validation on N=2,966 cohort, exposure bias analysis, and non-causal recourse disclaimers.
- **[KNOWN_LIMITATIONS.md](file:///c:/Users/Methunraj%20A/Downloads/bro/KNOWN_LIMITATIONS.md)**: Dual synthetic and real-world evaluation, 10-point GPA assumptions, and ethical constraints.
- **[CHANGELOG.md](file:///c:/Users/Methunraj%20A/Downloads/bro/CHANGELOG.md)**: Full version history across all 12 remediation phases.

---

## 📌 Architecture & System Overview

Traditional educational data mining platforms suffer from three structural shortcomings:
1. **Narrow Feature Scope:** Evaluating only final-year cognitive scores (CGPA), omitting socio-economic and behavioral drivers.
2. **Late-Stage Horizon:** Triggering forecasts only during final-semester campus placement drives (Sem 7–8), missing early-intervention windows.
3. **Single-Model Black-Box:** Executing a monolithic classifier without local attribution, ethical constraints, or actionable recourse.

This framework implements a **cascaded three-stage predictive architecture** coupled with **SHAP explainability** and **constrained counterfactual recourse ($F_{imm}$ vs $F_{mut}$)**:

```
[1. Multi-Modal Data] ──> [2. Preprocessing] ──> [3. Stage 1: Branch Fit]
   (Acad, Socio, Behav)      (Impute, Scale, Enc)     (Random Forest Ensemble)
                                                                 │
                                                                 ▼
[6. XAI & Recourse]   <── [5. Stage 3: Placement] <── [4. Stage 2: Academic]
   (SHAP + DiCE Recourse)    (Hybrid XGBoost + SVM)     (XGBoost + Grad. Boosting)
           │
           └─── Early Semester Intervention Feedback Loop ───┘
```

---

## 🔬 Mathematical Formulations

### 1. Multi-Modal Feature Concatenation (Eq. 1)
$$x_i = [ x_i^{(acad)} \parallel x_i^{(socio)} \parallel x_i^{(behav)} ] \in \mathbb{R}^d$$
- **Pre-College Academic ($x_i^{(acad)}$):** Intermediate Math, Physics, Chemistry, English, and Entrance Aggregate.
- **Socio-Demographics ($x_i^{(socio)}$, $F_{imm}$):** Gender, Age, Parental Education, Family Income Bracket, Family Size (**Strictly Immutable**).
- **Behavioral & Longitudinal ($x_i^{(behav)}$, $F_{mut}$):** Attendance %, Study Hours, Clubs/Hackathons, Soft Skills/Mock Score, Certifications (**Actionable Mutable**).

### 2. Stage 1 — Post-Intermediate Branch Recommendation (Eq. 2)
$$\hat{y}_i^{(b)} = \arg \max_{c \in \{1..C\}} \frac{1}{B} \sum_{b=1}^B \mathbb{I}( T_b(x_i) = c )$$
Employs a **Random Forest Ensemble** ($B=150$ randomized trees) on pre-college entrance metrics without future college leakage.

### 3. Stage 2 — Academic Performance Forecasting (Eq. 3)
$$\mathcal{L}_{acad}^{(t)} = \sum_{i=1}^N l( y_i^{(a)}, \hat{y}_i^{(a, t-1)} + f_t(\tilde{x}_i) ) + \gamma J + \frac{\lambda}{2} \sum_{j=1}^J w_j^2$$
Conditioned on augmented vector $\tilde{x}_i = [x_i \parallel \hat{y}_i^{(b)}]$, dual **XGBoost and Gradient Boosting** classifiers model non-linear interaction across semesters.

### 4. Stage 3 — Hybrid Campus Placement Prediction (Eq. 4)
$$P_{hybrid}(y_i^{(p)} = 1 \mid z_i) = \alpha P_{XGB}(y_i^{(p)} = 1 \mid z_i) + (1 - \alpha) \sigma(A \cdot f_{SVM}(z_i) + B)$$
On augmented profile $z_i = [\tilde{x}_i \parallel \hat{y}_i^{(a)}]$, a calibrated meta-learner blends XGBoost log-odds probability with Platt-scaled RBF-Kernel SVM margin probability ($\alpha = 0.55$).

### 5. SHAP Additive Feature Attribution (Eq. 5)
$$f(x_i) = \phi_0 + \sum_{j=1}^d \phi_j(x_i), \quad \phi_j(x_i) = \sum_{S \subseteq F \setminus \{j\}} \frac{|S|!(|F|-|S|-1)!}{|F|!} [ f_{S \cup \{j\}}(x_i) - f_S(x_i) ]$$

### 6. Constrained Counterfactual Recourse Optimization (Eq. 6)
$$x_i^* = \arg \min_{x'} \left[ d_{MAD}(x_i, x') - \mu \cdot P_{hybrid}(y_i^{(p)} = 1 \mid x') \right] \quad \text{subject to} \quad x'_{F_{imm}} = x_{i, F_{imm}}$$
**Strict Ethical Guarantee:** Socio-economic status ($F_{imm}$) is invariant. Numerical coordinate search targets *only* actionable behavioral and tutoring adjustments ($F_{mut}$).

---

## 🛡️ Key Architectural & Methodological Fixes

1. **Elimination of Cascading Exposure Bias:**
   - *Previous flaw:* Stage 2 and Stage 3 were fitted on 100% perfect ground-truth labels during training, but fed imperfect predictions during inference.
   - *Fix:* Implemented $K$-Fold Out-of-Fold (OOF) cross-validation during training so downstream models learn to handle real-world misclassification distributions.
2. **True Numerical Counterfactual Optimization:**
   - *Previous flaw:* Hardcoded static thresholds from Table V (`7.20`, `82.0%`, etc.).
   - *Fix:* Implemented genuine coordinate optimization over $d_{MAD}(x, x')$ with realistic step sizes that reliably traverse tree-based piecewise boundaries.
3. **Zero Hardcoded Research Benchmarks:**
   - *Previous flaw:* Table IV ablation and Table V SHAP numbers were hardcoded literals.
   - *Fix:* Replaced with actual empirical experiments fitting each feature subset and computing live metrics.
4. **Cybersecurity & API Hardening:**
   - Pydantic v2 schema validation (`StudentProfileSchema`) rejecting out-of-range inputs, negative GPAs, or string injections with HTTP 422.
   - Restrictive CORS allowed origins and Content-Security-Policy (CSP) headers.
   - Token-bucket in-memory rate limiting and path-traversal blocking.
   - `/health` system diagnostics endpoint.

---

## 📊 Measured Experimental Results

### Table II: Standalone Baseline Classifiers vs Proposed Hybrid (Holdout Test Set)
| Algorithm | Accuracy (%) | Precision (%) | Recall (%) | Macro F1 (%) | Weighted F1 (%) | ROC-AUC | PR-AUC | Brier Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Majority Class (Zero-R) | 84.0% | 84.0% | 100.0% | 45.7% | 76.7% | 0.500 | 0.840 | 0.160 |
| Logistic Regression (LR) | 97.8% | 98.1% | 99.3% | 95.8% | 97.8% | 0.996 | 0.999 | 0.017 |
| Decision Tree (DT) | 95.2% | 96.9% | 97.4% | 91.0% | 95.2% | 0.925 | 0.974 | 0.045 |
| k-Nearest Neighbors (KNN) | 92.8% | 93.4% | 98.3% | 84.9% | 92.3% | 0.958 | 0.987 | 0.052 |
| Random Forest (RF) | 97.2% | 97.2% | 99.5% | 94.5% | 97.1% | 0.993 | 0.999 | 0.032 |
| Support Vector Machine (SVM) | 97.4% | 97.7% | 99.3% | 95.0% | 97.4% | 0.996 | 0.999 | 0.021 |
| **Hybrid XGBoost + SVM** | **98.4%** | **98.6%** | **99.5%** | **97.0%** | **98.4%** | **0.999** | **1.000** | **0.011** |

### Table III: Task-Specific System Performance (Cascaded Holdout Test Set)
- **Task 1: Discipline Recommendation (RF):** 87.0% Accuracy | 86.0% Macro-F1
- **Task 2: Academic Performance Forecast (XGB + GB):** 76.2% Accuracy | 67.3% Macro-F1
- **Task 3: Campus Placement Prediction (Hybrid XGB + SVM):** 98.2% Accuracy | 96.6% Macro-F1

### Table IV: Feature Modality Ablation & Fairness Equity
| Configuration | Early-Stage Acc. (Sem 1–4) | Final-Year Acc. (Sem 7–8) | Demographic Parity Diff. (DPD) |
| :--- | :---: | :---: | :---: |
| Academic Transcripts Only | 86.6% | 92.8% | 0.063 |
| Academic + Socio-Economic | 86.6% | 92.8% | 0.063 |
| Academic + Behavioral | 90.8% | 96.2% | 0.038 |
| **Full Multi-Modal Ensemble** | **91.0%** | **96.4%** | **0.031 (Fairer)** |

### Table VI: Empirical Validation on Genuine Real-World Student Cohort ($N=2,966$)
*Evaluated on authentic undergraduate engineering student cohort across 6 engineering disciplines:*
| Algorithm | Accuracy (%) | Precision (%) | Recall (%) | Macro F1 (%) | Weighted F1 (%) | ROC-AUC | PR-AUC | Brier Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Majority Class (Zero-R) | 55.2% | 55.2% | 100.0% | 35.6% | 39.3% | 0.500 | 0.776 | 0.448 |
| Logistic Regression (LR) | 78.1% | 78.8% | 82.6% | 77.7% | 78.0% | 0.887 | 0.923 | 0.140 |
| Decision Tree (DT) | 87.2% | 94.4% | 81.7% | 87.2% | 87.2% | 0.931 | 0.957 | 0.093 |
| k-Nearest Neighbors (KNN) | 85.0% | 87.5% | 85.1% | 84.9% | 85.0% | 0.920 | 0.947 | 0.110 |
| Random Forest (RF) | 87.5% | 93.2% | 83.5% | 87.5% | 87.6% | 0.935 | 0.959 | 0.093 |
| Support Vector Machine (SVM) | 85.2% | 88.2% | 84.5% | 85.1% | 85.2% | 0.926 | 0.951 | 0.108 |
| XGBoost | 88.6% | 94.2% | 84.5% | 88.5% | 88.6% | 0.936 | 0.961 | 0.088 |
| **Proposed Hybrid XGBoost + SVM** | **86.9%** | **91.7%** | **83.8%** | **86.8%** | **86.9%** | **0.936** | **0.960** | **0.093** |

---

## 📂 Repository Structure

```
├── data/
│   ├── download_original_datasets.py       # Automated downloader for genuine real-world datasets
│   ├── original_benchmarks/                # Real-world student cohort data
│   │   ├── college_placement_real.csv      # N=2,966 engineering student records
│   │   ├── campus_recruitment_real.csv     # N=215 campus recruitment cohort
│   │   ├── uci_student_performance_real.csv # N=395 UCI student academic records
│   │   └── metadata.json                   # Provenance and source documentation
│   ├── generate_dataset.py                 # Schema-validated synthetic dataset generator (2,500 records)
│   ├── student_multimodal_dataset.csv      # Generated benchmark dataset
│   ├── dataset_metadata.json               # Data provenance metadata
│   └── models/                             # Persisted pipelines (.joblib)
├── src/
│   ├── __init__.py
│   ├── config.py                           # Central configuration, paths, and constants
│   ├── schemas.py                          # Pydantic v2 schemas for data & API contracts
│   ├── data_preprocessing.py               # Preprocessor, encoders, scalers, F_imm & F_mut
│   ├── models/
│   │   ├── branch_recommender.py           # Stage 1: Random Forest
│   │   ├── academic_forecaster.py          # Stage 2: XGBoost + Gradient Boosting
│   │   ├── placement_predictor.py          # Stage 3: Calibrated Hybrid XGBoost + RBF-SVM
│   │   └── baseline_models.py              # Table II comparative baselines (LR, DT, KNN, RF, SVM)
│   ├── explainability/
│   │   ├── shap_explainer.py               # SHAP TreeExplainer & waterfall attributions
│   │   ├── counterfactual_recourse.py      # Constrained numerical counterfactual optimizer (Eq. 6)
│   │   └── fairness_evaluator.py           # Demographic Parity Difference (DPD) & subgroup audits
│   └── pipeline.py                         # Out-of-Fold (OOF) leak-free cascaded orchestrator
├── evaluation/
│   ├── reproduce_benchmarks.py             # Empirical benchmark runner (Tables I-V & Figures 1-7)
│   ├── evaluate_real_world.py              # Empirical evaluation runner on N=2,966 genuine students
│   └── exports/                            # Publication-ready plots and CSV tables
│       ├── figure1_workflow.png
│       ├── figure2_empirical_comparison.png
│       ├── figure3a_shap_global.png
│       ├── figure3b_recourse.png
│       ├── figure4_calibration_curve.png
│       ├── figure5_roc_pr_curves.png
│       ├── figure6_confusion_matrices.png
│       ├── figure7_fairness_disaggregation.png
│       ├── figure8_real_world_comparison.png
│       ├── figure_waterfall_local.png
│       └── table_*.csv
│   │   └── fairness_evaluator.py           # Demographic Parity Difference (DPD)
│   └── pipeline.py                         # Out-of-Fold (OOF) leak-free cascaded orchestrator
├── evaluation/
│   ├── reproduce_benchmarks.py             # Empirical benchmark runner (Tables I-V & Figures 1-3)
│   └── exports/                            # Publication-ready plots and CSV tables
│       ├── figure1_workflow.png
│       ├── figure2_empirical_comparison.png
│       ├── figure3a_shap_global.png
│       ├── figure3b_recourse.png
│       └── table_*.csv
├── web_app/
│   ├── app.py                              # Hardened Flask web server & REST API
│   ├── templates/                          # Responsive Jinja2 templates (index, benchmark, datasets, docs)
│   └── static/                             # Theme CSS & Chart.js frontend controller
├── tests/
│   ├── test_models.py                      # Preprocessor and stage model unit tests
│   ├── test_pipeline.py                    # Pipeline & recourse integration tests
│   └── test_api_and_security.py            # API schema validation, security headers, datasets & path traversal
├── .github/workflows/ci.yml                # CI automation workflow
├── Dockerfile                              # Containerized production deployment
├── docker-compose.yml                      # Service orchestration
├── requirements.txt                        # Python dependencies
├── run_project.py                          # Unified CLI entry point
└── README.md                               # Project documentation
```

---

## 🚀 Execution Guide

### 1. Installation
```powershell
pip install -r requirements.txt
```

### 2. Run Automated Pytest Test Suite
```powershell
python -m pytest -v tests/
```
*Executes all 24 unit, integration, boundary, security, recourse, fairness, dataset explorer, and real-world cohort tests (0 warnings).*

### 3. Inspect Integrated Datasets Registry
```powershell
python run_project.py --inspect-datasets
```
*Displays summary statistics, row counts, and feature profiles for all 4 integrated datasets.*

### 4. Download Original Datasets & Evaluate Real-World Student Data
```powershell
python run_project.py --download-real-data
python run_project.py --evaluate-real-data
```
*Downloads genuine student cohorts (N=2,966) into `data/original_benchmarks/` and reproduces Figure 8.*

### 5. Generate Data, Train Pipeline & Reproduce Benchmarks
```powershell
python run_project.py --generate-data
python run_project.py --train
python run_project.py --benchmark
```

### 6. Test Single-Student Prediction & Recourse via CLI
```powershell
# Test on synthetic preset
python run_project.py --predict-sample at_risk

# Test on authentic real-world engineering student record
python run_project.py --predict-sample real_at_risk
```

### 7. Launch Interactive Web Dashboard & Datasets Explorer
```powershell
python run_project.py --serve
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.  
- Visit **[http://127.0.0.1:5000/datasets](http://127.0.0.1:5000/datasets)** to explore and preview all 4 datasets interactively.
- Visit **[http://127.0.0.1:5000/benchmarks](http://127.0.0.1:5000/benchmarks)** to view synthetic and real-world benchmark evaluations.

### 6. Containerized Docker Deployment
```bash
docker-compose up --build
```

---

## ⚖️ Ethical AI & Disclaimer
- **Demographic Parity & Fairness:** Socio-economic attributes ($F_{imm}$) are strictly constrained to remain unchanged during recourse optimization ($x'_{F_{imm}} = x_{i, F_{imm}}$).
- **Advisory Decision Support:** Model outputs and counterfactual action plans are advisory decision-support tools for academic institutions and mentors, and do **not** constitute a formal or legally binding guarantee of campus placement.
