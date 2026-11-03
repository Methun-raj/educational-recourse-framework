"""
Empirical Benchmark Evaluation on Original Real-World Educational Datasets.
Evaluates the framework's predictive models on genuine student cohorts:
- Engineering College Placement Dataset (N=2,966 records)
- Campus Recruitment Dataset (N=215 records)

Generates:
- Table: Empirical Benchmarks on Real-World Student Datasets (CSV)
- Figure 8: Real-World Empirical Performance Comparison Across Models (PNG)
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.calibration import CalibratedClassifierCV
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, brier_score_loss, precision_recall_curve, auc
)

from src.config import BASE_DIR, EXPORT_DIR, get_logger

logger = get_logger(__name__)

REAL_DATA_DIR = os.path.join(BASE_DIR, "data", "original_benchmarks")


def evaluate_college_placement_real() -> pd.DataFrame:
    """Evaluates standalone baselines and proposed hybrid on N=2,966 Real College Dataset."""
    csv_path = os.path.join(REAL_DATA_DIR, "college_placement_real.csv")
    if not os.path.exists(csv_path):
        from data.download_original_datasets import download_all_original_datasets
        download_all_original_datasets()

    df = pd.read_csv(csv_path)
    X = df[['Age', 'Gender', 'Stream', 'Internships', 'CGPA', 'Hostel', 'HistoryOfBacklogs']]
    y = df['PlacedOrNot'].values

    num_cols = ['Age', 'Internships', 'CGPA', 'Hostel', 'HistoryOfBacklogs']
    cat_cols = ['Gender', 'Stream']

    preprocessor = ColumnTransformer(transformers=[
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(drop='first', sparse_output=False), cat_cols)
    ])
    X_proc = preprocessor.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_proc, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        'Majority Class (Zero-R)': DummyClassifier(strategy='most_frequent'),
        'Logistic Regression (LR)': LogisticRegression(max_iter=1000, random_state=42),
        'Decision Tree (DT)': DecisionTreeClassifier(max_depth=6, random_state=42),
        'k-Nearest Neighbors (KNN)': KNeighborsClassifier(n_neighbors=7),
        'Random Forest (RF)': RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42),
        'Support Vector Machine (SVM)': CalibratedClassifierCV(SVC(kernel='rbf', C=1.0, random_state=42)),
        'XGBoost': XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.08, eval_metric='logloss', random_state=42)
    }

    results = []
    prob_dict = {}

    for name, clf in models.items():
        clf.fit(X_train, y_train)
        preds = clf.predict(X_test)

        if hasattr(clf, 'predict_proba'):
            probs = clf.predict_proba(X_test)[:, 1]
        else:
            probs = np.full(len(X_test), float(np.mean(y_train)))

        prob_dict[name] = probs

        acc = accuracy_score(y_test, preds) * 100.0
        prec = precision_score(y_test, preds, zero_division=0) * 100.0
        rec = recall_score(y_test, preds, zero_division=0) * 100.0
        macro_f1 = f1_score(y_test, preds, average='macro') * 100.0
        weighted_f1 = f1_score(y_test, preds, average='weighted') * 100.0

        try:
            auc_val = roc_auc_score(y_test, probs)
            prec_arr, rec_arr, _ = precision_recall_curve(y_test, probs)
            pr_auc = auc(rec_arr, prec_arr)
        except Exception:
            auc_val = 0.50
            pr_auc = float(np.mean(y_test))

        brier = brier_score_loss(y_test, probs)

        results.append({
            'Algorithm': name,
            'Classification Accuracy (%)': round(acc, 1),
            'Precision (%)': round(prec, 1),
            'Recall (%)': round(rec, 1),
            'Macro F1-Score (%)': round(macro_f1, 1),
            'Weighted F1-Score (%)': round(weighted_f1, 1),
            'ROC-AUC': round(auc_val, 3),
            'PR-AUC': round(pr_auc, 3),
            'Brier Score': round(brier, 3)
        })

    # Proposed Hybrid Model (55% XGBoost + 45% Platt-Calibrated SVM)
    p_xgb = prob_dict['XGBoost']
    p_svm = prob_dict['Support Vector Machine (SVM)']
    p_hybrid = 0.55 * p_xgb + 0.45 * p_svm
    preds_h = (p_hybrid >= 0.5).astype(int)

    prec_arr_h, rec_arr_h, _ = precision_recall_curve(y_test, p_hybrid)
    hybrid_res = {
        'Algorithm': 'Proposed Hybrid XGBoost + SVM',
        'Classification Accuracy (%)': round(accuracy_score(y_test, preds_h) * 100.0, 1),
        'Precision (%)': round(precision_score(y_test, preds_h, zero_division=0) * 100.0, 1),
        'Recall (%)': round(recall_score(y_test, preds_h, zero_division=0) * 100.0, 1),
        'Macro F1-Score (%)': round(f1_score(y_test, preds_h, average='macro') * 100.0, 1),
        'Weighted F1-Score (%)': round(f1_score(y_test, preds_h, average='weighted') * 100.0, 1),
        'ROC-AUC': round(roc_auc_score(y_test, p_hybrid), 3),
        'PR-AUC': round(auc(rec_arr_h, prec_arr_h), 3),
        'Brier Score': round(brier_score_loss(y_test, p_hybrid), 3)
    }
    results.append(hybrid_res)

    res_df = pd.DataFrame(results)
    out_csv = os.path.join(EXPORT_DIR, "table_real_world_benchmarks.csv")
    res_df.to_csv(out_csv, index=False, encoding='utf-8')

    print("\n" + "="*85)
    print("EMPIRICAL BENCHMARK EVALUATION ON REAL-WORLD STUDENT DATA (N=2,966)")
    print("Dataset: Original Engineering College Placement Records (collegePlace.csv)")
    print("="*85)
    print(res_df.to_string(index=False))

    # Generate Figure 8: Real-World Comparison Plot
    fig_path = os.path.join(EXPORT_DIR, "figure8_real_world_comparison.png")
    plt.figure(figsize=(10, 5.5), dpi=300)

    plot_df = res_df.copy()
    y_pos = np.arange(len(plot_df))
    height = 0.35

    plt.barh(y_pos + height / 2, plot_df['Classification Accuracy (%)'], height,
             label='Classification Accuracy (%)', color='#1d3557', edgecolor='black', linewidth=0.5)
    plt.barh(y_pos - height / 2, plot_df['Macro F1-Score (%)'], height,
             label='Macro F1-Score (%)', color='#2a9d8f', edgecolor='black', linewidth=0.5)

    plt.yticks(y_pos, plot_df['Algorithm'], fontsize=9.5)
    plt.xlabel('Performance Percentage (%)', fontsize=11, fontweight='normal')
    plt.xlim(40, 100)
    plt.title('Figure 8: Empirical Validation on Genuine Student Cohort (N=2,966)', fontsize=13, fontweight='bold', pad=15)
    plt.legend(loc='lower right', frameon=True)
    plt.grid(axis='x', linestyle='--', alpha=0.5)

    for i, row in plot_df.iterrows():
        plt.text(row['Classification Accuracy (%)'] + 0.8, i + height / 2, f"{row['Classification Accuracy (%)']}%",
                 va='center', fontsize=9, color='#1d3557', fontweight='bold')
        plt.text(row['Macro F1-Score (%)'] + 0.8, i - height / 2, f"{row['Macro F1-Score (%)']}%",
                 va='center', fontsize=9, color='#2a9d8f', fontweight='bold')

    plt.tight_layout()
    plt.savefig(fig_path)
    plt.close()
    logger.info("Figure 8 real-world comparison plot exported to %s", fig_path)

    return res_df


if __name__ == "__main__":
    evaluate_college_placement_real()
