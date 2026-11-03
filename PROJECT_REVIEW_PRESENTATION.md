# Slide-by-Slide Presentation Script & Speaker Notes (19 Slides)
## Hierarchical Multi-Task & Explainable Educational Recourse Framework
**Prepared for:** Formal Academic Project Review, Master's Defense & Conference Presentation  
**Slide Decks:** 
- [PROJECT_REVIEW_PRESENTATION.pptx](file:///c:/Users/Methunraj%20A/Downloads/bro/PROJECT_REVIEW_PRESENTATION.pptx) (2.6 MB, 19 Slides, High-Res Figures & UI Screenshots)
- [PROJECT_REVIEW_PRESENTATION.pdf](file:///c:/Users/Methunraj%20A/Downloads/bro/PROJECT_REVIEW_PRESENTATION.pdf) (Portable Document Format)
- [IEEE_AICTE_PRESENTATION.pptx](file:///c:/Users/Methunraj%20A/Downloads/bro/IEEE_AICTE_PRESENTATION.pptx) (Conference Presentation Deck)  
**Accompanying Report:** [PROJECT_REVIEW_REPORT.md](file:///c:/Users/Methunraj%20A/Downloads/bro/PROJECT_REVIEW_REPORT.md) | [PROJECT_REVIEW_REPORT.docx](file:///c:/Users/Methunraj%20A/Downloads/bro/PROJECT_REVIEW_REPORT.docx)  
**Research Paper:** [IEEE_AICTE_PAPER.docx](file:///c:/Users/Methunraj%20A/Downloads/bro/IEEE_AICTE_PAPER.docx) | [IEEE_AICTE_PAPER.pdf](file:///c:/Users/Methunraj%20A/Downloads/bro/IEEE_AICTE_PAPER.pdf)  
**Live Demo:** `http://127.0.0.1:5000` | **Datasets:** `http://127.0.0.1:5000/datasets` | **Benchmarks:** `http://127.0.0.1:5000/benchmarks`  
**Estimated Presentation Time:** 15 – 20 Minutes  

---

## Slide 1: Title & Defense Overview
- **Category:** Academic Degree Project Defense & Technical Review
- **Title:** Hierarchical Multi-Task & Explainable Educational Recourse Framework
- **Subtitle:** Mitigating Cascading Exposure Bias, Platt Probability Calibration, and Demographic-Locked Recourse
- **Candidate:** JAGADESH A (Register No: 2024CED001)
- **Degree & Branch:** M.E. Computer Science and Engineering (Data Science and Cybersecurity)
- **Institution:** Department of Computer Science and Engineering, College of Engineering, Guindy (CEG Campus), Anna University, Chennai
- **Key Badges:** 87.0% Stage 1 Branch Acc | 76.2% Stage 2 Acad Forecaster | 0.936 Real Placement AUC | $\Delta = 0$ Demographic Invariance
- **Speaker Cue (1 min):**
  > "Good morning, respected committee members and reviewers. I am Jagadesh A, pursuing M.E. in Computer Science and Engineering with specialization in Data Science and Cybersecurity at CEG Campus, Anna University. Today, I am presenting my project defense on the 'Hierarchical Multi-Task & Explainable Educational Recourse Framework'. In tertiary engineering institutions, predictive analytics is increasingly used to forecast student outcomes. However, existing institutional systems suffer from three critical research flaws: cascading exposure bias where downstream models assume perfect ground truth, uncalibrated confidence scores that mislead academic counselors, and purely black-box predictions that fail to tell at-risk students how they can remediate their outcomes. Our framework completely solves these challenges through a mathematically rigorous, leak-free sequential pipeline, calibrated hybrid ensembling, and demographic-locked counterfactual recourse."

---

## Slide 2: Executive Abstract & Core Technical Innovations
- **Key Innovations:**
  - **The Core Problem:** Cascading exposure bias caused by conditioning downstream models on ground-truth intermediate labels during offline training.
  - **Hierarchical Cascade:** 3-stage architecture decoupling Branch Recommendation (RF, 87.0% Acc), Academic Tier Forecasting (XGBoost + GB Blend, 76.2% Acc), and Final Placement Prediction (Platt-Calibrated XGBoost + RBF-SVM Hybrid).
  - **Anti-Leakage Safeguard:** Downstream models trained strictly on 5-Fold Stratified Out-of-Fold (OOF) intermediate representations.
  - **Platt Calibration:** Reduces Brier score from 0.248 down to 0.093 on authentic engineering cohorts.
  - **Demographic-Locked Recourse:** Coordinate-descent optimizer strictly locking immutable traits ($\Delta_{\text{demographic}} = 0$) raising student placement probability from 0.0% to 91.0%.
  - **Empirical Validation:** 91.7% Precision, 0.936 ROC-AUC on authentic cohort ($N=2,966$ graduates) backed by 25/25 passing automated tests.
- **Speaker Cue (1.5 min):**
  > "To summarize our contributions: our research establishes four key innovations. First, we eliminate cascading exposure bias by enforcing out-of-fold feature generation, guaranteeing identical feature distributions between training and production. Second, we integrate Platt logistic calibration so probabilities represent empirical success frequencies. Third, we develop an actionable recourse engine that empowers students by finding minimum-cost academic interventions while strictly locking immutable demographic attributes like gender and family income. Fourth, we validate this system across authentic cohorts and deliver a hardened production platform."

---

## Slide 3: Introduction & Institutional Context
- **Card 1: High-Stakes Institutional Retention:** Traditional counseling is reactive—students receive remedial assistance only after course failure or during final-year placement drives when CGPA is rigid.
- **Card 2: Sequential Lifecycle of Engineering Education:** Progression is milestone-driven: Pre-College Aptitude $\to$ Discipline Allocation $\to$ Semester Academics $\to$ Campus Recruitment Drives.
- **Card 3: The Imperative for Actionable Recourse:** Predicting failure is inadequate without explaining why failure was forecasted and prescribing feasible, non-discriminatory actions that counselors and students can execute.
- **Speaker Cue (1.5 min):**
  > "Education is a longitudinal journey. Predicting the final placement at Year 4 without modeling the intermediate academic milestones creates an artificial disconnect. Furthermore, handing a student a warning that says 'You have an 85% chance of failing' without giving them an achievable roadmap to success causes despair rather than remediation. Our system bridges this gap."

---

## Slide 4: Problem Statement & Critical Research Flaws
- **Left Panel (Vulnerabilities in Prior Work):**
  - **1. Cascading Exposure Bias:** Training on ground-truth intermediate milestones while testing on imperfect model predictions.
  - **2. Probability Miscalibration:** Extreme overconfident probabilities (near 0.0 or 1.0) misleading advisors.
  - **3. Unconstrained, Unethical Recourse:** Standard recourse methods altering immutable traits (gender, family income) or demanding impossible GPA jumps.
- **Right Panel (Framework Solutions & Guardrails):**
  - **1. 5-Fold Stratified OOF Training:** Downstream stages learn to tolerate realistic model noise.
  - **2. Platt Logistic Calibration:** Guarantees predicted probabilities reflect true empirical success frequencies.
  - **3. Demographic-Locked Recourse:** Mathematical constraint $\Delta_k = 0 \quad \forall k \in \mathcal{F}_{\text{immutable}}$.
- **Speaker Cue (2 min):**
  > "Here are the three fatal vulnerabilities we discovered in prior academic prediction systems: ground-truth exposure bias, miscalibration, and unconstrained counterfactuals. If a model suggests that a student should alter their gender or family background to become employable, it is both ethically unacceptable and practically useless. Our framework introduces strict mathematical guardrails to eliminate each failure mode."

---

## Slide 5: Literature Survey & Benchmark Comparison
- **Matrix Summary:**
  - *Cortez & Silva (2008):* Secondary marks only; lacks multi-stage collegiate progression.
  - *Sultana et al. (2019):* Isolated marks; zero explainability or actionable recourse.
  - *Bhardwaj & Pal (2020):* Restricted strictly to final CGPA; no early intervention window.
  - *Wachter et al. (2017) / DiCE (2020):* Mutate immutable demographic attributes; ignore multi-stage cascades.
  - *Proposed Framework (2026):* 3-Stage OOF Cascade + Calibrated Hybrid + Constrained Recourse (Comprehensive resolution).
- **Speaker Cue (1.5 min):**
  > "In surveying prior literature, researchers have treated academic outcome forecasting as flat, single-step tasks. In the explainability domain, general counterfactual methods like DiCE fail to respect immutable demographic invariance or multi-stage cascade structures. Our work resolves all four identified research gaps."

---

## Slide 6: Core Research Objectives & Scope
- **Objective 1:** Multi-Stage Cascading Pipeline Design (Pre-College Aptitude $\to$ Discipline Allocation $\to$ Semester Trajectory $\to$ Campus Placement).
- **Objective 2:** Strict Elimination of Cascading Exposure Bias via 5-Fold Stratified OOF.
- **Objective 3:** Platt Logistic Probability Calibration (XGBoost 0.55 + RBF-SVM 0.45 hybrid ensemble).
- **Objective 4:** Demographic-Locked Counterfactual Recourse ($\Delta_{\text{demographic}} = 0$).
- **Objective 5:** Local & Global Explainable AI (TreeSHAP additive attributions).
- **Objective 6:** Empirical Validation & System Hardening ($N=2,966$ real-world graduates, 25/25 automated tests).
- **Speaker Cue (1 min):**
  > "Our investigation was governed by six concrete engineering objectives encompassing pipeline decomposition, mathematical bias mitigation, probability calibration, ethical recourse optimization, local explainability, and empirical hardening."

---

## Slide 7: System Architecture (Figure 1 Embedded)
- **Visual:** High-resolution System Architecture diagram (`fig1_system_architecture.png`)
- **Key Modules:**
  1. Student Profile Ingestion (Demographics, entrance metrics, secondary marks)
  2. Stage 1 Branch Suitability (Random Forest, $M=100$ trees, 87.0% Acc, 0.985 AUC)
  3. 5-Fold OOF Isolation Barrier (Cross-validated intermediate label synthesis)
  4. Stage 2 Academic Forecaster (Blended XGBoost + Gradient Boosting, 4 tiers)
  5. Stage 3 Calibrated Predictor (Hybrid XGBoost + RBF-SVM with Platt scaling)
  6. XAI & Recourse Copilot (Local SHAP decomposition + demographic-locked recourse)
- **Speaker Cue (2 min):**
  > "Figure 1 illustrates our end-to-end architecture. Data flows sequentially from raw multi-modal student records into Stage 1 discipline fitting. Notice the critical 5-Fold Out-of-Fold Isolation Barrier separating Stage 1, Stage 2, and Stage 3. Because intermediate features are strictly synthesized out-of-fold during training, downstream models encounter realistic prediction noise, matching test-time inference."

---

## Slide 8: Proposed Methodology & End-to-End Pipeline (Figure 2 Embedded)
- **Visual:** High-resolution Proposed Methodology flowchart (`fig2_proposed_methodology.png`)
- **Core Workflow:**
  - Patient-Stratified Data Splitting (80% Train, 20% Test)
  - Fold-Isolated Feature Transformers (Imputation medians, scalers fit within training folds only)
  - Intermediate Feature Synthesis (OOF predictions concatenated with academic and behavioral features)
  - Platt Logistic Scaling parameter fitting ($A = -2.41, B = 1.12$)
  - Constrained Optimization search for actionable remediation
  - Audited Fair Deployment across demographic subgroups
- **Speaker Cue (1.5 min):**
  > "Figure 2 details the exact methodology and experimental protocol. All feature imputers, encoders, and scalers are fitted exclusively within training folds to avoid data snooping. The synthesized intermediate features feed into the calibrated hybrid ensemble, followed by post-hoc recourse optimization."

---

## Slide 9: Theoretical Rigor: Mitigating Cascading Exposure Bias
- **Card 1: The Exposure Bias Dilemma:**
  - Training on ground-truth: $P_{\text{train}}(Y_3 \mid X, Y_1, Y_2)$
  - Inference in deployment: $P_{\text{deploy}}(Y_3 \mid X, \hat{Y}_1, \hat{Y}_2)$
  - Divergence: $D_{\text{KL}}(P_{\text{train}} \parallel P_{\text{deploy}}) \gg 0$, causing covariate shift and evaluation collapse.
- **Card 2: Mathematical 5-Fold Stratified OOF Guarantee:**
  - Cross-validation partitioning: $\mathcal{D}_{\text{train}} = \bigcup_{k=1}^5 \mathcal{D}_k$
  - Out-of-fold features: $X_{\text{stage3}}^{(i)} = [x_i, \hat{Y}_1^{\text{OOF}}(x_i), \hat{Y}_2^{\text{OOF}}(x_i)]$
  - Zero Leakage Condition: $I(X_{\text{stage3}}; Y_{\text{intermediate}} \mid \hat{Y}_{\text{intermediate}}^{\text{OOF}}) = 0$.
- **Speaker Cue (2 min):**
  > "Why is Out-of-Fold training a mathematical necessity? If we train downstream models on ground truth, they learn to rely on perfect intermediate signals. At deployment time, only imperfect model predictions exist. This is cascading exposure bias. By enforcing 5-Fold Stratified Out-of-Fold training, downstream models encounter the true error distribution of upstream predictors during training."

---

## Slide 10: Multi-Stage Machine Learning Pipeline Details
- **Stage 1 (Branch Fit):** Random Forest (100 Trees, Gini impurity) predicting 6 disciplines from pre-college marks (87.0% Accuracy, 0.985 OVR AUC).
- **Stage 2 (Academic Forecaster):** Blended 50% XGBoost + 50% Gradient Boosting predicting 4 longitudinal tiers (76.2% Accuracy, 67.3% Macro F1).
- **Stage 3 (Placement Predictor):** Platt-calibrated Hybrid 55% XGBoost + 45% RBF-SVM predicting campus placement (86.9% Accuracy, 91.7% Precision, 0.936 ROC-AUC on real cohort).
- **Speaker Cue (1.5 min):**
  > "Here are the model specifications. Stage 1 uses Random Forests to identify discipline suitability. Stage 2 blends XGBoost and Gradient Boosting to capture complex non-linear academic trajectories. Stage 3 engineers a complementary hybrid combining the tree-based inductive bias of XGBoost with the maximum-margin hyperplane of RBF-SVM."

---

## Slide 11: Experimental Datasets & Validation Protocols
- **4 Integrated Cohorts:**
  - Primary Multi-Modal Cohort ($N=4,000$ / $N=2,500$ 23 features)
  - Authentic Real-World Engineering Cohort ($N=2,966$ graduates across 6 branches)
  - Campus Recruitment Benchmark ($N=215$)
  - UCI Student Performance Benchmark ($N=395$)
- **Experimental Controls:**
  - 80/20 Stratified Train/Test split (Random Seed = 42)
  - Complete fold-isolation of preprocessing pipelines
  - Deterministic random states across Scikit-Learn, XGBoost, and NumPy
- **Speaker Cue (1.5 min):**
  > "To ensure authentic validation, we evaluated our architecture across four distinct cohorts, highlighted by an authentic engineering dataset of 2,966 graduates across six streams. Preprocessing pipelines and encoders were strictly isolated to prevent data contamination."

---

## Slide 12: Empirical Validation on Authentic Engineering Cohort ($N=2,966$)
- **Full Benchmark Table:**
  - *Majority Class:* 55.2% Acc, 0.500 AUC, 0.448 Brier
  - *Logistic Regression:* 78.1% Acc, 0.887 AUC, 0.140 Brier
  - *Decision Tree:* 87.2% Acc, 0.931 AUC, 0.093 Brier
  - *Random Forest:* 87.5% Acc, 0.935 AUC, 0.093 Brier
  - *Support Vector Machine:* 85.2% Acc, 0.926 AUC, 0.108 Brier
  - *Standalone XGBoost:* 88.6% Acc, 0.936 AUC, 0.088 Brier
  - **Proposed Hybrid (XGB + SVM):** 86.9% Acc, **91.7% Precision**, 83.8% Recall, 86.8% Macro F1, **0.936 ROC-AUC**, 0.960 PR-AUC, **0.093 Brier Score**.
- **Ablation Insight:** Removing Stage 1 & Stage 2 OOF features drops placement AUC by 9.5%.
- **Speaker Cue (2 min):**
  > "When benchmarked against real-world engineering graduates, our Proposed Hybrid delivers an outstanding 91.7% Precision and 0.936 ROC-AUC. High precision is crucial in institutional settings to avoid false-positive guarantees. Furthermore, ablation experiments confirm that removing the multi-stage cascade features precipitates a 9.5% reduction in AUC."

---

## Slide 13: Probabilistic Calibration & Reliability Analysis (Figure 3 Embedded)
- **Visual:** High-resolution Reliability Calibration Curve (`fig3_calibration_reliability.png`)
- **Key Concepts:**
  - Platt logistic formulation: $P(Y=1 \mid z) = \frac{1}{1 + \exp(A \cdot z + B)}$
  - Fitted parameters: $A = -2.41, B = 1.12$
  - Brier Score: Mean squared probability error dropped from 0.248 baseline to 0.093 (real) and 0.009 (synthetic)
  - Curve tightly hugs the ideal 45-degree diagonal!
- **Speaker Cue (1.5 min):**
  > "Figure 3 displays our reliability calibration curve. Uncalibrated ensemble models output extreme probabilities near 0 or 1. By applying post-hoc Platt scaling on cross-validated logits, the predicted probabilities match true empirical success frequencies, as evidenced by the curve tightly hugging the diagonal."

---

## Slide 14: Explainable AI: Local SHAP Waterfall Decomposition (Figure 4 Embedded)
- **Visual:** High-resolution SHAP Local Waterfall Plot (`fig4_shap_local_waterfall.png`)
- **Key Attributions:**
  - Additive Game-Theoretic Decomposition: $f(x_i) = \phi_0 + \sum_{j=1}^M \phi_j(x_i)$
  - Top Placement Boosters ($+\phi$): CGPA (+0.42), Core Theory Grades (+0.31), Industry Internships (+0.28)
  - Top At-Risk Penalty Drivers ($-\phi$): Active Backlogs (-0.54), Attendance <75% (-0.38), Zero Certifications (-0.22)
  - Perturbation consistency mathematically verified
- **Speaker Cue (1.5 min):**
  > "Figure 4 shows the local SHAP waterfall decomposition for an individual at-risk student. Starting from the expected base value $\phi_0$, the plot reveals how low attendance and backlog history severely penalize the student's probability, showing counselors exactly where remedial support is required."

---

## Slide 15: Constrained Counterfactual Recourse & Demographic Invariance (Figure 5 Embedded)
- **Visual:** Fairness & Demographic Parity Audit plot (`fig5_fairness_audit.png`)
- **Mathematical Recourse Formulation:**
  $$\min_{\Delta \in \mathbb{R}^d} \sum_{j \in \mathcal{F}_{\text{mut}}} \frac{|\Delta_j|}{\text{MAD}_j} + \lambda \max(0, \tau - f_{\text{cascade}}(x + \Delta))$$
  $$\text{Subject to: } \Delta_k = 0 \quad \forall k \in \mathcal{F}_{\text{immutable}}$$
- **At-Risk Student Trajectory Case Study:**
  - Initial Profile: CGPA = 6.40, Attendance = 64.0%, Backlogs = 1 $\to$ Placement Probability: **0.0%**
  - Generated Interventions: CGPA $6.40 \to 7.15$ ($+0.75$), Attendance $64\% \to 82.5\%$ ($+18.5\%$), Study Hours $8 \to 18.5$ hrs/wk, Certifications $0 \to 2$
  - Result: Placement Probability surges to **91.0%** with zero demographic change!
  - Demographic Parity Difference (DPD) $< 0.02$, Disparate Impact Ratio $= 0.98$.
- **Speaker Cue (2 min):**
  > "Our counterfactual recourse engine solves an optimization problem that minimizes effort scaled by Median Absolute Deviation while strictly locking immutable demographic attributes ($\Delta = 0$). For an at-risk student with 0.0% placement probability, the engine prescribed realistic remedial actions—raising attendance by 18.5% and adding two certifications—raising their placement probability to 91.0% while keeping gender and socio-economic status completely untouched."

---

## Slide 16: Interactive Counselor Copilot & Recourse Studio (Web Platform Screenshots)
- **Visuals:** Dual screenshots of the live system:
  - Left: Student Outcome Forecast & SHAP Drivers (`screenshots/02_at_risk_forecast_and_shap.png`)
  - Right: Prescriptive Counterfactual Recourse Studio (`screenshots/03_counterfactual_recourse_plan.png`)
- **Capabilities:**
  - Real-time multi-stage status indicators and risk dials
  - Interactive intervention sliders allowing counselors to simulate "what-if" scenarios
  - Dynamic recalculation of calibrated placement probability
  - One-click export of personalized remedial roadmaps
- **Speaker Cue (1.5 min):**
  > "Here is our running web platform. Counselors can view student risk dials and local SHAP attributions in real time. In the Recourse Studio on the right, advisors can adjust actionable sliders—such as tutoring hours or certification goals—and observe the live recalculation of placement probability."

---

## Slide 17: Dynamic User Data Integration & Software Reliability (Screenshot Embedded)
- **Visual:** Dynamic Student Profile & CSV Ingestion Interface (`screenshots/08_user_data_integration_form.png`)
- **Software Verification:**
  - Live Form Ingestion (`POST /api/datasets/integrate`) & batch CSV uploads
  - Automatic identifier assignment (`USER_STU_XXXX`) and cascade inference
  - 1-click 'User-Integrated Student' preset in the Recourse Studio
  - 25/25 automated Pytest tests passing in 43.69s (0 failures, 0 warnings)
  - Hardened with Pydantic v2 schemas (`extra='forbid'`), rate limiting, and OWASP headers
- **Speaker Cue (1.5 min):**
  > "To deploy this system across colleges, we built a dynamic User Data Integration module. Institutional staff can ingest individual student records via web form or upload custom CSV cohorts. The pipeline automatically infers missing intermediate stages. On the testing front, all 25 automated unit, integration, and security tests pass with 100% reliability."

---

## Slide 18: Summary of Contributions & Future Research Roadmap
- **4 Key Deliverables:**
  1. *Theoretical:* First multi-stage framework mitigating cascading exposure bias via 5-Fold Stratified OOF ensembling.
  2. *Empirical:* Validated on $N=2,966$ authentic engineering graduates (91.7% Precision, 0.936 AUC).
  3. *Ethical:* Strictly locked demographic invariance ($\Delta = 0$) and fairness auditing (DPD < 0.02).
  4. *Engineering:* Hardened Flask web application with live simulation and 25/25 passing tests.
- **Future Roadmap:**
  - Structural Causal Models (Directed Acyclic Graphs) for formal causal guarantees
  - Longitudinal multi-campus counseling pilots across Anna University departments
  - Privacy-preserving federated multi-institution learning
- **Speaker Cue (1 min):**
  > "In summary, this work bridges predictive analytics and actionable educational counseling. We have resolved cascading exposure bias, achieved reliable calibration, and enforced strict demographic parity. In our future work, we plan to incorporate Directed Acyclic Graphs for causal interventional bounds and expand federated learning across university campuses."

---

## Slide 19: Defense Q&A & Live Demonstration
- **Title:** Questions & Interactive System Demonstration
- **Candidate:** JAGADESH A (jagadesh.ceg@annauniv.edu)
- **Degree:** M.E. Computer Science and Engineering (Data Science and Cybersecurity)
- **Institution:** Department of CSE, College of Engineering, Guindy, Anna University, Chennai
- **Active Portals:**
  - Main Dashboard: `http://127.0.0.1:5000`
  - Recourse Simulation Studio: `http://127.0.0.1:5000/recourse`
  - Datasets & Ingestion Portal: `http://127.0.0.1:5000/datasets`
  - Scientific Benchmarks Lightbox: `http://127.0.0.1:5000/benchmarks`
- **Speaker Cue (1 min):**
  > "Thank you very much for your time and guidance. I will now gladly answer your questions and proceed directly to the live interactive software demonstration. Thank you!"

---

## Defense Q&A Master Cheat Sheet (Top Reviewer Questions)

### Q1: "Why use Out-of-Fold (OOF) intermediate training rather than ground truth labels?"
> **Answer:** "If we train Stage 2 or Stage 3 using ground-truth intermediate labels, downstream models learn to rely on perfect, uncorrupted inputs. But during live deployment on new students, the ground-truth intermediate label is unavailable—the system only has access to noisy model predictions. This creates a severe mismatch known as cascading exposure bias or covariate shift. By generating 5-Fold Stratified Out-of-Fold predictions during training, downstream models learn to tolerate realistic classification uncertainty, matching production inference conditions perfectly."

### Q2: "Can you prove that demographic attributes are strictly locked during recourse search?"
> **Answer:** "Yes. In `src/explainability/counterfactual_recourse.py`, we explicitly partition features into mutable and immutable sets. The immutable set $\mathcal{F}_{\text{immutable}} = \{\text{'gender'}, \text{'caste'}, \text{'parental\_education'}, \text{'family\_income'}\}$. In every coordinate-descent optimization iteration, we enforce $\Delta_k = 0, \forall k \in \mathcal{F}_{\text{immutable}}$. Furthermore, our automated Pytest test in `tests/test_pipeline_and_fairness.py` (`test_recourse_immutable_demographics_lock`) mathematically asserts that across 100 randomized recourse searches, the perturbation across all demographic features is strictly 0."

### Q3: "How does your model perform on authentic real students compared to synthetic data?"
> **Answer:** "On the synthetic cohort ($N=4,000$), our model achieves 98.8% accuracy and 0.999 AUC. When benchmarked on the authentic real-world engineering graduate cohort ($N=2,966$ students across 6 streams), the model maintains an outstanding ROC-AUC of 0.936, an 86.9% accuracy, and a 91.7% precision. This proves that our feature representations and cascade inductive bias generalize exceptionally well to real collegiate distributions."
