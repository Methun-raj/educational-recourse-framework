"""
Unified Runner & CLI Interface.
Based on: "Machine Learning-Based Forecasting of Student Academic Success, Branch Recommendation,
and Career Placement: A Hierarchical Multi-Task and Explainable Recourse Framework"

Usage:
    python run_project.py --generate-data    # Generate synthetic multi-modal dataset
    python run_project.py --train            # Train and persist full 3-stage pipeline
    python run_project.py --benchmark        # Replicate Tables I-V and Figures 1-3
    python run_project.py --predict-sample   # Run prediction & recourse on at-risk student
    python run_project.py --serve            # Start interactive Flask web dashboard
    python run_project.py --all              # Execute data gen, training, benchmark & launch
"""

import os
import sys
import argparse
import pandas as pd

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.config import DATASET_PATH, MODEL_DIR, get_logger
from data.generate_dataset import save_default_dataset
from src.pipeline import HierarchicalMultiStagePipeline
from evaluation.reproduce_benchmarks import run_all_benchmarks

logger = get_logger("run_project")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Hierarchical Multi-Task & Explainable Educational Recourse Framework"
    )
    parser.add_argument("--generate-data", action="store_true", help="Generate 2,500 sample multi-modal dataset")
    parser.add_argument("--download-real-data", action="store_true", help="Download original real-world student datasets")
    parser.add_argument("--evaluate-real-data", action="store_true", help="Evaluate models on genuine student datasets")
    parser.add_argument("--inspect-datasets", action="store_true", help="Display summary statistics for all integrated datasets")
    parser.add_argument("--train", action="store_true", help="Train 3-stage pipeline models")
    parser.add_argument("--benchmark", action="store_true", help="Replicate paper Tables I-V and Figures 1-7")
    parser.add_argument("--predict-sample", type=str, default=None,
                        choices=['at_risk', 'balanced', 'high_achiever', 'real_at_risk', 'real_placed', 'real_student'],
                        help="Predict and generate recourse for a student preset or real cohort record")
    parser.add_argument("--serve", action="store_true", help="Launch interactive web application")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 5000)), help="Web application port (default 5000 or $PORT)")
    parser.add_argument("--all", action="store_true", help="Run full pipeline: verify data, train, benchmark, evaluate real cohort, and serve")
    return parser.parse_args()


def main():
    args = parse_args()

    if not (args.generate_data or args.train or args.benchmark or args.predict_sample or args.serve or args.all or args.download_real_data or args.evaluate_real_data or args.inspect_datasets):
        print("\n[+] No command specified. Running paper benchmarks by default...")
        args.benchmark = True

    if args.inspect_datasets:
        print("\n" + "="*80)
        print("[*] Inspecting Integrated Educational Datasets Registry")
        print("="*80)
        from web_app.app import DATASET_REGISTRY
        for fname, meta in DATASET_REGISTRY.items():
            exists = os.path.exists(meta["path"])
            status = "AVAILABLE" if exists else "NOT DOWNLOADED"
            print(f"\n[+] Dataset: {fname} [{status}]")
            print(f"    Title: {meta['title']}")
            print(f"    Type: {meta['type']}")
            print(f"    Target: {meta['target']}")
            print(f"    Path: {meta['path']}")
            if exists:
                df_temp = pd.read_csv(meta["path"])
                print(f"    Records: {len(df_temp):,} rows, {len(df_temp.columns)} columns")
                print(f"    Columns: {', '.join(df_temp.columns[:8])}...")

    if args.download_real_data:
        print("\n" + "="*80)
        print("[*] Downloading Original Real-World Educational Benchmark Datasets")
        print("="*80)
        from data.download_original_datasets import download_all_original_datasets
        download_all_original_datasets()

    if args.evaluate_real_data:
        print("\n" + "="*80)
        print("[*] Evaluating Predictive Framework on Real-World Student Cohorts")
        print("="*80)
        from evaluation.evaluate_real_world import evaluate_college_placement_real
        evaluate_college_placement_real()

    if args.all or args.generate_data:
        print("\n" + "="*80)
        print("[1/4] Generating Multi-Modal Student Dataset (Academic + Socio-Economic + Behavioral)")
        print("="*80)
        save_default_dataset(DATASET_PATH)

    if args.all or args.train:
        print("\n" + "="*80)
        print("[2/4] Training Hierarchical Multi-Stage Pipeline (RF -> XGB+GB -> Hybrid XGB+SVM)")
        print("="*80)
        df = pd.read_csv(DATASET_PATH)
        pipe = HierarchicalMultiStagePipeline(random_state=42)
        eval_res = pipe.train(df)
        pipe.save_pipeline(MODEL_DIR)
        print("[+] Stage 1 (Branch Recommender RF) Cascaded Test Accuracy: {:.1f}%".format(eval_res['stage1']['accuracy']*100))
        print("[+] Stage 2 (Academic Forecaster XGB+GB) Cascaded Test Accuracy: {:.1f}%".format(eval_res['stage2']['accuracy']*100))
        print("[+] Stage 3 (Campus Placement Hybrid) Cascaded Test Accuracy: {:.1f}%".format(eval_res['stage3']['accuracy']*100))

    if args.all or args.benchmark:
        print("\n" + "="*80)
        print("[3/5] Reproducing Research Paper Benchmarks (Tables I - V & Figures 1 - 7)")
        print("="*80)
        run_all_benchmarks()

    if args.all:
        print("\n" + "="*80)
        print("[4/5] Evaluating Predictive Framework on Real-World Student Cohorts (Figure 8 & Table VI)")
        print("="*80)
        from evaluation.evaluate_real_world import evaluate_college_placement_real
        evaluate_college_placement_real()

    if args.predict_sample:
        print("\n" + "="*80)
        print(f"Executing Prediction & Counterfactual Recourse for Sample: '{args.predict_sample}'")
        print("="*80)
        from web_app.app import app, get_sample_profile
        with app.test_request_context():
            sample_dict = get_sample_profile(args.predict_sample).json

        pipe = HierarchicalMultiStagePipeline(random_state=42)
        pipe.load_pipeline(MODEL_DIR)
        result = pipe.predict_student(sample_dict)
        recourse = pipe.recourse_engine.generate_recourse(pd.Series(sample_dict))

        print(f"\n[*] Stage 1 Recommended Branch: {result['stage1']['recommended_branch']}")
        print(f"[*] Stage 2 Forecasted Academic Tier: {result['stage2']['forecasted_academic_tier']}")
        print(f"[*] Stage 3 Campus Placement Decision: {result['stage3']['placement_prediction']} (Prob: {result['stage3']['placement_probability']:.1%})")
        print("\n[*] Counterfactual Recourse Trajectory:")
        print(f"    Baseline Expectation: 68.0%")
        print(f"    Current At-Risk Probability: {recourse['baseline_probability']:.1%}")
        print(f"    Target Achieved Probability: {recourse['target_probability']:.1%}")
        print("\n[*] Recommended Actions:")
        for action in recourse['interventions']:
            print(f"    - {action['Feature Name']} ({action['Current Value']} -> {action['Counterfactual Target (x_i*)']}): {action['Actionable Recommendation']}")

    if args.all or args.serve:
        print("\n" + "="*80)
        print(f"[5/5] Launching Interactive Web Dashboard on http://127.0.0.1:{args.port}")
        print("="*80)
        from web_app.app import app, get_or_load_pipeline
        get_or_load_pipeline()
        app.run(host="0.0.0.0", port=args.port, debug=False)


if __name__ == "__main__":
    main()
