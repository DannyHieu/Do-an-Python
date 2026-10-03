# Ứng dụng hỗ trợ sàng lọc và dự đoán nguy cơ tiểu đường

Đồ án môn Python — HK3
Công nghệ: **Python + Tkinter + Scikit-learn + SQLite**

---

## 1. Ứng dụng làm được gì?

- Quản lý hồ sơ bệnh nhân (thêm / sửa / tìm kiếm)
- **Sàng lọc theo triệu chứng**: tích 14 ô Có/Không, không cần xét nghiệm
- **Đánh giá theo chỉ số lâm sàng**: nhập 7 chỉ số từ kết quả xét nghiệm
- Hiển thị kết luận, xác suất %, mức rủi ro và phiên bản model đã dùng
- Lưu và tra cứu lại toàn bộ lịch sử đánh giá
- Màn hình tổng quan có biểu đồ, và màn hình thông tin model

Giao diện là một **phần mềm máy tính** chạy bằng Tkinter — mở ra một cửa sổ
riêng, không cần trình duyệt và không cần mạng.

---

## 2. Cài đặt (làm 1 lần)

### Bước 1 — Tạo môi trường ảo

Mở terminal tại thư mục gốc dự án:

```
python -m venv .venv
```

Kích hoạt môi trường ảo:

- **Windows:** `.venv\Scripts\activate`
- **macOS / Linux:** `source .venv/bin/activate`

Khi thành công, đầu dòng lệnh sẽ có chữ `(.venv)`.

### Bước 2 — Cài thư viện

```
pip install -r requirements.txt
```

> Dự án này chạy trên **Python 3.14**. File `requirements.txt` chỉ ghi phiên
> bản tối thiểu (dấu `>=`) chứ không ghim cứng, để pip tự chọn bản thư viện
> phù hợp. Nếu ghim cứng phiên bản cũ sẽ báo lỗi khi cài trên Python 3.14.

> **Tkinter không nằm trong danh sách** vì nó có sẵn trong Python. Cài Python
> là có luôn. (Riêng trên Linux đôi khi cần thêm: `sudo apt install python3-tk`)

---

## 3. Chạy lần đầu

Chạy **đúng theo thứ tự** các lệnh sau:

```
python ml/train_symptom.py      # huấn luyện model triệu chứng
python ml/train_clinical.py     # huấn luyện model chỉ số lâm sàng
python app.py                   # mở ứng dụng
```

Một cửa sổ phần mềm sẽ hiện ra. Đóng cửa sổ là thoát chương trình.

> **Muốn có sẵn dữ liệu để demo?** Chạy thêm `python tao_du_lieu_mau.py`
> trước khi mở app. Lệnh này tạo 10 bệnh nhân giả và 15 lượt đánh giá.

Các lần chạy sau chỉ cần `python app.py`. Không cần huấn luyện lại model
trừ khi bạn muốn.

---

## 4. Cấu trúc thư mục

```
do-an-python-tkinter/
├── app.py                      Chạy file này để mở ứng dụng
├── config.py                   Bảng cấu hình chung của toàn bộ chương trình
├── tao_du_lieu_mau.py          Tạo dữ liệu giả để demo
├── requirements.txt            Danh sách thư viện cần cài
│
├── diabetes.csv                Dữ liệu gốc — chỉ số lâm sàng (768 dòng)
├── diabetes_data.csv           Dữ liệu gốc — triệu chứng (520 dòng)
│
├── database/
│   ├── db.py                   Mở kết nối SQLite + tạo 6 bảng
│   └── queries.py              Toàn bộ hàm thêm / sửa / tìm / thống kê
│
├── ml/
│   ├── kham_pha_du_lieu.py     Thống kê 2 file CSV trước khi huấn luyện
│   ├── train_symptom.py        Huấn luyện model triệu chứng
│   ├── train_clinical.py       Huấn luyện model chỉ số lâm sàng
│   ├── predict.py              Nạp model và dự đoán (app gọi file này)
│   └── artifacts/              Model .joblib + bảng so sánh thuật toán
│
├── giao_dien/                  6 TAB CỦA GIAO DIỆN
│   ├── thanh_phan_chung.py     Bảng, ô số liệu, biểu đồ, cửa sổ kết quả
│   ├── tab_tong_quan.py
│   ├── tab_benh_nhan.py
│   ├── tab_trieu_chung.py
│   ├── tab_chi_so.py
│   ├── tab_lich_su.py
│   └── tab_model.py
│
└── data/
    └── diabetes.db             File database — tự sinh ra khi chạy lần đầu
```

---

## 5. Sáu tab của ứng dụng

| Tab | Nội dung | File |
|---|---|---|
| **Tổng quan** | 4 ô số liệu, 2 biểu đồ cột, bảng 10 lượt gần nhất | `tab_tong_quan.py` |
| **Bệnh nhân** | Tìm kiếm, bảng danh sách, form thêm và sửa | `tab_benh_nhan.py` |
| **Sàng lọc triệu chứng** | Chọn bệnh nhân, tích 14 ô, bấm Dự đoán | `tab_trieu_chung.py` |
| **Đánh giá chỉ số** | Chọn bệnh nhân, nhập 7 chỉ số, bấm Dự đoán | `tab_chi_so.py` |
| **Lịch sử** | 3 bộ lọc, bảng kết quả, cửa sổ xem chi tiết | `tab_lich_su.py` |
| **Thông tin model** | Model đang dùng, điểm số, bảng so sánh 4 thuật toán | `tab_model.py` |

Dữ liệu tự làm mới mỗi khi bạn chuyển tab, nên thêm bệnh nhân ở tab này
thì sang tab kia là thấy ngay.

---

## 6. Hai model hoạt động thế nào?

Hai model **hoàn toàn độc lập**, học từ hai bộ dữ liệu khác nhau.

### Model 1 — Sàng lọc triệu chứng (`diabetes_data.csv`)

| Bước | Việc làm | Vì sao |
|---|---|---|
| 1 | Đọc 520 dòng | |
| 2 | **Xoá 269 dòng trùng lặp** | Hơn 50% dữ liệu bị trùng. Không xoá thì một dòng vừa nằm ở phần học vừa nằm ở phần thi → điểm cao giả tạo |
| 3 | Chia 80% học / 20% thi, có `stratify` | Giữ nguyên tỷ lệ Dương/Âm ở cả hai phần |
| 4 | Chuẩn hoá tuổi, đổi Yes/No thành số | Model chỉ hiểu số |
| 5 | Thử 4 thuật toán, chọn F1 cao nhất | Có bảng so sánh để đưa vào báo cáo |

### Model 2 — Chỉ số lâm sàng (`diabetes.csv`)

| Bước | Việc làm | Vì sao |
|---|---|---|
| 1 | Đọc 768 dòng | |
| 2 | **Đổi số 0 thành "thiếu dữ liệu"** ở 5 cột: Glucose, BloodPressure, SkinThickness, Insulin, BMI | Huyết áp = 0 nghĩa là không đo được, không phải huyết áp thật |
| 3 | Chia 80% / 20%, có `stratify` | |
| 4 | Điền bù bằng **trung vị — bên trong Pipeline** | Nếu tính trung vị trên toàn bộ file trước khi chia, model đã "nhìn trộm" đề thi (lỗi *data leakage*) |
| 5 | Chuẩn hoá thang đo | Insulin tới 900 còn BMI chỉ 20–40, không chuẩn hoá thì Insulin lấn át |
| 6 | Thử 4 thuật toán, chọn F1 cao nhất | |

### Vì sao dùng `Pipeline`?

`Pipeline` gắn các bước xử lý dữ liệu và thuật toán thành **một khối duy nhất**,
rồi lưu chung vào file `.joblib`. Nhờ vậy khi ứng dụng nạp model lên dùng, dữ
liệu mới được xử lý **đúng y hệt** lúc huấn luyện.

Đây là cách tránh lỗi kinh điển của đồ án ML: lúc train xử lý một kiểu, lúc
chạy app xử lý kiểu khác, ra kết quả sai mà không biết vì sao.

---

## 7. Mức rủi ro hiển thị

| Xác suất | Mức hiển thị |
|---|---|
| Dưới 30% | THẤP (xanh lá) |
| 30% – dưới 70% | TRUNG BÌNH (vàng cam) |
| Từ 70% trở lên | CAO (đỏ) |

---

## 8. Cơ sở dữ liệu

6 bảng trong file `data/diabetes.db`:

| Bảng | Nội dung |
|---|---|
| `patients` | Hồ sơ bệnh nhân |
| `assessments` | Mỗi lượt đánh giá (dùng chung 2 loại) |
| `symptom_assessments` | Chi tiết 14 triệu chứng |
| `clinical_assessments` | Chi tiết 7 chỉ số lâm sàng |
| `ml_models` | Sổ đăng ký model: thuật toán, phiên bản, điểm số |
| `predictions` | Kết quả dự đoán kèm mã model đã dùng |

**Vì sao `assessments` lưu lại tuổi và giới tính?**
Hồ sơ bệnh nhân có thể được sửa sau này. Nhưng kết quả cũ phải giữ đúng dữ liệu
đã dùng tại thời điểm chạy model, nếu không sẽ không tra ngược lại được.

**Lịch sử là chỉ đọc.** Muốn có kết quả mới thì tạo một lượt đánh giá mới,
không sửa kết quả cũ.

---

## 9. Vài điểm kỹ thuật Tkinter đáng chú ý

Những chỗ này hay bị hỏi khi bảo vệ đồ án:

| Vấn đề | Cách xử lý trong dự án |
|---|---|
| Giữ giá trị người dùng nhập | `StringVar` / `IntVar` gắn vào ô nhập. Người dùng gõ gì thì biến tự cập nhật theo |
| Vẽ biểu đồ | Tkinter không có biểu đồ sẵn. Tự vẽ hình chữ nhật lên `tk.Canvas`, chiều cao tỉ lệ với giá trị — xem `ve_bieu_do_cot()` |
| Bảng dữ liệu | `ttk.Treeview` kèm `Scrollbar` tự nối vào |
| Thứ tự sắp xếp widget | `pack()` chia chỗ theo thứ tự được gọi. Widget có `expand=True` chiếm hết phần còn lại, nên thanh cảnh báo ở đáy phải đặt **trước** nó |
| Nội dung dài hơn cửa sổ | Tab Thông tin model bọc trong khung cuộn tự dựng: `Canvas` + `Scrollbar` — xem `tao_khung_cuon()` |
| Hiển thị "Nam"/"Nữ" nhưng gửi "Male"/"Female" cho model | Ô chọn của Tkinter không tách được phần hiển thị và giá trị thật, nên viết hai hàm đổi qua lại |
| Làm mới dữ liệu khi đổi tab | Bắt sự kiện `<<NotebookTabChanged>>`, gọi hàm làm mới của tab vừa được chọn |

---

## 10. Xử lý sự cố

| Lỗi | Cách khắc phục |
|---|---|
| `ModuleNotFoundError: No module named 'sklearn'` | Chưa kích hoạt `.venv` hoặc chưa chạy `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'tkinter'` | Hiếm gặp trên Windows. Trên Linux cần cài thêm: `sudo apt install python3-tk` |
| App báo "Chưa huấn luyện model" | Chạy `python ml/train_symptom.py` và `python ml/train_clinical.py` |
| App báo "Không tìm thấy file model" | File `.joblib` bị xoá — chạy lại lệnh huấn luyện |
| Muốn xoá sạch dữ liệu, làm lại từ đầu | Xoá file `data/diabetes.db` rồi chạy lại 2 lệnh huấn luyện |
| Cửa sổ quá nhỏ, chữ bị che | Kéo to cửa sổ ra. Tab Thông tin model có thanh cuộn bên phải |
| `pip install` báo lỗi build | Máy đang dùng Python 3.14. `requirements.txt` chỉ ghi phiên bản tối thiểu (`>=`) để pip tự chọn bản hợp |
| Chữ tiếng Việt bị lỗi font trong terminal Windows | Gõ `chcp 65001` trước khi chạy |


