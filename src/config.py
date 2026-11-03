"""
Central Configuration and Logging for Educational Recourse Framework.
Implements SOLID principles by centralizing paths, hyperparameters, and feature contracts.
"""

import os
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

# Base Directories
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(DATA_DIR, "models")
EXPORT_DIR = os.path.join(BASE_DIR, "evaluation", "exports")
DATASET_PATH = os.path.join(DATA_DIR, "student_multimodal_dataset.csv")

# Create required directories
for d in [DATA_DIR, MODEL_DIR, EXPORT_DIR]:
    os.makedirs(d, exist_ok=True)

# Logging Setup
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(BASE_DIR, "framework.log"), encoding="utf-8")
    ]
)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

# Model Targets
TARGET_STAGE_1 = "recommended_branch"
TARGET_STAGE_2 = "academic_performance"
TARGET_STAGE_3 = "placement_status"

# Engineering Disciplines (Stage 1 Classes)
ENGINEERING_BRANCHES = [
    "Computer Science & Engineering",
    "Data Science & AI",
    "Electronics & Communication",
    "Electrical & Electronics",
    "Mechanical Engineering",
    "Information Technology"
]

# Academic Performance Tiers (Stage 2 Classes)
ACADEMIC_TIERS = ["Distinction", "First Class", "Second Class", "At-Risk"]

# Feature Definitions
# 1. Socio-Demographic Features (Immutable: F_imm)
SOCIO_DEMOGRAPHIC_FEATURES = [
    "age", "gender", "parental_education", "parental_status",
    "family_income_bracket", "family_size"
]

# 2. Intermediate Academic Background (Pre-College)
INTERMEDIATE_ACADEMIC_FEATURES = [
    "intermediate_math", "intermediate_physics", "intermediate_chemistry",
    "intermediate_english", "intermediate_aggregate"
]

# 3. Behavioral & Co-Curricular Indicators (Mutable: F_mut)
BEHAVIORAL_FEATURES = [
    "attendance_percentage", "study_hours_per_week",
    "extracurricular_clubs", "soft_skills_score", "certifications_count"
]

# 4. College Academic Indicators (Mutable: F_mut)
COLLEGE_ACADEMIC_FEATURES = [
    "midterm_score", "core_course_score", "cgpa"
]

# Partitioning for Recourse Optimization (Eq. 6)
# Immutable Features: Demographics and Pre-College Academic Background
IMMUTABLE_FEATURES = list(SOCIO_DEMOGRAPHIC_FEATURES) + list(INTERMEDIATE_ACADEMIC_FEATURES)

MUTABLE_FEATURE_BOUNDS: Dict[str, Tuple[float, float, str]] = {
    # feature: (min_bound, max_bound, unit/description)
    "cgpa": (5.0, 10.0, "/ 10.0"),
    "attendance_percentage": (50.0, 99.0, "%"),
    "core_course_score": (45.0, 99.0, "%"),
    "midterm_score": (45.0, 99.0, "%"),
    "study_hours_per_week": (4.0, 45.0, "hrs/week"),
    "extracurricular_clubs": (0.0, 5.0, "clubs"),
    "soft_skills_score": (1.0, 5.0, "/ 5.0"),
    "certifications_count": (0.0, 4.0, "certs")
}

MUTABLE_FEATURES = list(MUTABLE_FEATURE_BOUNDS.keys())

# Stage 1 Pre-College Input Features (Temporal Leakage Free)
STAGE1_NUMERIC_FEATURES = [
    "age", "family_size",
    "intermediate_math", "intermediate_physics", "intermediate_chemistry",
    "intermediate_english", "intermediate_aggregate"
]
STAGE1_CATEGORICAL_FEATURES = [
    "gender", "parental_education", "parental_status", "family_income_bracket"
]

# Web App Configuration
@dataclass
class AppConfig:
    HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("APP_PORT", "5000"))
    DEBUG: bool = os.getenv("APP_DEBUG", "False").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "eduforecaster-secure-key-2026")
    ALLOWED_ORIGINS: List[str] = field(default_factory=lambda: [
        "http://127.0.0.1:5000",
        "http://localhost:5000"
    ])
    RATE_LIMIT: str = "60 per minute"
