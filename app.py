st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif !important;
}

/* ==========================================
   الاتجاه العام
   ========================================== */

.stApp {
    direction: rtl;
    text-align: right;
    background-color: #f7f9fc;
}

/* ==========================================
   إخفاء عناصر Streamlit
   ========================================== */

#MainMenu {
    visibility: hidden !important;
    display: none !important;
}

footer {
    visibility: hidden !important;
    display: none !important;
}

header {
    visibility: hidden !important;
    display: none !important;
    height: 0 !important;
}

[data-testid="stToolbar"] {
    visibility: hidden !important;
    display: none !important;
}

[data-testid="stDecoration"] {
    visibility: hidden !important;
    display: none !important;
}

[data-testid="stStatusWidget"] {
    visibility: hidden !important;
    display: none !important;
}

[data-testid="stHeader"] {
    visibility: hidden !important;
    display: none !important;
}

[data-testid="stAppViewContainer"] {
    padding-top: 0 !important;
}

[data-testid="stMainBlockContainer"] {
    padding-top: 1rem !important;
}

/* ==========================================
   الحاوية الرئيسية
   ========================================== */

.block-container {
    max-width: 900px;
    width: 94%;
    padding-top: 25px !important;
    padding-bottom: 30px !important;
    margin: auto;
}

/* ==========================================
   شاشة تسجيل الدخول
   ========================================== */

.login-container {
    width: 100%;
    min-height: 80vh;

    display: flex;
    flex-direction: column;

    justify-content: center;
    align-items: center;

    text-align: center;
}

/* اللوجو في شاشة الدخول */

.login-logo {
    width: 180px;
    height: 180px;

    object-fit: contain;

    display: block;

    margin: 0 auto 25px auto;
}

/* عنوان الأكاديمية في الشاشة الافتتاحية */

.login-main-title {
    text-align: center;

    color: #17365d;

    font-size: 32px;
    font-weight: 900;

    line-height: 1.6;

    margin: 0 auto 10px auto;
}

/* العنوان الفرعي */

.login-sub-title {
    text-align: center;

    color: #294d7c;

    font-size: 22px;
    font-weight: 700;

    line-height: 1.6;

    margin: 0 auto 30px auto;
}

/* صندوق كلمة المرور */

.login-box {
    width: 100%;
    max-width: 450px;

    margin: 0 auto;

    text-align: right;
}

/* ==========================================
   الشاشة الداخلية
   ========================================== */

.internal-logo-container {
    width: 100%;

    display: flex;

    justify-content: center;
    align-items: center;

    text-align: center;

    margin: 5px auto 15px auto;
}

/* اللوجو الداخلي */

.internal-logo {
    width: 145px;
    height: 145px;

    object-fit: contain;

    display: block;

    margin: 0 auto;
}

/* عنوان الأكاديمية الداخلي */

.main-title {
    text-align: center;

    color: #17365d;

    font-size: 27px;
    font-weight: 900;

    line-height: 1.6;

    margin: 5px auto 5px auto;
}

/* العنوان الفرعي الداخلي */

.sub-title {
    text-align: center;

    color: #294d7c;

    font-size: 19px;
    font-weight: 600;

    line-height: 1.6;

    margin: 0 auto 25px auto;
}

/* ==========================================
   العناوين الرئيسية
   ========================================== */

.section-title {

    background: linear-gradient(
        110deg,
        #19365d,
        #2d588d
    );

    color: white;

    padding: 15px 20px;

    border-radius: 12px;

    text-align: center;

    font-size: 21px;
    font-weight: 800;

    margin-top: 22px;
    margin-bottom: 15px;

    box-shadow: 0 3px 8px rgba(0,0,0,0.08);
}

/* ==========================================
   الأزرار
   ========================================== */

.stButton > button {

    width: 100%;

    min-height: 48px;

    border-radius: 11px;

    border: 1px solid #d0d5dd;

    font-family: 'Cairo', sans-serif !important;

    font-size: 16px;

    font-weight: 700;
}

.stButton > button[kind="primary"] {

    background: linear-gradient(
        110deg,
        #19365d,
        #2d588d
    );

    color: white;

    border: none;
}

/* ==========================================
   حقول الإدخال
   ========================================== */

.stTextInput input,
.stTextArea textarea,
.stDateInput input,
.stSelectbox div[data-baseweb="select"] {

    font-family: 'Cairo', sans-serif !important;

    text-align: right;

    border-radius: 9px;
}

/* ==========================================
   الجداول
   ========================================== */

[data-testid="stDataFrame"] {
    direction: rtl;
}

/* ==========================================
   الفوتر
   ========================================== */

.footer {

    text-align: center;

    color: #294d7c;

    font-family: 'Cairo', sans-serif;

    font-size: 14px;

    margin-top: 45px;

    padding: 15px 0;

    border-top: 1px solid #d8dee8;
}

/* ==========================================
   الموبايل
   ========================================== */

@media (max-width: 600px) {

    .block-container {
        width: 94%;
        padding-top: 15px !important;
    }

    .login-logo {
        width: 140px;
        height: 140px;
    }

    .login-main-title {
        font-size: 22px;
    }

    .login-sub-title {
        font-size: 17px;
    }

    .internal-logo {
        width: 120px;
        height: 120px;
    }

    .main-title {
        font-size: 21px;
    }

    .sub-title {
        font-size: 16px;
    }

    .section-title {
        font-size: 18px;
    }
}

</style>
""", unsafe_allow_html=True)
