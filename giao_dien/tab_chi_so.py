
import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

THU_MUC_GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if THU_MUC_GOC not in sys.path:
    sys.path.append(THU_MUC_GOC)

import config
from database import queries
from giao_dien import tab_trieu_chung
from giao_dien import thanh_phan_chung
from ml import predict


def tao_tab(so_tay, cua_so_chinh):
    khung = ttk.Frame(so_tay, padding=14)

    bien_benh_nhan = tk.StringVar()
    bien_tuoi = tk.StringVar(value="40")
    bien_ghi_chu = tk.StringVar()

    tra_nguoc_benh_nhan = {"du_lieu": {}}

    cac_bien_chi_so = {}
    for chi_so in config.DANH_SACH_CHI_SO:
        cac_bien_chi_so[chi_so["cot_db"]] = tk.StringVar(
            value=str(chi_so["mac_dinh"]))

    cac_o_nhap = {}

    thanh_phan_chung.tao_tieu_de(khung, "Đánh giá theo chỉ số lâm sàng", 13).pack(anchor="w")
    thanh_phan_chung.tao_ghi_chu(
        khung,
        "Nhập các chỉ số từ kết quả xét nghiệm. Chỉ số nào không đo được thì để 0."
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

    ttk.Label(khung_tren, text="Giới tính").grid(row=0, column=4, sticky="w", pady=4)
    nhan_gioi_tinh = ttk.Label(khung_tren, text="-",
                               font=("Segoe UI", 10, "bold"))
    nhan_gioi_tinh.grid(row=0, column=5, sticky="w", padx=(8, 0))

    thanh_phan_chung.tao_ghi_chu(
        khung_tren,
        "Giới tính lấy thẳng từ hồ sơ. Model lâm sàng không dùng giới tính, "
        "nhưng vẫn được lưu lại để tra cứu."
    ).grid(row=1, column=0, columnspan=6, sticky="w", pady=(6, 0))

    khung_chi_so = ttk.LabelFrame(khung, text=" Các chỉ số xét nghiệm ", padding=12)
    khung_chi_so.pack(fill="x", pady=(12, 0))

    for thu_tu in range(len(config.DANH_SACH_CHI_SO)):
        chi_so = config.DANH_SACH_CHI_SO[thu_tu]

        if thu_tu < 4:
            cot_goc = 0
            hang_goc = thu_tu * 2
        else:
            cot_goc = 2
            hang_goc = (thu_tu - 4) * 2

        ttk.Label(khung_chi_so, text=chi_so["nhan"]).grid(
            row=hang_goc, column=cot_goc, sticky="w", pady=(6, 0), padx=(0, 10))

        o_nhap = ttk.Spinbox(
            khung_chi_so,
            textvariable=cac_bien_chi_so[chi_so["cot_db"]],
            from_=chi_so["min"],
            to=chi_so["max"],
            increment=chi_so["buoc"],
            width=12,
        )
        o_nhap.grid(row=hang_goc, column=cot_goc + 1, sticky="w",
                    pady=(6, 0), padx=(0, 60))
        cac_o_nhap[chi_so["cot_db"]] = o_nhap

        thanh_phan_chung.tao_ghi_chu(khung_chi_so, chi_so["goi_y"]).grid(
            row=hang_goc + 1, column=cot_goc, columnspan=2, sticky="w",
            pady=(0, 2))

    khung_duoi = ttk.Frame(khung)
    khung_duoi.pack(fill="x", pady=(14, 0))

    ttk.Label(khung_duoi, text="Ghi chú (không bắt buộc):").pack(anchor="w")
    ttk.Entry(khung_duoi, textvariable=bien_ghi_chu, width=90).pack(anchor="w", pady=(4, 12))

    khung_nut = ttk.Frame(khung_duoi)
    khung_nut.pack(anchor="w")

    nhan_canh_bao_model = ttk.Label(khung, text="",
                                    foreground=thanh_phan_chung.MAU_DO,
                                    font=("Segoe UI", 9))
    nhan_canh_bao_model.pack(anchor="w", pady=(10, 0))


    def lam_moi():
        cac_dong_chu, tra_nguoc = thanh_phan_chung.lay_danh_sach_chon_benh_nhan()
        tra_nguoc_benh_nhan["du_lieu"] = tra_nguoc
        o_benh_nhan["values"] = cac_dong_chu

        if bien_benh_nhan.get() not in cac_dong_chu:
            if len(cac_dong_chu) > 0:
                bien_benh_nhan.set(cac_dong_chu[0])
            else:
                bien_benh_nhan.set("")

        dien_theo_ho_so()

        san_sang, thong_bao = thanh_phan_chung.kiem_tra_model("clinical")
        if san_sang:
            nhan_canh_bao_model.config(text="")
        else:
            nhan_canh_bao_model.config(
                text="⚠ " + thong_bao.replace("\n\n", " ").replace("\n", " "))

    def dien_theo_ho_so(su_kien=None):
        benh_nhan = tra_nguoc_benh_nhan["du_lieu"].get(bien_benh_nhan.get())

        if benh_nhan is None:
            nhan_gioi_tinh.config(text="-")
            return

        tuoi = tab_trieu_chung.tinh_tuoi(benh_nhan["date_of_birth"])
        if tuoi is not None and tuoi > 0:
            bien_tuoi.set(str(tuoi))

        gioi_tinh = benh_nhan["gender"]
        nhan_gioi_tinh.config(
            text=config.TEN_GIOI_TINH_TIENG_VIET.get(gioi_tinh, "Chưa rõ"))

        o_mang_thai = cac_o_nhap["pregnancies"]
        if gioi_tinh == "Male":
            cac_bien_chi_so["pregnancies"].set("0.0")
            o_mang_thai.config(state="disabled")
        else:
            o_mang_thai.config(state="normal")

    def dat_lai_mac_dinh():
        for chi_so in config.DANH_SACH_CHI_SO:
            cac_bien_chi_so[chi_so["cot_db"]].set(str(chi_so["mac_dinh"]))
        dien_theo_ho_so()

    def doc_cac_chi_so():
        gia_tri = {}

        for chi_so in config.DANH_SACH_CHI_SO:
            chuoi = cac_bien_chi_so[chi_so["cot_db"]].get().strip()

            if chuoi == "":
                return None, "Ô '%s' đang để trống. Nếu không đo được, hãy nhập 0." % chi_so["nhan"]

            chuoi = chuoi.replace(",", ".")
            try:
                so = float(chuoi)
            except ValueError:
                return None, "Ô '%s' phải là một con số." % chi_so["nhan"]

            if so < chi_so["min"] or so > chi_so["max"]:
                return None, ("Ô '%s' phải nằm trong khoảng %g đến %g."
                              % (chi_so["nhan"], chi_so["min"], chi_so["max"]))

            gia_tri[chi_so["cot_db"]] = so

        return gia_tri, ""

    def khi_bam_du_doan():
        benh_nhan = tra_nguoc_benh_nhan["du_lieu"].get(bien_benh_nhan.get())
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
                                 "Tuổi phải là một số nguyên, ví dụ 50.",
                                 parent=cua_so_chinh)
            return

        if tuoi < 1 or tuoi > 120:
            messagebox.showerror("Tuổi không hợp lệ",
                                 "Tuổi phải nằm trong khoảng 1 đến 120.",
                                 parent=cua_so_chinh)
            return

        cac_chi_so, thong_bao_loi = doc_cac_chi_so()
        if cac_chi_so is None:
            messagebox.showerror("Dữ liệu không hợp lệ", thong_bao_loi,
                                 parent=cua_so_chinh)
            return

        so_o_bang_0 = 0
        for chi_so in config.DANH_SACH_CHI_SO:
            if chi_so["cot_db"] == "pregnancies":
                continue
            if cac_chi_so[chi_so["cot_db"]] == 0:
                so_o_bang_0 = so_o_bang_0 + 1

        if so_o_bang_0 >= 3:
            dong_y = messagebox.askyesno(
                "Nhiều chỉ số đang để 0",
                "Có %d chỉ số đang để 0, tức là thiếu dữ liệu.\n"
                "Càng nhiều ô thiếu thì kết quả càng kém tin cậy.\n\n"
                "Vẫn tiếp tục dự đoán?" % so_o_bang_0,
                parent=cua_so_chinh)
            if not dong_y:
                return

        san_sang, thong_bao = thanh_phan_chung.kiem_tra_model("clinical")
        if not san_sang:
            messagebox.showerror("Chưa có model", thong_bao, parent=cua_so_chinh)
            return

        try:
            ket_qua = predict.du_doan_lam_sang(tuoi=tuoi, cac_chi_so=cac_chi_so)
        except Exception as loi:
            messagebox.showerror("Không dự đoán được", str(loi),
                                 parent=cua_so_chinh)
            return

        try:
            ma_danh_gia = queries.luu_danh_gia_lam_sang(
                ma_benh_nhan=benh_nhan["patient_id"],
                tuoi=tuoi,
                gioi_tinh=benh_nhan["gender"],
                cac_chi_so=cac_chi_so,
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
    ttk.Button(khung_nut, text="Đặt lại giá trị mặc định",
               command=dat_lai_mac_dinh).pack(side="left")

    o_benh_nhan.bind("<<ComboboxSelected>>", dien_theo_ho_so)

    lam_moi()

    return khung, lam_moi
