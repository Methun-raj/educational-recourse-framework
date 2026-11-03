"""
Synthetic Educational Multi-Modal Dataset Generator.
Based on: "Machine Learning-Based Forecasting of Student Academic Success, Branch Recommendation,
and Career Placement: A Hierarchical Multi-Task and Explainable Recourse Framework"

Generates calibrated synthetic longitudinal records explicitly tagged as synthetic:
- Academic Indicators (x_i^(acad))
- Socio-Economic & Demographic Indicators (x_i^(socio), F_imm)
- Behavioral & Co-Curricular Indicators (x_i^(behav), F_mut)
- College Academic Longitudinal Records (x_i^(coll_acad), F_mut)
"""

import os
import json
import numpy as np
import pandas as pd
from typing import Optional

from src.config import (
    DATASET_PATH,
    DATA_DIR,
    ENGINEERING_BRANCHES,
    ACADEMIC_TIERS,
    get_logger
)
from src.schemas import StudentProfileSchema

logger = get_logger(__name__)


def generate_multimodal_student_dataset(n_samples: int = 2500, random_seed: int = 42) -> pd.DataFrame:
    """
    Generates a reproducible, schema-validated synthetic educational dataset.
    Note: Explicitly labeled as synthetic educational benchmark data.
    """
    logger.info("Generating %d synthetic student records with seed %d", n_samples, random_seed)
    np.random.seed(random_seed)

    # 1. Socio-Economic & Demographic Indicators (F_imm)
    genders = np.random.choice(['Male', 'Female'], size=n_samples, p=[0.52, 0.48])
    ages = np.random.choice([18, 19, 20, 21, 22], size=n_samples, p=[0.12, 0.38, 0.32, 0.14, 0.04])
    parental_education = np.random.choice(
        ['High School', 'Bachelor', 'Master', 'Doctorate'],
        size=n_samples,
        p=[0.20, 0.52, 0.22, 0.06]
    )
    parental_status = np.random.choice(
        ['Married', 'Single', 'Divorced'],
        size=n_samples,
        p=[0.80, 0.12, 0.08]
    )
    income_brackets = np.random.choice(
        ['Tier-1 High', 'Tier-2 Middle', 'Tier-3 Low'],
        size=n_samples,
        p=[0.25, 0.50, 0.25]
    )
    family_sizes = np.random.choice([2, 3, 4, 5, 6], size=n_samples, p=[0.08, 0.32, 0.40, 0.15, 0.05])

    # 2. Intermediate Academic Background (Pre-College)
    math_base = np.random.normal(72, 13, size=n_samples)
    physics_base = 0.55 * math_base + np.random.normal(32, 9, size=n_samples)
    chem_base = 0.45 * math_base + np.random.normal(38, 10, size=n_samples)
    english_base = np.random.normal(70, 12, size=n_samples)

    intermediate_math = np.clip(math_base, 38, 99).round(1)
    intermediate_physics = np.clip(physics_base, 38, 99).round(1)
    intermediate_chemistry = np.clip(chem_base, 38, 99).round(1)
    intermediate_english = np.clip(english_base, 38, 99).round(1)
    intermediate_aggregate = (
        0.30 * intermediate_math +
        0.25 * intermediate_physics +
        0.25 * intermediate_chemistry +
        0.20 * intermediate_english
    ).round(2)

    # 3. Stage 1 Target: Branch Recommendation (Matches subject affinities)
    branch_rules = []
    for i in range(n_samples):
        m = intermediate_math[i]
        p = intermediate_physics[i]
        c = intermediate_chemistry[i]
        e = intermediate_english[i]

        if m >= 75 and e >= 70 and m > p:
            b = 'Computer Science & Engineering'
        elif m >= 74 and p >= 68:
            b = 'Data Science & AI'
        elif p >= 70 and m >= 65 and p > c:
            b = 'Electronics & Communication'
        elif p >= 68 and c >= 65:
            b = 'Electrical & Electronics'
        elif c >= 65 and p >= 60:
            b = 'Mechanical Engineering'
        else:
            b = 'Information Technology'

        # Introduce controlled ~10% student preference variance
        if np.random.rand() < 0.10:
            b = str(np.random.choice([x for x in ENGINEERING_BRANCHES if x != b]))
        branch_rules.append(b)

    recommended_branch = branch_rules

    # 4. Behavioral & Co-Curricular Indicators (F_mut)
    study_hours = np.clip(np.random.normal(19, 5.5, size=n_samples), 5, 38).round(1)
    attendance_rate = np.clip(
        62 + (study_hours / 38.0) * 26 + np.random.normal(0, 4.0, size=n_samples),
        55, 99
    ).round(1)
    extracurricular_clubs = np.random.choice([0, 1, 2, 3, 4], size=n_samples, p=[0.20, 0.40, 0.25, 0.10, 0.05])
    soft_skills_score = np.clip(
        1.2 + (attendance_rate / 100.0) * 2.1 + (extracurricular_clubs / 4.0) * 1.4 + np.random.normal(0, 0.3, size=n_samples),
        1.0, 5.0
    ).round(1)
    certifications_count = np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.25, 0.45, 0.22, 0.08])

    # 5. Longitudinal Academic Indicators
    cgpa_raw = (
        0.048 * intermediate_aggregate +
        0.027 * attendance_rate +
        0.026 * study_hours +
        np.random.normal(1.5, 0.40, size=n_samples)
    )
    cgpa = np.clip(cgpa_raw, 5.2, 9.90).round(2)
    midterm_score = np.clip(cgpa * 9.6 + np.random.normal(0, 3.2, size=n_samples), 48, 99).round(1)
    core_course_score = np.clip(cgpa * 9.7 + np.random.normal(0, 3.0, size=n_samples), 48, 99).round(1)

    # Stage 2 Target: Academic Performance Category
    perf_latent = 0.55 * cgpa + 0.02 * midterm_score + 0.015 * core_course_score + 0.01 * attendance_rate
    perf_noise = perf_latent + np.random.normal(0, 0.18, n_samples)
    academic_performance = []
    for val in perf_noise:
        if val >= 8.2:
            academic_performance.append('Distinction')
        elif val >= 7.3:
            academic_performance.append('First Class')
        elif val >= 6.4:
            academic_performance.append('Second Class')
        else:
            academic_performance.append('At-Risk')

    # 6. Stage 3 Target: Placement Status (Non-linear multi-modal decision boundary)
    # Decision boundary combining core competence, communication readiness, attendance discipline, and co-curricular projects
    norm_cgpa = (cgpa - 7.0) / 1.0
    norm_att = (attendance_rate - 75.0) / 10.0
    norm_core = (core_course_score - 70.0) / 10.0
    norm_soft = (soft_skills_score - 2.8) / 1.0
    norm_clubs = (extracurricular_clubs - 1.0) / 1.0

    non_linear_latent = (
        1.55 * norm_cgpa +
        0.80 * norm_att +
        0.75 * norm_core +
        0.65 * norm_soft +
        0.50 * norm_clubs +
        0.85 * (norm_core * norm_soft) +   # Interaction: Technical + Communication
        0.75 * (norm_cgpa * norm_att) +   # Interaction: Academic + Discipline
        0.65                               # Calibrated baseline shift (~68% placement rate)
    )

    placement_prob = 1.0 / (1.0 + np.exp(-1.40 * non_linear_latent))
    placement_status = (placement_prob >= 0.50).astype(int)

    # 3% margin fuzziness for natural non-deterministic outcomes
    margin_mask = (placement_prob > 0.47) & (placement_prob < 0.53)
    if margin_mask.sum() > 0:
        placement_status[margin_mask] = np.random.choice([0, 1], size=margin_mask.sum())

    df = pd.DataFrame({
        'student_id': [f"STU_{1000 + i}" for i in range(n_samples)],
        'age': ages,
        'gender': genders,
        'parental_education': parental_education,
        'parental_status': parental_status,
        'family_income_bracket': income_brackets,
        'family_size': family_sizes,
        'intermediate_math': intermediate_math,
        'intermediate_physics': intermediate_physics,
        'intermediate_chemistry': intermediate_chemistry,
        'intermediate_english': intermediate_english,
        'intermediate_aggregate': intermediate_aggregate,
        'recommended_branch': recommended_branch,
        'attendance_percentage': attendance_rate,
        'study_hours_per_week': study_hours,
        'extracurricular_clubs': extracurricular_clubs,
        'soft_skills_score': soft_skills_score,
        'certifications_count': certifications_count,
        'midterm_score': midterm_score,
        'core_course_score': core_course_score,
        'cgpa': cgpa,
        'academic_performance': academic_performance,
        'placement_status': placement_status
    })

    # Benchmark Row 0: Canonical Semester-4 student from Table V
    df.loc[0, 'age'] = 20
    df.loc[0, 'gender'] = 'Male'
    df.loc[0, 'family_income_bracket'] = 'Tier-3 Low'
    df.loc[0, 'family_size'] = 5
    df.loc[0, 'parental_education'] = 'High School'
    df.loc[0, 'parental_status'] = 'Married'
    df.loc[0, 'intermediate_math'] = 62.0
    df.loc[0, 'intermediate_physics'] = 59.0
    df.loc[0, 'intermediate_chemistry'] = 60.0
    df.loc[0, 'intermediate_english'] = 58.0
    df.loc[0, 'intermediate_aggregate'] = 59.8
    df.loc[0, 'recommended_branch'] = 'Mechanical Engineering'
    df.loc[0, 'attendance_percentage'] = 64.0
    df.loc[0, 'study_hours_per_week'] = 8.0
    df.loc[0, 'extracurricular_clubs'] = 0
    df.loc[0, 'soft_skills_score'] = 2.0
    df.loc[0, 'certifications_count'] = 0
    df.loc[0, 'midterm_score'] = 60.5
    df.loc[0, 'core_course_score'] = 58.0
    df.loc[0, 'cgpa'] = 6.40
    df.loc[0, 'academic_performance'] = 'At-Risk'
    df.loc[0, 'placement_status'] = 0

    return df


def validate_dataset_schema(df: pd.DataFrame) -> bool:
    """Validates dataframe records against StudentProfileSchema."""
    logger.info("Validating dataset schema integrity across %d records", len(df))
    # Validate a 10% sample for performance
    sample_df = df.sample(min(250, len(df)), random_state=42)
    for idx, row in sample_df.iterrows():
        try:
            StudentProfileSchema(**row.to_dict())
        except Exception as e:
            logger.error("Schema validation failed at row %d: %s", idx, str(e))
            raise ValueError(f"Dataset schema invalid at row {idx}: {e}")
    logger.info("Dataset schema validation passed.")
    return True


def save_default_dataset(output_path: str = DATASET_PATH) -> pd.DataFrame:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = generate_multimodal_student_dataset(n_samples=2500, random_seed=42)
    validate_dataset_schema(df)
    df.to_csv(output_path, index=False)

    # Write dataset provenance metadata
    metadata = {
        "dataset_type": "Synthetic Educational Benchmark Dataset",
        "sample_count": len(df),
        "source": "Generative simulation grounded in Educational Data Mining benchmarks",
        "placement_rate": float(df['placement_status'].mean()),
        "features": list(df.columns)
    }
    meta_path = os.path.join(os.path.dirname(output_path), "dataset_metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    logger.info("Dataset successfully generated and saved to %s", output_path)
    return df


if __name__ == "__main__":
    save_default_dataset()
