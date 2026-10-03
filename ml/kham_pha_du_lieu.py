
import os
import sys

import pandas as pd

THU_MUC_GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if THU_MUC_GOC not in sys.path:
    sys.path.append(THU_MUC_GOC)

import config


def in_tieu_de(chu):
    print()
    print("=" * 70)
    print(chu)
    print("=" * 70)


def kham_pha_du_lieu_lam_sang():
    in_tieu_de("FILE 1: diabetes.csv  --  DỮ LIỆU CHỈ SỐ LÂM SÀNG")

    bang = pd.read_csv(config.DUONG_DAN_CSV_LAM_SANG)

    so_dong = bang.shape[0]
    so_cot = bang.shape[1]
    print("Số dòng (số bệnh nhân) :", so_dong)
    print("Số cột                 :", so_cot)
    print("Tên các cột            :", list(bang.columns))

    print()
    print("Phân bố cột Outcome (0 = không bệnh, 1 = có bệnh):")
    dem_nhan = bang["Outcome"].value_counts()
    for gia_tri in dem_nhan.index:
        so_luong = dem_nhan[gia_tri]
        phan_tram = so_luong / so_dong * 100
        print("   Outcome =", gia_tri, "->", so_luong, "dòng", "(%.1f%%)" % phan_tram)

    so_o_trong = bang.isna().sum().sum()
    print()
    print("Số ô trống (NaN):", so_o_trong)

    so_dong_trung = bang.duplicated().sum()
    print("Số dòng trùng lặp hoàn toàn:", so_dong_trung)

    print()
    print("Số giá trị bằng 0 ở các cột không được phép bằng 0:")
    for ten_cot in config.CAC_COT_KHONG_DUOC_BANG_0:
        so_luong_bang_0 = (bang[ten_cot] == 0).sum()
        phan_tram = so_luong_bang_0 / so_dong * 100
        print("   %-18s : %4d dòng  (%.1f%%)" % (ten_cot, so_luong_bang_0, phan_tram))

    print()
    print(">>> KẾT LUẬN: các số 0 ở trên phải được coi là THIẾU DỮ LIỆU,")
    print("    sau đó điền bù bằng trung vị NGAY TRONG pipeline huấn luyện.")


def kham_pha_du_lieu_trieu_chung():
    in_tieu_de("FILE 2: diabetes_data.csv  --  DỮ LIỆU TRIỆU CHỨNG")

    bang = pd.read_csv(config.DUONG_DAN_CSV_TRIEU_CHUNG)

    so_dong = bang.shape[0]
    print("Số dòng (số bệnh nhân) :", so_dong)
    print("Số cột                 :", bang.shape[1])

    print()
    print("Phân bố cột DiabeticClass:")
    dem_nhan = bang["DiabeticClass"].value_counts()
    for gia_tri in dem_nhan.index:
        so_luong = dem_nhan[gia_tri]
        phan_tram = so_luong / so_dong * 100
        print("   %-10s -> %d dòng  (%.1f%%)" % (gia_tri, so_luong, phan_tram))

    print()
    print("Số ô trống (NaN):", bang.isna().sum().sum())

    so_dong_trung = bang.duplicated().sum()
    phan_tram_trung = so_dong_trung / so_dong * 100
    print("Số dòng trùng lặp hoàn toàn: %d  (%.1f%%)" % (so_dong_trung, phan_tram_trung))

    print()
    print("Tuổi nhỏ nhất :", bang["Age"].min())
    print("Tuổi lớn nhất :", bang["Age"].max())

    print()
    print("Giới tính có các giá trị:", list(bang["Gender"].unique()))
    print("Các cột triệu chứng có giá trị:", list(bang["Fatigue"].unique()))

    print()
    print(">>> KẾT LUẬN: phải XOÁ %d dòng trùng lặp TRƯỚC KHI chia dữ liệu." % so_dong_trung)
    print("    Nếu không xoá, một dòng có thể vừa nằm ở phần học vừa nằm ở phần thi,")
    print("    model đã nhìn thấy đáp án nên điểm đánh giá sẽ cao giả tạo.")


if __name__ == "__main__":
    kham_pha_du_lieu_lam_sang()
    kham_pha_du_lieu_trieu_chung()
    print()
    print("Đã khám phá xong dữ liệu.")
