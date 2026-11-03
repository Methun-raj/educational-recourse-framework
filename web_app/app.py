"""
Flask Web Application & Secure REST API for Educational Recourse Framework.
Implements robust request validation, security headers, rate limiting, and health checks.
"""

import os
import sys
import time
from collections import defaultdict
from typing import Dict, Any, Tuple

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify, send_from_directory, Response
from flask_cors import CORS
import pandas as pd
from pydantic import ValidationError

from src.config import (
    MODEL_DIR,
    EXPORT_DIR,
    DATASET_PATH,
    AppConfig,
    get_logger
)
from src.schemas import StudentProfileSchema
from src.pipeline import HierarchicalMultiStagePipeline

logger = get_logger(__name__)

# Initialize Flask app
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)
config = AppConfig()
app.config['SECRET_KEY'] = config.SECRET_KEY

# Configure Restrictive CORS
CORS(app, origins=config.ALLOWED_ORIGINS, supports_credentials=True)

# In-Memory Rate Limiter (Token Bucket per IP)
RATE_LIMIT_STORE: Dict[str, list] = defaultdict(list)
MAX_REQUESTS_PER_MINUTE = 60

def is_rate_limited(ip: str) -> bool:
    now = time.time()
    # Filter requests within past 60 seconds
    RATE_LIMIT_STORE[ip] = [t for t in RATE_LIMIT_STORE[ip] if now - t < 60]
    if len(RATE_LIMIT_STORE[ip]) >= MAX_REQUESTS_PER_MINUTE:
        return True
    RATE_LIMIT_STORE[ip].append(now)
    return False

# Security Headers Hook
@app.after_request
def apply_security_headers(response: Response) -> Response:
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
        "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        "img-src 'self' data: /exports/;"
    )
    return response

# Global Pipeline Instance
pipeline: HierarchicalMultiStagePipeline = None

def get_or_load_pipeline() -> HierarchicalMultiStagePipeline:
    global pipeline
    if pipeline is None:
        logger.info("Initializing global HierarchicalMultiStagePipeline instance")
        pipeline = HierarchicalMultiStagePipeline(random_state=42)
        stage3_file = os.path.join(MODEL_DIR, "stage3_model.joblib")

        if os.path.exists(stage3_file):
            pipeline.load_pipeline(MODEL_DIR)
        else:
            logger.info("Persisted models not found. Loading or generating dataset to train pipeline...")
            if not os.path.exists(DATASET_PATH):
                from data.generate_dataset import save_default_dataset
                df_data = save_default_dataset(DATASET_PATH)
            else:
                df_data = pd.read_csv(DATASET_PATH)
            pipeline.train(df_data)
            pipeline.save_pipeline(MODEL_DIR)

    return pipeline


# -------------------------------------------------------------
# Frontend View Routes
# -------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/benchmarks")
def benchmarks():
    return render_template("benchmark.html")


@app.route("/datasets")
def datasets_view():
    return render_template("datasets.html")


@app.route("/documentation")
def documentation():
    return render_template("documentation.html")


# -------------------------------------------------------------
# System & Health Check Endpoints
# -------------------------------------------------------------
@app.route("/health")
@app.route("/api/health")
def health_check():
    pipe_status = "ready" if (pipeline is not None and pipeline.is_trained) else "uninitialized"
    return jsonify({
        "status": "healthy",
        "pipeline_status": pipe_status,
        "timestamp": time.time(),
        "version": "1.0.0"
    }), 200


@app.route("/ready")
@app.route("/api/ready")
def readiness_check():
    try:
        pipe = get_or_load_pipeline()
        is_ready = pipe is not None and pipe.is_trained
        status_code = 200 if is_ready else 503
        return jsonify({
            "status": "ready" if is_ready else "not_ready",
            "models_loaded": is_ready,
            "timestamp": time.time()
        }), status_code
    except Exception as e:
        logger.error("Readiness check failure: %s", str(e))
        return jsonify({"status": "error", "error": "Pipeline unready"}), 503



# -------------------------------------------------------------
# Static Export Delivery with Path Traversal Protection
# -------------------------------------------------------------
ALLOWED_EXPORT_EXTENSIONS = {'.png', '.csv', '.json'}

@app.route("/exports/<path:filename>")
@app.route("/api/exports/<path:filename>")
def serve_exports(filename: str):
    # Sanitize and validate extension
    base_name = os.path.basename(filename)
    _, ext = os.path.splitext(base_name)
    if ext.lower() not in ALLOWED_EXPORT_EXTENSIONS or ".." in filename or base_name != filename:
        logger.warning("Blocked potential path traversal or disallowed export request: %s", filename)
        return jsonify({"error": "Invalid file request"}), 403

    safe_dir = os.path.abspath(EXPORT_DIR)
    return send_from_directory(safe_dir, base_name)


@app.route("/api/export")
def api_export_query():
    filename = request.args.get("file", "")
    if not filename:
        return jsonify({"error": "Missing 'file' query parameter"}), 400
    base_name = os.path.basename(filename)
    if base_name != filename or ".." in filename:
        logger.warning("Blocked path traversal attempt on /api/export: %s", filename)
        return jsonify({"error": "Path traversal prohibited"}), 400
    _, ext = os.path.splitext(base_name)
    if ext.lower() not in ALLOWED_EXPORT_EXTENSIONS:
        return jsonify({"error": "Invalid file extension"}), 403
    safe_dir = os.path.abspath(EXPORT_DIR)
    file_path = os.path.join(safe_dir, base_name)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    return send_from_directory(safe_dir, base_name)


# -------------------------------------------------------------
# REST API Endpoints
# -------------------------------------------------------------
def map_real_cohort_to_profile(row: pd.Series, student_idx: int = 1001) -> dict:
    """Maps a genuine student record from college_placement_real.csv into a validated StudentProfileSchema dictionary."""
    cgpa_val = float(row.get('CGPA', 6.5))
    stream_val = str(row.get('Stream', 'Computer Science'))
    backlogs = int(row.get('HistoryOfBacklogs', 0))
    internships = int(row.get('Internships', 0))
    gender_val = str(row.get('Gender', 'Male'))
    age_val = int(row.get('Age', 21))

    math_score = round(min(98.0, max(45.0, cgpa_val * 9.5 - (backlogs * 6.0) + (4.0 if 'Computer' in stream_val else 0.0))), 1)
    phys_score = round(min(96.0, max(45.0, cgpa_val * 9.2 - (backlogs * 5.0))), 1)
    chem_score = round(min(96.0, max(45.0, cgpa_val * 9.0 - (backlogs * 4.0))), 1)
    eng_score = round(min(95.0, max(50.0, 70.0 + (cgpa_val - 6.5) * 4.0)), 1)
    agg_score = round((math_score + phys_score + chem_score + eng_score) / 4.0, 1)

    attendance = round(min(98.0, max(55.0, 75.0 + (cgpa_val - 7.0) * 8.0 - (backlogs * 10.0))), 1)
    study_hrs = round(min(40.0, max(5.0, 14.0 + (cgpa_val - 6.5) * 5.0 - (backlogs * 3.0))), 1)
    soft_skills = round(min(5.0, max(1.5, 2.5 + (cgpa_val - 6.0) * 0.4 + (internships * 0.5))), 1)
    midterm = round(min(98.0, max(45.0, cgpa_val * 9.6 - (backlogs * 6.0))), 1)
    core_course = round(min(98.0, max(45.0, cgpa_val * 9.4 - (backlogs * 5.0))), 1)

    return {
        'student_id': f'REAL_STU_{student_idx:04d}',
        'age': int(min(28, max(18, age_val))),
        'gender': 'Male' if gender_val.lower().startswith('m') else 'Female',
        'family_income_bracket': 'Tier-3 Low' if backlogs > 0 or cgpa_val < 6.5 else 'Tier-2 Middle',
        'family_size': 4,
        'parental_education': 'High School' if cgpa_val < 6.5 else 'Bachelor',
        'parental_status': 'Married',
        'intermediate_math': math_score,
        'intermediate_physics': phys_score,
        'intermediate_chemistry': chem_score,
        'intermediate_english': eng_score,
        'intermediate_aggregate': agg_score,
        'attendance_percentage': attendance,
        'study_hours_per_week': study_hrs,
        'extracurricular_clubs': internships,
        'soft_skills_score': soft_skills,
        'certifications_count': internships,
        'midterm_score': midterm,
        'core_course_score': core_course,
        'cgpa': round(cgpa_val, 2),
        'recommended_branch': None,
        'academic_performance': None,
        'placement_status': None
    }


DATASET_REGISTRY = {
    "student_multimodal_dataset.csv": {
        "title": "Primary Hierarchical Multi-Modal Dataset",
        "path": DATASET_PATH,
        "type": "Synthetic Multi-Modal (Cascade Training)",
        "description": "2,500 comprehensive student records spanning admissions, academic trajectory, and campus placement with socio-demographic features.",
        "target": "placement_status"
    },
    "college_placement_real.csv": {
        "title": "Engineering College Placement Real Dataset",
        "path": os.path.join(os.path.dirname(DATASET_PATH), "original_benchmarks", "college_placement_real.csv"),
        "type": "Authentic Institutional Cohort (N=2,966)",
        "description": "2,966 authentic undergraduate engineering students across CSE, IT, ECE, EEE, Mechanical, and Civil streams with CGPA, internships, backlogs, and placement outcomes.",
        "target": "PlacedOrNot"
    },
    "campus_recruitment_real.csv": {
        "title": "Campus Recruitment Academic Dataset",
        "path": os.path.join(os.path.dirname(DATASET_PATH), "original_benchmarks", "campus_recruitment_real.csv"),
        "type": "Authentic Academic Dataset (N=215)",
        "description": "215 students with 10th, 12th, undergraduate degree percentages, employability test marks, and placement status.",
        "target": "status"
    },
    "uci_student_performance_real.csv": {
        "title": "UCI Student Academic Performance Dataset",
        "path": os.path.join(os.path.dirname(DATASET_PATH), "original_benchmarks", "uci_student_performance_real.csv"),
        "type": "Authentic Benchmark (Cortez & Silva, 2008)",
        "description": "395 student records evaluating socio-demographics, study time, alcohol consumption, absences, and longitudinal exam marks (G1, G2, G3).",
        "target": "G3"
    },
    "user_integrated_students.csv": {
        "title": "User-Integrated Student Cohort",
        "path": os.path.join(os.path.dirname(DATASET_PATH), "user_integrated_students.csv"),
        "type": "User-Supplied & Custom Data Integration",
        "description": "Student records dynamically contributed and integrated by users, validated against Pydantic contracts and evaluated across the cascade.",
        "target": "placement_status"
    }
}


@app.route("/api/datasets/integrate", methods=["POST"])
def integrate_user_data():
    """
    Accepts user-supplied student details, validates against Pydantic schema,
    generates hierarchical predictions for missing intermediate labels,
    and integrates the validated record into user_integrated_students.csv.
    """
    user_csv_path = os.path.join(os.path.dirname(DATASET_PATH), "user_integrated_students.csv")

    # Check if multipart form upload with CSV file
    if request.files and 'file' in request.files:
        uploaded_file = request.files['file']
        if not uploaded_file.filename.endswith('.csv'):
            return jsonify({'success': False, 'error': 'Uploaded file must be a CSV file (.csv)'}), 400

        try:
            df_uploaded = pd.read_csv(uploaded_file)
            pipe = get_or_load_pipeline()
            integrated_count = 0
            validated_rows = []

            for _, raw_row in df_uploaded.iterrows():
                row_dict = raw_row.dropna().to_dict()
                try:
                    profile = StudentProfileSchema(**row_dict)
                    flat = profile.to_flat_dict()
                    if flat.get('recommended_branch') is None or flat.get('placement_status') is None:
                        pred_res = pipe.predict_student(flat)
                        flat['recommended_branch'] = pred_res['stage1']['recommended_branch']
                        flat['academic_performance'] = pred_res['stage2']['forecasted_academic_tier']
                        flat['placement_status'] = 1 if pred_res['stage3']['placement_prediction'] == 'Placed' else 0
                    if not flat.get('student_id') or flat.get('student_id') == 'STU_QUERY':
                        flat['student_id'] = f"USER_STU_{int(time.time()*1000)%1000000:06d}"
                    validated_rows.append(flat)
                    integrated_count += 1
                except ValidationError:
                    continue

            if not validated_rows:
                return jsonify({'success': False, 'error': 'No rows in uploaded CSV conformed to the student schema'}), 422

            df_new = pd.DataFrame(validated_rows)
            if os.path.exists(user_csv_path):
                df_existing = pd.read_csv(user_csv_path)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True).drop_duplicates(subset=['student_id'], keep='last')
            else:
                df_combined = df_new

            df_combined.to_csv(user_csv_path, index=False)
            return jsonify({
                'success': True,
                'message': f'Successfully validated and integrated {integrated_count} student records from CSV.',
                'integrated_count': integrated_count,
                'total_user_records': len(df_combined)
            }), 200
        except Exception as e:
            logger.error("Error processing uploaded dataset: %s", str(e))
            return jsonify({'success': False, 'error': f'Failed to parse uploaded CSV: {str(e)}'}), 400

    # JSON payload input
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Request payload must be JSON or multipart CSV file'}), 400

    try:
        raw_json = request.get_json()
        validated_profile = StudentProfileSchema(**raw_json)
        data_dict = validated_profile.to_flat_dict()
        pipe = get_or_load_pipeline()

        # Run cascaded prediction if targets are not provided
        pred_res = pipe.predict_student(data_dict)
        if data_dict.get('recommended_branch') is None:
            data_dict['recommended_branch'] = pred_res['stage1']['recommended_branch']
        if data_dict.get('academic_performance') is None:
            data_dict['academic_performance'] = pred_res['stage2']['forecasted_academic_tier']
        if data_dict.get('placement_status') is None:
            data_dict['placement_status'] = 1 if pred_res['stage3']['placement_prediction'] == 'Placed' else 0

        # Generate unique ID if needed
        if not data_dict.get('student_id') or data_dict.get('student_id') == 'STU_QUERY':
            if os.path.exists(user_csv_path):
                cur_len = sum(1 for _ in open(user_csv_path, encoding='utf-8'))
            else:
                cur_len = 1
            data_dict['student_id'] = f'USER_STU_{cur_len:04d}'

        # Append to user_integrated_students.csv
        df_row = pd.DataFrame([data_dict])
        if os.path.exists(user_csv_path):
            df_row.to_csv(user_csv_path, mode='a', header=False, index=False)
            total_records = sum(1 for _ in open(user_csv_path, encoding='utf-8')) - 1
        else:
            df_row.to_csv(user_csv_path, mode='w', header=True, index=False)
            total_records = 1

        return jsonify({
            'success': True,
            'message': 'Student profile successfully validated and integrated into custom dataset.',
            'student_id': data_dict['student_id'],
            'predictions': {
                'recommended_branch': data_dict['recommended_branch'],
                'academic_performance': data_dict['academic_performance'],
                'placement_status': 'Placed' if data_dict['placement_status'] == 1 else 'Not Placed',
                'placement_probability': round(pred_res['stage3']['placement_probability'], 4)
            },
            'integrated_record': data_dict,
            'total_user_records': total_records
        }), 201

    except ValidationError as ve:
        logger.warning("User data integration validation error: %s", str(ve))
        return jsonify({'success': False, 'error': 'Validation Error', 'details': ve.errors()}), 422
    except Exception as e:
        logger.exception("Error integrating user student data: %s", str(e))
        return jsonify({'success': False, 'error': f'Integration failed: {str(e)}'}), 500


@app.route("/api/datasets")
def list_datasets():
    """Returns summary metadata and schema for all integrated datasets."""
    results = []
    for filename, info in DATASET_REGISTRY.items():
        if os.path.exists(info["path"]):
            df_sample = pd.read_csv(info["path"], nrows=5)
            row_count = sum(1 for _ in open(info["path"], encoding="utf-8")) - 1
            results.append({
                "id": filename,
                "title": info["title"],
                "type": info["type"],
                "description": info["description"],
                "target": info["target"],
                "row_count": row_count,
                "column_count": len(df_sample.columns),
                "columns": df_sample.columns.tolist()
            })
    return jsonify({"success": True, "datasets": results})


@app.route("/api/datasets/<dataset_name>")
def get_dataset_records(dataset_name: str):
    """Returns paginated preview rows for an integrated dataset."""
    safe_name = os.path.basename(dataset_name)
    if safe_name not in DATASET_REGISTRY:
        return jsonify({"success": False, "error": "Dataset not found"}), 404

    info = DATASET_REGISTRY[safe_name]
    if not os.path.exists(info["path"]):
        return jsonify({"success": False, "error": "Dataset file missing"}), 404

    try:
        limit = min(int(request.args.get("limit", 15)), 100)
        offset = max(int(request.args.get("offset", 0)), 0)
        df = pd.read_csv(info["path"])
        total_rows = len(df)
        records = df.iloc[offset:offset+limit].fillna("").to_dict(orient="records")
        return jsonify({
            "success": True,
            "dataset": safe_name,
            "title": info["title"],
            "total_rows": total_rows,
            "columns": df.columns.tolist(),
            "records": records,
            "limit": limit,
            "offset": offset
        })
    except Exception as e:
        logger.error("Error reading dataset %s: %s", safe_name, str(e))
        return jsonify({"success": False, "error": "Error reading dataset"}), 500


@app.route("/api/datasets/<dataset_name>/download")
def download_dataset(dataset_name: str):
    """Secure direct download of integrated dataset files."""
    safe_name = os.path.basename(dataset_name)
    if safe_name not in DATASET_REGISTRY:
        return jsonify({"success": False, "error": "Disallowed dataset"}), 404
    info = DATASET_REGISTRY[safe_name]
    directory = os.path.dirname(info["path"])
    return send_from_directory(directory, safe_name, as_attachment=True)


@app.route("/api/sample/<sample_type>")
def get_sample_profile(sample_type: str):
    """Returns validated preset student profiles from presets, authentic cohorts, or user-integrated data."""
    if sample_type in ["user_student", "user_integrated"]:
        user_csv = os.path.join(os.path.dirname(DATASET_PATH), "user_integrated_students.csv")
        if os.path.exists(user_csv):
            df_user = pd.read_csv(user_csv)
            if len(df_user) > 0:
                row = df_user.iloc[-1].dropna().to_dict()
                try:
                    profile = StudentProfileSchema(**row)
                    return jsonify(profile.to_flat_dict())
                except Exception:
                    pass
        return get_sample_profile("at_risk")

    if sample_type in ["real_student", "real_at_risk", "real_student_at_risk", "real_placed", "real_student_placed"]:
        real_csv = os.path.join(os.path.dirname(DATASET_PATH), "original_benchmarks", "college_placement_real.csv")
        if os.path.exists(real_csv):
            df_real = pd.read_csv(real_csv)
            if sample_type in ["real_at_risk", "real_student_at_risk"]:
                subset = df_real[(df_real['PlacedOrNot'] == 0) & (df_real['HistoryOfBacklogs'] == 1)]
                chosen_row = subset.sample(n=1, random_state=42).iloc[0] if len(subset) > 0 else df_real.iloc[0]
            elif sample_type in ["real_placed", "real_student_placed"]:
                subset = df_real[(df_real['PlacedOrNot'] == 1) & (df_real['CGPA'] >= 8.0)]
                chosen_row = subset.sample(n=1, random_state=42).iloc[0] if len(subset) > 0 else df_real.iloc[0]
            else:
                chosen_row = df_real.sample(n=1, random_state=42).iloc[0]
            return jsonify(map_real_cohort_to_profile(chosen_row))
        else:
            return get_sample_profile("at_risk")

    if sample_type == "at_risk":
        sample = {
            'student_id': 'STU_1000',
            'age': 20,
            'gender': 'Male',
            'family_income_bracket': 'Tier-3 Low',
            'family_size': 5,
            'parental_education': 'High School',
            'parental_status': 'Married',
            'intermediate_math': 62.0,
            'intermediate_physics': 59.0,
            'intermediate_chemistry': 60.0,
            'intermediate_english': 58.0,
            'intermediate_aggregate': 59.8,
            'attendance_percentage': 64.0,
            'study_hours_per_week': 8.0,
            'extracurricular_clubs': 0,
            'soft_skills_score': 2.0,
            'certifications_count': 0,
            'midterm_score': 60.5,
            'core_course_score': 58.0,
            'cgpa': 6.40
        }
    elif sample_type == "high_achiever":
        sample = {
            'student_id': 'STU_9999',
            'age': 20,
            'gender': 'Female',
            'family_income_bracket': 'Tier-1 High',
            'family_size': 4,
            'parental_education': 'Master',
            'parental_status': 'Married',
            'intermediate_math': 94.0,
            'intermediate_physics': 90.0,
            'intermediate_chemistry': 88.0,
            'intermediate_english': 92.0,
            'intermediate_aggregate': 91.2,
            'attendance_percentage': 94.0,
            'study_hours_per_week': 28.0,
            'extracurricular_clubs': 3,
            'soft_skills_score': 4.6,
            'certifications_count': 3,
            'midterm_score': 92.0,
            'core_course_score': 91.5,
            'cgpa': 9.25
        }
    else:  # balanced
        sample = {
            'student_id': 'STU_5555',
            'age': 21,
            'gender': 'Male',
            'family_income_bracket': 'Tier-2 Middle',
            'family_size': 4,
            'parental_education': 'Bachelor',
            'parental_status': 'Married',
            'intermediate_math': 78.0,
            'intermediate_physics': 75.0,
            'intermediate_chemistry': 72.0,
            'intermediate_english': 76.0,
            'intermediate_aggregate': 75.3,
            'attendance_percentage': 82.0,
            'study_hours_per_week': 18.0,
            'extracurricular_clubs': 1,
            'soft_skills_score': 3.4,
            'certifications_count': 1,
            'midterm_score': 77.0,
            'core_course_score': 76.0,
            'cgpa': 7.60
        }
    return jsonify(sample)


@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Executes 3-Stage Cascaded Inference, SHAP Waterfall, and Constrained Recourse.
    Enforces strict Pydantic schema validation and rate limiting.
    """
    client_ip = request.remote_addr or "127.0.0.1"
    if is_rate_limited(client_ip):
        logger.warning("Rate limit exceeded for IP: %s", client_ip)
        return jsonify({
            'success': False,
            'error': 'Rate limit exceeded. Maximum 60 requests per minute allowed.'
        }), 429

    if not request.is_json:
        return jsonify({
            'success': False,
            'error': 'Request payload must be application/json'
        }), 400

    try:
        # Validate payload against Pydantic Schema
        raw_json = request.get_json()
        validated_profile = StudentProfileSchema(**raw_json)
        data_dict = validated_profile.to_flat_dict()

        pipe = get_or_load_pipeline()
        result = pipe.predict_student(data_dict)

        # Generate Constrained Counterfactual Recourse
        df_row = pd.Series(data_dict)
        recourse = pipe.recourse_engine.generate_recourse(df_row)

        # Parse local SHAP for frontend visualization
        shap_records = []
        if 'local_shap' in result and result['local_shap'] is not None:
            top_shap = result['local_shap'].head(8)
            for _, r in top_shap.iterrows():
                shap_records.append({
                    'feature': str(r['feature']),
                    'value': round(float(r['feature_value']), 2),
                    'shap_value': round(float(r['shap_value']), 4),
                    'abs_shap': round(float(r['abs_shap']), 4)
                })

        response_payload = {
            'stage1': result['stage1'],
            'stage2': result['stage2'],
            'stage3': result['stage3'],
            'shap_attribution': shap_records,
            'recourse': {
                'baseline_probability': round(recourse['baseline_probability'], 4),
                'target_probability': round(recourse['target_probability'], 4),
                'delta_probability': round(recourse['delta_probability'], 4),
                'optimization_success': recourse.get('optimization_success', True),
                'interventions': recourse['interventions'],
                'counterfactual_profile': recourse['counterfactual_profile'],
                'disclaimer': recourse.get('disclaimer', '')
            }
        }
        return jsonify({'success': True, 'data': response_payload}), 200

    except ValidationError as ve:
        logger.warning("Input validation error: %s", str(ve))
        return jsonify({
            'success': False,
            'error': 'Validation Error',
            'details': ve.errors()
        }), 422
    except Exception as e:
        logger.exception("Unexpected server error during prediction pipeline execution: %s", str(e))
        return jsonify({
            'success': False,
            'error': 'Internal pipeline error occurred. Please verify inputs.'
        }), 500


@app.route("/api/benchmarks")
def get_benchmarks_data():
    """Returns evaluated tables from exported CSVs."""
    tables = {}
    csv_map = {
        'table_1': "table_1_literature_synthesis.csv",
        'table_2': "table_2_baseline_comparison.csv",
        'table_3': "table_3_task_specific_performance.csv",
        'table_4': "table_4_feature_ablation.csv",
        'table_5': "table_5_counterfactual_intervention.csv",
        'table_real_world': "table_real_world_benchmarks.csv"
    }

    for key, filename in csv_map.items():
        path = os.path.join(EXPORT_DIR, filename)
        if os.path.exists(path):
            df = pd.read_csv(path)
            tables[key] = df.to_dict(orient='records')
        else:
            tables[key] = []

    return jsonify({'success': True, 'tables': tables}), 200


if __name__ == "__main__":
    get_or_load_pipeline()
    logger.info("Starting production Flask web server on http://%s:%d ...", config.HOST, config.PORT)
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
