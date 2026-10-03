import os
import sys
from datetime import datetime

THU_MUC_GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if THU_MUC_GOC not in sys.path:
    sys.path.append(THU_MUC_GOC)

import config
from database.db import ket_noi


def _doi_sang_dict(danh_sach_dong):

    ket_qua = []
    for dong in danh_sach_dong:
        ket_qua.append(dict(dong))
    return ket_qua



def them_benh_nhan(ho_ten, ngay_sinh, gioi_tinh, dien_thoai):
    db = ket_noi()

    con_tro = db.execute(
        """
        INSERT INTO patients (full_name, date_of_birth, gender, phone)
        VALUES (?, ?, ?, ?)
        """,
        (ho_ten, ngay_sinh, gioi_tinh, dien_thoai),
    )

    ma_benh_nhan = con_tro.lastrowid

    db.commit()
    db.close()
    return ma_benh_nhan


def sua_benh_nhan(ma_benh_nhan, ho_ten, ngay_sinh, gioi_tinh, dien_thoai):

    db = ket_noi()
    db.execute(
        """
        UPDATE patients
        SET full_name = ?, date_of_birth = ?, gender = ?, phone = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE patient_id = ?
        """,
        (ho_ten, ngay_sinh, gioi_tinh, dien_thoai, ma_benh_nhan),
    )
    db.commit()
    db.close()


def lay_benh_nhan(ma_benh_nhan):

    db = ket_noi()

    dong = db.execute(
        "SELECT * FROM patients WHERE patient_id = ?",
        (ma_benh_nhan,),
    ).fetchone()
    db.close()

    if dong is None:
        return None
    return dict(dong)


def tim_benh_nhan(tu_khoa=""):

    db = ket_noi()

    if tu_khoa.strip() == "":

        danh_sach = db.execute(
            "SELECT * FROM patients ORDER BY patient_id DESC"
        ).fetchall()
    else:
        mau_tim = "%" + tu_khoa.strip() + "%"
        danh_sach = db.execute(
            """
            SELECT * FROM patients
            WHERE full_name LIKE ? OR phone LIKE ?
            ORDER BY patient_id DESC
            """,
            (mau_tim, mau_tim),
        ).fetchall()

    db.close()
    return _doi_sang_dict(danh_sach)


def _them_dong_assessment(db, ma_benh_nhan, loai, tuoi, gioi_tinh, ghi_chu):

    con_tro = db.execute(
        """
        INSERT INTO assessments
            (patient_id, assessment_type, age_at_assessment,
             gender_at_assessment, assessed_at, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (ma_benh_nhan, loai, tuoi, gioi_tinh,
         datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ghi_chu),
    )
    return con_tro.lastrowid


def _them_dong_prediction(db, ma_danh_gia, ket_qua):

    db.execute(
        """
        INSERT INTO predictions
            (assessment_id, model_id, predicted_class, probability,
             classification_threshold, risk_level)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (ma_danh_gia,
         ket_qua["model_id"],
         ket_qua["lop_du_doan"],
         ket_qua["xac_suat"],
         config.NGUONG_PHAN_LOAI,
         ket_qua["muc_rui_ro"]),
    )


def luu_danh_gia_trieu_chung(ma_benh_nhan, tuoi, gioi_tinh, cac_trieu_chung,
                             ket_qua, ghi_chu=""):

    db = ket_noi()
    try:
        ma_danh_gia = _them_dong_assessment(
            db, ma_benh_nhan, config.LOAI_DANH_GIA_TRIEU_CHUNG,
            tuoi, gioi_tinh, ghi_chu
        )

        ten_cac_cot = []
        gia_tri_cac_cot = []
        for trieu_chung in config.DANH_SACH_TRIEU_CHUNG:
            ten_cot = trieu_chung["cot_db"]
            ten_cac_cot.append(ten_cot)
            gia_tri_cac_cot.append(cac_trieu_chung[ten_cot])

        chuoi_ten_cot = ", ".join(ten_cac_cot)
        chuoi_dau_hoi = ", ".join(["?"] * len(ten_cac_cot))

        db.execute(
            "INSERT INTO symptom_assessments (assessment_id, %s) VALUES (?, %s)"
            % (chuoi_ten_cot, chuoi_dau_hoi),
            [ma_danh_gia] + gia_tri_cac_cot,
        )

        _them_dong_prediction(db, ma_danh_gia, ket_qua)

        db.commit()
        return ma_danh_gia

    except Exception as loi:
        db.rollback()
        raise loi
    finally:
        db.close()


def luu_danh_gia_lam_sang(ma_benh_nhan, tuoi, gioi_tinh, cac_chi_so,
                          ket_qua, ghi_chu=""):

    db = ket_noi()
    try:
        ma_danh_gia = _them_dong_assessment(
            db, ma_benh_nhan, config.LOAI_DANH_GIA_LAM_SANG,
            tuoi, gioi_tinh, ghi_chu
        )

        ten_cac_cot = []
        gia_tri_cac_cot = []
        for chi_so in config.DANH_SACH_CHI_SO:
            ten_cot = chi_so["cot_db"]
            ten_cac_cot.append(ten_cot)
            gia_tri_cac_cot.append(cac_chi_so[ten_cot])

        chuoi_ten_cot = ", ".join(ten_cac_cot)
        chuoi_dau_hoi = ", ".join(["?"] * len(ten_cac_cot))

        db.execute(
            "INSERT INTO clinical_assessments (assessment_id, %s) VALUES (?, %s)"
            % (chuoi_ten_cot, chuoi_dau_hoi),
            [ma_danh_gia] + gia_tri_cac_cot,
        )

        _them_dong_prediction(db, ma_danh_gia, ket_qua)

        db.commit()
        return ma_danh_gia

    except Exception as loi:
        db.rollback()
        raise loi
    finally:
        db.close()



def lay_lich_su(ma_benh_nhan=None, loai=None, tu_ngay=None, den_ngay=None):

    cau_lenh = """
        SELECT
            a.assessment_id,
            a.assessment_type,
            a.age_at_assessment,
            a.gender_at_assessment,
            a.assessed_at,
            a.notes,
            p.patient_id,
            p.full_name,
            pr.predicted_class,
            pr.probability,
            pr.risk_level,
            m.model_name,
            m.version
        FROM assessments a
        JOIN patients p ON p.patient_id = a.patient_id
        LEFT JOIN predictions pr ON pr.assessment_id = a.assessment_id
        LEFT JOIN ml_models m ON m.model_id = pr.model_id
        WHERE 1 = 1
    """

    cac_gia_tri = []

    if ma_benh_nhan is not None:
        cau_lenh = cau_lenh + " AND a.patient_id = ? "
        cac_gia_tri.append(ma_benh_nhan)

    if loai is not None:
        cau_lenh = cau_lenh + " AND a.assessment_type = ? "
        cac_gia_tri.append(loai)

    if tu_ngay is not None:
        cau_lenh = cau_lenh + " AND date(a.assessed_at) >= date(?) "
        cac_gia_tri.append(tu_ngay)

    if den_ngay is not None:
        cau_lenh = cau_lenh + " AND date(a.assessed_at) <= date(?) "
        cac_gia_tri.append(den_ngay)

    cau_lenh = cau_lenh + " ORDER BY a.assessed_at DESC, a.assessment_id DESC"

    db = ket_noi()
    danh_sach = db.execute(cau_lenh, cac_gia_tri).fetchall()
    db.close()
    return _doi_sang_dict(danh_sach)


def lay_chi_tiet_danh_gia(ma_danh_gia):

    db = ket_noi()

    dong_chung = db.execute(
        """
        SELECT
            a.*, p.full_name, p.phone,
            pr.predicted_class, pr.probability, pr.risk_level,
            pr.classification_threshold,
            m.model_name, m.version, m.algorithm
        FROM assessments a
        JOIN patients p ON p.patient_id = a.patient_id
        LEFT JOIN predictions pr ON pr.assessment_id = a.assessment_id
        LEFT JOIN ml_models m ON m.model_id = pr.model_id
        WHERE a.assessment_id = ?
        """,
        (ma_danh_gia,),
    ).fetchone()

    if dong_chung is None:
        db.close()
        return None

    if dong_chung["assessment_type"] == config.LOAI_DANH_GIA_TRIEU_CHUNG:
        dong_chi_tiet = db.execute(
            "SELECT * FROM symptom_assessments WHERE assessment_id = ?",
            (ma_danh_gia,),
        ).fetchone()
    else:
        dong_chi_tiet = db.execute(
            "SELECT * FROM clinical_assessments WHERE assessment_id = ?",
            (ma_danh_gia,),
        ).fetchone()

    db.close()

    return {
        "chung": dict(dong_chung),
        "chi_tiet": dict(dong_chi_tiet) if dong_chi_tiet is not None else None,
    }



def dang_ky_model(model_key, ten_model, phien_ban, thuat_toan,
                  duong_dan_file, chuoi_metrics):

    db = ket_noi()
    try:
        db.execute(
            "UPDATE ml_models SET is_active = 0 WHERE model_key = ?",
            (model_key,),
        )

        con_tro = db.execute(
            """
            INSERT INTO ml_models
                (model_key, model_name, version, algorithm,
                 artifact_path, metrics_json, is_active, trained_at)
            VALUES (?, ?, ?, ?, ?, ?, 1, ?)
            """,
            (model_key, ten_model, phien_ban, thuat_toan,
             duong_dan_file, chuoi_metrics,
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        ma_model = con_tro.lastrowid
        db.commit()
        return ma_model
    except Exception as loi:
        db.rollback()
        raise loi
    finally:
        db.close()


def lay_model_dang_dung(model_key):

    db = ket_noi()
    dong = db.execute(
        """
        SELECT * FROM ml_models
        WHERE model_key = ? AND is_active = 1
        ORDER BY model_id DESC
        """,
        (model_key,),
    ).fetchone()
    db.close()

    if dong is None:
        return None
    return dict(dong)


def lay_tat_ca_model():

    db = ket_noi()
    danh_sach = db.execute(
        "SELECT * FROM ml_models ORDER BY model_key, model_id DESC"
    ).fetchall()
    db.close()
    return _doi_sang_dict(danh_sach)



def _dem_mot_so(cau_lenh, cac_gia_tri=()):

    db = ket_noi()
    dong = db.execute(cau_lenh, cac_gia_tri).fetchone()
    db.close()
    return dong[0]


def dem_benh_nhan():
    return _dem_mot_so("SELECT COUNT(*) FROM patients")


def dem_danh_gia():
    return _dem_mot_so("SELECT COUNT(*) FROM assessments")


def dem_theo_ket_qua():

    duong_tinh = _dem_mot_so(
        "SELECT COUNT(*) FROM predictions WHERE predicted_class = 1"
    )
    am_tinh = _dem_mot_so(
        "SELECT COUNT(*) FROM predictions WHERE predicted_class = 0"
    )
    return {"duong_tinh": duong_tinh, "am_tinh": am_tinh}


def dem_theo_loai():

    db = ket_noi()
    danh_sach = db.execute(
        """
        SELECT assessment_type, COUNT(*) AS so_luong
        FROM assessments
        GROUP BY assessment_type
        """
    ).fetchall()
    db.close()

    ket_qua = {config.LOAI_DANH_GIA_TRIEU_CHUNG: 0,
               config.LOAI_DANH_GIA_LAM_SANG: 0}
    for dong in danh_sach:
        ket_qua[dong["assessment_type"]] = dong["so_luong"]
    return ket_qua


def dem_theo_muc_rui_ro():

    db = ket_noi()
    danh_sach = db.execute(
        """
        SELECT risk_level, COUNT(*) AS so_luong
        FROM predictions
        GROUP BY risk_level
        """
    ).fetchall()
    db.close()

    ket_qua = {"THẤP": 0, "TRUNG BÌNH": 0, "CAO": 0}
    for dong in danh_sach:
        if dong["risk_level"] in ket_qua:
            ket_qua[dong["risk_level"]] = dong["so_luong"]
    return ket_qua
