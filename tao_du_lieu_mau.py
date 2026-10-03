
import os
import random
import sys

THU_MUC_GOC = os.path.dirname(os.path.abspath(__file__))
if THU_MUC_GOC not in sys.path:
    sys.path.append(THU_MUC_GOC)

import config
from database.db import tao_bang
from database import queries
from ml import predict

random.seed(config.SO_NGAU_NHIEN)


DANH_SACH_BENH_NHAN_MAU = [
    ("Nguyễn Văn An",    "1975-03-12", "Male",   "0901000001"),
    ("Trần Thị Bình",    "1988-07-25", "Female", "0901000002"),
    ("Lê Hoàng Cường",   "1962-11-03", "Male",   "0901000003"),
    ("Phạm Thị Dung",    "1995-01-18", "Female", "0901000004"),
    ("Hoàng Minh Đức",   "1970-09-30", "Male",   "0901000005"),
    ("Vũ Thị Hoa",       "1983-05-22", "Female", "0901000006"),
    ("Đặng Văn Giang",   "1957-12-08", "Male",   "0901000007"),
    ("Bùi Thị Hương",    "1991-04-14", "Female", "0901000008"),
    ("Ngô Quang Huy",    "1979-08-27", "Male",   "0901000009"),
    ("Dương Thị Kim",    "1966-02-11", "Female", "0901000010"),
]


MUC_DO_NANG_TUNG_BENH_NHAN = [0.00, 0.05, 0.10, 0.15, 0.25,
                              0.35, 0.50, 0.65, 0.80, 0.90]


def tinh_tuoi_tu_nam_sinh(chuoi_ngay_sinh):
    from datetime import date
    nam_sinh = int(chuoi_ngay_sinh.split("-")[0])
    return date.today().year - nam_sinh


def tao_trieu_chung_ngau_nhien(muc_do_nang):
    ket_qua = {}
    for trieu_chung in config.DANH_SACH_TRIEU_CHUNG:
        if random.random() < muc_do_nang:
            ket_qua[trieu_chung["cot_db"]] = 1
        else:
            ket_qua[trieu_chung["cot_db"]] = 0
    return ket_qua


def tao_chi_so_ngau_nhien(muc_do_nang):
    return {
        "pregnancies": float(random.randint(0, 5)),
        "glucose": round(95 + muc_do_nang * 90 + random.uniform(-10, 10), 1),
        "blood_pressure": round(68 + muc_do_nang * 20 + random.uniform(-5, 5), 1),
        "skin_thickness": round(20 + muc_do_nang * 18 + random.uniform(-5, 5), 1),
        "insulin": round(80 + muc_do_nang * 160 + random.uniform(-20, 20), 1),
        "bmi": round(24 + muc_do_nang * 14 + random.uniform(-2, 2), 1),
        "diabetes_pedigree_function": round(0.15 + muc_do_nang * 0.8, 3),
    }


def main():
    print()
    print("=" * 70)
    print("TẠO DỮ LIỆU MẪU ĐỂ DEMO")
    print("=" * 70)
    print()

    tao_bang()

    if queries.lay_model_dang_dung("symptom") is None:
        print("LỖI: chưa có model triệu chứng. Hãy chạy trước:")
        print("     python ml/train_symptom.py")
        return

    if queries.lay_model_dang_dung("clinical") is None:
        print("LỖI: chưa có model lâm sàng. Hãy chạy trước:")
        print("     python ml/train_clinical.py")
        return

    print("Bước 1: Tạo 10 bệnh nhân mẫu")
    print("-" * 70)

    cac_ma_benh_nhan = []
    for ho_ten, ngay_sinh, gioi_tinh, dien_thoai in DANH_SACH_BENH_NHAN_MAU:
        ma = queries.them_benh_nhan(ho_ten, ngay_sinh, gioi_tinh, dien_thoai)
        cac_ma_benh_nhan.append({
            "ma": ma,
            "ho_ten": ho_ten,
            "tuoi": tinh_tuoi_tu_nam_sinh(ngay_sinh),
            "gioi_tinh": gioi_tinh,
        })
        print("   [%2d] %s" % (ma, ho_ten))

    print()

    print("Bước 2: Tạo các lượt đánh giá")
    print("-" * 70)

    so_luot = 0

    for thu_tu in range(len(cac_ma_benh_nhan)):
        benh_nhan = cac_ma_benh_nhan[thu_tu]

        muc_do_nang = MUC_DO_NANG_TUNG_BENH_NHAN[thu_tu]

        trieu_chung = tao_trieu_chung_ngau_nhien(muc_do_nang)
        ket_qua = predict.du_doan_trieu_chung(
            benh_nhan["tuoi"], benh_nhan["gioi_tinh"], trieu_chung
        )
        queries.luu_danh_gia_trieu_chung(
            benh_nhan["ma"], benh_nhan["tuoi"], benh_nhan["gioi_tinh"],
            trieu_chung, ket_qua, "Dữ liệu mẫu để demo",
        )
        so_luot = so_luot + 1
        print("   %-18s | Triệu chứng | %-11s | %.1f%%"
              % (benh_nhan["ho_ten"], ket_qua["muc_rui_ro"],
                 ket_qua["xac_suat"] * 100))

        if thu_tu % 2 == 0:
            chi_so = tao_chi_so_ngau_nhien(muc_do_nang)
            if benh_nhan["gioi_tinh"] == "Male":
                chi_so["pregnancies"] = 0.0

            ket_qua2 = predict.du_doan_lam_sang(benh_nhan["tuoi"], chi_so)
            queries.luu_danh_gia_lam_sang(
                benh_nhan["ma"], benh_nhan["tuoi"], benh_nhan["gioi_tinh"],
                chi_so, ket_qua2, "Dữ liệu mẫu để demo",
            )
            so_luot = so_luot + 1
            print("   %-18s | Lâm sàng    | %-11s | %.1f%%"
                  % (benh_nhan["ho_ten"], ket_qua2["muc_rui_ro"],
                     ket_qua2["xac_suat"] * 100))

    print()
    print("=" * 70)
    print("XONG: đã tạo %d bệnh nhân và %d lượt đánh giá."
          % (len(cac_ma_benh_nhan), so_luot))
    print("Chạy 'python app.py' để xem trên giao diện.")
    print("=" * 70)


if __name__ == "__main__":
    main()
