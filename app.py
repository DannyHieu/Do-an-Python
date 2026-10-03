
import os
import sys
import tkinter as tk
from tkinter import ttk

THU_MUC_GOC = os.path.dirname(os.path.abspath(__file__))
if THU_MUC_GOC not in sys.path:
    sys.path.append(THU_MUC_GOC)

import config
from database import db
from giao_dien import thanh_phan_chung
from giao_dien import tab_benh_nhan
from giao_dien import tab_chi_so
from giao_dien import tab_lich_su
from giao_dien import tab_model
from giao_dien import tab_tong_quan
from giao_dien import tab_trieu_chung


def tao_kieu_dang(cua_so):
    kieu = ttk.Style(cua_so)

    try:
        kieu.theme_use("clam")
    except Exception:
        pass

    kieu.configure(".", font=("Segoe UI", 10))
    kieu.configure("TLabel", background=thanh_phan_chung.MAU_NEN)
    kieu.configure("TFrame", background=thanh_phan_chung.MAU_NEN)
    kieu.configure("TLabelframe", background=thanh_phan_chung.MAU_NEN)
    kieu.configure("TLabelframe.Label", background=thanh_phan_chung.MAU_NEN,
                   foreground=thanh_phan_chung.MAU_CHU_PHU)
    kieu.configure("TCheckbutton", background=thanh_phan_chung.MAU_NEN)
    kieu.configure("TNotebook.Tab", padding=(14, 8))

    kieu.configure("Chinh.TButton", font=("Segoe UI", 10, "bold"))

    kieu.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
    kieu.configure("Treeview", rowheight=24)


def main():
    db.tao_bang()

    cua_so = tk.Tk()
    cua_so.title("Ứng dụng sàng lọc nguy cơ tiểu đường")

    cua_so.geometry("1150x760")

    cua_so.minsize(1000, 650)
    cua_so.configure(bg=thanh_phan_chung.MAU_NEN)

    tao_kieu_dang(cua_so)

    khung_dau = ttk.Frame(cua_so, padding=(16, 12, 16, 8))
    khung_dau.pack(fill="x")

    thanh_phan_chung.tao_tieu_de(
        khung_dau, "Ứng dụng hỗ trợ sàng lọc nguy cơ tiểu đường", 15
    ).pack(anchor="w")

    thanh_phan_chung.tao_ghi_chu(
        khung_dau,
        "Sàng lọc theo triệu chứng và đánh giá theo chỉ số lâm sàng "
        "bằng hai model Machine Learning độc lập"
    ).pack(anchor="w")

    khung_chan = ttk.Frame(cua_so, padding=(16, 0, 16, 10))
    khung_chan.pack(side="bottom", fill="x")

    tk.Message(khung_chan, text="⚠ " + config.CANH_BAO_Y_TE,
               width=1100, bg="#fef3c7", fg="#92400e",
               font=("Segoe UI", 9), padx=10, pady=6).pack(fill="x")

    so_tay = ttk.Notebook(cua_so)
    so_tay.pack(fill="both", expand=True, padx=12, pady=(4, 8))

    danh_sach_tab = [
        ("  Tổng quan  ", tab_tong_quan.tao_tab),
        ("  Bệnh nhân  ", tab_benh_nhan.tao_tab),
        ("  Sàng lọc triệu chứng  ", tab_trieu_chung.tao_tab),
        ("  Đánh giá chỉ số  ", tab_chi_so.tao_tab),
        ("  Lịch sử  ", tab_lich_su.tao_tab),
        ("  Thông tin model  ", tab_model.tao_tab),
    ]

    cac_ham_lam_moi = []

    for ten_tab, ham_tao_tab in danh_sach_tab:
        khung_tab, ham_lam_moi = ham_tao_tab(so_tay, cua_so)
        so_tay.add(khung_tab, text=ten_tab)
        cac_ham_lam_moi.append(ham_lam_moi)

    def khi_doi_tab(su_kien):
        thu_tu_tab = so_tay.index(so_tay.select())
        cac_ham_lam_moi[thu_tu_tab]()

    so_tay.bind("<<NotebookTabChanged>>", khi_doi_tab)

    cua_so.mainloop()


if __name__ == "__main__":
    main()
