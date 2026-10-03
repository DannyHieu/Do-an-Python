
import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

THU_MUC_GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if THU_MUC_GOC not in sys.path:
    sys.path.append(THU_MUC_GOC)

import config
from database import queries
from giao_dien import thanh_phan_chung
from ml import predict


def tinh_tuoi(chuoi_ngay_sinh):
    from datetime import date

    if chuoi_ngay_sinh is None or str(chuoi_ngay_sinh).strip() == "":
        return None

    cac_phan = str(chuoi_ngay_sinh).split("-")
    if len(cac_phan) < 3:
        return None

    try:
        nam_sinh = int(cac_phan[0])
        thang_sinh = int(cac_phan[1])
        ngay_sinh = int(cac_phan[2])
    except ValueError:
        return None

    hom_nay = date.today()
    tuoi = hom_nay.year - nam_sinh

    if (hom_nay.month, hom_nay.day) < (thang_sinh, ngay_sinh):
        tuoi = tuoi - 1

    return tuoi


def tao_tab(so_tay, cua_so_chinh):
    khung = ttk.Frame(so_tay, padding=14)

    bien_benh_nhan = tk.StringVar()
    bien_tuoi = tk.StringVar(value="40")
    bien_gioi_tinh = tk.StringVar(value="Nam")
    bien_ghi_chu = tk.StringVar()

    tra_nguoc_benh_nhan = {"du_lieu": {}}

    cac_bien_trieu_chung = {}
    for trieu_chung in config.DANH_SACH_TRIEU_CHUNG:
        cac_bien_trieu_chung[trieu_chung["cot_db"]] = tk.IntVar(value=0)

    thanh_phan_chung.tao_tieu_de(khung, "Sàng lọc theo triệu chứng", 13).pack(anchor="w")
    thanh_phan_chung.tao_ghi_chu(
        khung,
        "Tích vào các dấu hiệu bệnh nhân đang gặp phải. Cách sàng lọc này không cần xét nghiệm máu."
    ).pack(anchor="w", pady=(2, 12))

    khung_tren = ttk.LabelFrame(khung, text=" Thông tin cơ bản ", padding=12)
    khung_tren.pack(fill="x")

    ttk.Label(khung_tren, text="Bệnh nhân *").grid(row=0, column=0, sticky="w", pady=4)
    o_benh_nhan = ttk.Combobox(khung_tren, textvariable=bien_benh_nhan,
                               state="readonly", width=38)
    o_benh_nhan.grid(row=0, column=1, sticky="w", padx=(8, 30))

    ttk.Label(khung_tren, text="Tuổi *").grid(row=0, column=2, sticky="w", pady=4)
    ttk.Entry(khung_tren, textvariable=bien_tuoi, width=10).grid(
        row=0, column=3, sticky="w", padx=(8, 30))

    ttk.Label(khung_tren, text="Giới tính *").grid(row=0, column=4, sticky="w", pady=4)
    ttk.Combobox(khung_tren, textvariable=bien_gioi_tinh,
                 values=thanh_phan_chung.DANH_SACH_GIOI_TINH_VIET,
                 state="readonly", width=12).grid(row=0, column=5, sticky="w", padx=(8, 0))

    thanh_phan_chung.tao_ghi_chu(
        khung_tren, "Tuổi và giới tính tự điền theo hồ sơ, vẫn sửa được nếu cần."
    ).grid(row=1, column=0, columnspan=6, sticky="w", pady=(6, 0))

    khung_trieu_chung = ttk.LabelFrame(
        khung, text=" Các triệu chứng (tích vào ô nếu bệnh nhân CÓ dấu hiệu đó) ",
        padding=12)
    khung_trieu_chung.pack(fill="x", pady=(12, 0))

    for thu_tu in range(len(config.DANH_SACH_TRIEU_CHUNG)):
        trieu_chung = config.DANH_SACH_TRIEU_CHUNG[thu_tu]

        if thu_tu < 7:
            cot = 0
            hang = thu_tu
        else:
            cot = 1
            hang = thu_tu - 7

        ttk.Checkbutton(
            khung_trieu_chung,
            text=trieu_chung["nhan"],
            variable=cac_bien_trieu_chung[trieu_chung["cot_db"]],
            onvalue=1,
            offvalue=0,
        ).grid(row=hang, column=cot, sticky="w", padx=(0, 60), pady=3)

    khung_duoi = ttk.Frame(khung)
    khung_duoi.pack(fill="x", pady=(14, 0))

    ttk.Label(khung_duoi, text="Ghi chú (không bắt buộc):").pack(anchor="w")
    ttk.Entry(khung_duoi, textvariable=bien_ghi_chu, width=90).pack(anchor="w", pady=(4, 12))

    khung_nut = ttk.Frame(khung_duoi)
    khung_nut.pack(anchor="w")

    nhan_canh_bao_model = ttk.Label(khung, text="", foreground=thanh_phan_chung.MAU_DO,
                                    font=("Segoe UI", 9))
    nhan_canh_bao_model.pack(anchor="w", pady=(10, 0))


    def lam_moi():
        cac_dong_chu, tra_nguoc = thanh_phan_chung.lay_danh_sach_chon_benh_nhan()
        tra_nguoc_benh_nhan["du_lieu"] = tra_nguoc

        o_benh_nhan["values"] = cac_dong_chu

        if bien_benh_nhan.get() not in cac_dong_chu:
            if len(cac_dong_chu) > 0:
                bien_benh_nhan.set(cac_dong_chu[0])
                dien_theo_ho_so()
            else:
                bien_benh_nhan.set("")

        san_sang, thong_bao = thanh_phan_chung.kiem_tra_model("symptom")
        if san_sang:
            nhan_canh_bao_model.config(text="")
        else:
            nhan_canh_bao_model.config(
                text="⚠ " + thong_bao.replace("\n\n", " ").replace("\n", " "))

    def dien_theo_ho_so(su_kien=None):
        chuoi_dang_chon = bien_benh_nhan.get()
        benh_nhan = tra_nguoc_benh_nhan["du_lieu"].get(chuoi_dang_chon)

        if benh_nhan is None:
            return

        tuoi = tinh_tuoi(benh_nhan["date_of_birth"])
        if tuoi is not None and tuoi > 0:
            bien_tuoi.set(str(tuoi))

        if benh_nhan["gender"] in config.DANH_SACH_GIOI_TINH:
            bien_gioi_tinh.set(
                thanh_phan_chung.doi_sang_ten_viet_gioi_tinh(benh_nhan["gender"]))

    def bo_tich_het():
        for ten_cot in cac_bien_trieu_chung:
            cac_bien_trieu_chung[ten_cot].set(0)

    def khi_bam_du_doan():
        chuoi_dang_chon = bien_benh_nhan.get()
        benh_nhan = tra_nguoc_benh_nhan["du_lieu"].get(chuoi_dang_chon)

        if benh_nhan is None:
            messagebox.showerror(
                "Chưa chọn bệnh nhân",
                "Hãy chọn một bệnh nhân. Nếu danh sách trống, sang tab "
                "Bệnh nhân để thêm mới trước.",
                parent=cua_so_chinh)
            return

        try:
            tuoi = int(bien_tuoi.get().strip())
        except ValueError:
            messagebox.showerror("Tuổi không hợp lệ",
                                 "Tuổi phải là một số nguyên, ví dụ 45.",
                                 parent=cua_so_chinh)
            return

        if tuoi < 1 or tuoi > 120:
            messagebox.showerror("Tuổi không hợp lệ",
                                 "Tuổi phải nằm trong khoảng 1 đến 120.",
                                 parent=cua_so_chinh)
            return

        if tuoi < 16 or tuoi > 90:
            dong_y = messagebox.askyesno(
                "Tuổi ngoài phạm vi dữ liệu",
                "Tuổi %d nằm ngoài khoảng dữ liệu huấn luyện (16 - 90).\n"
                "Kết quả có thể kém chính xác.\n\nVẫn tiếp tục dự đoán?" % tuoi,
                parent=cua_so_chinh)
            if not dong_y:
                return

        san_sang, thong_bao = thanh_phan_chung.kiem_tra_model("symptom")
        if not san_sang:
            messagebox.showerror("Chưa có model", thong_bao, parent=cua_so_chinh)
            return

        cau_tra_loi = {}
        for ten_cot in cac_bien_trieu_chung:
            cau_tra_loi[ten_cot] = cac_bien_trieu_chung[ten_cot].get()

        ma_gioi_tinh = thanh_phan_chung.doi_sang_ma_gioi_tinh(bien_gioi_tinh.get())

        try:
            ket_qua = predict.du_doan_trieu_chung(
                tuoi=tuoi,
                gioi_tinh=ma_gioi_tinh,
                cac_trieu_chung=cau_tra_loi,
            )
        except Exception as loi:
            messagebox.showerror("Không dự đoán được", str(loi),
                                 parent=cua_so_chinh)
            return

        try:
            ma_danh_gia = queries.luu_danh_gia_trieu_chung(
                ma_benh_nhan=benh_nhan["patient_id"],
                tuoi=tuoi,
                gioi_tinh=ma_gioi_tinh,
                cac_trieu_chung=cau_tra_loi,
                ket_qua=ket_qua,
                ghi_chu=bien_ghi_chu.get().strip(),
            )
        except Exception as loi:
            messagebox.showerror(
                "Lỗi khi lưu",
                "Dự đoán xong nhưng không lưu được vào database:\n\n" + str(loi),
                parent=cua_so_chinh)
            return

        thanh_phan_chung.hien_cua_so_ket_qua(
            cua_so_chinh, ket_qua, benh_nhan["full_name"], ma_danh_gia)


    ttk.Button(khung_nut, text="🔍  Dự đoán nguy cơ", command=khi_bam_du_doan,
               style="Chinh.TButton").pack(side="left", padx=(0, 8))
    ttk.Button(khung_nut, text="Bỏ tích tất cả",
               command=bo_tich_het).pack(side="left")

    o_benh_nhan.bind("<<ComboboxSelected>>", dien_theo_ho_so)

    lam_moi()

    return khung, lam_moi
