
import streamlit as st
import sqlite3
import shutil
import hashlib
import os
import re
from contextlib import closing
from pathlib import Path
from datetime import date, datetime

# ==========================================
# إعدادات الصفحة
# ==========================================

st.set_page_config(
    page_title="منظومة الوارد والصادر",
    page_icon="📁",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# حماية البرنامج بكلمة مرور
# ==========================================

APP_PASSWORD = st.secrets.get("APP_PASSWORD", "1234")  # ضع كلمة مرور آمنة في secrets.toml
MAX_UPLOAD_MB = 20
ALLOWED_EXTENSIONS = {"pdf"}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown(
        '''
        <div class="app-header" style="margin-top: 70px;">
            <div class="main-title">الأكاديمية المهنية للمعلمين – فرع الجيزة</div>
            <div class="sub-title">المنظومة الرقمية للوارد والصادر</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    password = st.text_input(
        "كلمة المرور",
        type="password",
        placeholder="أدخل كلمة المرور",
        key="login_password"
    )

    if st.button("🔐 دخول إلى البرنامج", type="primary", use_container_width=True):
        if hashlib.sha256(password.encode()).digest() == hashlib.sha256(str(APP_PASSWORD).encode()).digest():
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("كلمة المرور غير صحيحة.")

    st.stop()


# ==========================================
# المسارات
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "documents.db"
ARCHIVE_DIR = BASE_DIR / "Archive_Files"

INCOMING_DIR = ARCHIVE_DIR / "Incoming"
OUTGOING_DIR = ARCHIVE_DIR / "Outgoing"

LOGO_PATH = BASE_DIR / "logo.png"

# إنشاء مجلدات الأرشيف إذا لم تكن موجودة
INCOMING_DIR.mkdir(parents=True, exist_ok=True)
OUTGOING_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# تنسيق الصفحة و CSS
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif !important;
}

.stApp {
    direction: rtl;
    text-align: right;
}

/* إخفاء شريط أدوات Streamlit العلوي */
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
#MainMenu,
footer {
    visibility: hidden !important;
    display: none !important;
}

/* منع ظهور مساحة شريط الأدوات المخفية */
header {
    visibility: hidden !important;
    height: 0 !important;
}


.block-container {
    max-width: 850px;
    width: 95%;
    padding-top: 5rem;
    padding-bottom: 2rem;
}

/* توسيط اللوجو */
.logo-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    margin: 5px auto 18px auto;
    text-align: center;
}

/* عناوين الأكاديمية */
.main-title {
    text-align: center;
    color: #17365d;
    font-size: 25px;
    font-weight: 800;
    margin-top: 10px;
    margin-bottom: 8px;
}

.sub-title {
    text-align: center;
    color: #294d7c;
    font-size: 17px;
    font-weight: 500;
    margin-bottom: 35px;
}

/* العناوين الرئيسية */
.section-title {
    background: linear-gradient(110deg, #19365d, #2d588d);
    color: white;
    padding: 15px 20px;
    border-radius: 12px;
    text-align: center;
    font-size: 21px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
}

/* الأزرار */
.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 11px;
    border: 1px solid #d0d5dd;
    font-family: 'Cairo', sans-serif;
    font-size: 16px;
    font-weight: 600;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(110deg, #19365d, #2d588d);
    color: white;
    border: none;
}

/* حقول الإدخال */
.stTextInput input,
.stTextArea textarea,
.stDateInput input,
.stSelectbox div[data-baseweb="select"] {
    font-family: 'Cairo', sans-serif;
    text-align: right;
    border-radius: 9px;
}

/* الجداول */
[data-testid="stDataFrame"] {
    direction: rtl;
}

/* الفوتر */
.footer {
    text-align: center;
    color: #294d7c;
    font-family: 'Cairo', sans-serif;
    font-size: 14px;
    margin-top: 45px;
    padding: 15px 0;
    border-top: 1px solid #d8dee8;
}

/* تحسين عرض الموبايل */
@media (max-width: 600px) {
    .block-container {
        width: 95%;
        padding-top: 10px;
    }

    .main-title {
        font-size: 20px;
    }

    .sub-title {
        font-size: 15px;
    }

    .section-title {
        font-size: 18px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# الاتصال بقاعدة البيانات
# ==========================================

# ==========================================
# أدوات الأمان والملفات
# ==========================================

def safe_filename(value: str) -> str:
    value = re.sub(r"[^\w\-\u0600-\u06FF ]+", "_", value, flags=re.UNICODE).strip()
    return value[:80] or "document"

def is_inside_archive(path: Path) -> bool:
    try:
        path.resolve().relative_to(ARCHIVE_DIR.resolve())
        return True
    except ValueError:
        return False

def validate_pdf(uploaded_file) -> None:
    if uploaded_file is None:
        return
    if Path(safe_filename(Path(uploaded_file.name).stem) + ".pdf").suffix.lower() != ".pdf":
        raise ValueError("يسمح بإرفاق ملفات PDF فقط.")
    data = uploaded_file.getvalue()
    if len(data) > MAX_UPLOAD_MB * 1024 * 1024:
        raise ValueError(f"حجم الملف يجب ألا يتجاوز {MAX_UPLOAD_MB} ميجابايت.")
    if not data.startswith(b"%PDF"):
        raise ValueError("الملف المرفق لا يبدو ملف PDF صالحًا.")

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_type TEXT NOT NULL,
            doc_number TEXT NOT NULL,
            doc_date TEXT NOT NULL,
            party TEXT NOT NULL,
            subject TEXT NOT NULL,
            file_path TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


init_db()


# ==========================================
# أدوات مساعدة
# ==========================================

def get_archive_folder(doc_type):
    if doc_type == "وارد":
        return INCOMING_DIR
    return OUTGOING_DIR


def save_uploaded_file(uploaded_file, doc_type):
    validate_pdf(uploaded_file)
    """حفظ ملف PDF داخل مجلد الأرشيف."""

    if uploaded_file is None:
        return None

    folder = get_archive_folder(doc_type)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    original_name = Path(safe_filename(Path(uploaded_file.name).stem) + ".pdf").name
    safe_name = f"{timestamp}_{original_name}"

    file_path = folder / safe_name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return str(file_path)


def get_documents(doc_type=None, search_text=""):
    conn = get_connection()

    query = "SELECT * FROM documents WHERE 1=1"
    params = []

    if doc_type:
        query += " AND doc_type = ?"
        params.append(doc_type)

    if search_text:
        query += """
            AND (
                doc_number LIKE ?
                OR party LIKE ?
                OR subject LIKE ?
                OR doc_date LIKE ?
            )
        """

        keyword = f"%{search_text}%"

        params.extend([
            keyword,
            keyword,
            keyword,
            keyword
        ])

    query += " ORDER BY id DESC"

    rows = conn.execute(query, params).fetchall()
    conn.close()

    return rows


def delete_document(doc_id):
    """حذف المستند من قاعدة البيانات وملفه من الأرشيف."""

    conn = get_connection()

    row = conn.execute(
        "SELECT file_path FROM documents WHERE id = ?",
        (doc_id,)
    ).fetchone()

    if row:
        file_path = row["file_path"]

        if file_path:
            path = Path(file_path)

            # حذف الملف فقط إذا كان داخل مجلد الأرشيف
            try:
                if path.exists() and ARCHIVE_DIR.resolve() in path.resolve().parents:
                    path.unlink()
            except OSError:
                pass

        conn.execute(
            "DELETE FROM documents WHERE id = ?",
            (doc_id,)
        )

        conn.commit()

    conn.close()


# ==========================================
# عرض اللوجو والعناوين
# ==========================================

if LOGO_PATH.exists():

    # ثلاثة أعمدة لتوسيط اللوجو فعليًا
    left_col, center_col, right_col = st.columns([1, 2, 1])

    with center_col:
        st.image(
            str(LOGO_PATH),
            width=140
        )

else:
    st.warning(
        "لم يتم العثور على ملف اللوجو. "
        "تأكد من وجود logo.png بجوار app.py"
    )

st.markdown("""
<div class="main-title">
الأكاديمية المهنية للمعلمين – فرع الجيزة
</div>

<div class="sub-title">
المنظومة الرقمية للوارد والصادر
</div>
""", unsafe_allow_html=True)


# ==========================================
# القائمة الرئيسية
# ==========================================

if "page" not in st.session_state:
    st.session_state.page = "الرئيسية"


def go_to(page):
    st.session_state.page = page


if st.session_state.page == "الرئيسية":

    st.markdown(
        '<div class="section-title">📥 سجل الوارد</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ إضافة وارد جديد", key="add_incoming"):
            go_to("إضافة وارد")
            st.rerun()

    with col2:
        if st.button("🏠 الرئيسية", key="home_incoming"):
            go_to("الرئيسية")
            st.rerun()

    st.markdown(
        '<div class="section-title">📤 سجل الصادر</div>',
        unsafe_allow_html=True
