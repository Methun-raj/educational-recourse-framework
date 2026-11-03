"""
Downloader and Validator for Original Real-World Educational Datasets.
Downloads and organizes canonical real-world student datasets:
1. Engineering College Placement Dataset (N=2,966 records)
2. Campus Recruitment & Placement Dataset (N=215 records)
3. UCI Student Academic Performance Dataset (N=395 records)
"""

import os
import sys
import json
import urllib.request
import pandas as pd
from typing import Dict, Any

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import BASE_DIR, get_logger

logger = get_logger(__name__)

ORIGINAL_DATA_DIR = os.path.join(BASE_DIR, "data", "original_benchmarks")
os.makedirs(ORIGINAL_DATA_DIR, exist_ok=True)

DATASET_SOURCES = {
    "college_placement_real.csv": {
        "title": "Engineering College Placement Dataset",
        "url": "https://raw.githubusercontent.com/Nileshshinde09/student-placement-prediction-app-using-online-machine-learning/main/collegePlace.csv",
        "description": "2,966 engineering student records across 6 engineering streams (CSE, IT, ECE, EEE, ME, Civil) with CGPA, internships, backlogs, and placement outcomes.",
        "target": "PlacedOrNot",
        "features": ["Age", "Gender", "Stream", "Internships", "CGPA", "Hostel", "HistoryOfBacklogs"]
    },
    "campus_recruitment_real.csv": {
        "title": "Campus Recruitment Academic & Placement Dataset",
        "url": "https://raw.githubusercontent.com/colema13/Placement_Data_Full_Class/main/Placement_Data_Full_Class.csv",
        "description": "215 undergraduate and postgraduate students with secondary (10th), higher secondary (12th), degree percentages, employability test marks, and placement status.",
        "target": "status",
        "features": ["gender", "ssc_p", "ssc_b", "hsc_p", "hsc_b", "hsc_s", "degree_p", "degree_t", "workex", "etest_p", "specialisation", "mba_p"]
    },
    "uci_student_performance_real.csv": {
        "title": "UCI Student Academic Performance Dataset (Cortez & Silva, 2008)",
        "url": "https://raw.githubusercontent.com/Le0n1996/Preprocessing-data--Decision-trees-and-Adaboost/main/student-mat.csv",
        "description": "395 secondary school student records evaluating socio-demographics, parental education, study time, alcohol consumption, absences, and longitudinal exam marks (G1, G2, G3).",
        "target": "G3",
        "features": ["school", "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu", "Mjob", "Fjob", "reason", "guardian", "traveltime", "studytime", "failures", "schoolsup", "famsup", "paid", "activities", "nursery", "higher", "internet", "romantic", "famrel", "freetime", "goout", "Dalc", "Walc", "health", "absences", "G1", "G2"]
    }
}


def download_all_original_datasets() -> Dict[str, str]:
    """Downloads all canonical real-world educational datasets and saves metadata."""
    saved_paths = {}
    metadata_records = {}

    for fname, info in DATASET_SOURCES.items():
        dest_path = os.path.join(ORIGINAL_DATA_DIR, fname)
        logger.info("Downloading %s from %s ...", info['title'], info['url'])

        try:
            req = urllib.request.Request(info['url'], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read()
                with open(dest_path, 'wb') as f:
                    f.write(content)

            sep = ';' if b';' in content[:100] else ','
            df = pd.read_csv(dest_path, sep=sep)
            logger.info("Successfully saved %s (Shape: %s)", dest_path, df.shape)

            saved_paths[fname] = dest_path
            metadata_records[fname] = {
                "title": info['title'],
                "url": info['url'],
                "description": info['description'],
                "sample_count": len(df),
                "column_count": len(df.columns),
                "columns": df.columns.tolist(),
                "target_variable": info['target']
            }

        except Exception as e:
            logger.error("Failed to download %s: %s", fname, str(e))
            raise

    # Write metadata.json
    meta_path = os.path.join(ORIGINAL_DATA_DIR, "metadata.json")
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata_records, f, indent=2)
    logger.info("Original datasets metadata saved to %s", meta_path)

    return saved_paths


if __name__ == "__main__":
    download_all_original_datasets()
