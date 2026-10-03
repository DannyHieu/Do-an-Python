import os
import sqlite3
import sys

THU_MUC_GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if THU_MUC_GOC not in sys.path:
    sys.path.append(THU_MUC_GOC)

import config


def ket_noi():
    thu_muc_data = os.path.dirname(config.DUONG_DAN_DATABASE)
    os.makedirs(thu_muc_data, exist_ok=True)

    ket_noi_db = sqlite3.connect(config.DUONG_DAN_DATABASE)

    ket_noi_db.row_factory = sqlite3.Row

    ket_noi_db.execute("PRAGMA foreign_keys = ON")

    return ket_noi_db



SQL_BANG_PATIENTS = """
CREATE TABLE IF NOT EXISTS patients (
    patient_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name     TEXT NOT NULL,
    date_of_birth DATE,
    gender        TEXT,
    phone         TEXT,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""

SQL_BANG_ASSESSMENTS = """
CREATE TABLE IF NOT EXISTS assessments (
    assessment_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id           INTEGER NOT NULL,
    assessment_type      TEXT NOT NULL CHECK (assessment_type IN ('SYMPTOM', 'CLINICAL')),
    age_at_assessment    INTEGER NOT NULL,
    gender_at_assessment TEXT,
    assessed_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    notes                TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
)
"""

SQL_BANG_SYMPTOM = """
CREATE TABLE IF NOT EXISTS symptom_assessments (
    assessment_id      INTEGER PRIMARY KEY,
    excess_urination   INTEGER NOT NULL,
    polydipsia         INTEGER NOT NULL,
    sudden_weight_loss INTEGER NOT NULL,
    fatigue            INTEGER NOT NULL,
    polyphagia         INTEGER NOT NULL,
    genital_thrush     INTEGER NOT NULL,
    blurred_vision     INTEGER NOT NULL,
    itching            INTEGER NOT NULL,
    irritability       INTEGER NOT NULL,
    delayed_healing    INTEGER NOT NULL,
    partial_psoriasis  INTEGER NOT NULL,
    muscle_stiffness   INTEGER NOT NULL,
    alopecia           INTEGER NOT NULL,
    obesity            INTEGER NOT NULL,
    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id)
)
"""

SQL_BANG_CLINICAL = """
CREATE TABLE IF NOT EXISTS clinical_assessments (
    assessment_id              INTEGER PRIMARY KEY,
    pregnancies                INTEGER,
    glucose                    REAL,
    blood_pressure             REAL,
    skin_thickness             REAL,
    insulin                    REAL,
    bmi                        REAL,
    diabetes_pedigree_function REAL,
    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id)
)
"""

SQL_BANG_ML_MODELS = """
CREATE TABLE IF NOT EXISTS ml_models (
    model_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    model_key     TEXT NOT NULL,
    model_name    TEXT NOT NULL,
    version       TEXT NOT NULL,
    algorithm     TEXT,
    artifact_path TEXT NOT NULL,
    metrics_json  TEXT,
    is_active     INTEGER NOT NULL DEFAULT 0,
    trained_at    DATETIME
)
"""

SQL_BANG_PREDICTIONS = """
CREATE TABLE IF NOT EXISTS predictions (
    prediction_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id            INTEGER NOT NULL,
    model_id                 INTEGER NOT NULL,
    predicted_class          INTEGER NOT NULL,
    probability              REAL NOT NULL,
    classification_threshold REAL NOT NULL DEFAULT 0.5,
    risk_level               TEXT,
    created_at               DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id),
    FOREIGN KEY (model_id) REFERENCES ml_models(model_id)
)
"""

SQL_INDEX_1 = """
CREATE INDEX IF NOT EXISTS idx_assessments_patient_date
ON assessments(patient_id, assessed_at)
"""

SQL_INDEX_2 = """
CREATE INDEX IF NOT EXISTS idx_predictions_assessment
ON predictions(assessment_id)
"""


def tao_bang():
    ket_noi_db = ket_noi()

    danh_sach_lenh = [
        SQL_BANG_PATIENTS,
        SQL_BANG_ASSESSMENTS,
        SQL_BANG_SYMPTOM,
        SQL_BANG_CLINICAL,
        SQL_BANG_ML_MODELS,
        SQL_BANG_PREDICTIONS,
        SQL_INDEX_1,
        SQL_INDEX_2,
    ]

    for cau_lenh in danh_sach_lenh:
        ket_noi_db.execute(cau_lenh)

    ket_noi_db.commit()
    ket_noi_db.close()


if __name__ == "__main__":
    print("Đang tạo database tại:", config.DUONG_DAN_DATABASE)
    tao_bang()
    print("Đã tạo xong 6 bảng và 2 chỉ mục.")

    ket_noi_db = ket_noi()
    danh_sach_bang = ket_noi_db.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
    ).fetchall()
    ket_noi_db.close()

    print()
    print("Các bảng hiện có trong database:")
    for dong in danh_sach_bang:
        print("   -", dong["name"])
