
import json
import os
import sys

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, f1_score, precision_score,
                             recall_score, roc_auc_score)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

THU_MUC_GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if THU_MUC_GOC not in sys.path:
    sys.path.append(THU_MUC_GOC)

import config
from database.db import tao_bang
from database import queries



def doc_va_lam_sach_du_lieu():
    print("BƯỚC 1: Đọc và làm sạch dữ liệu")
    print("-" * 70)

    bang = pd.read_csv(config.DUONG_DAN_CSV_LAM_SANG)
    print("   Đọc được", len(bang), "dòng từ file diabetes.csv")

    X = bang.drop(columns=["Outcome"])
    y = bang["Outcome"]

    print()
    print("   Đổi các số 0 vô lý thành 'thiếu dữ liệu':")
    for ten_cot in config.CAC_COT_KHONG_DUOC_BANG_0:
        so_luong_0 = (X[ten_cot] == 0).sum()
        X[ten_cot] = X[ten_cot].replace(0, np.nan)
        print("      %-18s : %4d ô" % (ten_cot, so_luong_0))

    print()
    print("   Số cột đầu vào:", X.shape[1])
    print("   Số ca có bệnh:", int(y.sum()), "| không bệnh:", int((y == 0).sum()))
    print()

    return X, y



def danh_sach_thuat_toan():
    return [
        {
            "ten": "LogisticRegression",
            "mo_hinh": LogisticRegression(max_iter=1000,
                                          random_state=config.SO_NGAU_NHIEN),
            "giai_thich": "Hồi quy logistic - đơn giản, chạy nhanh, dễ giải thích",
        },
        {
            "ten": "RandomForest",
            "mo_hinh": RandomForestClassifier(n_estimators=200,
                                              random_state=config.SO_NGAU_NHIEN),
            "giai_thich": "Rừng cây quyết định - gộp ý kiến của 200 cây nhỏ",
        },
        {
            "ten": "SVC",
            "mo_hinh": SVC(probability=True, random_state=config.SO_NGAU_NHIEN),
            "giai_thich": "Máy vector hỗ trợ - tìm ranh giới phân chia tốt nhất",
        },
        {
            "ten": "KNN",
            "mo_hinh": KNeighborsClassifier(n_neighbors=5),
            "giai_thich": "K láng giềng gần nhất - xem 5 ca giống nhất rồi kết luận",
        },
    ]



def danh_gia_mot_thuat_toan(ten, mo_hinh, X_hoc, y_hoc, X_thi, y_thi):
    duong_ong = Pipeline(steps=[
        ("dien_bu", SimpleImputer(strategy="median")),

        ("chuan_hoa", StandardScaler()),

        ("thuat_toan", mo_hinh),
    ])

    diem_cv = cross_val_score(duong_ong, X_hoc, y_hoc, cv=5, scoring="f1")

    duong_ong.fit(X_hoc, y_hoc)

    du_doan = duong_ong.predict(X_thi)
    xac_suat = duong_ong.predict_proba(X_thi)[:, 1]

    diem = {
        "Thuật toán": ten,
        "F1 kiểm tra chéo": round(diem_cv.mean(), 4),
        "Accuracy": round(accuracy_score(y_thi, du_doan), 4),
        "Precision": round(precision_score(y_thi, du_doan, zero_division=0), 4),
        "Recall": round(recall_score(y_thi, du_doan, zero_division=0), 4),
        "F1": round(f1_score(y_thi, du_doan, zero_division=0), 4),
        "ROC-AUC": round(roc_auc_score(y_thi, xac_suat), 4),
    }
    return duong_ong, diem



def main():
    print()
    print("=" * 70)
    print("HUẤN LUYỆN MODEL ĐÁNH GIÁ THEO CHỈ SỐ LÂM SÀNG")
    print("=" * 70)
    print()

    X, y = doc_va_lam_sach_du_lieu()

    print("BƯỚC 2: Chia dữ liệu")
    print("-" * 70)
    X_hoc, X_thi, y_hoc, y_thi = train_test_split(
        X, y,
        test_size=config.TY_LE_TEST,
        stratify=y,
        random_state=config.SO_NGAU_NHIEN,
    )
    print("   Phần học :", len(X_hoc), "dòng")
    print("   Phần thi :", len(X_thi), "dòng")
    print()

    print("BƯỚC 3: Thử 4 thuật toán")
    print("-" * 70)

    bang_diem = []
    cac_duong_ong = {}

    for thuat_toan in danh_sach_thuat_toan():
        ten = thuat_toan["ten"]
        print("   Đang huấn luyện:", ten, "-", thuat_toan["giai_thich"])

        duong_ong, diem = danh_gia_mot_thuat_toan(
            ten, thuat_toan["mo_hinh"], X_hoc, y_hoc, X_thi, y_thi
        )

        bang_diem.append(diem)
        cac_duong_ong[ten] = duong_ong

    print()

    print("BƯỚC 4: Bảng so sánh kết quả")
    print("-" * 70)
    bang_so_sanh = pd.DataFrame(bang_diem)
    bang_so_sanh = bang_so_sanh.sort_values(by="F1", ascending=False)
    bang_so_sanh = bang_so_sanh.reset_index(drop=True)
    print(bang_so_sanh.to_string(index=False))
    print()

    os.makedirs(config.THU_MUC_MODEL, exist_ok=True)
    duong_dan_bang = os.path.join(config.THU_MUC_MODEL,
                                  config.TEN_FILE_SO_SANH_LAM_SANG)
    bang_so_sanh.to_csv(duong_dan_bang, index=False, encoding="utf-8-sig")
    print("   Đã lưu bảng so sánh:", duong_dan_bang)
    print()

    print("BƯỚC 5: Chọn model tốt nhất và lưu lại")
    print("-" * 70)
    dong_tot_nhat = bang_so_sanh.iloc[0]
    ten_tot_nhat = dong_tot_nhat["Thuật toán"]
    model_tot_nhat = cac_duong_ong[ten_tot_nhat]

    print("   Thuật toán thắng cuộc:", ten_tot_nhat)
    print("   F1 =", dong_tot_nhat["F1"], "| Recall =", dong_tot_nhat["Recall"])
    print()

    du_doan_cuoi = model_tot_nhat.predict(X_thi)
    print("   Ma trận nhầm lẫn (confusion matrix):")
    ma_tran = confusion_matrix(y_thi, du_doan_cuoi)
    print("      Thực tế không bệnh -> đoán không:", ma_tran[0][0], "| đoán có:", ma_tran[0][1])
    print("      Thực tế có bệnh    -> đoán không:", ma_tran[1][0], "| đoán có:", ma_tran[1][1])
    print()
    print("   Báo cáo chi tiết:")
    print(classification_report(y_thi, du_doan_cuoi,
                                target_names=["Không bệnh", "Có bệnh"],
                                zero_division=0))

    duong_dan_model = os.path.join(config.THU_MUC_MODEL,
                                   config.TEN_FILE_MODEL_LAM_SANG)
    joblib.dump(model_tot_nhat, duong_dan_model)
    print("   Đã lưu model:", duong_dan_model)

    tao_bang()

    diem_de_luu = dong_tot_nhat.to_dict()
    chuoi_metrics = json.dumps(diem_de_luu, ensure_ascii=False)

    ma_model = queries.dang_ky_model(
        model_key="clinical",
        ten_model="Model đánh giá theo chỉ số lâm sàng",
        phien_ban=config.PHIEN_BAN_MODEL,
        thuat_toan=ten_tot_nhat,
        duong_dan_file=duong_dan_model,
        chuoi_metrics=chuoi_metrics,
    )
    print("   Đã ghi vào database, mã model =", ma_model)
    print()
    print("=" * 70)
    print("HOÀN TẤT HUẤN LUYỆN MODEL LÂM SÀNG")
    print("=" * 70)


if __name__ == "__main__":
    main()
