
import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date, timedelta

THU_MUC_GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if THU_MUC_GOC not in sys.path:
    sys.path.append(THU_MUC_GOC)

import config
from database import queries
from giao_dien import thanh_phan_chung

TAT_CA_BENH_NHAN = "— Tất cả bệnh nhân —"
TAT_CA_LOAI = "— Tất cả —"


def kiem_tra_ngay(chuoi_ngay, ten_o):
    chuoi_ngay = chuoi_ngay.strip()
    if chuoi_ngay == "":
        return None, ""

    cac_phan = chuoi_ngay.split("-")
    if len(cac_phan) != 3:
        return None, "Ô '%s' phải viết theo dạng NĂM-THÁNG-NGÀY, ví dụ 2026-01-31." % ten_o

    try:
        date(int(cac_phan[0]), int(cac_phan[1]), int(cac_phan[2]))
    except ValueError:
        return None, "Ô '%s' không phải là một ngày có thật." % ten_o

    return chuoi_ngay, ""


def tao_tab(so_tay, cua_so_chinh):
    khung = ttk.Frame(so_tay, padding=14)

    bien_benh_nhan = tk.StringVar(value=TAT_CA_BENH_NHAN)
    bien_loai = tk.StringVar(value=TAT_CA_LOAI)

    bien_tu_ngay = tk.StringVar(value=str(date.today() - timedelta(days=30)))
    bien_den_ngay = tk.StringVar(value=str(date.today()))

    tra_nguoc_benh_nhan = {"du_lieu": {}}

    thanh_phan_chung.tao_tieu_de(khung, "Lịch sử đánh giá", 13).pack(anchor="w", pady=(0, 10))

    khung_loc = ttk.LabelFrame(khung, text=" Bộ lọc ", padding=12)
    khung_loc.pack(fill="x")

    ttk.Label(khung_loc, text="Bệnh nhân").grid(row=0, column=0, sticky="w", pady=4)
    o_benh_nhan = ttk.Combobox(khung_loc, textvariable=bien_benh_nhan,
                               state="readonly", width=32)
    o_benh_nhan.grid(row=0, column=1, sticky="w", padx=(8, 26))

    ttk.Label(khung_loc, text="Loại đánh giá").grid(row=0, column=2, sticky="w", pady=4)
    ttk.Combobox(
        khung_loc,
        textvariable=bien_loai,
        values=[
            TAT_CA_LOAI,
            config.TEN_LOAI_DANH_GIA_TIENG_VIET[config.LOAI_DANH_GIA_TRIEU_CHUNG],
            config.TEN_LOAI_DANH_GIA_TIENG_VIET[config.LOAI_DANH_GIA_LAM_SANG],
        ],
        state="readonly",
        width=26,
    ).grid(row=0, column=3, sticky="w", padx=(8, 26))

    ttk.Label(khung_loc, text="Từ ngày").grid(row=1, column=0, sticky="w", pady=4)
    ttk.Entry(khung_loc, textvariable=bien_tu_ngay, width=16).grid(
        row=1, column=1, sticky="w", padx=(8, 26))

    ttk.Label(khung_loc, text="Đến ngày").grid(row=1, column=2, sticky="w", pady=4)
    ttk.Entry(khung_loc, textvariable=bien_den_ngay, width=16).grid(
        row=1, column=3, sticky="w", padx=(8, 26))

    khung_nut_loc = ttk.Frame(khung_loc)
    khung_nut_loc.grid(row=2, column=0, columnspan=4, sticky="w", pady=(10, 0))

    thanh_phan_chung.tao_ghi_chu(
        khung_loc, "Ngày viết theo dạng 2026-01-31. Để trống hai ô ngày để xem tất cả."
    ).grid(row=3, column=0, columnspan=4, sticky="w", pady=(8, 0))

    nhan_so_luong = thanh_phan_chung.tao_tieu_de(khung, "", 11)
    nhan_so_luong.pack(anchor="w", pady=(12, 6))

    khung_bang, bang = thanh_phan_chung.tao_bang(
        khung,
        cac_cot=["Mã lượt", "Bệnh nhân", "Loại", "Thời điểm", "Tuổi",
                 "Kết luận", "Xác suất", "Mức rủi ro", "Model"],
        do_rong_cot=[70, 165, 180, 155, 50, 90, 80, 100, 70],
        chieu_cao=14,
    )

    khung_nut_duoi = ttk.Frame(khung)
    khung_nut_duoi.pack(side="bottom", anchor="w", pady=(10, 0))

    khung_bang.pack(fill="both", expand=True)


    def lam_moi_danh_sach_benh_nhan():
        cac_dong_chu, tra_nguoc = thanh_phan_chung.lay_danh_sach_chon_benh_nhan()
        tra_nguoc_benh_nhan["du_lieu"] = tra_nguoc

        o_benh_nhan["values"] = [TAT_CA_BENH_NHAN] + cac_dong_chu

        if bien_benh_nhan.get() not in o_benh_nhan["values"]:
            bien_benh_nhan.set(TAT_CA_BENH_NHAN)

    def lay_dieu_kien_loc():
        chuoi_benh_nhan = bien_benh_nhan.get()
        if chuoi_benh_nhan == TAT_CA_BENH_NHAN:
            ma_benh_nhan = None
        else:
            benh_nhan = tra_nguoc_benh_nhan["du_lieu"].get(chuoi_benh_nhan)
            if benh_nhan is None:
                ma_benh_nhan = None
            else:
                ma_benh_nhan = benh_nhan["patient_id"]

        chuoi_loai = bien_loai.get()
        loai = None
        for ma_loai in config.TEN_LOAI_DANH_GIA_TIENG_VIET:
            if config.TEN_LOAI_DANH_GIA_TIENG_VIET[ma_loai] == chuoi_loai:
                loai = ma_loai

        tu_ngay, loi_1 = kiem_tra_ngay(bien_tu_ngay.get(), "Từ ngày")
        if loi_1 != "":
            return None, loi_1

        den_ngay, loi_2 = kiem_tra_ngay(bien_den_ngay.get(), "Đến ngày")
        if loi_2 != "":
            return None, loi_2

        if tu_ngay is not None and den_ngay is not None and tu_ngay > den_ngay:
            return None, "Ngày bắt đầu phải nhỏ hơn hoặc bằng ngày kết thúc."

        return {
            "ma_benh_nhan": ma_benh_nhan,
            "loai": loai,
            "tu_ngay": tu_ngay,
            "den_ngay": den_ngay,
        }, ""

    def lam_moi_bang():
        dieu_kien, thong_bao_loi = lay_dieu_kien_loc()

        if dieu_kien is None:
            messagebox.showerror("Bộ lọc không hợp lệ", thong_bao_loi,
                                 parent=cua_so_chinh)
            return

        lich_su = queries.lay_lich_su(**dieu_kien)

        cac_dong = []
        for dong in lich_su:
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
                dong["age_at_assessment"],
                ket_luan,
                xac_suat,
                dong["risk_level"] or "-",
                dong["version"] or "-",
            ])

        thanh_phan_chung.do_du_lieu_vao_bang(bang, cac_dong)
        nhan_so_luong.config(text="Tìm thấy %d lượt đánh giá" % len(lich_su))

    def xem_tat_ca():
        bien_benh_nhan.set(TAT_CA_BENH_NHAN)
        bien_loai.set(TAT_CA_LOAI)
        bien_tu_ngay.set("")
        bien_den_ngay.set("")
        lam_moi_bang()

    def hien_chi_tiet():
        gia_tri_dong = thanh_phan_chung.lay_dong_dang_chon(bang)

        if gia_tri_dong is None:
            messagebox.showinfo("Chưa chọn dòng",
                                "Hãy bấm chọn một dòng trong bảng trước.",
                                parent=cua_so_chinh)
            return

        ma_danh_gia = int(gia_tri_dong[0])
        chi_tiet = queries.lay_chi_tiet_danh_gia(ma_danh_gia)

        if chi_tiet is None:
            messagebox.showerror("Không tìm thấy",
                                 "Không tìm thấy lượt đánh giá này.",
                                 parent=cua_so_chinh)
            return

        phan_chung = chi_tiet["chung"]
        phan_chi_tiet = chi_tiet["chi_tiet"]

        cua_so = tk.Toplevel(cua_so_chinh)
        cua_so.title("Chi tiết lượt đánh giá số %d" % ma_danh_gia)
        cua_so.geometry("700x640")
        cua_so.transient(cua_so_chinh)

        khung_ct = ttk.Frame(cua_so, padding=16)
        khung_ct.pack(fill="both", expand=True)

        thanh_phan_chung.tao_tieu_de(
            khung_ct, "Lượt đánh giá số %d" % ma_danh_gia, 14
        ).pack(anchor="w", pady=(0, 10))

        khung_chung = ttk.LabelFrame(khung_ct, text=" Thông tin chung ", padding=10)
        khung_chung.pack(fill="x")

        cac_thong_tin = [
            ("Bệnh nhân", phan_chung["full_name"]),
            ("Điện thoại", phan_chung["phone"] or "(không có)"),
            ("Loại đánh giá",
             config.TEN_LOAI_DANH_GIA_TIENG_VIET.get(phan_chung["assessment_type"], "")),
            ("Thời điểm", phan_chung["assessed_at"]),
            ("Tuổi lúc đánh giá", phan_chung["age_at_assessment"]),
            ("Giới tính lúc đánh giá",
             config.TEN_GIOI_TINH_TIENG_VIET.get(phan_chung["gender_at_assessment"], "?")),
            ("Ghi chú", phan_chung["notes"] or "(không có)"),
        ]

        for thu_tu in range(len(cac_thong_tin)):
            ten, gia_tri = cac_thong_tin[thu_tu]
            ttk.Label(khung_chung, text=ten + ":").grid(
                row=thu_tu, column=0, sticky="w", pady=2, padx=(0, 12))
            ttk.Label(khung_chung, text=str(gia_tri),
                      font=("Segoe UI", 10, "bold")).grid(
                row=thu_tu, column=1, sticky="w", pady=2)

        khung_kq = ttk.LabelFrame(khung_ct, text=" Kết quả model đã trả về ", padding=10)
        khung_kq.pack(fill="x", pady=(12, 0))

        if phan_chung["predicted_class"] == 1:
            ket_luan = "DƯƠNG TÍNH"
        else:
            ket_luan = "ÂM TÍNH"

        mau = thanh_phan_chung.MAU_THEO_RUI_RO.get(
            phan_chung["risk_level"], thanh_phan_chung.MAU_CHU_CHINH)

        ttk.Label(khung_kq,
                  text="%s  -  %.1f%%  -  mức %s"
                       % (ket_luan, phan_chung["probability"] * 100,
                          phan_chung["risk_level"]),
                  foreground=mau,
                  font=("Segoe UI", 13, "bold")).pack(anchor="w")

        thanh_phan_chung.tao_ghi_chu(
            khung_kq,
            "Model: %s | Phiên bản: %s | Thuật toán: %s | Ngưỡng: %.2f"
            % (phan_chung["model_name"], phan_chung["version"],
               phan_chung["algorithm"], phan_chung["classification_threshold"])
        ).pack(anchor="w", pady=(4, 0))

        khung_du_lieu = ttk.LabelFrame(khung_ct, text=" Dữ liệu đã nhập lúc đánh giá ",
                                       padding=10)
        khung_du_lieu.pack(fill="both", expand=True, pady=(12, 0))

        if phan_chi_tiet is None:
            ttk.Label(khung_du_lieu,
                      text="Không tìm thấy dữ liệu chi tiết.").pack()

        elif phan_chung["assessment_type"] == config.LOAI_DANH_GIA_TRIEU_CHUNG:
            khung_bang_ct, bang_ct = thanh_phan_chung.tao_bang(
                khung_du_lieu,
                cac_cot=["Triệu chứng", "Trả lời"],
                do_rong_cot=[420, 100],
                chieu_cao=11,
            )
            khung_bang_ct.pack(fill="both", expand=True)

            cac_dong_ct = []
            for trieu_chung in config.DANH_SACH_TRIEU_CHUNG:
                if phan_chi_tiet[trieu_chung["cot_db"]] == 1:
                    tra_loi = "Có"
                else:
                    tra_loi = "Không"
                cac_dong_ct.append([trieu_chung["nhan"], tra_loi])

            thanh_phan_chung.do_du_lieu_vao_bang(bang_ct, cac_dong_ct)

        else:
            khung_bang_ct, bang_ct = thanh_phan_chung.tao_bang(
                khung_du_lieu,
                cac_cot=["Chỉ số", "Giá trị"],
                do_rong_cot=[420, 100],
                chieu_cao=9,
            )
            khung_bang_ct.pack(fill="both", expand=True)

            cac_dong_ct = []
            for chi_so in config.DANH_SACH_CHI_SO:
                gia_tri = phan_chi_tiet[chi_so["cot_db"]]
                if gia_tri == 0 and chi_so["cot_db"] != "pregnancies":
                    hien_thi = "0  (thiếu dữ liệu)"
                else:
                    hien_thi = str(gia_tri)
                cac_dong_ct.append([chi_so["nhan"], hien_thi])

            thanh_phan_chung.do_du_lieu_vao_bang(bang_ct, cac_dong_ct)

        ttk.Button(khung_ct, text="Đóng",
                   command=cua_so.destroy).pack(pady=(12, 0))

    def lam_moi_tat_ca():
        lam_moi_danh_sach_benh_nhan()
        lam_moi_bang()


    ttk.Button(khung_nut_loc, text="Lọc", command=lam_moi_bang,
               style="Chinh.TButton").pack(side="left", padx=(0, 8))
    ttk.Button(khung_nut_loc, text="Xem tất cả",
               command=xem_tat_ca).pack(side="left")

    ttk.Button(khung_nut_duoi, text="Xem chi tiết lượt đang chọn",
               command=hien_chi_tiet,
               style="Chinh.TButton").pack(side="left")
    thanh_phan_chung.tao_ghi_chu(
        khung_nut_duoi, "  hoặc bấm đúp chuột vào một dòng trong bảng"
    ).pack(side="left", padx=(10, 0))

    bang.bind("<Double-1>", lambda su_kien: hien_chi_tiet())

    lam_moi_tat_ca()

    return khung, lam_moi_tat_ca
