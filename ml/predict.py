
import os
import sys

import joblib
import numpy as np
import pandas as pd

THU_MUC_GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if THU_MUC_GOC not in sys.path:
    sys.path.append(THU_MUC_GOC)

import config
from database import queries


_BO_NHO_MODEL = {}


def nap_model(loai_model):
    thong_tin = queries.lay_model_dang_dung(loai_model)

    if thong_tin is None:
        raise Exception(
            "Chưa có model '%s' nào trong database.\n"
            "Hãy chạy lệnh sau trước khi dùng ứng dụng:\n"
            "    python ml/train_%s.py" % (loai_model, loai_model)
        )

    duong_dan_file = thong_tin["artifact_path"]

    if not os.path.exists(duong_dan_file):
        raise Exception(
            "Database có ghi model nhưng không tìm thấy file:\n"
            "    %s\n"
            "Hãy chạy lại: python ml/train_%s.py" % (duong_dan_file, loai_model)
        )

    if loai_model in _BO_NHO_MODEL:
        return _BO_NHO_MODEL[loai_model], thong_tin

    mo_hinh = joblib.load(duong_dan_file)
    _BO_NHO_MODEL[loai_model] = mo_hinh

    return mo_hinh, thong_tin


def tinh_muc_rui_ro(xac_suat):
    if xac_suat < config.NGUONG_RUI_RO_THAP:
        return "THẤP"

    elif xac_suat < config.NGUONG_RUI_RO_TRUNG_BINH:
        return "TRUNG BÌNH"

    else:
        return "CAO"


def _chay_du_doan(mo_hinh, thong_tin, bang_mot_dong):
    lop_du_doan = int(mo_hinh.predict(bang_mot_dong)[0])

    xac_suat = float(mo_hinh.predict_proba(bang_mot_dong)[0][1])

    return {
        "lop_du_doan": lop_du_doan,
        "xac_suat": xac_suat,
        "muc_rui_ro": tinh_muc_rui_ro(xac_suat),
        "model_id": thong_tin["model_id"],
        "ten_model": thong_tin["model_name"],
        "phien_ban": thong_tin["version"],
        "thuat_toan": thong_tin["algorithm"],
    }


def du_doan_trieu_chung(tuoi, gioi_tinh, cac_trieu_chung):
    mo_hinh, thong_tin = nap_model("symptom")

    du_lieu = {
        "Age": tuoi,
        "Gender": gioi_tinh,
    }

    for trieu_chung in config.DANH_SACH_TRIEU_CHUNG:
        ten_cot_db = trieu_chung["cot_db"]
        ten_cot_csv = trieu_chung["cot_csv"]

        if cac_trieu_chung[ten_cot_db] == 1:
            du_lieu[ten_cot_csv] = "Yes"
        else:
            du_lieu[ten_cot_csv] = "No"

    bang_mot_dong = pd.DataFrame(du_lieu, index=[0])

    return _chay_du_doan(mo_hinh, thong_tin, bang_mot_dong)


def du_doan_lam_sang(tuoi, cac_chi_so):
    mo_hinh, thong_tin = nap_model("clinical")

    du_lieu = {}
    for chi_so in config.DANH_SACH_CHI_SO:
        du_lieu[chi_so["cot_csv"]] = cac_chi_so[chi_so["cot_db"]]
    du_lieu["Age"] = tuoi

    bang_mot_dong = pd.DataFrame(du_lieu, index=[0])

    for ten_cot in config.CAC_COT_KHONG_DUOC_BANG_0:
        bang_mot_dong[ten_cot] = bang_mot_dong[ten_cot].replace(0, np.nan)

    return _chay_du_doan(mo_hinh, thong_tin, bang_mot_dong)


if __name__ == "__main__":
    print("Thử dự đoán theo triệu chứng...")
    trieu_chung_thu = {}
    for tc in config.DANH_SACH_TRIEU_CHUNG:
        trieu_chung_thu[tc["cot_db"]] = 1
    ket_qua = du_doan_trieu_chung(45, "Male", trieu_chung_thu)
    print("   ", ket_qua)

    print()
    print("Thử dự đoán theo chỉ số lâm sàng...")
    chi_so_thu = {}
    for cs in config.DANH_SACH_CHI_SO:
        chi_so_thu[cs["cot_db"]] = cs["mac_dinh"]
    ket_qua2 = du_doan_lam_sang(50, chi_so_thu)
    print("   ", ket_qua2)
