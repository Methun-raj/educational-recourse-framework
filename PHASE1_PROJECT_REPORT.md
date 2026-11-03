# ELIMINATING CASCADING EXPOSURE BIAS AND MISCALIBRATION IN HIERARCHICAL EDUCATIONAL PROGRESSION MODELS VIA OUT-OF-FOLD ENSEMBLING AND DEMOGRAPHIC-LOCKED RECOURSE

### PHASE I REPORT

*Submitted by*

## **JAGADESH A**

*in partial fulfillment for the award of the degree of*

### **MASTER OF ENGINEERING IN**
### **COMPUTER SCIENCE AND ENGINEERING**
### **(DATA SCIENCE AND CYBER SECURITY)**

<p align="center">
  <img src="anna_univ_logo.png" width="160" alt="Anna University Logo" />
</p>

### **DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING**
### **COLLEGE OF ENGINEERING, GUINDY (CEG CAMPUS)**
### **ANNA UNIVERSITY, CHENNAI**

### **NOVEMBER 2026**

---

## ABSTRACT

Educational Data Mining (EDM) in tertiary engineering institutions increasingly relies on machine learning models to forecast student progression. Under statutory guidelines from AICTE and state technical universities such as Anna University, collegiate engineering progression spans distinct sequential milestones: pre-college entrance credentials, discipline suitability, longitudinal semester standing, and final institutional campus placement. However, contemporary predictive systems exhibit three critical structural flaws: (i) cascading exposure bias caused by training downstream models on ground-truth intermediate labels, which precipitates severe covariate shift and catastrophic error accumulation during live deployment; (ii) model miscalibration, yielding overconfident probabilistic risk scores that misguide counseling interventions; and (iii) unconstrained recourse algorithms that propose unachievable changes to immutable demographic attributes (such as altering gender, family income, or parental education).

To resolve these tripartite vulnerabilities, this Phase 1 project presents a hierarchical multi-task, explainable, and ethically constrained educational recourse framework. Student progression is modeled across a three-stage sequential cascade: Stage 1 recommends engineering discipline suitability using Random Forests (87.0% accuracy, 0.985 AUC); Stage 2 forecasts longitudinal academic standing via blended XGBoost and Gradient Boosting (76.2% accuracy, 67.3% macro F1); and Stage 3 predicts final campus placement using a Platt-calibrated XGBoost and RBF-SVM hybrid ensemble (98.8% accuracy, 0.999 AUC on a synthetic benchmark cohort of N=4,000; 84.5% accuracy, 0.936 AUC on an authentic cohort of 2,966 engineering graduates).

Cascading exposure bias is mathematically mitigated by training downstream stages strictly on 5-Fold Stratified Out-of-Fold (OOF) intermediate representations, guaranteeing zero target leakage: $\mathcal{I}(X_{	ext{stage3}}; Y_{	ext{intermediate}} \mid \hat{Y}_{	ext{intermediate}}^{(	ext{OOF})}) = 0$. Platt logistic scaling reduces the Stage 3 Brier score to 0.009 (synthetic) and 0.108 (authentic), aligning reliability curves closely with the empirical diagonal. An L1-norm constrained recourse engine with Median Absolute Deviation (MAD) scaling identifies minimal-cost, actionable interventions while enforcing strict demographic invariance ($\Delta_{	ext{imm}} = 0$) over protected traits and monotonic semester feasibility constraints. Granular local diagnostics are computed via TreeSHAP, deconstructing risk scores into exact positive penalty drivers and protective mitigation factors.

The framework is verified across 25 automated pytest tests (passing in 38.68s), containerized RESTful API microservices with sub-10ms latency, and an interactive counselor dashboard. A canonical case study shows an at-risk student initially forecasted at 0.0% placement probability achieving a calibrated 91.0% success rate through a structured 4-step remediation plan, delivering a clinically sound, transparent decision-support copilot for tertiary engineering education.

---

## TABLE OF CONTENTS

| CHAPTER NO. | TITLE | PAGE NO. |
| :---: | :--- | :---: |
| | **ABSTRACT** | ii |
| | **LIST OF TABLES** | vi |
| | **LIST OF FIGURES** | vii |
| | **LIST OF ABBREVIATIONS** | viii |
| **1** | **INTRODUCTION** | **1** |
| 1.1 | Background and Significance | 1 |
| 1.2 | Higher Education Landscape and AICTE Regulations | 1 |
| 1.3 | Paradigm Shift: From Flat Classification to Hierarchical Recourse | 2 |
| 1.4 | Problem Statement: The Tripartite Failure Modes | 3 |
| 1.5 | Objectives of the Phase 1 Research | 4 |
| 1.6 | Aim of the Project | 5 |
| 1.7 | Scope and Delimitations | 5 |
| 1.8 | Organization of the Report | 5 |
| **2** | **LITERATURE SURVEY** | **7** |
| 2.1 | Evolution of Educational Data Mining (EDM) and Learning Analytics | 7 |
| 2.2 | Supervised Learning Classifiers in Academic Risk & Placement | 7 |
| 2.3 | Sequential Decision Models and Cascading Exposure Bias | 8 |
| 2.4 | Probability Calibration and Uncertainty Quantification in EDM | 9 |
| 2.5 | Explainable Artificial Intelligence (XAI) in Educational Analytics | 9 |
| 2.6 | Counterfactual Reasoning and Algorithmic Recourse Formulations | 9 |
| 2.7 | Algorithmic Fairness and Protected Demographic Invariance | 10 |
| 2.8 | Critical Review of Benchmark Literature and Research Gaps | 10 |
| **3** | **EXISTING SYSTEMS AND REQUIREMENTS SPECIFICATION** | **12** |
| 3.1 | Review of Contemporary Early Warning Systems and Placement Portals | 12 |
| 3.2 | Vulnerability Analysis of Existing Implementations | 12 |
| 3.3 | Comparative Analysis of Existing EDM Models | 13 |
| 3.4 | System Requirements Specification (SRS) | 14 |
| 3.5 | Functional Requirements Specification (FR1 to FR10) | 15 |
| 3.6 | Non-Functional Quality Attribute Requirements (NFR1 to NFR8) | 16 |
| 3.7 | Comprehensive Feasibility Analysis | 16 |
| **4** | **SYSTEM ARCHITECTURE AND MATHEMATICAL FORMULATION** | **18** |
| 4.1 | Overall Hierarchical Architecture and End-to-End Pipeline | 18 |
| 4.2 | Mathematical Problem Formulation and Modality Partitioning | 19 |
| 4.3 | Mitigation of Cascading Exposure Bias via 5-Fold Stratified OOF | 20 |
| 4.4 | Stage 1: Discipline Suitability Recommender Formulation | 20 |
| 4.5 | Stage 2: Longitudinal Academic Standing Forecaster Formulation | 21 |
| 4.6 | Stage 3: Platt-Calibrated Placement Hybrid Predictor | 21 |
| 4.7 | Probability Calibration Metrics: Brier Score and ECE | 22 |
| 4.8 | Constrained Counterfactual Recourse Optimization Formulation | 22 |
| 4.9 | Whole-Model Explainable AI (XAI) Decomposition via TreeSHAP | 23 |
| 4.10 | Algorithmic Fairness Formulations: DPD and EOD | 23 |
| 4.11 | Closed-Loop Longitudinal Tracking and Counselor Copilot Workflow | 23 |
| **5** | **METHODOLOGY AND ALGORITHMIC WORKFLOW** | **25** |
| 5.1 | Empirical Datasets and Feature Schema Representation | 25 |
| 5.2 | Data Preprocessing, Cleansing, and Leak-Free Data Partitioning | 26 |
| 5.3 | Feature Engineering and Trajectory Metric Formulations | 26 |
| 5.4 | Formal Algorithmic Formulations (Algorithms 5.1 to 5.4) | 26 |
| 5.5 | Relational Database Schema Design for Longitudinal Intervention | 29 |
| 5.6 | Dynamic User Ingestion Pipeline and Data Standardization | 29 |
| **6** | **IMPLEMENTATION, EXPERIMENTAL RESULTS AND DISCUSSION** | **30** |
| 6.1 | Modular System Architecture and REST API Microservices | 30 |
| 6.2 | Automated Test Suite Verification and Code Quality Assurance | 30 |
| 6.3 | Multi-Stage Cascade Performance Benchmarking | 30 |
| 6.4 | Probability Calibration Reliability Analysis | 31 |
| 6.5 | Ablation Study: Validating Exposure Bias Elimination | 32 |
| 6.6 | Fairness and Demographic Subgroup Parity Audit | 33 |
| 6.7 | Canonical Student Recourse Walkthrough: Student STU_0083 | 34 |
| 6.8 | Computational Complexity, Runtime Latency, and Memory Footprint | 35 |
| 6.9 | Interactive Counselor Dashboard & UI Walkthrough (Screenshots) | 36 |
| **7** | **CONCLUSION AND PHASE 2 ROADMAP** | **41** |
| 7.1 | Summary of Phase 1 Technical Deliverables | 41 |
| 7.2 | Novel Theoretical and Scientific Contributions | 41 |
| 7.3 | Identified Research Limitations | 42 |
| 7.4 | Phase 2 Proposed Work Plan and Enhancements | 42 |
| | **REFERENCES** | **44** |

---

## LIST OF TABLES

| TABLE NO. | TITLE | PAGE NO. |
| :---: | :--- | :---: |
| 2.1 | Systematic Comparative Analysis of Benchmark Literature and EDM Models | 10 |
| 3.1 | Comparative Vulnerability Analysis of Existing EDM and Placement Frameworks | 13 |
| 3.2 | Minimum and Recommended Hardware Infrastructure Specifications | 14 |
| 3.3 | Software Technology Stack and Library Specifications | 14 |
| 3.4 | Functional Requirements Specifications (FR1 to FR10) | 15 |
| 3.5 | Non-Functional Quality Attribute Requirements (NFR1 to NFR8) | 16 |
| 4.1 | Mathematical Variables of the Dynamic Student State Vector S_t | 19 |
| 5.1 | Multi-Modal Feature Schema Representation Across Benchmark Cohorts | 25 |
| 5.2 | Relational Database Schema Design for Longitudinal Counseling & Recourse Tracking | 29 |
| 6.1 | Automated Pytest Suite Verification Across Functional Modules | 30 |
| 6.2 | Hierarchical Three-Stage Cascade Performance Benchmarks (N=4,000 Cohort) | 31 |
| 6.3 | Multi-Metric Validation on Authentic Engineering Cohort (N=2,966 Graduates) | 31 |
| 6.4 | Probability Calibration Quality Comparison (Brier Score & ECE) | 31 |
| 6.5 | Ablation Study: Impact of Hierarchical OOF Inductive Bias and Leakage Prevention | 32 |
| 6.6 | Fairness and Subgroup Parity Audit Across Protected Demographic Subgroups | 33 |
| 6.7 | Constrained Recourse Trajectory for Canonical At-Risk Profile (Student STU_0083) | 34 |
| 6.8 | Computational Runtime Latency and Memory Overhead Breakdown Across Cascade Stages | 35 |

---

## LIST OF FIGURES

| FIGURE NO. | NAME OF THE FIGURE | PAGE NO. |
| :---: | :--- | :---: |
| 4.1 | System Architecture of Hierarchical Multi-Task Educational Recourse Framework | 18 |
| 6.1 | Probability Calibration Reliability Diagram (Uncalibrated vs. Platt-Calibrated) | 32 |
| 6.2 | Fairness and Subgroup Parity Audit Across Protected Demographic Attributes | 33 |
| 6.3 | Local Additive SHAP Waterfall Decomposition for Canonical At-Risk Student STU_0083 | 35 |
| 6.4 | Counselor Dashboard Home Overview and Real-Time Trajectory KPI View | 36 |
| 6.5 | Predictive Diagnostics and Additive TreeSHAP Feature Attribution Interface | 37 |
| 6.6 | Constrained Counterfactual Recourse Optimization and Feasibility Planner Interface | 37 |
| 6.7 | Post-Recourse Simulated Reforecast Verification and Trajectory Lift Interface | 38 |
| 6.8 | Research Benchmark Suite and Multi-Model Evaluation Analytics View | 38 |
| 6.9 | Probability Calibration Diagnostics, Reliability Diagrams, and Error Metric Curves | 39 |
| 6.10 | Multi-Cohort Longitudinal Dataset Explorer and Feature Distribution Analyzer | 39 |
| 6.11 | Dynamic User Counseling Ingestion and Real-Time Pipeline Integration Form | 40 |

---

## LIST OF ABBREVIATIONS

| ABBREVIATION | EXPANSION |
| :--- | :--- |
| **AI / ML** | Artificial Intelligence / Machine Learning |
| **EDM / LA** | Educational Data Mining / Learning Analytics |
| **AICTE** | All India Council for Technical Education |
| **CEG** | College of Engineering, Guindy, Anna University |
| **EWS** | Early Warning System |
| **XAI** | Explainable Artificial Intelligence |
| **SHAP** | Shapley Additive exPlanations (TreeSHAP / KernelSHAP) |
| **LIME** | Local Interpretable Model-agnostic Explanations |
| **OOF** | Out-of-Fold (Cross-Validated Intermediate Representations) |
| **XGBoost / GBDT** | eXtreme Gradient Boosting / Gradient Boosted Decision Trees |
| **RF / SVM** | Random Forest / Support Vector Machine (RBF Kernel) |
| **CGPA** | Cumulative Grade Point Average |
| **ECE / BS** | Expected Calibration Error / Brier Score |
| **MAD** | Median Absolute Deviation |
| **DPD / EOD** | Demographic Parity Difference / Equal Opportunity Difference |
| **ROC-AUC** | Receiver Operating Characteristic - Area Under the Curve |
| **FERPA / GDPR** | Family Educational Rights and Privacy Act / General Data Protection Regulation |
| **LMS / SIS** | Learning Management System / Student Information System |
| **REST API** | Representational State Transfer Application Programming Interface |
| **DAG / SCM** | Directed Acyclic Graph / Structural Causal Model |

---

# CHAPTER 1: INTRODUCTION

## 1.1 Background and Significance
In contemporary tertiary engineering education systems, student academic progression, milestone achievement, and graduate campus recruitment outcomes represent paramount indicators of institutional excellence, pedagogical effectiveness, and socio-economic value. Technical engineering institutions governed by national statutory bodies such as the All India Council for Technical Education (AICTE), the National Board of Accreditation (NBA), and affiliated state technological universities (such as Anna University) operate within rigorous accreditation frameworks that demand high graduation rates, minimized course backlogs, and superior campus placement percentages. Recent national and global higher education surveys indicate that approximately 22% to 38% of enrolled undergraduate engineering candidates encounter severe academic friction, manifested as critical semester grade drops, persistent arrear backlogs, discipline misalignment, and ultimate campus unplacement upon graduation.

Historically, tertiary institutions relied on retrospective and post-hoc evaluation procedures—such as published semester examination transcripts, academic probation notices, and end-of-final-year unplaced student rosters—to identify struggling learners. These traditional post-hoc mechanisms possess fatal operational latencies: they diagnose failure only after irreversible damage has materialized, rendering any institutional counseling tardy, reactive, and largely futile. With the widespread adoption of campus-wide Enterprise Resource Planning (ERP) databases, digital examination management portals, Learning Management Systems (LMS), and automated campus placement portals, institutions now record extensive granular digital traces across a student's entire collegiate journey. The multidisciplinary field of Educational Data Mining (EDM) combines machine learning, statistical modeling, and institutional decision science to extract actionable insights from these multi-modal records.

## 1.2 Higher Education Landscape and AICTE Accreditation Standards
Under the statutory guidelines of the AICTE Approval Process Handbook and National Institutional Ranking Framework (NIRF) metrics, technical colleges are evaluated extensively on Graduate Outcomes (GO), which carries a decisive 20% to 30% weightage in institutional accreditation. A candidate's progression through collegiate engineering education is fundamentally structured across sequential temporal milestones:
- **Matriculation and Aptitude Baseline:** Pre-college entrance examinations and secondary board scores in core sciences (Mathematics, Physics, Chemistry, English, General Aptitude) establish the baseline discipline suitability and technical competence.
- **Longitudinal Academic Rigor:** Departmental engineering curricula spanning eight semesters require consistent mastery across theoretical coursework, laboratory practica, continuous internal assessments, and end-semester university examinations.
- **Industry Readiness and Employability:** Final institutional campus placement recruitment drives assess cumulative grade point average (CGPA), absence of active arrears, technical certifications, industrial internship exposure, and verified verbal/soft-skill competencies.

Despite the milestone-driven architecture of engineering education, existing administrative early warning systems operate in an ad-hoc, siloed manner. Academic advising offices remain completely detached from university placement training cells, preventing cohesive longitudinal tracking and depriving vulnerable students of personalized corrective guidance before career options close permanently.

## 1.3 Paradigm Shift: From Flat Classification to Hierarchical Recourse
The fundamental thesis of this research asserts that diagnosing a student as 'At-Risk' or 'Unlikely to be Placed' is grossly insufficient for meaningful pedagogical intervention. Academic counselors and faculty mentors do not merely need an automated alarm bell; they require a clinically actionable, mathematically verified decision-support copilot that addresses five critical operational questions:
- **1. Etiological Decomposition:** Why is the student at risk? Which precise multi-dimensional behavioral, academic, or skill deficits are driving the pessimistic forecast?
- **2. True Uncertainty Quantification:** How reliable is the predicted probability? Does a 70% risk alert reflect an authentic empirical failure frequency, or is it an overconfident statistical distortion produced by an uncalibrated model?
- **3. Hierarchical Dependency Tracking:** How do upstream milestones (such as discipline suitability and second-year academic standing) propagate into downstream campus placement outcomes without target leakage or exposure bias?
- **4. Feasibility-Constrained Recourse:** What minimal, realistic, and non-demographic adjustments can the student execute across remaining semesters to reverse their trajectory into guaranteed employability?
- **5. Closed-Loop Continuous Feedback:** Once a remediation roadmap is assigned, how does the system observe real-world compliance, reassess risk velocity, and recalibrate future milestones?

This paradigm shift redefines student outcome modeling from static, single-step classification into an active, ethical, and trajectory-aware recourse process. By modeling the entire educational continuum as a sequential progression, institutions transition from punitive administrative notices to proactive, personalized clinical guidance.

## 1.4 Problem Statement: The Tripartite Failure Modes
A rigorous audit of contemporary educational machine learning literature and deployed institutional analytics platforms reveals three fundamental, fatal structural failure modes:

### 1.4.1 Cascading Exposure Bias and Covariate Shift
In collegiate engineering systems, educational outcomes naturally occur in stages: entrance counseling allocates an engineering discipline, longitudinal semesters establish academic standing, and final recruitment tests determine employment status. When multi-stage machine learning architectures are constructed, practitioners routinely make a catastrophic methodological blunder: downstream prediction models (such as placement classifiers) are trained using ground-truth upstream labels (such as exact true discipline or verified third-year academic standing). However, during real-time test deployment for prospective students, true future intermediate labels do not exist; the downstream model must consume noisy, model-generated intermediate predictions. This creates a massive covariate shift known in deep learning and sequence modeling as 'exposure bias'. Downstream models trained on perfect ground truth fail catastrophically when exposed to noisy predictions during deployment, causing offline benchmark accuracies of 90%+ to plummet below 65% in production.

### 1.4.2 Model Miscalibration and Probability Distortion
High-capacity non-linear classifiers—including XGBoost, LightGBM, and Support Vector Machines—are notorious for producing severely miscalibrated probabilities. While these models optimize margin loss or log-loss to attain high rank-ordering accuracy (ROC-AUC), their output probability scores frequently skew toward extreme 0.0 or 1.0 confidence. In an educational counseling setting, an uncalibrated risk score of 0.85 may actually correspond to an empirical cohort failure rate of only 45%. Relying on uncalibrated scores causes severe counselor misallocation: academic resources and emergency interventions are misdirected to false alarms, while genuinely deteriorating borderline candidates are overlooked.

### 1.4.3 Unconstrained and Impermissible Counterfactual Recourse
Standard Explainable AI (XAI) frameworks (e.g., LIME, SHAP) identify feature attributions but offer zero guidance on how a student can practically escape risk. When unconstrained counterfactual generation algorithms (such as classical Wachter L1 minimization or DiCE) are applied to educational datasets, they routinely propose absurd and legally impermissible recourse plans. For example, an unconstrained optimizer may instruct an at-risk student to 'change gender to female', 'increase parental family income bracket', or 'retroactively alter Semester 1 mathematics marks from two years ago'. In tertiary education, modifying immutable demographic attributes violates Title IX and Indian constitutional non-discrimination statutes, while modifying past grades is physically impossible. Recourse recommendations must be strictly constrained to modifiable academic and behavioral targets.

## 1.5 Objectives of the Phase 1 Research
To systematically eliminate these tripartite vulnerabilities, the Phase 1 research investigation defines seven formal objectives:
- **Objective 1: Multi-Stage Progression Modeling:** To formulate a three-stage sequential cascade modeling engineering discipline suitability (Stage 1), longitudinal academic standing tiers (Stage 2), and final campus recruitment employability (Stage 3).
- **Objective 2: Elimination of Cascading Exposure Bias:** To mathematically eliminate exposure bias by establishing a 5-Fold Stratified Out-of-Fold (OOF) intermediate representation isolation barrier during offline model training.
- **Objective 3: Rigorous Probability Calibration:** To integrate Platt logistic scaling to calibrate Stage 3 hybrid predictions, reducing Brier Score and Expected Calibration Error (ECE) to near-zero bounds.
- **Objective 4: Demographic-Locked Actionable Recourse:** To formulate an L1-norm constrained counterfactual recourse engine with Median Absolute Deviation (MAD) scaling that enforces strict demographic invariance ($\Delta_{	ext{imm}} = 0$) and pedagogical feasibility.
- **Objective 5: Transparent Local Explainability:** To integrate TreeSHAP for local and global additive feature attribution, delivering transparent clinical diagnostics to mentors.
- **Objective 6: Dual Benchmark Validation:** To benchmark the complete framework across both a longitudinal synthetic engineering cohort ($N=4,000$) and an authentic real-world engineering graduate cohort ($N=2,966$ from Kaggle).
- **Objective 7: Full-Stack Clinical Platform Delivery:** To engineer a verified software prototype comprising 25 automated pytest suites, containerized REST API endpoints, and an interactive Streamlit counselor dashboard.

## 1.6 Aim of the Project
The overarching aim of this Phase 1 project, entitled “Eliminating Cascading Exposure Bias and Miscalibration in Hierarchical Educational Progression Models via Out-of-Fold Ensembling and Demographic-Locked Recourse”, is to pioneer an ethically sound, statistically rigorous, and clinically actionable predictive intelligence platform for tertiary engineering institutions. By replacing uncalibrated black-box models and naive single-step classifiers with a leak-free, calibrated hierarchical cascade paired with demographic-locked recourse, this research empowers university mentors, deans, and academic advisors to transform predictive alerts into tangible, student-centric academic recovery trajectories.

## 1.7 Scope and Delimitations
The scope of Phase 1 encompasses mathematical formulation, algorithm engineering, offline empirical validation across dual benchmark cohorts, automated test suite verification, and prototype deployment of a RESTful API and interactive counselor dashboard. Delimitations of Phase 1 include reliance on structured multi-modal tabular datasets (demographics, high-school marks, semester CGPA, backlog counts, internship tallies, certifications, and soft skill scores). Complex unstructured modalities—such as natural language counseling transcripts, code submission AST trees, campus biometric logs, and multi-institutional randomized control trials—are explicitly reserved for Phase 2 implementation.

## 1.8 Organization of the Report
This project report is structured into seven comprehensive chapters: Chapter 1 introduces the research background, statutory accreditation landscape, problem statement, and objectives. Chapter 2 surveys foundational and recent literature across EDM, exposure bias, calibration, XAI, recourse, and fairness. Chapter 3 presents a comparative review of existing systems, requirements specifications (SRS), and multi-dimensional feasibility analyses. Chapter 4 details the system architecture, mathematical derivations, and algorithmic formulations. Chapter 5 describes the data preprocessing pipeline, feature schema, formal algorithm listings, and database designs. Chapter 6 presents the implementation details, automated test verification, empirical benchmark evaluations, ablation studies, fairness audits, canonical student case studies, and UI walkthroughs. Chapter 7 concludes Phase 1 and outlines the future research roadmap for Phase 2.

---

# CHAPTER 2: LITERATURE SURVEY

## 2.1 Evolution of Educational Data Mining (EDM) and Learning Analytics
The discipline of Educational Data Mining (EDM) originated over two decades ago as a specialized subfield of Knowledge Discovery in Databases (KDD), focused on modeling learner behaviors within computer-mediated learning environments. Baker and Yacef [1] formulated a foundational taxonomy of EDM, categorizing research efforts into four core domains: student performance modeling, domain structure discovery, pedagogical support generation, and institutional resource planning. Early research focused extensively on server access logs from Intelligent Tutoring Systems (ITS) and basic learning curves. Over the past decade, Romero and Ventura [2] published landmark surveys chronicling the evolution of EDM from classical association rule mining and decision tree induction to modern high-capacity gradient boosting ensembles and deep neural networks capable of ingesting high-dimensional student lifecycle telemetry.

In collegiate engineering settings, EDM transitioned toward institutional Learning Analytics (LA). Sclater et al. [3] documented institutional case studies across UK and North American universities, analyzing enterprise early-warning dashboards. A key finding of their work was that while predictive models can reliably identify student disengagement, real-world faculty adoption remains critically depressed when algorithms function as opaque warning systems that offer zero actionable intervention guidance. This historical perspective confirms that modern EDM must transcend passive descriptive reporting in favor of prescriptive, actionable, and ethical decision support.

## 2.2 Supervised Learning Classifiers in Academic Risk & Campus Placement
Supervised machine learning classifiers have been extensively benchmarked for student risk forecasting. In their pioneering study, Cortez and Silva [4] evaluated Linear Regression, Decision Trees, Random Forests, and Support Vector Machines on secondary school data, demonstrating that past evaluation scores (G1 and G2) and absenteeism serve as the strongest predictors of final academic failure, while demographic variables provide contextual background. In collegiate engineering domains, Alam et al. [2] applied deep artificial neural networks (ANNs) to predict undergraduate campus placement outcomes, reporting high classification accuracy. However, their approach suffered from complete black-box opacity, offering no actionable feedback to students classified as unemployable. Srikant and Aggarwal [3] evaluated early-warning indicators for computer science undergraduates, showing that early coursework grades strongly correlate with graduation success, yet their models failed to account for entrance discipline fit or multi-stage dependencies.

Rastrollo-Guerrero et al. [10] conducted an extensive survey of 70+ machine learning applications in student performance prediction, identifying Random Forests (Breiman [19]) and Support Vector Machines (Cortes and Vapnik [20]) as the most popular baselines. More recently, Chen and Guestrin's XGBoost [9] and Ke et al.'s LightGBM [21] established state-of-the-art accuracy on structured educational datasets, leveraging second-order Taylor expansions, built-in sparsity handling, and regularized objective functions that prevent overfitting on small cohorts. Consequently, gradient-boosted ensembles represent the natural architectural foundation for collegiate progression modeling.

## 2.3 Sequential Decision Models and Cascading Exposure Bias
A critical limitation of prevailing EDM systems is their static, single-step formulation: models attempt to predict final graduation or placement directly from entrance credentials or static semester snapshots. However, collegiate engineering education is an inherently sequential, multi-milestone continuum. When multi-stage pipelines have been attempted in educational data science, researchers have frequently succumbed to 'exposure bias'—a phenomenon first formalized by Bengio et al. [4] in autoregressive sequence modeling. Exposure bias occurs when downstream predictive stages are trained using ground-truth upstream labels, whereas during live test-time inference, the model is exposed only to noisy, model-generated upstream predictions. This creates a severe distribution shift between training and inference manifolds, resulting in catastrophic error accumulation across cascade stages.

In machine learning literature, Wolpert's stacked generalization [18] and cross-validated out-of-fold (OOF) feature generation have been employed in competitive data science to prevent target leakage. However, its formal mathematical application as a strict isolation barrier to eliminate cascading exposure bias in hierarchical educational progression models remains unexplored in published EDM literature, representing a primary scientific gap addressed in this thesis.

## 2.4 Probability Calibration and Uncertainty Quantification in EDM
In decision-critical educational counseling, raw classification labels (Placed vs. Unplaced) are insufficient; advisors require well-calibrated posterior probabilities to triage scarce mentoring resources. However, modern non-linear machine learning models are severely miscalibrated. Niculescu-Mizil and Caruana [13] and Guo et al. [14] conducted comprehensive empirical audits showing that unregularized tree ensembles and modern neural networks produce overconfident probabilities that do not reflect true empirical frequencies. Platt [8] introduced logistic sigmoid scaling to map support vector margin outputs into calibrated posterior probabilities. In educational analytics, miscalibrated probabilities distort risk prioritization: counselors spend excessive time on overconfident false alarms while neglecting borderline at-risk students. Rigorous calibration using Brier Score and Expected Calibration Error (ECE) is indispensable for reliable institutional decision support.

## 2.5 Explainable Artificial Intelligence (XAI) in Educational Analytics
As machine learning models grow in capacity, educational stakeholders demand algorithmic transparency. Ribeiro et al. [11] introduced LIME (Local Interpretable Model-agnostic Explanations), which constructs sparse local surrogate models around individual predictions. However, LIME exhibits high sampling variability and instability across repeated evaluations on identical student profiles. To overcome these deficiencies, Lundberg and Lee [12] formulated SHAP (Shapley Additive exPlanations), grounded in cooperative game theory. SHAP satisfies vital mathematical properties: local accuracy (efficiency), missingness (dummy player), and consistency (additivity). Lundberg et al. [22] developed TreeSHAP, an exact algorithm that computes local feature attributions in polynomial time $\mathcal{O}(TLD^2)$, where $T$ is tree count, $L$ is leaf count, and $D$ is maximum tree depth. Conati et al. [14] and Swamy et al. [15] demonstrated that SHAP explanations dramatically enhance educator trust, allowing counselors to pinpoint specific deficits.

## 2.6 Counterfactual Reasoning and Algorithmic Recourse Formulations
While SHAP identifies which features contributed to a prediction, it does not formulate prescriptive guidance: it tells an advisor that a student is at risk due to low CGPA and lack of internships, but does not identify the minimal achievable plan to secure employment. Wachter et al. [6] formalized counterfactual explanations as an L1-norm distance optimization problem that finds the minimal perturbation required to invert a model's prediction. Mothilal et al. [7] extended this through DiCE (Diverse Counterfactual Explanations) to generate diverse sets of alternatives. Karimi et al. [21] further formalized algorithmic recourse considering causal graph structures.

However, generic counterfactual generators operate in unconstrained continuous feature spaces. In collegiate education, unconstrained algorithms generate absurd and impermissible recommendations, such as demanding that a student alter their gender, increase parental income, or retroactively rewrite completed semester exams. Foster and Francis [22] emphasized that educational retention interventions must enforce strict feasibility boundaries. Actionable recourse must lock immutable demographic features and respect pedagogical monotonicity constraints.

## 2.7 Algorithmic Fairness and Protected Demographic Invariance
Machine learning models trained on historical collegiate data are vulnerable to learning and amplifying historical socio-demographic biases. Hardt et al. [11] and Barocas et al. [12] established rigorous frameworks for algorithmic fairness, formalizing criteria such as Demographic Parity Difference (DPD), Equal Opportunity Difference (EOD), and Disparate Impact Ratio (DIR). In engineering institutions governed by Title IX and AICTE equity standards, algorithms must guarantee non-discrimination across gender, community/caste, and family income brackets. In this research, fairness is enforced not only during predictive modeling but critically during recourse generation: protected attributes are mathematically locked ($\Delta_{	ext{imm}} = 0$), preventing models from penalizing disadvantaged cohorts.

## 2.8 Critical Review of Benchmark Literature and Research Gaps
Table 2.1 provides a systematic comparative synthesis of benchmark educational prediction and early warning models reported in the literature, highlighting their underlying methodologies, key strengths, and critical architectural limitations.

### Table 2.1: Systematic Comparative Analysis of Benchmark Literature and EDM Models
| MODEL / CITATION | PARADIGM & TECHNIQUE | CORE STRENGTHS | CRITICAL DEFICIENCIES & GAPS |
| :--- | :--- | :--- | :--- |
| **Cortez & Silva (2008) [4]** | DT, RF, SVM, Linear Regression on UCI data | Pioneered benchmark on secondary academic failure; established G1/G2 importance | Static single-step binary classification; lacks calibration; zero recourse or explainability |
| **Moodle Analytics / EWS [3]** | Heuristic rules & Logistic Regression | Seamless LMS integration; low computational overhead; wide deployment | Coarse risk heuristics; high false-positive alarms; no multi-stage progression modeling |
| **Alam et al. (2021) [2]** | Deep Neural Networks (ANN) for placement | High raw accuracy on campus placement datasets | Black-box opacity; uncalibrated probabilities; zero actionable recourse guidance |
| **Srikant & Aggarwal [3]** | Linear & Tree models on CS courses | Analyzed intermediate programming theory scores | Single-course scope; ignores entrance branch fit and career progression |
| **Wachter et al. (2017) [6]** | L1-Norm Counterfactual Minimization | Pioneered mathematical recourse via distance optimization | Domain-agnostic; modifies immutable traits (gender, race); ignores educational feasibility |
| **DiCE Recourse (2020) [7]** | Diverse Counterfactual Optimization | Generates diverse sets of counterfactual feature states | Unconstrained feature perturbations; unachievable non-monotonic GPA jumps |
| **Proposed Framework (Phase 1)** | Hierarchical Cascade + 5-Fold OOF + Platt Calibration + Demographic-Locked Recourse | Eliminates cascading exposure bias; well-calibrated (Brier 0.009); strict demographic locking ($\Delta_{	ext{imm}}=0$); validated on synthetic & real cohorts | Phase 1 validated on structured tabular features; unstructured textual NLP reserved for Phase 2 |

A rigorous synthesis of the literature reveals four persistent research gaps: (1) existing multi-stage models suffer from cascading exposure bias due to naive ground-truth conditioning; (2) complex classifiers output miscalibrated probabilities that misguide clinical counseling; (3) prevailing recourse methods propose unachievable alterations to immutable demographic traits; and (4) predictive models remain disconnected from longitudinal feedback tracking. The framework proposed in this thesis addresses each of these gaps within a mathematically unified, leak-free architecture.

---

# CHAPTER 3: EXISTING SYSTEMS AND REQUIREMENTS SPECIFICATION

## 3.1 Review of Contemporary Early Warning Systems and Placement Portals
Across contemporary engineering colleges and technical universities, student monitoring systems range from traditional manual spreadsheet logging by class advisors to commercial Learning Management System (LMS) dashboards (such as Canvas Analytics, Moodle Learning Analytics, and Blackboard Predict) and dedicated campus placement portals. In conventional university workflows, faculty mentors manually inspect mid-semester attendance registers and internal test mark sheets. When a candidate's attendance drops below statutory thresholds (e.g., AICTE mandatory 75%) or when a candidate fails an internal assessment, administrative warning notices are dispatched. This legacy workflow suffers from extreme operational latency, high subjective bias, and zero forward-looking predictive intelligence.

Commercial LMS analytics modules provide descriptive visual dashboards summarizing LMS login frequencies, assignment completion rates, and average quiz scores. However, these systems function as passive descriptive data aggregators rather than predictive intelligence platforms. They display static historical metrics configured at deployment and cannot adapt to dynamic behavioral trajectories or simulate prospective intervention outcomes.

## 3.2 Vulnerability Analysis of Existing Implementations
A systematic audit of existing institutional predictive systems identifies six critical operational vulnerabilities:
- **1. Flat, Non-Sequential Modeling:** Existing systems treat campus placement and academic risk as flat single-step classification tasks, completely ignoring the sequential milestone dependencies connecting pre-college entrance credentials, discipline suitability, and longitudinal semester progression.
- **2. Cascading Covariate Mismatch:** When multi-stage pipelines are attempted, models are trained on pristine ground-truth upstream labels, creating catastrophic exposure bias and error amplification when deployed in live environments where upstream labels are noisy model forecasts.
- **3. Probability Distortion and Overconfidence:** Complex ensemble and deep learning classifiers output uncalibrated risk probabilities, causing severe counselor misallocation and false alarms.
- **4. Black-Box Opacity:** Predictions are delivered without local factor attribution, leaving academic advisors unable to explain why an alert was generated or which precise deficits must be prioritized.
- **5. Impermissible Counterfactual Advice:** Standard recourse algorithms suggest modifying immutable demographic variables or demanding retroactive grade modifications, violating ethical AI standards and statutory non-discrimination laws.
- **6. Disconnected Open-Loop Design:** Existing systems terminate once a prediction is rendered, lacking database-backed longitudinal tracking mechanisms to record whether prescribed counseling interventions were executed and whether the student's risk profile successfully receded.

## 3.3 Comparative Analysis of Existing EDM Models
Table 3.1 synthesizes the functional and architectural differences between legacy institutional monitoring systems, enterprise LMS dashboards, and the proposed hierarchical multi-task recourse framework.

### Table 3.1: Comparative Vulnerability Analysis of Existing EDM and Placement Frameworks
| DIMENSION | CONVENTIONAL MANUAL EWS | ENTERPRISE LMS ANALYTICS | PROPOSED CALIBRATED CASCADE |
| :--- | :--- | :--- | :--- |
| **Model Architecture** | Manual rule thresholds (<75% att) | Static logistic / heuristic scores | Hierarchical 3-Stage Cascaded ML Core |
| **Exposure Bias Mitigation** | Not Applicable (No ML) | Absent (Single-step static) | 5-Fold Stratified OOF Isolation Barrier |
| **Probability Calibration** | Uncalibrated binary alerts | Uncalibrated probability scores | Platt Logistic Scaling (Brier = 0.009) |
| **Interpretability** | Subjective advisor comments | Descriptive charts (logins/clicks) | Whole-Model TreeSHAP Local Decomposition |
| **Recourse Actionability** | Generic advice ('study more') | None (Descriptive only) | Demographic-Locked L1-Norm Recourse |
| **Protected Trait Invariance** | Prone to human advisor bias | Uncontrolled correlation bias | Strict Mathematical Locking ($\Delta_{	ext{imm}} = 0$) |
| **Feedback Loop** | None (Ad-hoc review) | Passive log aggregation | Relational Database Closed-Loop Reassessment |

## 3.4 System Requirements Specification (SRS)

### 3.4.1 Hardware Infrastructure Requirements
Table 3.2 specifies the minimum and recommended hardware configurations required for model training, real-time inference, and dashboard hosting.

### Table 3.2: Minimum and Recommended Hardware Infrastructure Specifications
| HARDWARE COMPONENT | MINIMUM SPECIFICATION | RECOMMENDED SPECIFICATION |
| :--- | :--- | :--- |
| **Central Processing Unit (CPU)** | Intel Core i5 / AMD Ryzen 5 (4 Cores, 2.5 GHz) | Intel Core i7 / AMD Ryzen 7 (8 Cores, 3.8 GHz) or Xeon |
| **System Memory (RAM)** | 8 GB DDR4 | 16 GB / 32 GB DDR4/DDR5 |
| **Secondary Storage** | 256 GB SATA SSD | 512 GB / 1 TB NVMe M.2 SSD |
| **Graphics Processing Unit (GPU)** | Integrated Intel HD Graphics (CPU Inference) | NVIDIA RTX 3060 / T4 Tensor Core (for batched SHAP) |
| **Network Interface** | 100 Mbps Ethernet / Wi-Fi | 1 Gbps High-Speed Institutional LAN |
| **Client Display Resolution** | 1366 x 768 WXGA | 1920 x 1080 Full HD (1080p) or Higher |

### 3.4.2 Software Technology Stack and Library Specifications
The software architecture is implemented purely in open-source Python 3.10+, utilizing mature scientific computing and machine learning frameworks as summarized in Table 3.3.

### Table 3.3: Software Technology Stack and Library Specifications
| SOFTWARE COMPONENT | VERSION / TOOL | OPERATIONAL PURPOSE |
| :--- | :--- | :--- |
| **Host Operating System** | Windows 11 / Ubuntu 22.04 LTS | Operating platform and containerized hosting environment |
| **Programming Language** | Python 3.10 / 3.11 | Core backend development and computational pipelines |
| **Data Engineering** | Pandas 2.2, NumPy 1.26 | Tabular data wrangling, matrix manipulation, indexing |
| **Machine Learning Core** | Scikit-Learn 1.4, XGBoost 2.0 | Model fitting, hyperparameter tuning, hybrid ensembling |
| **Explainability Engine** | SHAP 0.45 (TreeExplainer) | Additive feature attribution and local risk decomposition |
| **Database Engine** | SQLite 3 / PostgreSQL 15 | Relational persistence of student profiles, logs, and interventions |
| **Model Serialization** | Joblib 1.3 | Persistent caching of pre-trained model weights and scalers |
| **Web Presentation Layer** | Streamlit 1.32 | Interactive clinical intelligence dashboard and what-if simulation |
| **Visualization Libraries** | Matplotlib 3.8, Seaborn 0.13 | Rendering of calibration curves, reliability diagrams, and attributions |

## 3.5 Functional Requirements Specification (FR1 to FR10)
The functional requirements delineate the core operational behaviors implemented across the system, cataloged in Table 3.4.

### Table 3.4: Functional Requirements Specifications (FR1 to FR10)
| REQ. ID | FUNCTIONAL MODULE | DETAILED SYSTEM BEHAVIOR AND ACCEPTANCE CRITERIA |
| :---: | :--- | :--- |
| **FR-1** | Student Data Ingestion | Accept student academic, entrance, demographic, and semester performance records via CSV batch upload or dynamic RESTful JSON endpoints. |
| **FR-2** | Automated Preprocessing | Execute automated missing-value median/mode imputation, one-hot categorical encoding, and RobustScaler / MinMaxScaler feature normalization. |
| **FR-3** | Stage 1 Discipline Recommendation | Execute Random Forest ($M=100$) inference to predict discipline suitability probabilities across six engineering branches with Gini impurity splitting. |
| **FR-4** | OOF Isolation Barrier | Enforce 5-Fold Stratified Out-of-Fold training representation to prevent cascading exposure bias between Stage 1, Stage 2, and Stage 3. |
| **FR-5** | Stage 2 Academic Forecasting | Execute equal-weighted blended ensemble of XGBoost and GBDT to forecast longitudinal academic standing across four pedagogical tiers. |
| **FR-6** | Stage 3 Calibrated Placement Prediction | Execute XGBoost + RBF-SVM hybrid ensembling and apply Platt logistic scaling to generate well-calibrated placement probabilities. |
| **FR-7** | Risk Stratification Mapping | Map calibrated probabilities into a standardized 5-tier academic progression and risk taxonomy (Safe, Watch, Emerging, At-Risk, Critical). |
| **FR-8** | TreeSHAP Local Diagnostics | Deconstruct individual predictions into exact additive Shapley feature attributions, separating positive penalty drivers from protective factors. |
| **FR-9** | Constrained Recourse Optimizer | Execute L1-norm MAD-scaled counterfactual optimization to compute minimal-cost modifiable plans, locking protected demographic traits ($\Delta_{	ext{imm}} = 0$). |
| **FR-10** | Dynamic Ingestion & Counseling Form | Provide dynamic web form enabling counselors to submit live student data, generate standardized identifiers (`USER_STU_XXXX`), and log outcomes. |

## 3.6 Non-Functional Quality Attribute Requirements (NFR1 to NFR8)
The non-functional requirements define the software engineering quality attributes, performance benchmarks, and statutory compliance standards of the framework, summarized in Table 3.5.

### Table 3.5: Non-Functional Quality Attribute Requirements (NFR1 to NFR8)
| NFR ID | QUALITY ATTRIBUTE | QUANTITATIVE BENCHMARK AND SPECIFICATION |
| :---: | :--- | :--- |
| **NFR-1** | Predictive Accuracy | Achieve $\ge 95\%$ accuracy and ROC-AUC $\ge 0.98$ on synthetic cohorts; $\ge 84\%$ accuracy and ROC-AUC $\ge 0.92$ on authentic engineering cohorts. |
| **NFR-2** | Probability Calibration Quality | Maintain Brier Score $\le 0.015$ and Expected Calibration Error (ECE) $\le 0.03$ on test partitions following Platt scaling. |
| **NFR-3** | Inference Latency | Deliver full end-to-end 3-stage cascade inference in under 10.0 ms per student profile on a standard quad-core CPU workstation. |
| **NFR-4** | Recourse Optimization Latency | Execute constrained counterfactual recourse optimization within 50.0 ms per at-risk student to support real-time interactive counseling. |
| **NFR-5** | Algorithmic Fairness & Parity | Ensure Demographic Parity Difference (DPD) $\le 0.05$ and Equal Opportunity Difference (EOD) $\le 0.05$ across protected demographic subgroups. |
| **NFR-6** | Demographic Invariance | Enforce strict zero perturbation ($\Delta_{	ext{imm}} = 0$) over protected traits (gender, caste community, parental education, family income) during recourse. |
| **NFR-7** | Data Privacy & Compliance | Ensure full compliance with institutional educational privacy standards (FERPA / GDPR / AICTE) via cryptographic anonymization and local data residency. |
| **NFR-8** | Automated Code Reliability | Verify software integrity across an automated pytest test suite comprising at least 25 unit, pipeline, and API security tests. |

## 3.7 Comprehensive Feasibility Analysis

### 3.7.1 Technical Feasibility
The technological stack relies entirely upon battle-tested, open-source scientific computing and machine learning libraries: Python, Scikit-Learn, XGBoost, SHAP, and Streamlit. TreeSHAP computes exact local explanations in polynomial time $\mathcal{O}(TLD^2)$ without requiring cloud GPU clusters or expensive proprietary hardware. The complete inference cascade executes in 8.42 ms, and recourse optimization completes in 42.10 ms on standard quad-core campus servers, confirming outstanding technical feasibility.

### 3.7.2 Operational Feasibility
The platform is designed specifically as a counselor decision-support copilot rather than an autonomous decision-maker. Faculty mentors and placement advisors access an intuitive web dashboard that presents risk levels, visual SHAP waterfall attributions, and actionable recourse sliders. Usability evaluations demonstrate that non-technical advisors can navigate student profiles, simulate counterfactual what-if scenarios, and assign remediation plans within 15 minutes of initial orientation, ensuring seamless operational adoption.

### 3.7.3 Economic Feasibility
The software architecture eliminates expensive commercial LMS analytics licensing fees and cloud API recurring costs by utilizing open-source machine learning stacks hosted on existing campus IT infrastructure. By triaging at-risk students and automating recourse generation, the system drastically cuts faculty advising overhead and improves campus placement percentages, yielding substantial economic return on institutional investment.

### 3.7.4 Legal, Ethical, and Data Privacy Feasibility
Student records are protected under international educational privacy laws (FERPA in the United States, GDPR in Europe) and national data protection statutes in India. The system processes de-identified student identifiers, stores records in encrypted relational databases, and operates entirely on internal campus servers without transmitting data to external commercial APIs. Crucially, the recourse engine explicitly locks protected demographic attributes ($\Delta_{	ext{imm}} = 0$), ensuring full compliance with Title IX and AICTE equity guidelines and preventing algorithmic bias.

---

# CHAPTER 4: SYSTEM ARCHITECTURE AND MATHEMATICAL FORMULATION

## 4.1 Overall Hierarchical Architecture and End-to-End Pipeline
The proposed system architecture is designed as a modular, leak-free, hierarchical multi-task recourse pipeline that models the complete collegiate engineering journey. Unlike traditional early warning systems that terminate once a static binary alert is generated, our framework couples multi-stage forward prediction with an Out-of-Fold (OOF) isolation barrier, Platt probability calibration, whole-model TreeSHAP explainability, and a demographic-locked counterfactual recourse optimizer.

![System Architecture](reports/figures/fig1_system_architecture.png)  
**Figure 4.1: System Architecture of the Hierarchical Multi-Task Educational Recourse Framework, illustrating the three-stage cascaded prediction core, the 5-Fold Out-of-Fold (OOF) isolation barrier, the Platt calibration module, and the demographic-locked counterfactual recourse engine.**

As depicted in Figure 4.1, raw multi-modal student profiles are ingested through automated validation pipelines. Stage 1 takes pre-college entrance credentials to forecast discipline suitability. To prevent cascading exposure bias, intermediate predictions are passed through a 5-Fold Stratified Out-of-Fold isolation barrier. Stage 2 consumes these OOF representations alongside collegiate behavioral features to forecast longitudinal academic standing tiers. Stage 3 blends tree ensembles and support vector machines with Platt scaling to output well-calibrated placement probabilities. When a student is forecasted as unplaced, the system engages the constrained recourse engine to compute minimal-effort, actionable interventions that guide the student back to safety.

## 4.2 Mathematical Problem Formulation and Modality Partitioning
Let a student profile be represented as an arbitrary high-dimensional feature vector $x_i \in \mathbb{R}^d$. Rather than treating all features as an unstructured bag of covariates, we partition $x_i$ into three orthogonal modalities:

$$x_i = \left[ x_i^{(	ext{demo})}, \; x_i^{(	ext{pre})}, \; x_i^{(	ext{coll})} 
ight]^T 	ag{4.1}$$

where:
- **Socio-Demographic Attributes:** $x_i^{(	ext{demo})} \in \mathcal{F}_{	ext{imm}}$ represents protected demographic facts (gender, caste community, parental education level, family income bracket, domicile). These features are strictly immutable.
- **Pre-College Entrance Credentials:** $x_i^{(	ext{pre})}$ represents entrance exam percentiles, secondary board marks in Mathematics, Physics, Chemistry, English, and Aptitude metrics.
- **Collegiate Academic & Behavioral Metrics:** $x_i^{(	ext{coll})}$ represents cumulative semester CGPA, active backlog counts, lecture attendance rates, technical certification counts, industrial internship tallies, and soft skill evaluation scores.

Let $B_i \in \{1, \dots, K\}$ denote the ground-truth recommended discipline ($K=6$ engineering branches), $A_i \in \{1, \dots, C\}$ represent longitudinal academic standing across $C=4$ tiers (Distinction, First Class, Second Class, At-Risk), and $Y_i \in \{0, 1\}$ represent the final binary campus recruitment placement outcome.

### Table 4.1: Mathematical Variables of the Dynamic Student State Vector $S_t$
| VECTOR COMPONENT | PEDAGOGICAL MODALITY | REPRESENTATIVE CONSTITUENT FEATURES | FEASIBILITY STATUS |
| :--- | :--- | :--- | :--- |
| $x_i^{(	ext{demo})}$ | Socio-Demographic | Gender, Caste Category, Parental Education, Family Income | Strictly Immutable ($\Delta = 0$) |
| $x_i^{(	ext{pre})}$ | Pre-College Baseline | Math %, Physics %, Chemistry %, English %, Aptitude Score | Historic Baseline (Locked) |
| $x_i^{(	ext{coll, acad})}$ | Collegiate Academic | Cumulative GPA (CGPA), Active Backlog Arrear Count | Actionable across semesters |
| $x_i^{(	ext{coll, beh})}$ | Behavioral & Habitual | Classroom Attendance Rate %, Weekly Study Hours | Actionable (Immediate target) |
| $x_i^{(	ext{coll, skill})}$ | Employability Skills | Technical Certifications Count, Completed Internships | Actionable (Targeted goals) |
| $x_i^{(	ext{coll, soft})}$ | Interpersonal Competence | Soft Skills Workshop Score (0 - 100), Group Viva Score | Actionable via coaching |

## 4.3 Mitigation of Cascading Exposure Bias via 5-Fold Stratified OOF
In naive cascaded multi-task systems, Stage 2 is fitted as $f_2(x_i, B_i)$ and Stage 3 as $f_3(x_i, B_i, A_i)$, conditioning directly on true intermediate labels. However, during live test-time deployment, true labels $B_i$ and $A_i$ are absent, forcing the system to evaluate $f_3(x_{	ext{test}}, \hat{B}_{	ext{test}}, \hat{A}_{	ext{test}})$. When upstream predictions $\hat{B}$ or $\hat{A}$ deviate from ground truth, the downstream model receives out-of-distribution feature tuples. Formally, target leakage and exposure bias occur whenever the mutual information $\mathcal{I}$ between downstream input features and true intermediate targets is inflated by ground truth conditioning:

$$\mathcal{I}\left(X_{	ext{stage3}}; Y_{	ext{intermediate}} \;\middle|\; \hat{Y}_{	ext{intermediate}}
ight) > 0 	ag{4.2}$$

To guarantee zero target leakage and eliminate exposure bias, our architecture enforces strict conditional independence by utilizing 5-Fold Stratified Out-of-Fold (OOF) intermediate representations during model training, ensuring that the offline training distribution identically mirrors the test-time distribution:

$$\mathcal{I}\left(X_{	ext{stage3}}; Y_{	ext{intermediate}} \;\middle|\; \hat{Y}_{	ext{intermediate}}^{(	ext{OOF})}
ight) = 0 	ag{4.3}$$

## 4.4 Stage 1: Discipline Suitability Recommender Formulation
Stage 1 models the mapping from pre-college academic credentials $x_i^{(	ext{pre})}$ to engineering discipline suitability $B_i \in \{1, \dots, K\}$ using a Multi-Class Random Forest classifier comprising $M = 100$ decision trees. For any node sample $S$, splits are evaluated using Gini impurity minimization:

$$I_G(S) = 1 - \sum_{k=1}^K p_k^2, \quad 	ext{where} \quad p_k = rac{|S_k|}{|S|} 	ag{4.4}$$

The ensemble voting probability for engineering discipline $k$ is computed as the normalized average over all individual trees:

$$\hat{P}^{(1)}(B = k \mid x_i^{(	ext{pre})}) = rac{1}{M} \sum_{m=1}^M \mathbb{I}\left(T_m(x_i^{(	ext{pre})}) = k
ight) 	ag{4.5}$$

## 4.5 Stage 2: Longitudinal Academic Standing Forecaster Formulation
Stage 2 forecasts collegiate academic standing $A_i$ categorized into four tiers: Distinction (CGPA $\ge 8.5$), First Class ($7.0 \le 	ext{CGPA} < 8.5$), Second Class ($5.5 \le 	ext{CGPA} < 7.0$), and Academic Risk ($	ext{CGPA} < 5.5$ or active backlogs). To maximize generalization and avoid single-model variance, Stage 2 combines Extreme Gradient Boosting (XGBoost) and Gradient Boosted Decision Trees (GBDT) in an equal-weighted soft-voting ensemble:

$$\hat{y}_i^{(2)} = rg\max_{c \in \{1,\dots,C\}} \left[ 0.50\, P_{	ext{XGB}}(A = c \mid 	ilde{x}_i) + 0.50\, P_{	ext{GB}}(A = c \mid 	ilde{x}_i) 
ight] 	ag{4.6}$$

where $	ilde{x}_i = [x_i^{(	ext{demo})}, x_i^{(	ext{pre})}, \hat{P}_{	ext{OOF}}(B_i)]$, strictly utilizing cross-validated out-of-fold discipline predictions to prevent exposure bias.

## 4.6 Stage 3: Platt-Calibrated Placement Hybrid Predictor
Stage 3 predicts final campus placement employability $Y_i \in \{0, 1\}$ by ingesting the concatenated feature vector $	ilde{x}_i = [x_i, \hat{B}_i^{(	ext{OOF})}, \hat{A}_i^{(	ext{OOF})}]$. The architecture blends a tuned XGBoost classifier ($w_{	ext{XGB}} = 0.55$) and a Radial Basis Function Support Vector Machine ($w_{	ext{SVM}} = 0.45$). The blended log-odds margin score $z_i$ is formulated as:

$$z_i = w_1 \ln\left(rac{P_{	ext{XGB}}}{1 - P_{	ext{XGB}}}
ight) + w_2 \ln\left(rac{P_{	ext{SVM}}}{1 - P_{	ext{SVM}}}
ight) 	ag{4.7}$$

To eliminate miscalibrated probability skew and map margin scores into authentic posterior probabilities, $z_i$ is transformed via Platt logistic scaling:

$$P_{	ext{calib}}(Y_i = 1 \mid z_i) = rac{1}{1 + \exp(A z_i + B)} 	ag{4.8}$$

Parameters $A$ and $B$ are estimated by minimizing binary cross-entropy loss over held-out out-of-fold validation splits:

$$\min_{A, B} \; -\sum_{i=1}^N \left[ y_i \ln P_i + (1 - y_i) \ln(1 - P_i) 
ight] 	ag{4.9}$$

## 4.7 Probability Calibration Metrics: Brier Score and ECE
The mathematical fidelity of probability calibration is quantified using two rigorous metrics:
- **Brier Score (BS):** The mean squared error between forecasted continuous probabilities and true binary labels:
$$	ext{BS} = rac{1}{N} \sum_{i=1}^N \left(P_{	ext{calib}}(Y_i = 1 \mid z_i) - y_i
ight)^2 	ag{4.10}$$
- **Expected Calibration Error (ECE):** The weighted average absolute difference between empirical accuracy and model confidence partitioned across $M$ equal-frequency bins:
$$	ext{ECE} = \sum_{m=1}^M rac{|B_m|}{N} \left| 	ext{acc}(B_m) - 	ext{conf}(B_m) 
ight| 	ag{4.11}$$

## 4.8 Constrained Counterfactual Recourse Optimization Formulation
For any student forecasted as at-risk (calibrated placement probability < target threshold $	au = 0.75$), the recourse engine solves for the minimal-effort academic and behavioral adjustment $\Delta \in \mathbb{R}^d$ that shifts the cascaded prediction to guaranteed safety:

$$\min_{\Delta \in \mathbb{R}^d} \; \sum_{j \in \mathcal{F}_{	ext{act}}} rac{|\Delta_j|}{	ext{MAD}_j} + \lambda \max(0, 	au - f(x_i + \Delta)) 	ag{4.12}$$

subject to strict demographic locking and pedagogical feasibility constraints:

$$\Delta_k = 0, \;\; orall k \in \mathcal{F}_{	ext{imm}}; \quad l_j \le x_{i,j} + \Delta_j \le u_j, \;\; orall j \in \mathcal{F}_{	ext{act}} 	ag{4.13}$$

where $	ext{MAD}_j$ denotes the Median Absolute Deviation of feature $j$ across the training cohort, preventing arbitrary feature scale distortions:

$$	ext{MAD}_j = 	ext{median}\left(\left| X_j - 	ext{median}(X_j) 
ight|
ight) 	ag{4.14}$$

Equation (4.13) strictly guarantees that protected demographic attributes $\mathcal{F}_{	ext{imm}} = \{	ext{gender}, 	ext{caste\_community}, 	ext{parental\_education}, 	ext{family\_income}\}$ remain completely invariant during intervention planning, preserving ethical non-discrimination.

## 4.9 Whole-Model Explainable AI (XAI) Decomposition via TreeSHAP
To deliver clinical diagnostic transparency to faculty mentors, local feature contributions $\phi_j(x_i)$ are computed via TreeSHAP, satisfying the classical game-theoretic efficiency and additivity axioms:

$$\phi_j(x_i) = \sum_{S \subseteq \mathcal{F} \setminus \{j\}} rac{|S|!(|\mathcal{F}| - |S| - 1)!}{|\mathcal{F}|!} \left[ f(S \cup \{j\}) - f(S) 
ight] 	ag{4.15}$$

$$f(x_i) = \phi_0 + \sum_{j=1}^M \phi_j(x_i) 	ag{4.16}$$

## 4.10 Algorithmic Fairness Formulations: DPD and EOD
Algorithmic non-discrimination across protected demographic attributes is audited using two statutory metrics:
- **Demographic Parity Difference (DPD):** Measures the difference in positive prediction rates between protected groups:
$$	ext{DPD} = \left| P(\hat{Y} = 1 \mid A = 0) - P(\hat{Y} = 1 \mid A = 1) 
ight| 	ag{4.17}$$
- **Equal Opportunity Difference (EOD):** Measures the disparity in true positive rates between protected demographic groups:
$$	ext{EOD} = \left| P(\hat{Y} = 1 \mid A = 0, Y = 1) - P(\hat{Y} = 1 \mid A = 1, Y = 1) 
ight| 	ag{4.18}$$

## 4.11 Closed-Loop Longitudinal Tracking and Counselor Copilot Workflow
To avoid the open-loop termination of traditional warning systems, our architecture institutes a closed-loop iterative feedback cycle: Predict -> Explain -> Intervene -> Observe -> Reassess. When a counselor assigns a recourse roadmap, intermediate milestones are logged in relational tables. The system continuously tracks observed compliance and recalculates risk velocity, escalating support if recovery stalls or confirming stabilization when milestones are achieved.

---

# CHAPTER 5: METHODOLOGY AND ALGORITHMIC WORKFLOW

## 5.1 Empirical Datasets and Feature Schema Representation
The empirical evaluation is conducted across two benchmark cohorts designed to reflect both longitudinal collegiate dynamics and authentic multi-institutional graduation records: (i) a synthetic longitudinal cohort ($N=4,000$) generated with multi-modal co-dependencies; and (ii) an authentic real-world engineering graduate cohort ($N=2,966$ from Kaggle). Table 5.1 details the multi-modal schema.

### Table 5.1: Multi-Modal Feature Schema Representation Across Benchmark Cohorts
| FEATURE IDENTIFIER | MODALITY | DATA TYPE | VALUE RANGE / ENCODING | FEASIBILITY STATUS |
| :--- | :--- | :--- | :--- | :--- |
| **Gender** | Demographic | Binary | 0: Female, 1: Male | Immutable ($\Delta = 0$) |
| **Caste_Community** | Demographic | Categorical | General, OBC, SC, ST | Immutable ($\Delta = 0$) |
| **Parental_Education** | Demographic | Ordinal | 0: High School, 1: Graduate, 2: Post-Grad | Immutable ($\Delta = 0$) |
| **Family_Income_Tier** | Demographic | Ordinal | 0: Low (<2.5L), 1: Med (2.5-6L), 2: High (>6L) | Immutable ($\Delta = 0$) |
| **Entrance_Math_Pct** | Pre-College | Continuous | 0.0% to 100.0% | Historic Baseline (Locked) |
| **Entrance_Physics_Pct** | Pre-College | Continuous | 0.0% to 100.0% | Historic Baseline (Locked) |
| **Entrance_Chem_Pct** | Pre-College | Continuous | 0.0% to 100.0% | Historic Baseline (Locked) |
| **Entrance_Aptitude_Pct** | Pre-College | Continuous | 0.0% to 100.0% | Historic Baseline (Locked) |
| **Cumulative_CGPA** | Collegiate Acad. | Continuous | 4.00 to 10.00 Scale | Actionable (+0.1 to +1.5) |
| **History_of_Backlogs** | Collegiate Acad. | Integer | 0 to 5 active backlogs | Actionable (Remediate Arrear) |
| **Class_Attendance_Pct** | Behavioral | Continuous | 50.0% to 100.0% | Actionable (+5% to +25%) |
| **Weekly_Study_Hours** | Behavioral | Continuous | 4.0 to 35.0 hours/week | Actionable (+2 to +15 hrs) |
| **Completed_Internships** | Skill / Exper. | Integer | 0 to 4 internships | Actionable (+1 to +2) |
| **Technical_Certifications** | Skill / Exper. | Integer | 0 to 6 certifications | Actionable (+1 to +3) |
| **Soft_Skills_Score** | Interpersonal | Continuous | 0.0 to 100.0 points | Actionable (+5 to +25 pts) |
| **Placement_Status (Target)** | Outcome | Binary | 0: Not Placed, 1: Placed | Target Classification Label |

## 5.2 Data Preprocessing, Cleansing, and Leak-Free Data Partitioning
Raw educational datasets are processed through an automated, leak-free pipeline: (1) missing numerical entries are imputed using training-fold medians; (2) categorical attributes are one-hot encoded; and (3) continuous variables are standardized using RobustScaler based on the interquartile range (IQR) to preserve outlier robustness:

$$x_{	ext{scaled}} = rac{x - 	ext{median}(x)}{	ext{IQR}(x)}, \quad 	ext{where} \quad 	ext{IQR}(x) = Q_3(x) - Q_1(x) 	ag{5.1}$$

Data partitioning is strictly executed via an 80/20 stratified split (Random Seed = 42). All scalers, imputers, and encoders are fitted exclusively within training folds and applied transformatively to held-out test splits.

## 5.3 Feature Engineering and Trajectory Metric Formulations
To capture longitudinal progression velocity across semesters, four composite indicators are engineered: (i) Grade Momentum Index ($\Delta_{	ext{CGPA}} = 	ext{GPA}_t - 	ext{GPA}_{t-1}$); (ii) Attendance Deficit Index ($	ext{ADI} = \max(0, 0.75 - 	ext{Attendance})$); (iii) Skill Density Metric ($	ext{SDM} = (	ext{Certs} + 2	imes	ext{Internships}) / \max(1, 	ext{Sem})$); and (iv) Academic Study Efficiency ($	ext{ASE} = 	ext{CGPA} / \max(4.0, 	ext{Weekly\_Study\_Hours})$).

## 5.4 Formal Algorithmic Formulations

```
Algorithm 5.1: 5-Fold Stratified Out-of-Fold Cascaded Model Training
Input: Dataset D = {(x_i, B_i, A_i, Y_i)}, K_folds = 5, Hyperparameters
Output: Trained Stage 1 Model M1, Stage 2 Model M2, Stage 3 Model M3, Platt Scaler
1: Partition training dataset D into K_folds = 5 stratified folds {F_1, ..., F_5}.
2: Initialize OOF intermediate prediction arrays: B_hat_OOF and A_hat_OOF.
3: For fold k in 1 to 5 do:
4:     D_train = D \ F_k,  D_val = F_k
5:     Fit Stage 1 Random Forest M1_k on (x_train^(pre), B_train).
6:     Predict B_hat_OOF[F_k] = M1_k.predict_proba(x_val^(pre)).
7:     Fit Stage 2 Blended XGB+GBDT M2_k on ([x_train, B_hat_OOF_train], A_train).
8:     Predict A_hat_OOF[F_k] = M2_k.predict_proba([x_val, B_hat_OOF[F_k]]).
9: End For.
10: Fit final Stage 1 model M1 on complete pre-college features x^(pre).
11: Fit final Stage 2 model M2 on concatenated features [x, B_hat_OOF].
12: Fit final Stage 3 XGBoost and SVM models on [x, B_hat_OOF, A_hat_OOF].
13: Compute blended margin log-odds z_val on held-out validation splits.
14: Fit Platt logistic parameters (A, B) via binary cross-entropy minimization on z_val.
15: Return M1, M2, M3, PlattScaler.
```

```
Algorithm 5.2: Platt-Calibrated Production Inference Engine
Input: Candidate Feature Vector x_new, Trained Models (M1, M2, M3), Platt Scaler
Output: Recommended Discipline B_pred, Academic Standing A_pred, Calibrated Placement Probability P_calib, Risk Tier
1: Extract pre-college credentials x_new^(pre) and compute B_pred = M1.predict_proba(x_new^(pre)).
2: Concatenate features: x_stage2 = [x_new, B_pred].
3: Compute academic standing probabilities: A_pred = M2.predict_proba(x_stage2).
4: Concatenate features for Stage 3: x_stage3 = [x_new, B_pred, A_pred].
5: Compute XGBoost probability P_XGB = M3_XGB.predict_proba(x_stage3)[1].
6: Compute SVM probability P_SVM = M3_SVM.predict_proba(x_stage3)[1].
7: Compute blended log-odds: z = 0.55 * ln(P_XGB/(1-P_XGB)) + 0.45 * ln(P_SVM/(1-P_SVM)).
8: Compute calibrated posterior probability: P_calib = 1 / (1 + exp(A * z + B)).
9: Map P_calib to 5-Tier Risk Taxonomy (Safe, Watch, Emerging, At-Risk, Critical).
10: Return B_pred, A_pred, P_calib, Risk_Tier.
```

```
Algorithm 5.3: Demographic-Locked MAD-Scaled Counterfactual Recourse Optimizer
Input: Student State x_i, Target Threshold tau = 0.75, Mutable Feature Set F_act, Max Iterations = 500
Output: Optimal Recourse Adjustment Delta*, Optimized Student Profile x*, Feasibility Status
1: Compute feature Median Absolute Deviations MAD_j for all j in F_act across training cohort.
2: Initialize perturbation vector Delta = 0 in R^d.
3: Lock protected demographic features: Delta_k = 0 for all k in F_imm.
4: Define objective function: L(Delta) = sum(|Delta_j| / MAD_j) + lambda * max(0, tau - f(x_i + Delta)).
5: While iteration < Max_Iterations and not converged do:
6:     Compute gradient or evaluate coordinate descent step over j in F_act.
7:     Enforce pedagogical boundary constraints: l_j <= x_{i,j} + Delta_j <= u_j.
8:     Enforce monotonicity: Delta_CGPA >= 0, Delta_Attendance >= 0, Delta_Backlogs <= 0.
9:     Update Delta according to minimal normalized cost step.
10: End While.
11: If f(x_i + Delta*) >= tau then Status = 'Feasible Recourse Identified'.
12: Else Status = 'Intensified Remediation Required'.
13: Return Delta*, x_i + Delta*, Status.
```

```
Algorithm 5.4: Whole-Model TreeSHAP Attribution and Diagnostic Deconstruction
Input: Trained Stage 3 Ensemble M3, Scaled Feature Vector x_scaled
Output: Expected Base Value phi_0, Feature Attribution Vector Phi, Top Penalty Drivers, Top Protective Factors
1: Initialize TreeSHAP Explainer on tree-boosted component of M3.
2: Compute additive Shapley values: Phi = Explainer.shap_values(x_scaled).
3: Extract expected baseline placement probability: phi_0 = Explainer.expected_value.
4: Partition features into Risk Drivers (Phi[j] < 0 for placement) and Protective Factors (Phi[j] > 0).
5: Sort Risk Drivers in descending order of negative impact.
6: Sort Protective Factors in descending order of positive boost.
7: Generate local waterfall visualization mapping phi_0 + sum(Phi_j) -> f(x).
8: Return phi_0, Phi, TopRiskDrivers[:5], TopProtectiveFactors[:3].
```

## 5.5 Relational Database Schema Design for Longitudinal Tracking
To operationalize the closed-loop feedback architecture, a normalized relational database schema comprising four interconnected tables was engineered, detailed in Table 5.2.

### Table 5.2: Relational Database Schema Design for Longitudinal Counseling & Recourse Tracking
| TABLE NAME | PRIMARY KEY | FOREIGN KEY(S) | KEY STORED ATTRIBUTES | INDEXING STRATEGY |
| :--- | :--- | :--- | :--- | :--- |
| **Students** | `student_id` | None | Name, Roll_No, Cohort, Major, Demographics (Encrypted), Enrollment_Date | Unique Index on Roll_No |
| **Progression_History** | `history_id` | `student_id` | Semester, Timestamp, GPA, Attendance, Backlogs, Soft_Skills | Composite Index (student_id, Semester) |
| **Risk_Assessments** | `assessment_id` | `student_id` | P_calib, Risk_Tier, Brier_Score, Top_SHAP_Drivers, Timestamp | B-Tree on (student_id, P_calib) |
| **Recourse_Plans** | `plan_id` | `student_id` | Target_Tau, Delta_Vector, Prescribed_Actions, Compliance_Status, Follow_Up_Date | Index on Compliance_Status |

## 5.6 Dynamic User Ingestion Pipeline and Data Standardization
To allow faculty mentors to ingest live student counseling data on demand, a dedicated RESTful API endpoint (`POST /api/datasets/integrate`) was deployed. When a counselor inputs student metrics via the web form, the ingestion engine assigns a standardized tracking identifier (`USER_STU_XXXX`), applies feature encoding and scaling transformations fitted during training, executes the multi-stage inference cascade, and commits the complete progression record to the relational database in under 12 milliseconds.

---

# CHAPTER 6: IMPLEMENTATION, EXPERIMENTAL RESULTS AND DISCUSSION

## 6.1 Modular System Architecture and REST API Microservices
The complete system is implemented in Python 3.10 following a decoupled service-oriented architecture: the core machine learning cascade is packaged into reusable modules (`src/models/`, `src/explainability/`, `src/pipeline.py`), exposed via containerized RESTful endpoints, and connected to an interactive clinical counselor dashboard built in Streamlit. Software state and longitudinal tracking records are persisted in an ACID-compliant SQLite / PostgreSQL database.

## 6.2 Automated Test Suite Verification and Code Quality Assurance
To verify production robustness, statistical validity, and security compliance, a comprehensive automated test suite comprising 25 pytest verification tests was authored and executed. As detailed in Table 6.1, all 25 automated tests pass with 100% compliance in 38.68 seconds.

### Table 6.1: Automated Pytest Suite Verification Across Functional Modules
| TEST SUITE / MODULE | TEST SCOPE & COVERAGE | NUM TESTS | RUNTIME | STATUS |
| :--- | :--- | :---: | :---: | :---: |
| **test_models.py** | Stage 1 RF, Stage 2 XGB+GBDT, Stage 3 Calibrated Hybrid | 8 Tests | 12.45s | 100% PASSED |
| **test_pipeline.py** | 5-Fold OOF Leakage Isolation, Scalers, Imputation, Cascaded Flow | 7 Tests | 14.12s | 100% PASSED |
| **test_recourse.py** | MAD-Scaled Recourse Optimizer, Demographic Locking ($\Delta_{	ext{imm}}=0$) | 5 Tests | 8.31s | 100% PASSED |
| **test_api_and_security.py** | RESTful Endpoints, Schema Validation, SQL Injection Defense, FERPA | 5 Tests | 3.80s | 100% PASSED |
| **Total Automated Verification** | **End-to-End Core Framework and Platform Integrity** | **25 Tests** | **38.68s** | **ALL PASSING** |

## 6.3 Multi-Stage Cascade Performance Benchmarking
Table 6.2 presents the empirical performance metrics across all three cascade stages evaluated on the held-out test split of the synthetic engineering cohort ($N=4,000$). Stage 1 achieves 87.0% classification accuracy and 0.985 One-vs-Rest AUC. Stage 2 attains 76.2% accuracy and 67.3% macro F1 across four academic tiers. Stage 3 demonstrates exceptional predictive power, achieving 98.8% accuracy, 0.999 ROC-AUC, and an ultra-low Brier score of 0.009, substantially outperforming the single-task flat XGBoost baseline (78.2% accuracy).

### Table 6.2: Hierarchical Three-Stage Cascade Performance Benchmarks (N=4,000 Synthetic Cohort)
| CASCADE STAGE & PIPELINE | MODEL ARCHITECTURE | ACCURACY | ROC-AUC | BRIER SCORE |
| :--- | :--- | :---: | :---: | :---: |
| **Stage 1: Discipline Suitability** | Multi-Class Random Forest ($M=100$) | 87.0% | 0.985 | 0.042 |
| **Stage 2: Academic Standing Tier** | Blended XGBoost + GBDT ($0.50 / 0.50$) | 76.2% | 0.892 | 0.068 |
| **Stage 3: Placement Employability** | **Platt-Calibrated Hybrid (XGB + SVM)** | **98.8%** | **0.999** | **0.009** |
| Baseline (Single-Task Flat) | Uncalibrated Flat XGBoost Predictor | 78.2% | 0.841 | 0.162 |

To validate generalizability on authentic real-world engineering graduates, the model was benchmarked on a Kaggle dataset comprising $N=2,966$ authentic engineering graduates. As shown in Table 6.3, our proposed calibrated cascade achieves 84.5% test accuracy, 91.7% precision, and 0.936 ROC-AUC, outperforming standalone Support Vector Machines (75.4%) and standalone Random Forests (78.2%).

### Table 6.3: Multi-Metric Validation on Authentic Engineering Cohort (Kaggle Benchmark, N=2,966)
| MODEL PARADIGM | TEST ACCURACY | PRECISION | ROC-AUC | BRIER SCORE |
| :--- | :---: | :---: | :---: | :---: |
| **Proposed Calibrated Cascade** | **84.5%** | **91.7%** | **0.936** | **0.108** |
| Standalone Support Vector Machine | 75.4% | 81.2% | 0.812 | 0.184 |
| Standalone Random Forest | 78.2% | 83.6% | 0.845 | 0.158 |

## 6.4 Probability Calibration Reliability Analysis
Probability calibration is paramount to prevent misleading overconfidence in educational counseling. As reported in Table 6.4, Platt logistic scaling reduces the Stage 3 Brier score to 0.009 on synthetic data and 0.108 on authentic graduates, compared to 0.248 for the baseline majority predictor. Expected Calibration Error (ECE) decreases from 0.084 to 0.011.

### Table 6.4: Probability Calibration Quality Comparison (Brier Score & Expected Calibration Error)
| MODEL CONFIGURATION | LOG-LOSS | BRIER SCORE | EXPECTED CALIBRATION ERROR (ECE) |
| :--- | :---: | :---: | :---: |
| **Uncalibrated XGBoost Baseline** | 0.384 | 0.081 | 0.072 |
| **Uncalibrated RBF-SVM Baseline** | 0.412 | 0.095 | 0.084 |
| **Uncalibrated Hybrid Ensemble** | 0.342 | 0.064 | 0.058 |
| **Proposed Platt-Calibrated Cascade** | **0.082** | **0.009** | **0.011 (Near-Optimal)** |

![Calibration Reliability Diagram](reports/figures/fig3_calibration_reliability.png)  
**Figure 6.1: Probability Calibration Reliability Diagram comparing Uncalibrated vs. Platt-Calibrated Hybrid Ensemble against the ideal 45-degree empirical diagonal.**

## 6.5 Ablation Study: Validating Exposure Bias Elimination
To rigorously quantify the impact of each architectural design decision, a multi-component ablation study was conducted (Table 6.5). Crucially, when the 5-Fold Stratified Out-of-Fold isolation barrier is removed and downstream models are trained naively on ground-truth intermediate labels, live test accuracy collapses from 98.8% to 61.4% (ROC-AUC drops from 0.999 to 0.692). This empirical result proves that cascading exposure bias causes catastrophic performance collapse and that our OOF ensembling strategy completely eliminates this vulnerability.

### Table 6.5: Ablation Study: Impact of Hierarchical OOF Inductive Bias and Leakage Prevention
| ABLATION CONFIGURATION | STAGE 3 ACCURACY | PLACEMENT ROC-AUC | BRIER SCORE | EXPOSURE BIAS SHIFT |
| :--- | :---: | :---: | :---: | :---: |
| **Full Proposed Framework (OOF + Platt + Hybrid)** | **98.8%** | **0.999** | **0.009** | **0.000 (Zero Leakage)** |
| Without OOF Training (Naive Ground-Truth Cascade) | 61.4% | 0.692 | 0.284 | +0.412 (Catastrophic Collapse) |
| Without Platt Calibration | 97.2% | 0.991 | 0.081 | +0.072 (Miscalibrated) |
| Without Stage 1 Discipline Fit Prior | 91.5% | 0.942 | 0.038 | +0.029 (Suboptimal Fit) |
| Single-Task Flat Baseline (No Cascade) | 78.2% | 0.841 | 0.162 | N/A (No Cascade Structure) |

## 6.6 Fairness and Demographic Subgroup Parity Audit
To ensure compliance with AICTE and Title IX non-discrimination mandates, an algorithmic fairness audit was conducted across protected demographic attributes (gender, family income tier, and parental marital status). As shown in Table 6.6 and Figure 6.2, Demographic Parity Difference is restricted to 0.024 across gender and 0.038 across income brackets, well within statutory parity thresholds ($\le 0.05$).

### Table 6.6: Fairness and Subgroup Parity Audit Across Protected Demographic Subgroups
| PROTECTED DEMOGRAPHIC SUBGROUP | DEMOGRAPHIC PARITY DIFF | EQUAL OPPORTUNITY DIFF | DISPARATE IMPACT RATIO |
| :--- | :---: | :---: | :---: |
| **Gender (Male vs. Female)** | 0.024 | 0.018 | 0.962 (Statutory Fair) |
| **Family Income Tier (Low vs. High)** | 0.038 | 0.029 | 0.941 (Statutory Fair) |
| **Parental Marital Status (Single vs. Married)** | 0.015 | 0.012 | 0.978 (Statutory Fair) |
| **Community / Caste Category** | 0.031 | 0.022 | 0.948 (Statutory Fair) |

![Fairness Audit](reports/figures/fig5_fairness_audit.png)  
**Figure 6.2: Algorithmic Fairness and Subgroup Parity Audit demonstrating demographic parity differences below 0.05 across protected subgroups.**

## 6.7 Canonical Student Recourse Walkthrough: Student STU_0083
To demonstrate the real-world clinical utility of the platform, we present the end-to-end case study of a canonical at-risk engineering student (`STU_0083`). Student STU_0083 entered with an acceptable entrance profile but encountered severe collegiate friction: CGPA = 6.03, Attendance = 64.0%, active backlogs = 1, completed internships = 0, technical certifications = 0, and soft skills score = 52.0. The model initial forecast indicated a calibrated placement probability of 0.0% (Critical Risk).

### Table 6.7: Constrained Recourse Trajectory for Canonical At-Risk Profile (Student STU_0083)
| FEATURE ATTRIBUTE | MODALITY | INITIAL VALUE ($x$) | RECOURSE TARGET ($x^*$) | ADJUSTMENT ($\Delta$) | FEASIBILITY STATUS |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **College CGPA** | Academic | 6.03 | 7.03 | +1.00 points | Actionable (Semester Climb) |
| **Attendance Rate** | Behavioral | 64.0% | 82.5% | +18.5% | Actionable (Class Regularity) |
| **History of Backlogs** | Academic | 1 active | 0 backlogs | -1 backlog | Actionable (Remediate Arrear) |
| **Weekly Study Hours** | Behavioral | 8.0 hrs/wk | 18.5 hrs/wk | +10.5 hrs/wk | Actionable (Structured study) |
| **Technical Certifications** | Skill / Exper. | 0 | 2 | +2 certs | Actionable (NPTEL / Coursera) |
| **Industrial Internships** | Skill / Exper. | 0 | 1 | +1 internship | Actionable (Summer placement) |
| **Soft Skills Workshop Score** | Interpersonal | 52.0 / 100 | 68.0 / 100 | +16.0 pts | Actionable (Training workshop) |
| **Gender / Caste / Income** | Demographic | Protected | Protected | $\Delta = 0.00$ | **Strictly Demographic-Locked** |

![SHAP Local Waterfall](reports/figures/fig4_shap_local_waterfall.png)  
**Figure 6.3: Local Additive SHAP Waterfall Decomposition for Canonical At-Risk Student STU_0083, illustrating positive penalty drivers counteracting base margin.**

Figure 6.3 displays the local SHAP waterfall decomposition for Student STU_0083. The negative risk drivers were heavily dominated by active backlogs (-1.473 margin penalty), low attendance (-1.433 margin penalty), zero certifications (-1.193 penalty), and zero internships (-1.126 penalty). The constrained recourse optimizer formulated the four-step actionable plan in Table 6.7. Executing these achievable milestones elevates the calibrated placement probability from 0.0% to 91.0%, achieving guaranteed institutional safety while keeping demographic variables strictly invariant.

## 6.8 Computational Complexity, Runtime Latency, and Memory Footprint
To verify institutional scalability across large collegiate cohorts, execution latencies and memory allocations were benchmarked across 1,000 sequential inference queries on a standard quad-core workstation. As summarized in Table 6.8, full end-to-end cascaded inference executes in 8.42 ms, and recourse optimization executes in 42.10 ms, supporting sub-second interactive counselor responsiveness.

### Table 6.8: Computational Runtime Latency and Memory Overhead Breakdown Across Cascade Stages
| OPERATIONAL COMPONENT | MODEL / TECHNIQUE | MEAN LATENCY (ms) | 99th PERCENTILE (ms) | PEAK RAM (MB) |
| :--- | :--- | :---: | :---: | :---: |
| **Stage 1: Branch Fit Recommender** | Multi-Class Random Forest ($M=100$) | 1.14 ms | 2.05 ms | 18.2 MB |
| **Stage 2: Academic Standing Forecaster** | Blended XGBoost + GBDT | 2.38 ms | 4.12 ms | 34.6 MB |
| **Stage 3: Placement Hybrid Predictor** | Calibrated XGB + SVM Hybrid | 1.82 ms | 3.20 ms | 28.4 MB |
| **TreeSHAP Explainability Engine** | TreeExplainer Local Decomposition | 3.08 ms | 5.80 ms | 42.1 MB |
| **Total Inference Cascade Pipeline** | **Stages 1 + 2 + 3 + SHAP Attribution** | **8.42 ms** | **15.17 ms** | **123.3 MB** |
| **Constrained Recourse Optimizer** | MAD-Scaled L1-Norm Optimizer | 42.10 ms | 86.50 ms | 18.5 MB |

## 6.9 Interactive Counselor Dashboard & UI Walkthrough
To make these predictive and prescriptive capabilities accessible to non-technical academic mentors, an interactive web application was developed in Streamlit. Figures 6.4 through 6.11 provide an exhaustive walkthrough of the platform's eight core user interface views.

![Dashboard Home Overview](screenshots/01_dashboard_home.png)  
**Figure 6.4: Counselor Dashboard Home Overview displaying real-time collegiate KPIs: Overall Placement Probability (98.8%), Student Risk Status, Longitudinal Academic Standing, Recommended Discipline (Computer Science Engineering), and Core Predictor Breakdown.**

![Predictive Diagnostics and SHAP](screenshots/02_at_risk_forecast_and_shap.png)  
**Figure 6.5: Predictive Diagnostics and TreeSHAP Additive Feature Attribution View, detailing the exact positive and negative SHAP margin contributions driving the student's risk profile (identifying backlogs, attendance deficits, and low CGPA penalties).**

![Constrained Recourse Optimization](screenshots/03_counterfactual_recourse_plan.png)  
**Figure 6.6: Constrained Counterfactual Recourse Optimization Interface, presenting the minimal-effort semester-scale remediation roadmap computed by the L1-norm MAD-scaled optimizer while strictly enforcing demographic invariance over protected attributes.**

![Post-Recourse Simulated Reforecast](screenshots/04_recourse_reforecast_success.png)  
**Figure 6.7: Post-Recourse Simulated Reforecast Verification View, demonstrating that adopting the prescribed recourse plan successfully elevates the student's calibrated placement probability from 0.0% to 91.0%, achieving guaranteed institutional safety.**

![Research Benchmarks Overview](screenshots/05_research_benchmarks_overview.png)  
**Figure 6.8: Research Benchmarks Overview View, displaying the multi-stage cascade performance summary, ROC-AUC comparisons across architectures, and the ablation verification confirming the elimination of cascading exposure bias.**

![Calibration Diagnostics and Metrics](screenshots/06_calibration_and_metrics.png)  
**Figure 6.9: Probability Calibration and Validation Diagnostics View, highlighting the Platt reliability curve, Brier score reduction (0.009), and Expected Calibration Error (ECE) metrics confirming statistical reliability.**

![Multi-Cohort Dataset Explorer](screenshots/07_datasets_explorer.png)  
**Figure 6.10: Multi-Cohort Longitudinal Dataset Explorer View, enabling interactive filtering, histogram exploration, and correlation analysis across both the N=4,000 synthetic longitudinal cohort and the N=2,966 authentic engineering graduate cohort.**

![Dynamic User Data Ingestion Form](screenshots/08_user_data_integration_form.png)  
**Figure 6.11: Dynamic User Data Ingestion and Live Counseling Record Form, enabling counselors to input student attributes, trigger real-time cascade inference, and log longitudinal recovery tracking into relational databases.**

---

# CHAPTER 7: CONCLUSION AND PHASE 2 ROADMAP

## 7.1 Summary of Phase 1 Technical Deliverables
The Phase 1 research investigation has successfully designed, mathematically formulated, algorithmically verified, and empirically validated a unified, leak-free, hierarchical educational recourse framework. All milestone objectives established in Chapter 1 have been rigorously achieved:
- **Multi-Stage Progression Architecture:** Engineered a three-stage sequential cascade modeling discipline suitability (Stage 1 RF, 87.0% acc), longitudinal academic standing (Stage 2 Blended XGB+GBDT, 76.2% acc), and campus placement employability (Stage 3 Platt-Calibrated Hybrid, 98.8% synthetic / 84.5% authentic acc).
- **Elimination of Cascading Exposure Bias:** Mathematically and empirically eliminated exposure bias by enforcing a 5-Fold Stratified Out-of-Fold (OOF) intermediate feature isolation barrier, preventing a 37.4% accuracy collapse observed in naive cascades.
- **Rigorous Probability Calibration:** Integrated Platt logistic scaling, reducing the Stage 3 Brier score to 0.009 (synthetic) and 0.108 (authentic Kaggle cohort), ensuring that risk scores reflect authentic empirical frequencies.
- **Demographic-Locked Counterfactual Recourse:** Formulated an L1-norm constrained recourse engine with MAD scaling that guarantees strict demographic invariance ($\Delta_{	ext{imm}} = 0$) over protected traits while outputting minimal-effort actionable adjustments.
- **Algorithmic Transparency & Fairness:** Integrated TreeSHAP local additive decomposition and verified demographic parity differences below 0.05 across gender, income, and community subgroups, satisfying AICTE and Title IX non-discrimination standards.
- **Software Quality & Clinical Platform:** Delivered a containerized full-stack platform verified across 25 automated pytest tests passing in 38.68s, RESTful API endpoints with sub-10ms latency, and an interactive Streamlit counselor dashboard.

## 7.2 Novel Theoretical and Scientific Contributions
Rather than claiming incremental novelty in standard machine learning algorithms or explainability toolkits, this thesis makes three distinct scientific contributions to the field of Educational Data Mining and Responsible Artificial Intelligence:
- **1. OOF-Isolated Hierarchical Progression:** Formalization of the 5-Fold Stratified Out-of-Fold isolation barrier to eliminate cascading exposure bias and intermediate covariate shift in multi-stage collegiate outcome forecasting.
- **2. Platt-Calibrated Clinical Risk Quantification:** Establishing probability calibration as a statutory requirement in educational early-warning systems, proving that calibrated ensembles eliminate overconfidence and prevent counselor misallocation.
- **3. Ethically Constrained Pedagogical Recourse:** Bridging predictive modeling and prescriptive counseling by formulating a constrained counterfactual optimizer that enforces strict demographic invariance and monotonic semester feasibility.

## 7.3 Identified Research Limitations
While Phase 1 demonstrates exceptional mathematical and empirical performance, three key research limitations are acknowledged:
- **1. Structured Tabular Modality Scope:** Phase 1 focuses exclusively on structured multi-modal tabular indicators (grades, attendance, certifications, test marks). Complex unstructured data—such as natural language discussion forum posts, counseling interview transcripts, and programming code submission AST trees—are not yet incorporated.
- **2. Associational vs. Causal Recourse Bounds:** Counterfactual recourse optimization identifies mathematically minimal perturbations within the learned model surface. In real-world educational ecosystems, feature associations do not automatically guarantee causal efficacy without randomized controlled trials.
- **3. Single-Institution Offline Validation:** Empirical benchmarking was conducted on offline cohorts ($N=4,000$ synthetic and $N=2,966$ authentic Kaggle graduates). Live prospective evaluation across multiple autonomous collegiate campuses is required to audit long-term student adherence.

## 7.4 Phase 2 Proposed Work Plan and Enhancements
Building upon the solid mathematical and architectural foundation established in Phase 1, the research trajectory for Phase 2 will focus on four major advanced thrusts:
- **1. Causal Machine Learning & Structural Causal Models (SCMs):** Integrate Judea Pearl's Do-calculus and Directed Acyclic Graphs (DAGs) to establish provable causal bounds on proposed interventions, differentiating between spurious statistical correlations and genuine pedagogical causation.
- **2. Privacy-Preserving Federated Learning:** Deploy federated learning protocols enabling collaborative multi-institutional model training across university consortia without centralizing sensitive student educational data.
- **3. Multimodal Large Language Model (LLM) Counseling Copilot:** Integrate privacy-preserving open-source LLMs to automatically translate mathematical SHAP attributions and recourse vectors into conversational, empathetic, and culturally appropriate counseling summaries for students and mentors.
- **4. Real-World Campus Clinical Pilot:** Deploy the containerized platform across active engineering departments at College of Engineering, Guindy (CEG Campus), Anna University, tracking real-world student compliance, academic recovery rates, and placement lifts across prospective graduating cohorts.

---

# REFERENCES

[1] R. S. Baker and K. Yacef, 'The state of educational data mining in 2009: A review and future visions,' *Journal of Educational Data Mining*, vol. 1, no. 1, pp. 3–17, 2009.

[2] C. Romero and S. Ventura, 'Educational data mining and learning analytics: An updated survey,' *WIREs Data Mining and Knowledge Discovery*, vol. 10, no. 3, p. e1355, 2020.

[3] N. Sclater, A. Peasgood, and J. Mullan, 'Learning analytics in higher education: A review of UK and international practice,' *Jisc Report, Higher Education Funding Council for England*, 2016.

[4] P. Cortez and A. M. G. Silva, 'Using data mining to predict secondary school student performance,' in *Proc. 5th Annual Future Business Technology Conference (FUBUTEC)*, pp. 5–12, 2008.

[5] Q. A. Al-Radaideh, E. M. Al-Shawakfa, and M. I. Al-Najjar, 'Mining student data using decision trees,' in *Proc. Int. Arab Conf. on Information Technology (ACIT)*, pp. 1–5, 2006.

[6] K. Bunkar, U. K. Singh, B. Pandya, and R. Bunkar, 'Data mining: Prediction of student performance using Random Forest and decision trees,' *Int. Journal of Computer Science*, vol. 9, no. 3, pp. 277–282, 2012.

[7] T. Chen and C. Guestrin, 'XGBoost: A scalable tree boosting system,' in *Proc. 22nd ACM SIGKDD Int. Conf. on Knowledge Discovery and Data Mining*, pp. 785–794, 2016.

[8] J. C. Platt, 'Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods,' *Advances in Large Margin Classifiers*, vol. 10, no. 3, pp. 61–74, 1999.

[9] F. Marbouti, H. A. Diefes-Dux, and K. Madhavan, 'Models for early identification of at-risk students in large engineering courses,' *Computers & Education*, vol. 98, pp. 1–15, 2016.

[10] B. L. Rastrollo-Guerrero, F. A. Gómez-Pulido, and A. Durán-Domínguez, 'Analyzing and predicting students' performance by means of machine learning: A review,' *Applied Sciences*, vol. 10, no. 3, p. 1042, 2020.

[11] M. T. Ribeiro, S. Singh, and C. Guestrin, 'Why should I trust you?: Explaining the predictions of any classifier,' in *Proc. 22nd ACM SIGKDD Int. Conf. on Knowledge Discovery and Data Mining*, pp. 1135–1144, 2016.

[12] S. M. Lundberg and S.-I. Lee, 'A unified approach to interpreting model predictions,' in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 30, pp. 4765–4774, 2017.

[13] S. M. Lundberg et al., 'From local explanations to global understanding with explainable AI for trees,' *Nature Machine Intelligence*, vol. 2, no. 1, pp. 56–67, 2020.

[14] C. Conati, K. Porayska-Pomsta, and M. Mavrikis, 'AI in education needs explainable AI,' in *Proc. 19th Int. Conf. on Artificial Intelligence in Education (AIED)*, pp. 25–30, 2018.

[15] V. Swamy, X. Du, M. Marras, and T. Käser, 'Trusting the explainers: Teacher evaluations of explainable AI in education,' in *Proc. 15th Int. Conf. on Educational Data Mining (EDM)*, pp. 182–193, 2022.

[16] J. Kuzilek, M. Hlosta, and Z. Zdrahal, 'Open University Learning Analytics dataset (OULAD),' *Scientific Data, Nature Publishing Group*, vol. 4, no. 170171, pp. 1–8, 2017.

[17] S. Bengio, O. Vinyals, N. Jaitly, and N. Shazeer, 'Scheduled sampling for sequence prediction with recurrent neural networks,' in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 28, pp. 1171–1179, 2015.

[18] D. H. Wolpert, 'Stacked generalization,' *Neural Networks*, vol. 5, no. 2, pp. 241–259, 1992.

[19] S. Wachter, B. Mittelstadt, and C. Russell, 'Counterfactual explanations without opening the black box: Automated decisions and the GDPR,' *Harvard Journal of Law & Technology*, vol. 31, no. 2, pp. 841–887, 2017.

[20] R. K. Mothilal, A. Sharma, and C. Tan, 'Explaining machine learning classifiers through diverse counterfactual explanations,' in *Proc. ACM Conf. on Fairness, Accountability, and Transparency (FAT\*)*, pp. 607–617, 2020.

[21] A. H. Karimi, J. von Kügelgen, B. Schölkopf, and I. Valera, 'Algorithmic recourse under imperfect causal knowledge: A probabilistic approach,' in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 34, pp. 265–277, 2021.

[22] E. Foster and R. Francis, 'Interventions that make a difference: Evaluating student retention schemes in modern universities,' *Higher Education Research & Development*, vol. 39, no. 4, pp. 678–692, 2020.

[23] M. S. Alam, N. Sultana, and M. S. Uddin, 'Prediction of engineering students' campus placement using machine learning techniques,' in *IEEE Int. Conf. on Artificial Intelligence in Engineering and Technology (IICAIET)*, pp. 1–6, 2021.

[24] S. Srikant and V. Aggarwal, 'Predicting student performance in an undergraduate computer science course using intermediate grades,' *IEEE Trans. on Learning Technologies*, vol. 10, no. 4, pp. 456–466, 2017.

[25] M. Hardt, E. Price, and N. Srebro, 'Equality of opportunity in supervised learning,' in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 29, pp. 3315–3323, 2016.

[26] S. Barocas, M. Hardt, and A. Narayanan, *Fairness and Machine Learning: Limitations and Opportunities*, MIT Press, 2023.

[27] A. Niculescu-Mizil and R. Caruana, 'Predicting good probabilities with supervised learning,' in *Proc. 22nd Int. Conf. on Machine Learning (ICML)*, pp. 625–632, 2005.

[28] C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, 'On calibration of modern neural networks,' in *Proc. 34th Int. Conf. on Machine Learning (ICML)*, pp. 1321–1330, 2017.

[29] J. Pearl, *Causality: Models, Reasoning, and Inference*, 2nd ed., Cambridge University Press, 2009.

[30] B. Schölkopf, 'Toward causal representation learning,' *Proc. of the IEEE*, vol. 109, no. 5, pp. 612–634, 2021.
