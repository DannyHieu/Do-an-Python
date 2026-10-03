
import json
import os
import sys
import tkinter as tk
from tkinter import ttk

THU_MUC_GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if THU_MUC_GOC not in sys.path:
    sys.path.append(THU_MUC_GOC)

import config
from database import queries
from giao_dien import thanh_phan_chung


def doc_bang_so_sanh(ten_file):
    import csv

    duong_dan = os.path.join(config.THU_MUC_MODEL, ten_file)

    if not os.path.exists(duong_dan):
        return None, None

    with open(duong_dan, "r", encoding="utf-8-sig") as tep:
        bo_doc = csv.reader(tep)
        tat_ca = list(bo_doc)

    if len(tat_ca) == 0:
        return None, None

    tieu_de = tat_ca[0]
    cac_dong = tat_ca[1:]

    return tieu_de, cac_dong


def tao_khoi_mot_model(khung_cha, khoa_model, ten_hien_thi, ten_file_so_sanh, mo_ta):
    khung = ttk.LabelFrame(khung_cha, text=" " + ten_hien_thi + " ", padding=12)
    khung.pack(fill="both", expand=True, pady=(0, 12))

    thanh_phan_chung.tao_ghi_chu(khung, mo_ta).pack(anchor="w", pady=(0, 10))

    nhan_thong_tin = ttk.Label(khung, text="", font=("Segoe UI", 10, "bold"))
    nhan_thong_tin.pack(anchor="w")

    nhan_duong_dan = thanh_phan_chung.tao_ghi_chu(khung, "")
    nhan_duong_dan.pack(anchor="w", pady=(2, 10))

    nhan_diem = ttk.Label(khung, text="", font=("Segoe UI", 10))
    nhan_diem.pack(anchor="w", pady=(0, 10))

    khung_bang, bang = thanh_phan_chung.tao_bang(
        khung,
        cac_cot=["Thuật toán", "F1 kiểm tra chéo", "Accuracy",
                 "Precision", "Recall", "F1", "ROC-AUC"],
        do_rong_cot=[180, 140, 100, 100, 100, 100, 100],
        chieu_cao=5,
    )
    khung_bang.pack(fill="x", pady=(0, 6))

    nhan_ghi_chu_bang = thanh_phan_chung.tao_ghi_chu(khung, "")
    nhan_ghi_chu_bang.pack(anchor="w")

    def lam_moi():
        thong_tin = queries.lay_model_dang_dung(khoa_model)

        if thong_tin is None:
            nhan_thong_tin.config(
                text="⚠ Chưa huấn luyện model này.",
                foreground=thanh_phan_chung.MAU_DO)
            nhan_duong_dan.config(
                text="Hãy chạy lệnh:  python ml/train_%s.py" % khoa_model)
            nhan_diem.config(text="")
            thanh_phan_chung.do_du_lieu_vao_bang(bang, [])
            nhan_ghi_chu_bang.config(text="")
            return

        ngay_train = str(thong_tin["trained_at"]).split(" ")[0]
        nhan_thong_tin.config(
            text="Thuật toán: %s     |     Phiên bản: %s     |     Huấn luyện ngày: %s"
                 % (thong_tin["algorithm"], thong_tin["version"], ngay_train),
            foreground=thanh_phan_chung.MAU_CHU_CHINH)

        if os.path.exists(thong_tin["artifact_path"]):
            nhan_duong_dan.config(
                text="✓ File model: " + thong_tin["artifact_path"],
                foreground=thanh_phan_chung.MAU_XANH_LA)
        else:
            nhan_duong_dan.config(
                text="✗ Không tìm thấy file: " + thong_tin["artifact_path"],
                foreground=thanh_phan_chung.MAU_DO)

        if thong_tin["metrics_json"]:
            try:
                cac_diem = json.loads(thong_tin["metrics_json"])
                nhan_diem.config(
                    text="Accuracy: %s     Precision: %s     Recall: %s     "
                         "F1: %s     ROC-AUC: %s"
                         % (cac_diem.get("Accuracy", "-"),
                            cac_diem.get("Precision", "-"),
                            cac_diem.get("Recall", "-"),
                            cac_diem.get("F1", "-"),
                            cac_diem.get("ROC-AUC", "-")))
            except Exception:
                nhan_diem.config(text="Không đọc được điểm số đã lưu.")
        else:
            nhan_diem.config(text="")

        tieu_de, cac_dong = doc_bang_so_sanh(ten_file_so_sanh)

        if cac_dong is None:
            thanh_phan_chung.do_du_lieu_vao_bang(bang, [])
            nhan_ghi_chu_bang.config(
                text="Chưa có file bảng so sánh. Chạy lại script huấn luyện để tạo.")
        else:
            thanh_phan_chung.do_du_lieu_vao_bang(bang, cac_dong)
            nhan_ghi_chu_bang.config(
                text="Thuật toán có điểm F1 cao nhất được chọn làm model chính thức. "
                     "F1 là điểm cân bằng giữa Precision và Recall.")

    return lam_moi


def tao_tab(so_tay, cua_so_chinh):
    khung_vo = ttk.Frame(so_tay)
    khung_ngoai = thanh_phan_chung.tao_khung_cuon(khung_vo)
    khung_ngoai.configure(padding=14)

    thanh_phan_chung.tao_tieu_de(khung_ngoai, "Thông tin model", 13).pack(anchor="w")
    thanh_phan_chung.tao_ghi_chu(
        khung_ngoai,
        "Ứng dụng dùng hai model độc lập, mỗi model học từ một bộ dữ liệu khác nhau "
        "và giải quyết một bài toán riêng. Chúng không dùng chung dữ liệu."
    ).pack(anchor="w", pady=(2, 12))

    lam_moi_model_1 = tao_khoi_mot_model(
        khung_ngoai,
        khoa_model="symptom",
        ten_hien_thi="Model 1 - Sàng lọc theo triệu chứng",
        ten_file_so_sanh=config.TEN_FILE_SO_SANH_TRIEU_CHUNG,
        mo_ta="Học từ diabetes_data.csv (520 dòng, đã xoá 269 dòng trùng). "
              "Đầu vào: tuổi, giới tính và 14 triệu chứng Có/Không.",
    )

    lam_moi_model_2 = tao_khoi_mot_model(
        khung_ngoai,
        khoa_model="clinical",
        ten_hien_thi="Model 2 - Đánh giá theo chỉ số lâm sàng",
        ten_file_so_sanh=config.TEN_FILE_SO_SANH_LAM_SANG,
        mo_ta="Học từ diabetes.csv (768 dòng). Đầu vào: 8 chỉ số y tế. "
              "Các giá trị 0 vô lý được coi là thiếu dữ liệu và điền bù bằng trung vị.",
    )

    khung_giai_thich = ttk.LabelFrame(
        khung_ngoai, text=" Giải thích các chỉ số đánh giá ", padding=12)
    khung_giai_thich.pack(fill="x")

    giai_thich = [
        ("Accuracy", "Tỷ lệ đoán đúng trên tổng số ca",
         "Dễ hiểu nhất, nhưng dễ đánh lừa khi dữ liệu lệch"),
        ("Precision", "Model báo 'có bệnh' thì bao nhiêu % đúng",
         "Cao thì ít báo động giả"),
        ("Recall", "Người thực sự có bệnh, model bắt được bao nhiêu %",
         "QUAN TRỌNG NHẤT trong y tế - bỏ sót nguy hiểm hơn báo nhầm"),
        ("F1", "Điểm cân bằng giữa Precision và Recall",
         "Dùng để chọn model tốt nhất"),
        ("ROC-AUC", "Khả năng phân biệt người bệnh và không bệnh",
         "Từ 0.5 (đoán bừa) đến 1.0 (hoàn hảo)"),
    ]

    for thu_tu in range(len(giai_thich)):
        ten, nghia, vi_sao = giai_thich[thu_tu]

        ttk.Label(khung_giai_thich, text=ten,
                  font=("Segoe UI", 10, "bold")).grid(
            row=thu_tu, column=0, sticky="w", pady=3, padx=(0, 16))
        ttk.Label(khung_giai_thich, text=nghia).grid(
            row=thu_tu, column=1, sticky="w", pady=3, padx=(0, 20))
        thanh_phan_chung.tao_ghi_chu(khung_giai_thich, vi_sao).grid(
            row=thu_tu, column=2, sticky="w", pady=3)

    def lam_moi_tat_ca():
        lam_moi_model_1()
        lam_moi_model_2()

    lam_moi_tat_ca()

    return khung_vo, lam_moi_tat_ca
