
import os



THU_MUC_GOC = os.path.dirname(os.path.abspath(__file__))

DUONG_DAN_DATABASE = os.path.join(THU_MUC_GOC, "data", "diabetes.db")

DUONG_DAN_CSV_LAM_SANG = os.path.join(THU_MUC_GOC, "diabetes.csv")
DUONG_DAN_CSV_TRIEU_CHUNG = os.path.join(THU_MUC_GOC, "diabetes_data.csv")

THU_MUC_MODEL = os.path.join(THU_MUC_GOC, "ml", "artifacts")

TEN_FILE_MODEL_TRIEU_CHUNG = "symptom_model_v1.joblib"
TEN_FILE_MODEL_LAM_SANG = "clinical_model_v1.joblib"

TEN_FILE_SO_SANH_TRIEU_CHUNG = "so_sanh_symptom.csv"
TEN_FILE_SO_SANH_LAM_SANG = "so_sanh_clinical.csv"



TY_LE_TEST = 0.2

SO_NGAU_NHIEN = 42

NGUONG_PHAN_LOAI = 0.5

PHIEN_BAN_MODEL = "1.0.0"



NGUONG_RUI_RO_THAP = 0.30
NGUONG_RUI_RO_TRUNG_BINH = 0.70



DANH_SACH_TRIEU_CHUNG = [
    {"cot_csv": "ExcessUrination",  "cot_db": "excess_urination",   "nhan": "Đi tiểu nhiều lần trong ngày"},
    {"cot_csv": "Polydipsia",       "cot_db": "polydipsia",         "nhan": "Khát nước liên tục, uống nhiều nước"},
    {"cot_csv": "WeightLossSudden", "cot_db": "sudden_weight_loss", "nhan": "Sụt cân đột ngột không rõ lý do"},
    {"cot_csv": "Fatigue",          "cot_db": "fatigue",            "nhan": "Mệt mỏi, uể oải kéo dài"},
    {"cot_csv": "Polyphagia",       "cot_db": "polyphagia",         "nhan": "Ăn nhiều bất thường, nhanh đói"},
    {"cot_csv": "GenitalThrush",    "cot_db": "genital_thrush",     "nhan": "Nhiễm nấm vùng kín"},
    {"cot_csv": "BlurredVision",    "cot_db": "blurred_vision",     "nhan": "Nhìn mờ, thị lực giảm"},
    {"cot_csv": "Itching",          "cot_db": "itching",            "nhan": "Ngứa da"},
    {"cot_csv": "Irritability",     "cot_db": "irritability",       "nhan": "Dễ cáu gắt, thay đổi tâm trạng"},
    {"cot_csv": "DelayHealing",     "cot_db": "delayed_healing",    "nhan": "Vết thương lâu lành"},
    {"cot_csv": "PartialPsoriasis", "cot_db": "partial_psoriasis",  "nhan": "Vảy nến / tổn thương da từng vùng"},
    {"cot_csv": "MuscleStiffness",  "cot_db": "muscle_stiffness",   "nhan": "Cứng cơ, đau mỏi cơ bắp"},
    {"cot_csv": "Alopecia",         "cot_db": "alopecia",           "nhan": "Rụng tóc"},
    {"cot_csv": "Obesity",          "cot_db": "obesity",            "nhan": "Béo phì"},
]



DANH_SACH_CHI_SO = [
    {
        "cot_csv": "Pregnancies", "cot_db": "pregnancies",
        "nhan": "Số lần mang thai",
        "min": 0.0, "max": 20.0, "buoc": 1.0, "mac_dinh": 0.0,
        "goi_y": "Bệnh nhân nam để là 0",
    },
    {
        "cot_csv": "Glucose", "cot_db": "glucose",
        "nhan": "Đường huyết (mg/dL)",
        "min": 0.0, "max": 300.0, "buoc": 1.0, "mac_dinh": 120.0,
        "goi_y": "Người bình thường khoảng 70 - 140",
    },
    {
        "cot_csv": "BloodPressure", "cot_db": "blood_pressure",
        "nhan": "Huyết áp tâm trương (mm Hg)",
        "min": 0.0, "max": 200.0, "buoc": 1.0, "mac_dinh": 70.0,
        "goi_y": "Người bình thường khoảng 60 - 90",
    },
    {
        "cot_csv": "SkinThickness", "cot_db": "skin_thickness",
        "nhan": "Độ dày nếp gấp da (mm)",
        "min": 0.0, "max": 100.0, "buoc": 1.0, "mac_dinh": 20.0,
        "goi_y": "Đo ở vùng cơ tam đầu cánh tay",
    },
    {
        "cot_csv": "Insulin", "cot_db": "insulin",
        "nhan": "Insulin huyết thanh (mu U/ml)",
        "min": 0.0, "max": 900.0, "buoc": 1.0, "mac_dinh": 80.0,
        "goi_y": "Người bình thường khoảng 16 - 166",
    },
    {
        "cot_csv": "BMI", "cot_db": "bmi",
        "nhan": "Chỉ số khối cơ thể BMI",
        "min": 0.0, "max": 70.0, "buoc": 0.1, "mac_dinh": 25.0,
        "goi_y": "BMI = cân nặng (kg) chia cho bình phương chiều cao (m)",
    },
    {
        "cot_csv": "DiabetesPedigreeFunction", "cot_db": "diabetes_pedigree_function",
        "nhan": "Chỉ số di truyền tiểu đường",
        "min": 0.0, "max": 3.0, "buoc": 0.001, "mac_dinh": 0.3,
        "goi_y": "Mức độ người thân trong gia đình từng mắc bệnh",
    },
]

CAC_COT_KHONG_DUOC_BANG_0 = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]



DANH_SACH_GIOI_TINH = ["Male", "Female"]
TEN_GIOI_TINH_TIENG_VIET = {"Male": "Nam", "Female": "Nữ"}

LOAI_DANH_GIA_TRIEU_CHUNG = "SYMPTOM"
LOAI_DANH_GIA_LAM_SANG = "CLINICAL"

TEN_LOAI_DANH_GIA_TIENG_VIET = {
    "SYMPTOM": "Sàng lọc triệu chứng",
    "CLINICAL": "Đánh giá chỉ số lâm sàng",
}

CANH_BAO_Y_TE = (
    "Kết quả này chỉ mang tính chất hỗ trợ sàng lọc và tham khảo. "
    "Đây KHÔNG phải kết luận chẩn đoán y khoa. "
    "Vui lòng đến cơ sở y tế để được bác sĩ khám và tư vấn."
)
