
import os
import sys
import tkinter as tk
from tkinter import ttk

THU_MUC_GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if THU_MUC_GOC not in sys.path:
    sys.path.append(THU_MUC_GOC)

import config
from database import queries


MAU_NEN = "#f5f6f8"
MAU_CHU_CHINH = "#1f2933"
MAU_CHU_PHU = "#6b7280"
MAU_XANH = "#2563eb"
MAU_DO = "#dc2626"
MAU_VANG = "#d97706"
MAU_XANH_LA = "#16a34a"

MAU_THEO_RUI_RO = {
    "THẤP": MAU_XANH_LA,
    "TRUNG BÌNH": MAU_VANG,
    "CAO": MAU_DO,
}



def tao_tieu_de(khung_cha, chu, co_chu=16):
    nhan = ttk.Label(khung_cha, text=chu, font=("Segoe UI", co_chu, "bold"))
    return nhan


def tao_ghi_chu(khung_cha, chu):
    return ttk.Label(khung_cha, text=chu, foreground=MAU_CHU_PHU,
                     font=("Segoe UI", 9))


def tao_o_so_lieu(khung_cha, nhan, gia_tri, mau=None, co_chu=22, do_rong=None):
    if mau is None:
        mau = MAU_CHU_CHINH

    khung = ttk.LabelFrame(khung_cha, text=" " + nhan + " ", padding=(14, 10))

    nhan_so = ttk.Label(khung, text=str(gia_tri), foreground=mau,
                        font=("Segoe UI", co_chu, "bold"), anchor="center")

    if do_rong is not None:
        nhan_so.config(width=do_rong)

    nhan_so.pack(fill="x")

    return khung


def tao_bang(khung_cha, cac_cot, do_rong_cot, chieu_cao=12):
    khung_bao = ttk.Frame(khung_cha)

    bang = ttk.Treeview(khung_bao, columns=cac_cot, show="headings",
                        height=chieu_cao)

    for thu_tu in range(len(cac_cot)):
        ten_cot = cac_cot[thu_tu]
        bang.heading(ten_cot, text=ten_cot)
        bang.column(ten_cot, width=do_rong_cot[thu_tu], anchor="w")

    thanh_cuon = ttk.Scrollbar(khung_bao, orient="vertical", command=bang.yview)
    bang.configure(yscrollcommand=thanh_cuon.set)

    bang.pack(side="left", fill="both", expand=True)
    thanh_cuon.pack(side="right", fill="y")

    return khung_bao, bang


def do_du_lieu_vao_bang(bang, cac_dong):
    for ma_dong in bang.get_children():
        bang.delete(ma_dong)

    for dong in cac_dong:
        bang.insert("", "end", values=dong)


def tao_khung_cuon(khung_cha):
    canvas = tk.Canvas(khung_cha, highlightthickness=0, bg=MAU_NEN)
    thanh_cuon = ttk.Scrollbar(khung_cha, orient="vertical", command=canvas.yview)
    khung_trong = ttk.Frame(canvas)

    ma_cua_so = canvas.create_window((0, 0), window=khung_trong, anchor="nw")

    canvas.configure(yscrollcommand=thanh_cuon.set)
    canvas.pack(side="left", fill="both", expand=True)
    thanh_cuon.pack(side="right", fill="y")

    def cap_nhat_vung_cuon(su_kien=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def khop_be_ngang(su_kien):
        canvas.itemconfig(ma_cua_so, width=su_kien.width)

    khung_trong.bind("<Configure>", cap_nhat_vung_cuon)
    canvas.bind("<Configure>", khop_be_ngang)

    def cuon_bang_chuot(su_kien):
        if su_kien.num == 4:
            canvas.yview_scroll(-1, "units")
        elif su_kien.num == 5:
            canvas.yview_scroll(1, "units")
        else:
            canvas.yview_scroll(int(-su_kien.delta / 120), "units")

    def bat_dau_nghe_chuot(su_kien):
        canvas.bind_all("<MouseWheel>", cuon_bang_chuot)
        canvas.bind_all("<Button-4>", cuon_bang_chuot)
        canvas.bind_all("<Button-5>", cuon_bang_chuot)

    def ngung_nghe_chuot(su_kien):
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")

    canvas.bind("<Enter>", bat_dau_nghe_chuot)
    canvas.bind("<Leave>", ngung_nghe_chuot)

    return khung_trong


def lay_dong_dang_chon(bang):
    cac_dong_chon = bang.selection()
    if len(cac_dong_chon) == 0:
        return None
    return bang.item(cac_dong_chon[0])["values"]



DANH_SACH_GIOI_TINH_VIET = []
for _ma in config.DANH_SACH_GIOI_TINH:
    DANH_SACH_GIOI_TINH_VIET.append(config.TEN_GIOI_TINH_TIENG_VIET[_ma])


def doi_sang_ma_gioi_tinh(ten_viet):
    for ma in config.TEN_GIOI_TINH_TIENG_VIET:
        if config.TEN_GIOI_TINH_TIENG_VIET[ma] == ten_viet:
            return ma
    return "Male"


def doi_sang_ten_viet_gioi_tinh(ma):
    return config.TEN_GIOI_TINH_TIENG_VIET.get(ma, "Nam")



def lay_danh_sach_chon_benh_nhan():
    danh_sach = queries.tim_benh_nhan("")

    cac_dong_chu = []
    tra_nguoc = {}

    for benh_nhan in danh_sach:
        dong_chu = "[%d] %s" % (benh_nhan["patient_id"], benh_nhan["full_name"])
        cac_dong_chu.append(dong_chu)
        tra_nguoc[dong_chu] = benh_nhan

    return cac_dong_chu, tra_nguoc



def hien_cua_so_ket_qua(cua_so_cha, ket_qua, ten_benh_nhan, ma_danh_gia):
    cua_so = tk.Toplevel(cua_so_cha)
    cua_so.title("Kết quả dự đoán")
    cua_so.geometry("660x480")
    cua_so.configure(bg="white")

    cua_so.transient(cua_so_cha)
    cua_so.grab_set()

    khung = ttk.Frame(cua_so, padding=20)
    khung.pack(fill="both", expand=True)

    tao_tieu_de(khung, "Kết quả cho: " + ten_benh_nhan, 14).pack(anchor="w")
    tao_ghi_chu(khung, "Đã lưu vào lịch sử với mã lượt số %d" % ma_danh_gia).pack(anchor="w", pady=(2, 14))

    if ket_qua["lop_du_doan"] == 1:
        chu_ket_luan = "DƯƠNG TÍNH"
    else:
        chu_ket_luan = "ÂM TÍNH"

    mau_rui_ro = MAU_THEO_RUI_RO.get(ket_qua["muc_rui_ro"], MAU_CHU_CHINH)

    khung_so = ttk.Frame(khung)
    khung_so.pack(fill="x", pady=(0, 14))

    phan_tram = "%.1f%%" % (ket_qua["xac_suat"] * 100)

    tao_o_so_lieu(khung_so, "Kết luận", chu_ket_luan, mau_rui_ro,
                  co_chu=15, do_rong=12).pack(side="left", padx=(0, 10))

    tao_o_so_lieu(khung_so, "Xác suất", phan_tram, mau_rui_ro,
                  co_chu=15, do_rong=8).pack(side="left", padx=(0, 10))

    tao_o_so_lieu(khung_so, "Mức rủi ro", ket_qua["muc_rui_ro"], mau_rui_ro,
                  co_chu=15, do_rong=12).pack(side="left")

    ttk.Label(khung, text="Thanh xác suất:").pack(anchor="w")
    khung_thanh = tk.Canvas(khung, height=22, bg="#e5e7eb",
                            highlightthickness=0)
    khung_thanh.pack(fill="x", pady=(4, 14))

    def ve_thanh(su_kien=None):
        khung_thanh.delete("all")
        do_rong = khung_thanh.winfo_width()
        do_dai = int(do_rong * ket_qua["xac_suat"])
        khung_thanh.create_rectangle(0, 0, do_dai, 22, fill=mau_rui_ro, width=0)

    khung_thanh.bind("<Configure>", ve_thanh)

    loi_khuyen = {
        "CAO": "Nguy cơ CAO - nên đi khám chuyên khoa sớm.",
        "TRUNG BÌNH": "Nguy cơ TRUNG BÌNH - nên theo dõi và kiểm tra định kỳ.",
        "THẤP": "Nguy cơ THẤP - duy trì lối sống lành mạnh.",
    }
    ttk.Label(khung, text=loi_khuyen[ket_qua["muc_rui_ro"]],
              foreground=mau_rui_ro,
              font=("Segoe UI", 11, "bold")).pack(anchor="w")

    nhan_model = tao_ghi_chu(
        khung,
        "Model: %s | Phiên bản: %s | Thuật toán: %s | Ngưỡng phân loại: %.2f"
        % (ket_qua["ten_model"], ket_qua["phien_ban"],
           ket_qua["thuat_toan"], config.NGUONG_PHAN_LOAI),
    )
    nhan_model.config(wraplength=600, justify="left")
    nhan_model.pack(anchor="w", pady=(10, 0))

    nhan_canh_bao = tk.Message(khung, text="⚠ " + config.CANH_BAO_Y_TE,
                               width=600, bg="#fef3c7", fg="#92400e",
                               font=("Segoe UI", 9), padx=10, pady=8)
    nhan_canh_bao.pack(fill="x", pady=(12, 12))

    ttk.Button(khung, text="Đóng", command=cua_so.destroy).pack()



def ve_bieu_do_cot(canvas, cac_nhan, cac_gia_tri, cac_mau):
    canvas.delete("all")

    do_rong = canvas.winfo_width()
    chieu_cao = canvas.winfo_height()

    if do_rong <= 1 or chieu_cao <= 1:
        return

    if len(cac_gia_tri) == 0:
        return

    le_duoi = 30
    le_tren = 22
    chieu_cao_ve = chieu_cao - le_duoi - le_tren

    gia_tri_lon_nhat = max(cac_gia_tri)
    if gia_tri_lon_nhat == 0:
        gia_tri_lon_nhat = 1

    so_cot = len(cac_gia_tri)
    do_rong_o = do_rong / so_cot
    do_rong_cot = do_rong_o * 0.5

    for thu_tu in range(so_cot):
        gia_tri = cac_gia_tri[thu_tu]

        chieu_cao_cot = (gia_tri / gia_tri_lon_nhat) * chieu_cao_ve

        giua_o = do_rong_o * thu_tu + do_rong_o / 2
        x_trai = giua_o - do_rong_cot / 2
        x_phai = giua_o + do_rong_cot / 2
        y_duoi = chieu_cao - le_duoi
        y_tren = y_duoi - chieu_cao_cot

        canvas.create_rectangle(x_trai, y_tren, x_phai, y_duoi,
                                fill=cac_mau[thu_tu], width=0)

        canvas.create_text(giua_o, y_tren - 10, text=str(gia_tri),
                           font=("Segoe UI", 10, "bold"), fill=MAU_CHU_CHINH)

        canvas.create_text(giua_o, chieu_cao - le_duoi / 2,
                           text=cac_nhan[thu_tu],
                           font=("Segoe UI", 9), fill=MAU_CHU_PHU)



def kiem_tra_model(loai_model):
    thong_tin = queries.lay_model_dang_dung(loai_model)

    if thong_tin is None:
        return False, ("Chưa huấn luyện model. Hãy mở terminal tại thư mục dự án "
                       "và chạy lệnh:\n\n    python ml/train_%s.py" % loai_model)

    if not os.path.exists(thong_tin["artifact_path"]):
        return False, ("Không tìm thấy file model tại:\n%s\n\n"
                       "Hãy chạy lại:\n    python ml/train_%s.py"
                       % (thong_tin["artifact_path"], loai_model))

    return True, ""
