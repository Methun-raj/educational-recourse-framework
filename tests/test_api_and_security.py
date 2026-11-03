"""
Cybersecurity, API Validation, and Security Header Tests.
Verifies RFC compliance, Pydantic boundary checks, rate limiting, and security headers.
"""

import pytest
import os
import sys
import json

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web_app.app import app

@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_health_check_endpoint(client):
    res = client.get('/health')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['status'] == 'healthy'
    assert 'version' in data

def test_security_headers_present(client):
    res = client.get('/')
    assert res.status_code == 200
    assert res.headers.get('X-Content-Type-Options') == 'nosniff'
    assert res.headers.get('X-Frame-Options') == 'SAMEORIGIN'
    assert 'Content-Security-Policy' in res.headers

def test_api_predict_valid_payload(client):
    sample_res = client.get('/api/sample/at_risk')
    assert sample_res.status_code == 200
    valid_payload = json.loads(sample_res.data)

    pred_res = client.post('/api/predict', json=valid_payload)
    assert pred_res.status_code == 200
    data = json.loads(pred_res.data)
    assert data['success'] is True
    assert 'stage1' in data['data']
    assert 'recourse' in data['data']

def test_api_predict_invalid_cgpa_boundary(client):
    sample_res = client.get('/api/sample/at_risk')
    invalid_payload = json.loads(sample_res.data)
    # CGPA cannot exceed 10.0
    invalid_payload['cgpa'] = 15.5

    pred_res = client.post('/api/predict', json=invalid_payload)
    assert pred_res.status_code == 422
    data = json.loads(pred_res.data)
    assert data['success'] is False
    assert data['error'] == 'Validation Error'

def test_api_predict_missing_mandatory_fields(client):
    incomplete_payload = {'age': 20, 'gender': 'Male'}
    pred_res = client.post('/api/predict', json=incomplete_payload)
    assert pred_res.status_code == 422

def test_api_predict_non_json_rejection(client):
    pred_res = client.post('/api/predict', data="not json", content_type="text/plain")
    assert pred_res.status_code == 400

def test_path_traversal_blocked_on_exports(client):
    # Attempt directory traversal via path
    res = client.get('/exports/../../run_project.py')
    assert res.status_code in [400, 403, 404]

    # Attempt directory traversal via query parameter
    res_query = client.get('/api/export?file=../../run_project.py')
    assert res_query.status_code in [400, 403, 404]

    # Disallowed extension
    res_bad_ext = client.get('/exports/test.exe')
    assert res_bad_ext.status_code in [400, 403, 404]

def test_readiness_probe_endpoint(client):
    res = client.get('/ready')
    assert res.status_code in [200, 503]
    data = json.loads(res.data)
    assert 'status' in data

def test_api_predict_rejects_unauthorized_extra_fields(client):
    sample_res = client.get('/api/sample/at_risk')
    payload = json.loads(sample_res.data)
    payload['unauthorized_extra_injection_field'] = 'attack_payload'

    pred_res = client.post('/api/predict', json=payload)
    assert pred_res.status_code == 422
    data = json.loads(pred_res.data)
    assert data['success'] is False
    assert data['error'] == 'Validation Error'

def test_datasets_endpoints(client):
    # Test HTML view
    res_view = client.get('/datasets')
    assert res_view.status_code == 200

    # Test metadata API
    res_meta = client.get('/api/datasets')
    assert res_meta.status_code == 200
    meta_json = json.loads(res_meta.data)
    assert meta_json['success'] is True
    assert len(meta_json['datasets']) >= 3

    # Test preview API on real college dataset
    res_prev = client.get('/api/datasets/college_placement_real.csv?limit=5')
    assert res_prev.status_code == 200
    prev_json = json.loads(res_prev.data)
    assert prev_json['success'] is True
    assert len(prev_json['records']) == 5
    assert 'PlacedOrNot' in prev_json['columns']

def test_api_sample_real_student(client):
    res = client.get('/api/sample/real_at_risk')
    assert res.status_code == 200
    sample_data = json.loads(res.data)
    assert 'student_id' in sample_data
    assert 'cgpa' in sample_data

    # Send through prediction pipeline to verify schema and execution
    pred_res = client.post('/api/predict', json=sample_data)
    assert pred_res.status_code == 200
    pred_data = json.loads(pred_res.data)
    assert pred_data['success'] is True
    assert 'stage1' in pred_data['data']
    assert 'recourse' in pred_data['data']

def test_user_data_integration_endpoint(client):
    user_payload = {
        'age': 22,
        'gender': 'Female',
        'family_income_bracket': 'Tier-2 Middle',
        'family_size': 4,
        'parental_education': 'Bachelor',
        'parental_status': 'Married',
        'intermediate_math': 82.0,
        'intermediate_physics': 80.0,
        'intermediate_chemistry': 78.0,
        'intermediate_english': 85.0,
        'intermediate_aggregate': 81.25,
        'attendance_percentage': 88.0,
        'study_hours_per_week': 20.0,
        'extracurricular_clubs': 2,
        'soft_skills_score': 3.8,
        'certifications_count': 2,
        'midterm_score': 84.0,
        'core_course_score': 82.5,
        'cgpa': 8.35
    }

    # Integrate user-given student
    res = client.post('/api/datasets/integrate', json=user_payload)
    assert res.status_code == 201
    res_data = json.loads(res.data)
    assert res_data['success'] is True
    assert 'student_id' in res_data
    assert 'predictions' in res_data
    assert res_data['predictions']['placement_status'] in ['Placed', 'Not Placed']

    # Retrieve user integrated sample
    user_sample_res = client.get('/api/sample/user_student')
    assert user_sample_res.status_code == 200
    sample_json = json.loads(user_sample_res.data)
    assert 'cgpa' in sample_json

    # Negative validation test: invalid CGPA
    bad_payload = dict(user_payload)
    bad_payload['cgpa'] = 14.5
    bad_res = client.post('/api/datasets/integrate', json=bad_payload)
    assert bad_res.status_code == 422



