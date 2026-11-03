"""
Script to generate publication-grade IEEE Architecture and Methodology diagrams.
Generates:
1. reports/figures/fig1_system_architecture.png (Architecture Diagram)
2. reports/figures/fig2_proposed_methodology.png (Methodology Flowchart Diagram)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports", "figures")
os.makedirs(OUT_DIR, exist_ok=True)

# Set high-quality font styling
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    # Color Palette (IEEE Modern / Professional Academic)
    NAVY = "#0f172a"
    BLUE = "#1e40af"
    TEAL = "#0284c7"
    GREEN = "#059669"
    AMBER = "#d97706"
    PURPLE = "#7c3aed"
    RED = "#dc2626"
    GRAY_BG = "#f8fafc"
    CARD_BORDER = "#cbd5e1"
    TEXT_DARK = "#0f172a"
    TEXT_MUTED = "#475569"

    # Background canvas
    fig.patch.set_facecolor('#ffffff')

    # Title
    ax.text(7.5, 8.15, "Figure 1: Hierarchical Multi-Task System Architecture & Data Flow", 
            ha='center', va='center', fontsize=16, fontweight='bold', color=NAVY)
    ax.text(7.5, 7.82, "Modular Pipeline for Leakage Mitigation, Platt Probability Calibration, and Demographic-Locked Recourse",
            ha='center', va='center', fontsize=11, color=TEXT_MUTED, style='italic')

    # Function to draw rounded card
    def draw_card(x, y, w, h, title, subtitle="", bg="#ffffff", border=CARD_BORDER, title_color=BLUE):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                             facecolor=bg, edgecolor=border, linewidth=1.5, zorder=2)
        ax.add_patch(box)
        if title:
            ax.text(x + w/2, y + h - 0.28, title, ha='center', va='top', fontsize=11, fontweight='bold', color=title_color, zorder=3)
        if subtitle:
            ax.text(x + w/2, y + h - 0.55, subtitle, ha='center', va='top', fontsize=9, color=TEXT_MUTED, zorder=3)

    # Function to draw arrow
    def draw_arrow(x1, y1, x2, y2, color=BLUE, style="->", rad=0.0, lw=2.0):
        arr = FancyArrowPatch((x1, y1), (x2, y2),
                              connectionstyle=f"arc3,rad={rad}",
                              arrowstyle=style, mutation_scale=15,
                              color=color, linewidth=lw, zorder=4)
        ax.add_patch(arr)

    # ========================================================
    # 1. INPUT MODALITIES (Left Column, x = 0.5 to 3.5)
    # ========================================================
    draw_card(0.5, 0.6, 3.2, 6.8, "MULTI-MODAL INPUT SPACE", "Concatenated Profile Vector x_i in R^d", bg="#f1f5f9", title_color=NAVY)

    # Sub-box 1A: Demographics
    draw_card(0.7, 5.2, 2.8, 1.7, "Modality 1: Demographics", "x^(demo) in F_immutable", bg="#ffffff", border=RED, title_color=RED)
    ax.text(0.85, 5.85, "• Gender, Caste, Category\n• Parental Education & Status\n• Family Income Bracket\n[DEMOGRAPHIC LOCK: Δ = 0]", 
            ha='left', va='top', fontsize=8.5, color=TEXT_DARK, zorder=3)

    # Sub-box 1B: Pre-College Aptitude
    draw_card(0.7, 3.2, 2.8, 1.7, "Modality 2: Entrance Aptitude", "x^(pre) (Pre-College Marks)", bg="#ffffff", border=TEAL, title_color=TEAL)
    ax.text(0.85, 3.85, "• 10th & 12th Board Percentile\n• Math, Physics, Chemistry Marks\n• Entrance Aptitude Percentile\n• English Proficiency Score", 
            ha='left', va='top', fontsize=8.5, color=TEXT_DARK, zorder=3)

    # Sub-box 1C: Collegiate & Behavioral
    draw_card(0.7, 1.0, 2.8, 1.9, "Modality 3: College Performance", "x^(coll) (Collegiate Academics)", bg="#ffffff", border=GREEN, title_color=GREEN)
    ax.text(0.85, 2.05, "• Midterm & Core Theory Marks\n• Cumulative Grade Point Average (CGPA)\n• Lecture Attendance Rate (%)\n• Active Backlogs History\n• Certifications & Internships", 
            ha='left', va='top', fontsize=8.5, color=TEXT_DARK, zorder=3)

    # ========================================================
    # 2. 5-FOLD STRATIFIED OOF ISOLATION BARRIER
    # ========================================================
    draw_card(4.1, 0.6, 1.0, 6.8, "5-FOLD OOF", "Leak Barrier", bg="#e0e7ff", border="#6366f1", title_color=BLUE)
    ax.text(4.6, 4.3, "OOF\nTraining\nBarrier\n\nI(X; Y) = 0\n\nZero Label\nLeakage\nEnforced", 
            ha='center', va='center', fontsize=9, fontweight='bold', color=BLUE, zorder=3)

    # Arrows from Inputs into OOF Barrier
    draw_arrow(3.5, 4.05, 4.1, 4.05, color=TEAL, lw=2)

    # ========================================================
    # 3. HIERARCHICAL CASCADED PIPELINE (Center, x = 5.5 to 10.2)
    # ========================================================
    draw_card(5.5, 0.6, 4.8, 6.8, "HIERARCHICAL CASCADED LEARNING CORE", "Sequential Pipeline with Platt Calibration", bg="#f8fafc", title_color=NAVY)

    # Stage 1: Branch Recommender
    draw_card(5.7, 5.1, 4.4, 1.8, "STAGE 1: DISCIPLINE FIT", "Multi-Class Random Forest (M=100 Trees)", bg="#ffffff", border=TEAL, title_color=TEAL)
    ax.text(5.85, 5.85, "Input: Pre-College Credentials x^(pre)\nOutput: Predicted Branch B_hat in {CSE, IT, ECE, EEE, ME, CE}\nMetric: 87.0% Accuracy | 0.985 OVR ROC-AUC\nAction: Emits OOF predicted branch as downstream feature", 
            ha='left', va='top', fontsize=8.5, color=TEXT_DARK, zorder=3)

    # Stage 2: Academic Forecaster
    draw_card(5.7, 2.9, 4.4, 1.9, "STAGE 2: ACADEMIC STANDING", "Blended Ensemble: XGBoost (0.50) + GBDT (0.50)", bg="#ffffff", border=GREEN, title_color=GREEN)
    ax.text(5.85, 3.85, "Input: [x^(pre), x^(coll), Predicted Branch B_hat]\nOutput: Forecasted Tier A_hat in {Distinction, First, Second, At-Risk}\nMetric: 76.2% Accuracy | 67.3% Macro F1\nAction: Emits OOF predicted tier into Stage 3", 
            ha='left', va='top', fontsize=8.5, color=TEXT_DARK, zorder=3)

    # Stage 3: Placement Predictor + Platt Calibration
    draw_card(5.7, 0.8, 4.4, 1.8, "STAGE 3: PLATT-CALIBRATED PLACEMENT", "Hybrid: XGBoost (0.55) + RBF-SVM (0.45)", bg="#ffffff", border=PURPLE, title_color=PURPLE)
    ax.text(5.85, 1.70, "Input: [x_i, B_hat, A_hat] (Complete Concatenated Context)\nRaw Hybrid Logits: z_i = w1*logit(P_xgb) + w2*logit(P_svm)\nCalibration: P(Y=1|z) = 1 / [1 + exp(A*z + B)]  (Platt Scaling)\nMetric: 98.8% Acc (Synth), 84.5% Acc | 0.936 AUC | Brier=0.009", 
            ha='left', va='top', fontsize=8.2, color=TEXT_DARK, zorder=3)

    # Cascade Arrows within Pipeline
    draw_arrow(5.1, 4.05, 5.7, 5.8, color=TEAL, rad=0.1, lw=2)
    draw_arrow(7.9, 5.1, 7.9, 4.8, color=TEAL, lw=2) # S1 to S2
    draw_arrow(7.9, 2.9, 7.9, 2.6, color=GREEN, lw=2) # S2 to S3

    # ========================================================
    # 4. EXPLAINABILITY & RECOURSE ENGINES (Right Column, x = 10.7 to 14.5)
    # ========================================================
    draw_card(10.7, 0.6, 3.8, 6.8, "EXPLAINABILITY & RECOURSE", "Model-Agnostic Post-Hoc Analysis", bg="#f1f5f9", title_color=NAVY)

    # Engine A: SHAP Waterfall Explainer
    draw_card(10.9, 4.4, 3.4, 2.5, "WHOLE-MODEL SHAP EXPLAINER", "TreeSHAP + KernelSHAP Decomposition", bg="#ffffff", border=BLUE, title_color=BLUE)
    ax.text(11.05, 5.95, "Formulation: f(x) = φ_0 + Σ φ_j(x)\n• Local attribution for hybrid ensemble\n• Identifies positive boosters (+CGPA, +Intern)\n• Identifies risk penalties (-Attendance, -Backlog)\n• Validated via prediction perturbation", 
            ha='left', va='top', fontsize=8.5, color=TEXT_DARK, zorder=3)

    # Engine B: Constrained Recourse Optimizer
    draw_card(10.9, 0.9, 3.4, 3.2, "CONSTRAINED RECOURSE ENGINE", "L1-Norm MAD-Scaled Optimization", bg="#ffffff", border=GREEN, title_color=GREEN)
    ax.text(11.05, 3.25, "Objective: min Σ |Δ_j| / MAD_j + λ max(0, τ - P_calib)\nConstraints:\n  1. Δ_k = 0, for all k in F_immutable  (Demographic Lock)\n  2. l_j <= x_j + Δ_j <= u_j  (Feasibility Bounds)\nCase Study (Canonical At-Risk Profile):\n  • Initial Prob: 0.0%  -->  Target Achieved: 91.0%\n  • CGPA: +0.75 | Attendance: +18.5% | Certs: +2\n  • Gender / Caste / Income Invariance: Δ = 0", 
            ha='left', va='top', fontsize=8.2, color=TEXT_DARK, zorder=3)

    # Arrows from Stage 3 to SHAP & Recourse
    draw_arrow(10.1, 1.7, 10.9, 5.4, color=BLUE, rad=-0.2, lw=2)
    draw_arrow(10.1, 1.7, 10.9, 2.5, color=GREEN, rad=0.1, lw=2.5)

    # Save diagram
    out_path = os.path.join(OUT_DIR, "fig1_system_architecture.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor='#ffffff')
    plt.close()
    print(f"Generated Figure 1: {out_path} ({os.path.getsize(out_path):,} bytes)")

def create_methodology_flow_diagram():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    NAVY = "#0f172a"
    BLUE = "#1e40af"
    TEAL = "#0284c7"
    GREEN = "#059669"
    AMBER = "#d97706"
    RED = "#dc2626"
    CARD_BORDER = "#cbd5e1"
    TEXT_DARK = "#0f172a"
    TEXT_MUTED = "#475569"

    fig.patch.set_facecolor('#ffffff')

    ax.text(7.5, 8.15, "Figure 2: Proposed End-to-End Methodology & Execution Flowchart", 
            ha='center', va='center', fontsize=16, fontweight='bold', color=NAVY)
    ax.text(7.5, 7.82, "Fold-Isolated Out-of-Fold Protocol, Cascaded Sequential Inference, and Actionable Intervention Loop",
            ha='center', va='center', fontsize=11, color=TEXT_MUTED, style='italic')

    def draw_box(x, y, w, h, title, subtitle="", bg="#ffffff", border=CARD_BORDER, title_color=BLUE):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.12",
                             facecolor=bg, edgecolor=border, linewidth=1.5, zorder=2)
        ax.add_patch(box)
        if title:
            ax.text(x + w/2, y + h - 0.22, title, ha='center', va='top', fontsize=10.5, fontweight='bold', color=title_color, zorder=3)
        if subtitle:
            ax.text(x + w/2, y + h - 0.50, subtitle, ha='center', va='top', fontsize=8.5, color=TEXT_MUTED, zorder=3)

    def draw_arrow(x1, y1, x2, y2, color=BLUE, style="->", rad=0.0, lw=2.0, label=""):
        arr = FancyArrowPatch((x1, y1), (x2, y2),
                              connectionstyle=f"arc3,rad={rad}",
                              arrowstyle=style, mutation_scale=14,
                              color=color, linewidth=lw, zorder=4)
        ax.add_patch(arr)
        if label:
            mx, my = (x1 + x2)/2, (y1 + y2)/2 + 0.15
            ax.text(mx, my, label, ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=color, zorder=5)

    # -------------------------------------------------------------
    # PHASE 1: DATA INGESTION & ISOLATION (x=0.5, y=5.2, w=4.2, h=2.2)
    # -------------------------------------------------------------
    draw_box(0.5, 5.2, 4.2, 2.2, "PHASE 1: DATA INGESTION & SPLIT", "Leak-Free Partitioning & Cohort Verification", bg="#f8fafc", border=TEAL, title_color=TEAL)
    ax.text(0.7, 6.25, "• Synthetic Research Cohort (N = 4,000, 23 attributes)\n• Authentic Real Engineering Cohort (N = 2,966)\n• Stratified 80% Train (N=3,200) / 20% Held-Out Test (N=800)\n• Imputers, Encoders, Scalers fitted exclusively on Train", 
            ha='left', va='top', fontsize=8.5, color=TEXT_DARK, zorder=3)

    # -------------------------------------------------------------
    # PHASE 2: 5-FOLD STRATIFIED OOF GENERATION (x=5.4, y=5.2, w=4.2, h=2.2)
    # -------------------------------------------------------------
    draw_box(5.4, 5.2, 4.2, 2.2, "PHASE 2: 5-FOLD OOF PIPELINE", "Eliminating Cascading Exposure Bias", bg="#f8fafc", border=BLUE, title_color=BLUE)
    ax.text(5.6, 6.25, "• K-Fold Stratified Cross-Validation on Training Set\n• Fold k predicted using models trained on folds {1..5}\\k\n• Downstream stages trained on OOF predictions, NOT ground truth!\n• Guarantees training distribution matches test distribution", 
            ha='left', va='top', fontsize=8.5, color=TEXT_DARK, zorder=3)

    draw_arrow(4.7, 6.3, 5.4, 6.3, color=BLUE, label="Train Split")

    # -------------------------------------------------------------
    # PHASE 3: MODEL FITTING & PLATT SCALING (x=10.3, y=5.2, w=4.2, h=2.2)
    # -------------------------------------------------------------
    draw_box(10.3, 5.2, 4.2, 2.2, "PHASE 3: PLATT CALIBRATION", "Probabilistic Reliability Optimization", bg="#f8fafc", border=GREEN, title_color=GREEN)
    ax.text(10.5, 6.25, "• Stage 1: RF (Gini Impurity, 100 Trees)\n• Stage 2: Blended XGBoost (0.50) + GBDT (0.50)\n• Stage 3: Hybrid XGBoost (0.55) + RBF-SVM (0.45)\n• Platt Logistic Scaling: P(Y=1|z) = 1 / [1 + exp(Az + B)]", 
            ha='left', va='top', fontsize=8.5, color=TEXT_DARK, zorder=3)

    draw_arrow(9.6, 6.3, 10.3, 6.3, color=GREEN, label="OOF Features")

    # -------------------------------------------------------------
    # PHASE 4: PRODUCTION INFERENCE PIPELINE (x=0.5, y=1.2, w=5.2, h=3.4)
    # -------------------------------------------------------------
    draw_box(0.5, 1.2, 5.2, 3.4, "PHASE 4: LIVE INFERENCE PIPELINE", "Sequential Cascaded Evaluation (Zero Leakage)", bg="#f1f5f9", border=NAVY, title_color=NAVY)
    ax.text(0.7, 3.95, "Step 1: Input Pre-College Profile x^(pre)\nStep 2: Stage 1 Recommends Engineering Branch B_hat\nStep 3: Construct [x^(pre), x^(coll), B_hat] for Stage 2\nStep 4: Stage 2 Forecasts Academic Performance Tier A_hat\nStep 5: Construct [x_i, B_hat, A_hat] for Stage 3\nStep 6: Calculate Hybrid Logits & Platt-Calibrated Probability:\n           P_calib = 1 / [1 + exp(A*z_i + B)]\nTest Results: 98.8% Acc (Synth), 84.5% Acc (Real, N=2,966), AUC=0.936", 
            ha='left', va='top', fontsize=8.5, color=TEXT_DARK, zorder=3)

    # Arrow from Phase 3 to Phase 4
    draw_arrow(12.4, 5.2, 5.7, 2.9, color=NAVY, rad=0.2, label="Fitted Production Pipeline")

    # -------------------------------------------------------------
    # PHASE 5: DECISION GATE & RECOURSE LOOP (x=6.3, y=1.2, w=8.2, h=3.4)
    # -------------------------------------------------------------
    draw_box(6.3, 1.2, 8.2, 3.4, "PHASE 5: RECOURSE & INTERVENTION LOOP", "Constrained Optimization with Demographic Locks", bg="#f8fafc", border=AMBER, title_color=AMBER)

    # Decision diamond representation
    box_dec = FancyBboxPatch((6.6, 2.2), 2.2, 1.5, boxstyle="round,pad=0.08,rounding_size=0.1",
                             facecolor="#fef3c7", edgecolor=AMBER, linewidth=1.5, zorder=3)
    ax.add_patch(box_dec)
    ax.text(7.7, 3.1, "Risk Gate:\nP_calib >= 0.75?", ha='center', va='center', fontsize=9.5, fontweight='bold', color=AMBER, zorder=4)

    draw_arrow(5.7, 2.9, 6.6, 2.9, color=NAVY, label="P_calib")

    # Branch: YES -> Placed Confirmed
    box_yes = FancyBboxPatch((9.4, 3.1), 4.8, 1.1, boxstyle="round,pad=0.08,rounding_size=0.1",
                             facecolor="#ecfdf5", edgecolor=GREEN, linewidth=1.5, zorder=3)
    ax.add_patch(box_yes)
    ax.text(11.8, 3.8, "Target Satisfied: Placement Confirmed", ha='center', va='top', fontsize=9.5, fontweight='bold', color=GREEN, zorder=4)
    ax.text(11.8, 3.45, "• Calibrated P >= 75% | No remediation needed\n• SHAP waterfall generates positive feature explanation", ha='center', va='top', fontsize=8.2, color=TEXT_DARK, zorder=4)

    draw_arrow(8.8, 3.4, 9.4, 3.6, color=GREEN, label="YES (Placed)")

    # Branch: NO -> Recourse Optimization
    box_no = FancyBboxPatch((9.4, 1.4), 4.8, 1.5, boxstyle="round,pad=0.08,rounding_size=0.1",
                            facecolor="#fff1f2", edgecolor=RED, linewidth=1.5, zorder=3)
    ax.add_patch(box_no)
    ax.text(11.8, 2.65, "At-Risk Recourse Engine (Target τ = 0.85)", ha='center', va='top', fontsize=9.5, fontweight='bold', color=RED, zorder=4)
    ax.text(11.8, 2.30, "1. Optimize: min Σ |Δ_j| / MAD_j + λ max(0, τ - P_calib)\n2. Strict Demographic Lock: Δ_k = 0, for all k in F_imm\n3. Actionable Remediations: Attendance, CGPA, Certs\n4. Re-forecast verifies placement probability jumps to 91.0%", ha='center', va='top', fontsize=8.0, color=TEXT_DARK, zorder=4)

    draw_arrow(8.8, 2.4, 9.4, 2.1, color=RED, label="NO (At-Risk)")

    # Save diagram
    out_path = os.path.join(OUT_DIR, "fig2_proposed_methodology.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor='#ffffff')
    plt.close()
    print(f"Generated Figure 2: {out_path} ({os.path.getsize(out_path):,} bytes)")

if __name__ == "__main__":
    create_architecture_diagram()
    create_methodology_flow_diagram()
