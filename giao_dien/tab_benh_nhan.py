
import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date

THU_MUC_GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if THU_MUC_GOC not in sys.path:
    sys.path.append(THU_MUC_GOC)

import config
from database import queries
from giao_dien import thanh_phan_chung


def kiem_tra_ngay_sinh(chuoi_ngay):
    chuoi_ngay = chuoi_ngay.strip()

    if chuoi_ngay == "":
        return True, ""

    cac_phan = chuoi_ngay.split("-")
    if len(cac_phan) != 3:
        return False, "Ngày sinh phải viết theo dạng NĂM-THÁNG-NGÀY, ví dụ 1990-05-20."

    try:
        nam = int(cac_phan[0])
        thang = int(cac_phan[1])
        ngay = int(cac_phan[2])
        ngay_sinh = date(nam, thang, ngay)
    except ValueError:
        return False, "Ngày sinh không hợp lệ. Ví dụ đúng: 1990-05-20"

    if ngay_sinh > date.today():
        return False, "Ngày sinh không thể ở tương lai."

    if nam < 1900:
        return False, "Năm sinh phải từ 1900 trở lên."

    return True, ""


def tao_tab(so_tay, cua_so_chinh):
    khung = ttk.Frame(so_tay, padding=14)

    bien_tu_khoa = tk.StringVar()

    bien_ho_ten = tk.StringVar()
    bien_ngay_sinh = tk.StringVar()
    bien_gioi_tinh = tk.StringVar(value="Nam")
    bien_dien_thoai = tk.StringVar()

    ma_dang_sua = {"gia_tri": None}

    khung_tim = ttk.Frame(khung)
    khung_tim.pack(fill="x", pady=(0, 10))

    thanh_phan_chung.tao_tieu_de(khung_tim, "Danh sách bệnh nhân", 13).pack(side="left")

    ttk.Label(khung_tim, text="Tìm:").pack(side="left", padx=(24, 6))
    o_tim = ttk.Entry(khung_tim, textvariable=bien_tu_khoa, width=30)
    o_tim.pack(side="left")

    khung_bang, bang = thanh_phan_chung.tao_bang(
        khung,
        cac_cot=["Mã", "Họ tên", "Ngày sinh", "Giới tính", "Điện thoại", "Ngày tạo"],
        do_rong_cot=[60, 240, 120, 100, 130, 180],
        chieu_cao=11,
    )
    khung_bang.pack(fill="both", expand=True)

    nhan_tong = thanh_phan_chung.tao_ghi_chu(khung, "")
    nhan_tong.pack(anchor="w", pady=(4, 12))

    khung_form = ttk.LabelFrame(khung, text=" Thông tin bệnh nhân ", padding=14)
    khung_form.pack(fill="x")

    ttk.Label(khung_form, text="Họ và tên *").grid(row=0, column=0, sticky="w", pady=4)
    ttk.Entry(khung_form, textvariable=bien_ho_ten, width=34).grid(
        row=0, column=1, sticky="w", padx=(8, 30))

    ttk.Label(khung_form, text="Ngày sinh").grid(row=0, column=2, sticky="w", pady=4)
    ttk.Entry(khung_form, textvariable=bien_ngay_sinh, width=18).grid(
        row=0, column=3, sticky="w", padx=(8, 4))
    thanh_phan_chung.tao_ghi_chu(khung_form, "dạng 1990-05-20").grid(
        row=0, column=4, sticky="w")

    ttk.Label(khung_form, text="Giới tính *").grid(row=1, column=0, sticky="w", pady=4)

    o_gioi_tinh = ttk.Combobox(
        khung_form,
        textvariable=bien_gioi_tinh,
        values=thanh_phan_chung.DANH_SACH_GIOI_TINH_VIET,
        state="readonly",
        width=32,
    )
    o_gioi_tinh.grid(row=1, column=1, sticky="w", padx=(8, 30))

    ttk.Label(khung_form, text="Điện thoại").grid(row=1, column=2, sticky="w", pady=4)
    ttk.Entry(khung_form, textvariable=bien_dien_thoai, width=18).grid(
        row=1, column=3, sticky="w", padx=(8, 4))

    nhan_trang_thai = ttk.Label(khung_form, text="Đang ở chế độ: THÊM MỚI",
                                foreground=thanh_phan_chung.MAU_XANH,
                                font=("Segoe UI", 9, "bold"))
    nhan_trang_thai.grid(row=2, column=0, columnspan=3, sticky="w", pady=(10, 0))

    khung_nut = ttk.Frame(khung_form)
    khung_nut.grid(row=3, column=0, columnspan=5, sticky="w", pady=(12, 0))


    def lam_moi_bang(su_kien=None):
        danh_sach = queries.tim_benh_nhan(bien_tu_khoa.get())

        cac_dong = []
        for benh_nhan in danh_sach:
            gioi_tinh_viet = config.TEN_GIOI_TINH_TIENG_VIET.get(
                benh_nhan["gender"], "")

            cac_dong.append([
                benh_nhan["patient_id"],
                benh_nhan["full_name"],
                benh_nhan["date_of_birth"] or "",
                gioi_tinh_viet,
                benh_nhan["phone"] or "",
                benh_nhan["created_at"] or "",
            ])

        thanh_phan_chung.do_du_lieu_vao_bang(bang, cac_dong)
        nhan_tong.config(text="Tìm thấy %d bệnh nhân" % len(danh_sach))

    def xoa_form():
        ma_dang_sua["gia_tri"] = None
        bien_ho_ten.set("")
        bien_ngay_sinh.set("")
        bien_gioi_tinh.set("Nam")
        bien_dien_thoai.set("")
        nhan_trang_thai.config(text="Đang ở chế độ: THÊM MỚI",
                               foreground=thanh_phan_chung.MAU_XANH)
        bang.selection_remove(bang.selection())

    def khi_chon_dong(su_kien):
        gia_tri_dong = thanh_phan_chung.lay_dong_dang_chon(bang)
        if gia_tri_dong is None:
            return

        ma_benh_nhan = int(gia_tri_dong[0])
        benh_nhan = queries.lay_benh_nhan(ma_benh_nhan)
        if benh_nhan is None:
            return

        ma_dang_sua["gia_tri"] = ma_benh_nhan
        bien_ho_ten.set(benh_nhan["full_name"])
        bien_ngay_sinh.set(benh_nhan["date_of_birth"] or "")
        bien_gioi_tinh.set(
            thanh_phan_chung.doi_sang_ten_viet_gioi_tinh(benh_nhan["gender"]))
        bien_dien_thoai.set(benh_nhan["phone"] or "")

        nhan_trang_thai.config(
            text="Đang ở chế độ: SỬA bệnh nhân mã %d" % ma_benh_nhan,
            foreground=thanh_phan_chung.MAU_VANG)

    def khi_bam_luu():
        ho_ten = bien_ho_ten.get().strip()
        chuoi_ngay_sinh = bien_ngay_sinh.get().strip()
        gioi_tinh = thanh_phan_chung.doi_sang_ma_gioi_tinh(bien_gioi_tinh.get())
        dien_thoai = bien_dien_thoai.get().strip()

        if ho_ten == "":
            messagebox.showerror("Thiếu thông tin",
                                 "Họ tên không được để trống.",
                                 parent=cua_so_chinh)
            return

        ngay_hop_le, thong_bao_loi = kiem_tra_ngay_sinh(chuoi_ngay_sinh)
        if not ngay_hop_le:
            messagebox.showerror("Ngày sinh không hợp lệ", thong_bao_loi,
                                 parent=cua_so_chinh)
            return

        if gioi_tinh not in config.DANH_SACH_GIOI_TINH:
            messagebox.showerror("Thiếu thông tin", "Hãy chọn giới tính.",
                                 parent=cua_so_chinh)
            return

        if chuoi_ngay_sinh == "":
            ngay_sinh_de_luu = None
        else:
            ngay_sinh_de_luu = chuoi_ngay_sinh

        try:
            if ma_dang_sua["gia_tri"] is None:
                ma_moi = queries.them_benh_nhan(ho_ten, ngay_sinh_de_luu,
                                                gioi_tinh, dien_thoai)
                messagebox.showinfo(
                    "Thành công",
                    "Đã thêm bệnh nhân %s với mã số %d." % (ho_ten, ma_moi),
                    parent=cua_so_chinh)
            else:
                queries.sua_benh_nhan(ma_dang_sua["gia_tri"], ho_ten,
                                      ngay_sinh_de_luu, gioi_tinh, dien_thoai)
                messagebox.showinfo("Thành công", "Đã lưu thay đổi.",
                                    parent=cua_so_chinh)
        except Exception as loi:
            messagebox.showerror("Lỗi khi lưu", str(loi), parent=cua_so_chinh)
            return

        xoa_form()
        lam_moi_bang()

    def khi_bam_xem_lich_su():
        if ma_dang_sua["gia_tri"] is None:
            messagebox.showinfo("Chưa chọn bệnh nhân",
                                "Hãy bấm chọn một dòng trong bảng trước.",
                                parent=cua_so_chinh)
            return

        benh_nhan = queries.lay_benh_nhan(ma_dang_sua["gia_tri"])
        lich_su = queries.lay_lich_su(ma_benh_nhan=ma_dang_sua["gia_tri"])

        cua_so_con = tk.Toplevel(cua_so_chinh)
        cua_so_con.title("Lịch sử đánh giá - " + benh_nhan["full_name"])
        cua_so_con.geometry("820x420")
        cua_so_con.transient(cua_so_chinh)

        khung_con = ttk.Frame(cua_so_con, padding=14)
        khung_con.pack(fill="both", expand=True)

        thanh_phan_chung.tao_tieu_de(
            khung_con, "Lịch sử của: " + benh_nhan["full_name"], 13
        ).pack(anchor="w", pady=(0, 10))

        if len(lich_su) == 0:
            ttk.Label(khung_con,
                      text="Bệnh nhân này chưa có lượt đánh giá nào.").pack()
        else:
            khung_bang_con, bang_con = thanh_phan_chung.tao_bang(
                khung_con,
                cac_cot=["Mã lượt", "Loại", "Thời điểm", "Kết luận",
                         "Xác suất", "Mức rủi ro"],
                do_rong_cot=[80, 190, 160, 110, 90, 120],
                chieu_cao=12,
            )
            khung_bang_con.pack(fill="both", expand=True)

            cac_dong = []
            for dong in lich_su:
                cac_dong.append([
                    dong["assessment_id"],
                    config.TEN_LOAI_DANH_GIA_TIENG_VIET.get(
                        dong["assessment_type"], ""),
                    dong["assessed_at"],
                    "Dương tính" if dong["predicted_class"] == 1 else "Âm tính",
                    "%.1f%%" % (dong["probability"] * 100),
                    dong["risk_level"],
                ])
            thanh_phan_chung.do_du_lieu_vao_bang(bang_con, cac_dong)

        ttk.Button(khung_con, text="Đóng",
                   command=cua_so_con.destroy).pack(pady=(10, 0))


    ttk.Button(khung_nut, text="Lưu", command=khi_bam_luu,
               style="Chinh.TButton").pack(side="left", padx=(0, 8))
    ttk.Button(khung_nut, text="Xoá form / Thêm mới",
               command=xoa_form).pack(side="left", padx=(0, 8))
    ttk.Button(khung_nut, text="Xem lịch sử của bệnh nhân này",
               command=khi_bam_xem_lich_su).pack(side="left")

    bang.bind("<<TreeviewSelect>>", khi_chon_dong)

    bien_tu_khoa.trace_add("write", lambda *doi_so: lam_moi_bang())

    lam_moi_bang()

    return khung, lam_moi_bang
