
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


def tao_tab(so_tay, cua_so_chinh):
    khung = ttk.Frame(so_tay, padding=14)

    thanh_phan_chung.tao_tieu_de(khung, "Tổng quan hệ thống", 13).pack(anchor="w")
    thanh_phan_chung.tao_ghi_chu(
        khung, "Mọi con số dưới đây lấy trực tiếp từ database, không tính lại từ file CSV."
    ).pack(anchor="w", pady=(2, 12))

    khung_so_lieu = ttk.Frame(khung)
    khung_so_lieu.pack(fill="x")

    cac_nhan_so = {}

    danh_sach_o = [
        ("Tổng bệnh nhân", "benh_nhan", thanh_phan_chung.MAU_CHU_CHINH),
        ("Tổng lượt đánh giá", "danh_gia", thanh_phan_chung.MAU_CHU_CHINH),
        ("Kết quả Dương tính", "duong_tinh", thanh_phan_chung.MAU_DO),
        ("Kết quả Âm tính", "am_tinh", thanh_phan_chung.MAU_XANH_LA),
    ]

    for nhan, khoa, mau in danh_sach_o:
        o = ttk.LabelFrame(khung_so_lieu, text=" " + nhan + " ", padding=(18, 12))
        o.pack(side="left", padx=(0, 12))

        nhan_so = ttk.Label(o, text="0", foreground=mau,
                            font=("Segoe UI", 22, "bold"))
        nhan_so.pack()
        cac_nhan_so[khoa] = nhan_so

    nhan_ty_le = thanh_phan_chung.tao_ghi_chu(khung, "")
    nhan_ty_le.pack(anchor="w", pady=(8, 0))

    khung_bieu_do = ttk.Frame(khung)
    khung_bieu_do.pack(fill="x", pady=(14, 0))

    khung_trai = ttk.LabelFrame(khung_bieu_do, text=" Số lượt theo loại đánh giá ",
                                padding=10)
    khung_trai.pack(side="left", fill="both", expand=True, padx=(0, 10))

    canvas_loai = tk.Canvas(khung_trai, height=180, bg="white",
                            highlightthickness=0)
    canvas_loai.pack(fill="both", expand=True)

    khung_phai = ttk.LabelFrame(khung_bieu_do, text=" Phân bố mức rủi ro ",
                                padding=10)
    khung_phai.pack(side="left", fill="both", expand=True)

    canvas_rui_ro = tk.Canvas(khung_phai, height=180, bg="white",
                              highlightthickness=0)
    canvas_rui_ro.pack(fill="both", expand=True)

    thanh_phan_chung.tao_tieu_de(khung, "10 lượt đánh giá gần nhất", 11).pack(
        anchor="w", pady=(16, 6))

    khung_bang, bang = thanh_phan_chung.tao_bang(
        khung,
        cac_cot=["Mã lượt", "Bệnh nhân", "Loại", "Thời điểm",
                 "Kết luận", "Xác suất", "Mức rủi ro"],
        do_rong_cot=[70, 200, 180, 150, 100, 90, 120],
        chieu_cao=9,
    )
    khung_bang.pack(fill="both", expand=True)

    nhan_trong = ttk.Label(
        khung,
        text="Chưa có lượt đánh giá nào. Sang tab Bệnh nhân để tạo hồ sơ, "
             "rồi thực hiện một lượt đánh giá.",
        foreground=thanh_phan_chung.MAU_CHU_PHU)

    du_lieu_bieu_do = {
        "loai": {"nhan": [], "gia_tri": [], "mau": []},
        "rui_ro": {"nhan": [], "gia_tri": [], "mau": []},
    }


    def ve_lai_bieu_do(su_kien=None):
        thanh_phan_chung.ve_bieu_do_cot(
            canvas_loai,
            du_lieu_bieu_do["loai"]["nhan"],
            du_lieu_bieu_do["loai"]["gia_tri"],
            du_lieu_bieu_do["loai"]["mau"],
        )
        thanh_phan_chung.ve_bieu_do_cot(
            canvas_rui_ro,
            du_lieu_bieu_do["rui_ro"]["nhan"],
            du_lieu_bieu_do["rui_ro"]["gia_tri"],
            du_lieu_bieu_do["rui_ro"]["mau"],
        )

    def lam_moi():
        so_benh_nhan = queries.dem_benh_nhan()
        so_danh_gia = queries.dem_danh_gia()
        ket_qua = queries.dem_theo_ket_qua()

        cac_nhan_so["benh_nhan"].config(text=str(so_benh_nhan))
        cac_nhan_so["danh_gia"].config(text=str(so_danh_gia))
        cac_nhan_so["duong_tinh"].config(text=str(ket_qua["duong_tinh"]))
        cac_nhan_so["am_tinh"].config(text=str(ket_qua["am_tinh"]))

        tong_co_ket_qua = ket_qua["duong_tinh"] + ket_qua["am_tinh"]
        if tong_co_ket_qua > 0:
            ty_le = ket_qua["duong_tinh"] / tong_co_ket_qua * 100
            nhan_ty_le.config(
                text="Tỷ lệ Dương tính: %.1f%% trên tổng %d lượt có kết quả."
                     % (ty_le, tong_co_ket_qua))
        else:
            nhan_ty_le.config(text="Chưa có lượt đánh giá nào có kết quả.")

        dem_loai = queries.dem_theo_loai()
        du_lieu_bieu_do["loai"] = {
            "nhan": ["Triệu chứng", "Chỉ số lâm sàng"],
            "gia_tri": [
                dem_loai[config.LOAI_DANH_GIA_TRIEU_CHUNG],
                dem_loai[config.LOAI_DANH_GIA_LAM_SANG],
            ],
            "mau": [thanh_phan_chung.MAU_XANH, "#7c3aed"],
        }

        dem_rui_ro = queries.dem_theo_muc_rui_ro()
        du_lieu_bieu_do["rui_ro"] = {
            "nhan": ["THẤP", "TRUNG BÌNH", "CAO"],
            "gia_tri": [
                dem_rui_ro["THẤP"],
                dem_rui_ro["TRUNG BÌNH"],
                dem_rui_ro["CAO"],
            ],
            "mau": [
                thanh_phan_chung.MAU_XANH_LA,
                thanh_phan_chung.MAU_VANG,
                thanh_phan_chung.MAU_DO,
            ],
        }

        ve_lai_bieu_do()

        lich_su = queries.lay_lich_su()

        lich_su_gan_day = lich_su[:10]

        cac_dong = []
        for dong in lich_su_gan_day:
            if dong["predicted_class"] == 1:
                ket_luan = "Dương tính"
            else:
                ket_luan = "Âm tính"

            if dong["probability"] is None:
                xac_suat = "-"
            else:
                xac_suat = "%.1f%%" % (dong["probability"] * 100)

            cac_dong.append([
                dong["assessment_id"],
                dong["full_name"],
                config.TEN_LOAI_DANH_GIA_TIENG_VIET.get(dong["assessment_type"], ""),
                dong["assessed_at"],
                ket_luan,
                xac_suat,
                dong["risk_level"] or "-",
            ])

        thanh_phan_chung.do_du_lieu_vao_bang(bang, cac_dong)

        if len(lich_su) == 0:
            nhan_trong.pack(anchor="w", pady=(6, 0))
        else:
            nhan_trong.pack_forget()

    canvas_loai.bind("<Configure>", ve_lai_bieu_do)
    canvas_rui_ro.bind("<Configure>", ve_lai_bieu_do)

    lam_moi()

    return khung, lam_moi
