# Known Limitations and Research Disclaimers

**Project:** Hierarchical Multi-Task & Explainable Educational Recourse Framework  
**Document Version:** 2.0.0  
**Status:** Canonical Reference

---

## 1. Synthetic Data Dependency & Lack of Real-World External Validation

> [!WARNING]
> **CRITICAL RESEARCH NOTICE**:  
> The underlying dataset used for training, benchmarking, and evaluating this framework is **100% synthetically generated** via parametric simulation (`data/generate_dataset.py`). It has **NOT** been evaluated on, calibrated against, or validated using real student records from an accredited educational institution.

- **Simulation Assumptions:** Student attributes, academic trajectories, semester exam scores, and campus placement outcomes were synthesized using parameterized normal, beta, binomial, and categorical distributions reflecting educational domain heuristics.
- **Risk of Circularity:** Although the data generation formulas separate pre-college traits from college-level outcomes, any parametric synthetic generator encodes implicit inductive biases and structural assumptions that machine learning models may easily exploit.
- **Real-World Generalizability:** Real student populations exhibit complex sociodemographic disparities, unmeasured life events, institutional grading curve shifts, non-linear dropout patterns, and macroeconomic hiring fluctuations that synthetic distributions cannot faithfully replicate.
- **Operational Requirement:** Prior to any institutional pilot, deployment, or policy decision, the pipeline must be retrained and validated from scratch on an institutionally vetted, IRB-approved, anonymized real-world longitudinal cohort.

---

## 2. Non-Causal Nature of Algorithmic Recourse

> [!IMPORTANT]
> **NON-CAUSAL ADVISORY**:  
> Algorithmic counterfactual recourse trajectories produced by [`CounterfactualRecourseEngine`](file:///c:/Users/Methunraj%20A/Downloads/bro/src/explainability/counterfactual_recourse.py) identify **predictive model inversion points**, NOT causal interventional guarantees.

- **Correlation vs. Causation:** The underlying models (Random Forest, Gradient Boosting, XGBoost, Support Vector Machines) estimate conditional correlations $P(Y \mid X)$, not causal interventional distributions $P(Y \mid \text{do}(X))$.
- **No Placement Guarantee:** Generating a counterfactual indicating that increasing study hours from 14 to 22 hours/week and CGPA from 6.2 to 7.8 shifts predicted placement probability from 0.42 to 0.75 **does not guarantee** that a student who enacts these changes will receive a job offer. Hiring outcomes depend on macroeconomic job market conditions, interview performance, soft skill nuances, company-specific hiring criteria, and macroeconomic factors external to the model.
- **Actionability & Agency:** Recommendations serve exclusively as advisory educational guidance to assist academic advisors and students in identifying modifiable risk factors.

---

## 3. Fixed Feature Constraints and Grading Scale Specifics

- **Grading Scale Assumption:** The preprocessing and model feature contracts assume a 10.0-point Cumulative Grade Point Average (CGPA) system and a 100-point percentage scale for intermediate exams and attendance. Educational systems utilizing 4.0 scales, letter grading, or European ECTS scales require explicit re-scaling and schema adjustments.
- **Immutable Characteristics:** Gender, age, parental status, parental education, and pre-matriculation entrance scores are strictly enforced as immutable ($\delta_j = 0$). Any institutional modification to the definition of actionable features must be audited for ethical and legal compliance.
- **Discretization and Thresholds:** Branch suitability and academic performance categories are discretized into predefined ordinal/categorical classes. Fine-grained performance nuances near decision boundaries may be smoothed out.

---

## 4. Explainability & Multicollinearity Limitations

- **TreeExplainer Credit Allocation:** SHAP values are calculated via TreeExplainer on the tree ensemble components. While mathematically sound under game-theoretic axioms, multicollinearity among academic features (e.g., intermediate mathematics, intermediate aggregate, core course scores, CGPA) can cause Shapley credit to disperse across correlated features.
- **Local Approximation:** While perturbation tests demonstrate local attribution consistency, local SHAP values reflect marginal contributions around specific feature configurations and may not extrapolate globally across distant regions of the feature manifold.

---

## 5. Computational and Latency Constraints

- **Single Student Inference:** Sequential three-stage cascade inference requires ~30–50 ms.
- **Counterfactual Search:** The coordinate descent recourse optimization performs up to 100 sequential multi-stage evaluations per request, requiring ~250–500 ms per student profile.
- **Batch Recourse:** Running counterfactual recourse across large cohorts ($N > 10,000$) should be scheduled as asynchronous background jobs rather than real-time synchronous HTTP requests.
