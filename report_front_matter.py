"""
Front matter builder for Anna University / CEG Phase 1 Project Report.
Candidate: JAGADESH A, M.E. CSE (Data Science and Cybersecurity), CEG Campus.
Formatted to exact Anna University M.E. Cover Page Model with Logo.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from report_helpers import (
    add_body_paragraph, add_bullet_item, add_styled_table,
    add_table_caption, set_cell_margins, set_cell_background, set_cell_borders
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "anna_univ_logo.png")

def build_front_matter(doc):
    # -------------------------------------------------------------
    # 1. TITLE / COVER PAGE (Page 1) - EXACT RECREATION OF USER'S MODEL
    # -------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(20)
    p_title.paragraph_format.space_after = Pt(22)
    p_title.paragraph_format.line_spacing = 1.3
    
    r_title = p_title.add_run(
        "ELIMINATING CASCADING EXPOSURE BIAS AND \n"
        "MISCALIBRATION IN HIERARCHICAL EDUCATIONAL \n"
        "PROGRESSION MODELS VIA OUT-OF-FOLD ENSEMBLING AND \n"
        "DEMOGRAPHIC-LOCKED RECOURSE"
    )
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(14)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_phase = doc.add_paragraph()
    p_phase.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_phase.paragraph_format.space_before = Pt(12)
    p_phase.paragraph_format.space_after = Pt(16)
    r_phase = p_phase.add_run("PHASE I REPORT")
    r_phase.font.name = 'Times New Roman'
    r_phase.font.size = Pt(13)
    r_phase.font.bold = True
    r_phase.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(10)
    r_sub = p_sub.add_run("Submitted by")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True

    p_name = doc.add_paragraph()
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_name.paragraph_format.space_before = Pt(4)
    p_name.paragraph_format.space_after = Pt(16)
    r_name = p_name.add_run("JAGADESH A")
    r_name.font.name = 'Times New Roman'
    r_name.font.size = Pt(13.5)
    r_name.font.bold = True
    r_name.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_deg_req = doc.add_paragraph()
    p_deg_req.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_deg_req.paragraph_format.space_before = Pt(8)
    p_deg_req.paragraph_format.space_after = Pt(14)
    r_dreq = p_deg_req.add_run("in partial fulfillment for the award of the degree of")
    r_dreq.font.name = 'Times New Roman'
    r_dreq.font.size = Pt(12)
    r_dreq.font.italic = True

    p_deg = doc.add_paragraph()
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_deg.paragraph_format.space_before = Pt(0)
    p_deg.paragraph_format.space_after = Pt(18)
    p_deg.paragraph_format.line_spacing = 1.25
    r_deg = p_deg.add_run(
        "MASTER OF ENGINEERING IN\n"
        "COMPUTER SCIENCE AND ENGINEERING\n"
        "(DATA SCIENCE AND CYBER SECURITY)"
    )
    r_deg.font.name = 'Times New Roman'
    r_deg.font.size = Pt(12.5)
    r_deg.font.bold = True
    r_deg.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    # ANNA UNIVERSITY EMBLEM / LOGO
    if os.path.exists(LOGO_PATH):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(4)
        p_logo.paragraph_format.space_after = Pt(16)
        r_logo = p_logo.add_run()
        r_logo.add_picture(LOGO_PATH, width=Inches(1.7))

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_before = Pt(4)
    p_dept.paragraph_format.space_after = Pt(28)
    p_dept.paragraph_format.line_spacing = 1.2
    r_dept = p_dept.add_run(
        "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\n"
        "COLLEGE OF ENGINEERING, GUINDY (CEG CAMPUS)\n"
        "ANNA UNIVERSITY, CHENNAI"
    )
    r_dept.font.name = 'Times New Roman'
    r_dept.font.size = Pt(12)
    r_dept.font.bold = True
    r_dept.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_date.paragraph_format.space_before = Pt(14)
    p_date.paragraph_format.space_after = Pt(0)
    r_date = p_date.add_run("NOVEMBER 2026")
    r_date.font.name = 'Times New Roman'
    r_date.font.size = Pt(12.5)
    r_date.font.bold = True
    r_date.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 2. ABSTRACT (Page 2)
    # -------------------------------------------------------------
    p_abs_hdr = doc.add_paragraph()
    p_abs_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs_hdr.paragraph_format.space_before = Pt(10)
    p_abs_hdr.paragraph_format.space_after = Pt(6)
    r_abs = p_abs_hdr.add_run("ABSTRACT")
    r_abs.font.name = 'Times New Roman'
    r_abs.font.size = Pt(14)
    r_abs.font.bold = True
    r_abs.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)

    add_body_paragraph(
        doc,
        "Educational Data Mining (EDM) in tertiary engineering institutions increasingly relies on machine learning models "
        "to forecast student progression. Under statutory guidelines from AICTE and state technical universities such as Anna University, "
        "collegiate engineering progression spans distinct sequential milestones: pre-college entrance credentials, discipline suitability, "
        "longitudinal semester standing, and final institutional campus placement. However, contemporary predictive systems exhibit three "
        "critical structural flaws: (i) cascading exposure bias caused by training downstream models on ground-truth intermediate labels, "
        "which precipitates severe covariate shift and catastrophic error accumulation during live deployment; (ii) model miscalibration, "
        "yielding overconfident probabilistic risk scores that misguide counseling interventions; and (iii) unconstrained recourse "
        "algorithms that propose unachievable changes to immutable demographic attributes (such as altering gender, family income, or parental education).",
        space_after=3, line_spacing=1.12
    )
    add_body_paragraph(
        doc,
        "To resolve these tripartite vulnerabilities, this Phase 1 project presents a hierarchical multi-task, explainable, and ethically "
        "constrained educational recourse framework. Student progression is modeled across a three-stage sequential cascade: Stage 1 recommends "
        "engineering discipline suitability using Random Forests (87.0% accuracy, 0.985 AUC); Stage 2 forecasts longitudinal academic standing "
        "via blended XGBoost and Gradient Boosting (76.2% accuracy, 67.3% macro F1); and Stage 3 predicts final campus placement using a "
        "Platt-calibrated XGBoost and RBF-SVM hybrid ensemble (98.8% accuracy, 0.999 AUC on a synthetic benchmark cohort of N=4,000; 84.5% "
        "accuracy, 0.936 AUC on an authentic cohort of 2,966 engineering graduates).",
        space_after=3, line_spacing=1.12
    )
    add_body_paragraph(
        doc,
        "Cascading exposure bias is mathematically mitigated by training downstream stages strictly on 5-Fold Stratified Out-of-Fold (OOF) "
        "intermediate representations, guaranteeing zero target leakage: I(X_stage3; Y_intermediate | Y_hat_OOF) = 0. Platt logistic scaling "
        "reduces the Stage 3 Brier score to 0.009 (synthetic) and 0.108 (authentic), aligning reliability curves closely with the empirical diagonal. "
        "An L1-norm constrained recourse engine with Median Absolute Deviation (MAD) scaling identifies minimal-cost, actionable interventions while "
        "enforcing strict demographic invariance (Delta_imm = 0) over protected traits and monotonic semester feasibility constraints. Granular local "
        "diagnostics are computed via TreeSHAP, deconstructing risk scores into exact positive penalty drivers and protective mitigation factors.",
        space_after=3, line_spacing=1.12
    )
    add_body_paragraph(
        doc,
        "The framework is verified across 25 automated pytest tests (passing in 38.68s), containerized RESTful API microservices with sub-10ms latency, "
        "and an interactive counselor dashboard. A canonical case study shows an at-risk student initially forecasted at 0.0% placement probability "
        "achieving a calibrated 91.0% success rate through a structured 4-step remediation plan, delivering a clinically sound, transparent decision-support "
        "copilot for tertiary engineering education.",
        space_after=4, line_spacing=1.12
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 6. TABLE OF CONTENTS (Pages 6-8)
    # -------------------------------------------------------------
    p_toc_hdr = doc.add_paragraph()
    p_toc_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_hdr.paragraph_format.space_before = Pt(16)
    p_toc_hdr.paragraph_format.space_after = Pt(10)
    r_toc = p_toc_hdr.add_run("TABLE OF CONTENTS")
    r_toc.font.name = 'Times New Roman'
    r_toc.font.size = Pt(14)
    r_toc.font.bold = True
    r_toc.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)

    toc_headers = ["CHAPTER NO.", "TITLE", "PAGE NO."]
    toc_data = [
        ["", "ABSTRACT", "ii"],
        ["", "LIST OF TABLES", "vi"],
        ["", "LIST OF FIGURES", "vii"],
        ["", "LIST OF ABBREVIATIONS", "viii"],
        ["1", "INTRODUCTION", "1"],
        ["1.1", "Background and Significance", "1"],
        ["1.2", "Higher Education Landscape and AICTE Regulations", "1"],
        ["1.3", "Paradigm Shift: From Flat Classification to Hierarchical Recourse", "2"],
        ["1.4", "Problem Statement: The Tripartite Failure Modes", "3"],
        ["1.5", "Objectives of the Phase 1 Research", "4"],
        ["1.6", "Aim of the Project", "5"],
        ["1.7", "Scope and Delimitations", "5"],
        ["1.8", "Organization of the Report", "5"],
        ["2", "LITERATURE SURVEY", "7"],
        ["2.1", "Evolution of Educational Data Mining (EDM) and Learning Analytics", "7"],
        ["2.2", "Supervised Learning Classifiers in Academic Risk & Placement", "7"],
        ["2.3", "Sequential Decision Models and Cascading Exposure Bias", "8"],
        ["2.4", "Probability Calibration and Uncertainty Quantification in EDM", "9"],
        ["2.5", "Explainable Artificial Intelligence (XAI) in Educational Analytics", "9"],
        ["2.6", "Counterfactual Reasoning and Algorithmic Recourse Formulations", "9"],
        ["2.7", "Algorithmic Fairness and Protected Demographic Invariance", "10"],
        ["2.8", "Critical Review of Benchmark Literature and Research Gaps", "10"],
        ["3", "EXISTING SYSTEMS AND REQUIREMENTS SPECIFICATION", "12"],
        ["3.1", "Review of Contemporary Early Warning Systems and Placement Portals", "12"],
        ["3.2", "Vulnerability Analysis of Existing Implementations", "12"],
        ["3.3", "Comparative Analysis of Existing EDM Models", "13"],
        ["3.4", "System Requirements Specification (SRS)", "14"],
        ["3.5", "Functional Requirements Specification (FR1 to FR10)", "15"],
        ["3.6", "Non-Functional Quality Attribute Requirements (NFR1 to NFR8)", "16"],
        ["3.7", "Comprehensive Feasibility Analysis", "16"],
        ["4", "SYSTEM ARCHITECTURE AND MATHEMATICAL FORMULATION", "18"],
        ["4.1", "Overall Hierarchical Architecture and End-to-End Pipeline", "18"],
        ["4.2", "Mathematical Problem Formulation and Modality Partitioning", "19"],
        ["4.3", "Mitigation of Cascading Exposure Bias via 5-Fold Stratified OOF", "20"],
        ["4.4", "Stage 1: Discipline Suitability Recommender Formulation", "20"],
        ["4.5", "Stage 2: Longitudinal Academic Standing Forecaster Formulation", "21"],
        ["4.6", "Stage 3: Platt-Calibrated Placement Hybrid Predictor", "21"],
        ["4.7", "Probability Calibration Metrics: Brier Score and ECE", "22"],
        ["4.8", "Constrained Counterfactual Recourse Optimization Formulation", "22"],
        ["4.9", "Whole-Model Explainable AI (XAI) Decomposition via TreeSHAP", "23"],
        ["4.10", "Algorithmic Fairness Formulations: DPD and EOD", "23"],
        ["4.11", "Closed-Loop Longitudinal Tracking and Counselor Copilot Workflow", "23"],
        ["5", "METHODOLOGY AND ALGORITHMIC WORKFLOW", "25"],
        ["5.1", "Empirical Datasets and Feature Schema Representation", "25"],
        ["5.2", "Data Preprocessing, Cleansing, and Leak-Free Data Partitioning", "26"],
        ["5.3", "Feature Engineering and Trajectory Metric Formulations", "26"],
        ["5.4", "Formal Algorithmic Formulations (Algorithms 5.1 to 5.4)", "26"],
        ["5.5", "Relational Database Schema Design for Longitudinal Intervention", "29"],
        ["5.6", "Dynamic User Ingestion Pipeline and Data Standardization", "29"],
        ["6", "IMPLEMENTATION, EXPERIMENTAL RESULTS AND DISCUSSION", "30"],
        ["6.1", "Modular System Architecture and REST API Microservices", "30"],
        ["6.2", "Automated Test Suite Verification and Code Quality Assurance", "30"],
        ["6.3", "Multi-Stage Cascade Performance Benchmarking", "30"],
        ["6.4", "Probability Calibration Reliability Analysis", "31"],
        ["6.5", "Ablation Study: Validating Exposure Bias Elimination", "32"],
        ["6.6", "Fairness and Demographic Subgroup Parity Audit", "33"],
        ["6.7", "Canonical Student Recourse Walkthrough: Student STU_0083", "34"],
        ["6.8", "Computational Complexity, Runtime Latency, and Memory Footprint", "35"],
        ["6.9", "Interactive Counselor Dashboard & UI Walkthrough (Screenshots)", "36"],
        ["7", "CONCLUSION AND PHASE 2 ROADMAP", "41"],
        ["7.1", "Summary of Phase 1 Technical Deliverables", "41"],
        ["7.2", "Novel Theoretical and Scientific Contributions", "41"],
        ["7.3", "Identified Research Limitations", "42"],
        ["7.4", "Phase 2 Proposed Work Plan and Enhancements", "42"],
        ["", "REFERENCES", "44"]
    ]
    add_styled_table(doc, toc_headers, toc_data, col_widths=[1.1, 4.2, 0.7])

    doc.add_page_break()

    # -------------------------------------------------------------
    # 7. LIST OF TABLES (Page 9)
    # -------------------------------------------------------------
    p_lot_hdr = doc.add_paragraph()
    p_lot_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lot_hdr.paragraph_format.space_before = Pt(16)
    p_lot_hdr.paragraph_format.space_after = Pt(10)
    r_lot = p_lot_hdr.add_run("LIST OF TABLES")
    r_lot.font.name = 'Times New Roman'
    r_lot.font.size = Pt(14)
    r_lot.font.bold = True
    r_lot.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)

    lot_headers = ["TABLE NO.", "TITLE", "PAGE NO."]
    lot_data = [
        ["2.1", "Systematic Comparative Analysis of Benchmark Literature and EDM Models", "10"],
        ["3.1", "Comparative Vulnerability Analysis of Existing EDM and Placement Frameworks", "13"],
        ["3.2", "Minimum and Recommended Hardware Infrastructure Specifications", "14"],
        ["3.3", "Software Technology Stack and Library Specifications", "14"],
        ["3.4", "Functional Requirements Specifications (FR1 to FR10)", "15"],
        ["3.5", "Non-Functional Quality Attribute Requirements (NFR1 to NFR8)", "16"],
        ["4.1", "Mathematical Variables of the Dynamic Student State Vector S_t", "19"],
        ["5.1", "Multi-Modal Feature Schema Representation Across Benchmark Cohorts", "25"],
        ["5.2", "Relational Database Schema Design for Longitudinal Counseling & Recourse Tracking", "29"],
        ["6.1", "Automated Pytest Suite Verification Across Functional Modules", "30"],
        ["6.2", "Hierarchical Three-Stage Cascade Performance Benchmarks (N=4,000 Cohort)", "31"],
        ["6.3", "Multi-Metric Validation on Authentic Engineering Cohort (N=2,966 Graduates)", "31"],
        ["6.4", "Probability Calibration Quality Comparison (Brier Score & ECE)", "31"],
        ["6.5", "Ablation Study: Impact of Hierarchical OOF Inductive Bias and Leakage Prevention", "32"],
        ["6.6", "Fairness and Subgroup Parity Audit Across Protected Demographic Subgroups", "33"],
        ["6.7", "Constrained Recourse Trajectory for Canonical At-Risk Profile (Student STU_0083)", "34"],
        ["6.8", "Computational Runtime Latency and Memory Overhead Breakdown Across Cascade Stages", "35"]
    ]
    add_styled_table(doc, lot_headers, lot_data, col_widths=[1.1, 4.2, 0.7])

    doc.add_page_break()

    # -------------------------------------------------------------
    # 8. LIST OF FIGURES (Page 10)
    # -------------------------------------------------------------
    p_lof_hdr = doc.add_paragraph()
    p_lof_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lof_hdr.paragraph_format.space_before = Pt(16)
    p_lof_hdr.paragraph_format.space_after = Pt(10)
    r_lof = p_lof_hdr.add_run("LIST OF FIGURES")
    r_lof.font.name = 'Times New Roman'
    r_lof.font.size = Pt(14)
    r_lof.font.bold = True
    r_lof.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)

    lof_headers = ["FIGURE NO.", "NAME OF THE FIGURE", "PAGE NO."]
    lof_data = [
        ["4.1", "System Architecture of Hierarchical Multi-Task Educational Recourse Framework", "18"],
        ["6.1", "Probability Calibration Reliability Diagram (Uncalibrated vs. Platt-Calibrated)", "32"],
        ["6.2", "Fairness and Subgroup Parity Audit Across Protected Demographic Attributes", "33"],
        ["6.3", "Local Additive SHAP Waterfall Decomposition for Canonical At-Risk Student STU_0083", "35"],
        ["6.4", "Counselor Dashboard Home Overview and Real-Time Trajectory KPI View", "36"],
        ["6.5", "Predictive Diagnostics and Additive TreeSHAP Feature Attribution Interface", "37"],
        ["6.6", "Constrained Counterfactual Recourse Optimization and Feasibility Planner Interface", "37"],
        ["6.7", "Post-Recourse Simulated Reforecast Verification and Trajectory Lift Interface", "38"],
        ["6.8", "Research Benchmark Suite and Multi-Model Evaluation Analytics View", "38"],
        ["6.9", "Probability Calibration Diagnostics, Reliability Diagrams, and Error Metric Curves", "39"],
        ["6.10", "Multi-Cohort Longitudinal Dataset Explorer and Feature Distribution Analyzer", "39"],
        ["6.11", "Dynamic User Counseling Ingestion and Real-Time Pipeline Integration Form", "40"]
    ]
    add_styled_table(doc, lof_headers, lof_data, col_widths=[1.1, 4.2, 0.7])

    doc.add_page_break()

    # -------------------------------------------------------------
    # 9. LIST OF ABBREVIATIONS (Page 11)
    # -------------------------------------------------------------
    p_abb_hdr = doc.add_paragraph()
    p_abb_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abb_hdr.paragraph_format.space_before = Pt(16)
    p_abb_hdr.paragraph_format.space_after = Pt(10)
    r_abb = p_abb_hdr.add_run("LIST OF ABBREVIATIONS")
    r_abb.font.name = 'Times New Roman'
    r_abb.font.size = Pt(14)
    r_abb.font.bold = True
    r_abb.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)

    abb_headers = ["ABBREVIATION", "EXPANSION"]
    abb_data = [
        ["AI / ML", "Artificial Intelligence / Machine Learning"],
        ["EDM / LA", "Educational Data Mining / Learning Analytics"],
        ["AICTE", "All India Council for Technical Education"],
        ["CEG", "College of Engineering, Guindy, Anna University"],
        ["EWS", "Early Warning System"],
        ["XAI", "Explainable Artificial Intelligence"],
        ["SHAP", "Shapley Additive exPlanations (TreeSHAP / KernelSHAP)"],
        ["LIME", "Local Interpretable Model-agnostic Explanations"],
        ["OOF", "Out-of-Fold (Cross-Validated Intermediate Representations)"],
        ["XGBoost / GBDT", "eXtreme Gradient Boosting / Gradient Boosted Decision Trees"],
        ["RF / SVM", "Random Forest / Support Vector Machine (RBF Kernel)"],
        ["CGPA", "Cumulative Grade Point Average"],
        ["ECE / BS", "Expected Calibration Error / Brier Score"],
        ["MAD", "Median Absolute Deviation"],
        ["DPD / EOD", "Demographic Parity Difference / Equal Opportunity Difference"],
        ["ROC-AUC", "Receiver Operating Characteristic - Area Under the Curve"],
        ["FERPA / GDPR", "Family Educational Rights and Privacy Act / General Data Protection Regulation"],
        ["LMS / SIS", "Learning Management System / Student Information System"],
        ["REST API", "Representational State Transfer Application Programming Interface"],
        ["DAG / SCM", "Directed Acyclic Graph / Structural Causal Model"]
    ]
    add_styled_table(doc, abb_headers, abb_data, col_widths=[1.6, 4.4])

    doc.add_page_break()
    print("Front matter generated successfully with exact cover layout.")
