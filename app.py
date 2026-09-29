import streamlit as st
import sqlite3
from pathlib import Path
from datetime import date, datetime


# =========================================================
# إعدادات الصفحة
# =========================================================

st.set_page_config(
    page_title="منظومة الوارد والصادر",
    page_icon="📁",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# المسارات
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "documents.db"

ARCHIVE_DIR = BASE_DIR / "Archive_Files"
INCOMING_DIR = ARCHIVE_DIR / "Incoming"
OUTGOING_DIR = ARCHIVE_DIR / "Outgoing"


# =========================================================
# البحث عن الشعار
# =========================================================

def find_logo():

    candidates = [
        BASE_DIR / "logo.png",
        BASE_DIR / "logo.PNG",
        BASE_DIR / "logo.jpg",
        BASE_DIR / "logo.jpeg",
        BASE_DIR / "شعار.png",
        BASE_DIR / "شعار.jpg",
    ]

    for path in candidates:
        if path.exists():
            return path

    return None


LOGO_PATH = find_logo()


# =========================================================
# إنشاء المجلدات
# =========================================================

INCOMING_DIR.mkdir(parents=True, exist_ok=True)
OUTGOING_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# كلمة المرور
# =========================================================

APP_PASSWORD = "1234"


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =========================================
       الصفحة العامة
       ========================================= */

    html,
    body {
        margin: 0 !important;
        padding: 0 !important;
    }

    .stApp {
        margin: 0 !important;
        padding: 0 !important;
        direction: rtl;
        text-align: right;
        background-color: #f7f9fc;
    }

    .block-container {
        max-width: 950px !important;
        width: 94% !important;
        padding-top: 8px !important;
        padding-bottom: 25px !important;
        margin: 0 auto !important;
    }

    header,
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    #MainMenu,
    footer {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }


    /* =========================================
       الخطوط العامة
       ========================================= */

    body,
    .stApp,
    input,
    textarea,
    button,
    select {
        font-family:
            "Tahoma",
            "Arial",
            sans-serif !important;
    }


    /* =========================================
       تسجيل الدخول
       ========================================= */

    .login-container {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        text-align: center;
        padding-top: 5px;
        padding-bottom: 20px;
        margin: 0 auto;
    }

    .login-title {
        color: #17365d;
        font-size: 27px;
        font-weight: 900;
        margin-top: 5px;
        margin-bottom: 5px;
        text-align: center;
    }

    .login-subtitle {
        color: #65748b;
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 18px;
        text-align: center;
    }

    .login-box {
        width: 100%;
        max-width: 450px;
        background: white;
        border: 1px solid #dfe5ec;
        border-radius: 16px;
        padding: 24px;
        box-sizing: border-box;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        margin: 0 auto;
        text-align: right;
    }


    /* =========================================
       الشعار
       ========================================= */

    .logo-space {
        width: 100%;
        text-align: center;
        margin-top: 0;
        margin-bottom: 5px;
    }


    /* =========================================
       العنوان الرئيسي
       ========================================= */

    .main-title {
        width: 100%;
        text-align: center;
        color: #17365d;
        font-size: 27px;
        font-weight: 900;
        margin-top: 4px;
        margin-bottom: 3px;
    }

    .main-subtitle {
        width: 100%;
        text-align: center;
        color: #68778c;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 18px;
    }


    /* =========================================
       العناوين
       ========================================= */

    .section-title {
        color: #17365d;
        font-size: 21px;
        font-weight: 900;
        margin-top: 10px;
        margin-bottom: 10px;
        text-align: right;
    }

    .page-title {
        color: #17365d;
        font-size: 24px;
        font-weight: 900;
        text-align: center;
        margin-top: 8px;
        margin-bottom: 15px;
    }


    /* =========================================
       بطاقات الوارد والصادر
       ========================================= */

    .document-card {
        width: 100%;
        box-sizing: border-box;
        background: #ffffff;
        border: 1px solid #dce3eb;
        border-radius: 13px;
        padding: 18px;
        margin: 4px 0 14px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        direction: rtl;
    }

    .document-card-title {
        width: 100%;
        color: #17365d;
        font-size: 19px;
        font-weight: 900;
        border-bottom: 2px solid #edf1f5;
        padding-bottom: 10px;
        margin-bottom: 14px;
        text-align: right;
    }

    .document-grid {
        width: 100%;
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
    }

    .document-field {
        background: #f7f9fc;
        border: 1px solid #edf0f4;
        border-radius: 9px;
        padding: 11px;
        min-width: 0;
        box-sizing: border-box;
    }

    .document-field-label {
        color: #6b7280;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 4px;
        text-align: right;
    }

    .document-field-value {
        color: #17365d;
        font-size: 15px;
        font-weight: 800;
        line-height: 1.7;
        word-break: break-word;
        overflow-wrap: anywhere;
        text-align: right;
    }

    .document-subject {
        grid-column: 1 / -1;
        background: #f7f9fc;
        border: 1px solid #edf0f4;
        border-radius: 9px;
        padding: 12px;
        box-sizing: border-box;
    }

    .document-subject-value {
        color: #17365d;
        font-size: 15px;
        font-weight: 700;
        line-height: 1.9;
        word-break: break-word;
        overflow-wrap: anywhere;
        text-align: right;
    }


    /* =========================================
       البطاقات الإحصائية
       ========================================= */

    .stat-card {
        background: #ffffff;
        border: 1px solid #dfe5ec;
        border-radius: 13px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .stat-title {
        color: #6b7280;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .stat-number {
        color: #17365d;
        font-size: 26px;
        font-weight: 900;
    }


    /* =========================================
       الفوتر
       ========================================= */

    .app-footer {
        width: 100%;
        text-align: center;
        margin-top: 30px;
        padding-top: 15px;
        border-top: 1px solid #dfe5ec;
        color: #68778c;
        font-size: 13px;
        line-height: 1.8;
    }

    .footer-main {
        color: #17365d;
        font-weight: 800;
    }

    .footer-credit {
        color: #7b8798;
        font-weight: 600;
    }


    /* =========================================
       أزرار Streamlit
       ========================================= */

    .stButton > button {
        width: 100%;
        border-radius: 9px !important;
        font-weight: 800 !important;
        min-height: 42px !important;
    }

    .stDownloadButton > button {
        width: 100%;
        border-radius: 9px !important;
        font-weight: 800 !important;
    }


    /* =========================================
       الحقول
       ========================================= */

    .stTextInput input,
    .stTextArea textarea,
    .stDateInput input,
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 9px !important;
    }


    /* =========================================
       الموبايل
       ========================================= */

    @media(max-width:600px) {

        .block-container {
            width: 96% !important;
            padding-top: 5px !important;
        }

        .main-title {
            font-size: 22px;
        }

        .main-subtitle {
            font-size: 13px;
        }

        .login-title {
            font-size: 22px;
        }

        .document-grid {
            grid-template-columns: 1fr;
        }

        .document-subject {
            grid-column: auto;
        }

        .document-card {
            padding: 12px;
        }

        .document-card-title {
            font-size: 17px;
        }

        .document-field-value,
        .document-subject-value {
            font-size: 14px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# قاعدة البيانات
# =========================================================

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_connection()

    conn.execute(
        """
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
        """
    )

    conn.commit()
    conn.close()


init_db()


# =========================================================
# دوال الشعار
# =========================================================

def show_logo(width=170):

    if LOGO_PATH is None:

        st.warning(
            "⚠️ لم يتم العثور على ملف الشعار.\n\n"
            "ضع ملف الشعار باسم logo.png بجوار ملف app.py."
        )

        return False

    try:

        left, center, right = st.columns([1, 2, 1])

        with center:
            st.image(
                str(LOGO_PATH),
                width=width
            )

        return True

    except Exception as e:

        st.warning(f"تعذر عرض الشعار: {e}")

        return False


# =========================================================
# دوال الملفات
# =========================================================

def get_archive_folder(doc_type):

    if doc_type == "وارد":
        return INCOMING_DIR

    return OUTGOING_DIR


def save_uploaded_file(uploaded_file, doc_type):

    if uploaded_file is None:
        return None

    folder = get_archive_folder(doc_type)

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    original_name = Path(uploaded_file.name).name

    safe_name = f"{timestamp}_{original_name}"

    file_path = folder / safe_name

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return str(file_path)


def delete_old_file(file_path):

    if not file_path:
        return

    try:

        path = Path(file_path).resolve()
        archive_root = ARCHIVE_DIR.resolve()

        if archive_root in path.parents and path.exists():
            path.unlink()

    except Exception:
        pass


# =========================================================
# دوال قاعدة البيانات
# =========================================================

def get_documents(
    doc_type=None,
    search_text=None
):

    conn = get_connection()

    query = """
        SELECT *
        FROM documents
        WHERE 1=1
    """

    params = []

    if doc_type and doc_type != "الكل":

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

        search_value = f"%{search_text}%"

        params.extend(
            [
                search_value,
                search_value,
                search_value,
                search_value
            ]
        )

    query += " ORDER BY id DESC"

    rows = conn.execute(
        query,
        params
    ).fetchall()

    conn.close()

    return rows


def get_document(document_id):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT *
        FROM documents
        WHERE id = ?
        """,
        (document_id,)
    ).fetchone()

    conn.close()

    return row


def add_document(
    doc_type,
    doc_number,
    doc_date,
    party,
    subject,
    file_path
):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO documents
        (
            doc_type,
            doc_number,
            doc_date,
            party,
            subject,
            file_path
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            doc_type,
            doc_number,
            doc_date,
            party,
            subject,
            file_path
        )
    )

    conn.commit()
    conn.close()


def update_document(
    document_id,
    doc_number,
    doc_date,
    party,
    subject,
    new_file_path=None
):

    conn = get_connection()

    if new_file_path:

        conn.execute(
            """
            UPDATE documents

            SET
                doc_number = ?,
                doc_date = ?,
                party = ?,
                subject = ?,
                file_path = ?

            WHERE id = ?
            """,
            (
                doc_number,
                doc_date,
                party,
                subject,
                new_file_path,
                document_id
            )
        )

    else:

        conn.execute(
            """
            UPDATE documents

            SET
                doc_number = ?,
                doc_date = ?,
                party = ?,
                subject = ?

            WHERE id = ?
            """,
            (
                doc_number,
                doc_date,
                party,
                subject,
                document_id
            )
        )

    conn.commit()
    conn.close()


def delete_document(document_id):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT file_path
        FROM documents
        WHERE id = ?
        """,
        (document_id,)
    ).fetchone()

    if row:

        delete_old_file(
            row["file_path"]
        )

    conn.execute(
        """
        DELETE FROM documents
        WHERE id = ?
        """,
        (document_id,)
    )

    conn.commit()
    conn.close()


# =========================================================
# التنقل بين الصفحات
# =========================================================

def go_to(page):

    st.session_state.page = page

    st.rerun()


# =========================================================
# Session State
# =========================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "page" not in st.session_state:
    st.session_state.page = "الرئيسية"

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

if "view_filter" not in st.session_state:
    st.session_state.view_filter = "الكل"


# =========================================================
# صفحة تسجيل الدخول
# =========================================================

if not st.session_state.authenticated:

    st.markdown(
        '<div class="login-container">',
        unsafe_allow_html=True
    )

    show_logo(170)

    st.markdown(
        """
        <div class="login-title">
            منظومة الوارد والصادر
        </div>

        <div class="login-subtitle">
            الأكاديمية المهنية للمعلمين – فرع الجيزة
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            color:#17365d;
            font-size:18px;
            font-weight:900;
            margin-bottom:10px;
            text-align:right;
        ">
            🔐 تسجيل الدخول
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # كلمة المرور
    #
    # type="password"
    # و Enter يعمل تلقائياً لأن الحقل داخل Form
    # =====================================================

    with st.form(
        "login_form",
        clear_on_submit=False
    ):

        password = st.text_input(
            "كلمة المرور",
            type="password",
            placeholder="أدخل كلمة المرور ثم اضغط Enter",
            key="login_password"
        )

        login_button = st.form_submit_button(
            "دخول",
            use_container_width=True
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    # =====================================================
    # تسجيل الدخول
    #
    # الضغط على Enter داخل خانة كلمة المرور
    # يقوم بإرسال Form وبالتالي ينفذ هذا الجزء
    # =====================================================

    if login_button:

        if password == APP_PASSWORD:

            st.session_state.authenticated = True
            st.session_state.page = "الرئيسية"

            st.rerun()

        else:

            st.error(
                "❌ كلمة المرور غير صحيحة"
            )

    st.markdown(
        """
        <div class="app-footer">

            <div class="footer-main">
                الأكاديمية المهنية للمعلمين - فرع الجيزة
            </div>

            <div class="footer-credit">
                ✦ تصميم وتنفيذ أحمد الجنزوري ✦
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# =========================================================
# الهيدر الداخلي
# =========================================================

show_logo(145)

st.markdown(
    """
    <div class="main-title">
        منظومة الوارد والصادر
    </div>

    <div class="main-subtitle">
        الأكاديمية المهنية للمعلمين – فرع الجيزة
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# القائمة الرئيسية
# =========================================================

menu_col1, menu_col2, menu_col3, menu_col4 = st.columns(4)

with menu_col1:

    if st.button(
        "🏠 الرئيسية",
        use_container_width=True
    ):
        go_to("الرئيسية")


with menu_col2:

    if st.button(
        "📥 إضافة وارد",
        use_container_width=True
    ):
        go_to("إضافة وارد")


with menu_col3:

    if st.button(
        "📤 إضافة صادر",
        use_container_width=True
    ):
        go_to("إضافة صادر")


with menu_col4:

    if st.button(
        "📋 السجلات",
        use_container_width=True
    ):
        go_to("السجلات")


search_col, logout_col = st.columns([3, 1])

with search_col:

    if st.button(
        "🔎 البحث",
        use_container_width=True
    ):
        go_to("البحث")


with logout_col:

    if st.button(
        "🚪 خروج",
        use_container_width=True
    ):

        st.session_state.authenticated = False

        st.rerun()


st.divider()


# =========================================================
# عرض بطاقة مستند
# =========================================================

def display_document_card(row):

    doc_type = row["doc_type"]

    type_icon = "📥" if doc_type == "وارد" else "📤"

    st.markdown(
        f"""
        <div class="document-card">

            <div class="document-card-title">
                {type_icon} {doc_type}
            </div>

            <div class="document-grid">

                <div class="document-field">

                    <div class="document-field-label">
                        رقم المستند
                    </div>

                    <div class="document-field-value">
                        {row["doc_number"]}
                    </div>

                </div>


                <div class="document-field">

                    <div class="document-field-label">
                        التاريخ
                    </div>

                    <div class="document-field-value">
                        {row["doc_date"]}
                    </div>

                </div>


                <div class="document-field">

                    <div class="document-field-label">
                        الجهة
                    </div>

                    <div class="document-field-value">
                        {row["party"]}
                    </div>

                </div>


                <div class="document-subject">

                    <div class="document-field-label">
                        الموضوع
                    </div>

                    <div class="document-subject-value">
                        {row["subject"]}
                    </div>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# الصفحة الرئيسية
# =========================================================

if st.session_state.page == "الرئيسية":

    st.markdown(
        '<div class="page-title">🏠 الرئيسية</div>',
        unsafe_allow_html=True
    )

    all_docs = get_documents()

    incoming_docs = [
        row for row in all_docs
        if row["doc_type"] == "وارد"
    ]

    outgoing_docs = [
        row for row in all_docs
        if row["doc_type"] == "صادر"
    ]

    # =====================================================
    # الإحصائيات
    # =====================================================

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-title">
                    إجمالي المستندات
                </div>

                <div class="stat-number">
                    {len(all_docs)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-title">
                    الوارد
                </div>

                <div class="stat-number">
                    {len(incoming_docs)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-title">
                    الصادر
                </div>

                <div class="stat-number">
                    {len(outgoing_docs)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # =====================================================
    # أحدث الوارد
    # =====================================================

    st.markdown(
        '<div class="section-title">📥 أحدث الوارد</div>',
        unsafe_allow_html=True
    )

    if incoming_docs:

        for row in incoming_docs[:5]:

            display_document_card(row)

            col1, col2, col3 = st.columns(3)

            with col1:

                if row["file_path"]:

                    file_path = Path(row["file_path"])

                    if file_path.exists():

                        with open(
                            file_path,
                            "rb"
                        ) as file:

                            st.download_button(
                                "📄 تحميل PDF",
                                data=file.read(),
                                file_name=file_path.name,
                                mime="application/pdf",
                                key=f"home_in_pdf_{row['id']}",
                                use_container_width=True
                            )

            with col2:

                if st.button(
                    "✏️ تعديل",
                    key=f"home_in_edit_{row['id']}",
                    use_container_width=True
                ):

                    st.session_state.edit_id = row["id"]
                    go_to("تعديل")

            with col3:

                if st.button(
                    "🗑️ حذف",
                    key=f"home_in_delete_{row['id']}",
                    use_container_width=True
                ):

                    st.session_state.delete_id = row["id"]
                    go_to("تأكيد الحذف")

    else:

        st.info(
            "لا توجد مستندات واردة حتى الآن."
        )


    # =====================================================
    # أحدث الصادر
    # =====================================================

    st.markdown(
        '<div class="section-title">📤 أحدث الصادر</div>',
        unsafe_allow_html=True
    )

    if outgoing_docs:

        for row in outgoing_docs[:5]:

            display_document_card(row)

            col1, col2, col3 = st.columns(3)

            with col1:

                if row["file_path"]:

                    file_path = Path(row["file_path"])

                    if file_path.exists():

                        with open(
                            file_path,
                            "rb"
                        ) as file:

                            st.download_button(
                                "📄 تحميل PDF",
                                data=file.read(),
                                file_name=file_path.name,
                                mime="application/pdf",
                                key=f"home_out_pdf_{row['id']}",
                                use_container_width=True
                            )

            with col2:

                if st.button(
                    "✏️ تعديل",
                    key=f"home_out_edit_{row['id']}",
                    use_container_width=True
                ):

                    st.session_state.edit_id = row["id"]
                    go_to("تعديل")

            with col3:

                if st.button(
                    "🗑️ حذف",
                    key=f"home_out_delete_{row['id']}",
                    use_container_width=True
                ):

                    st.session_state.delete_id = row["id"]
                    go_to("تأكيد الحذف")


    else:

        st.info(
            "لا توجد مستندات صادرة حتى الآن."
        )


# =========================================================
# إضافة وارد / صادر
# =========================================================

elif st.session_state.page in [
    "إضافة وارد",
    "إضافة صادر"
]:

    doc_type = (
        "وارد"
        if st.session_state.page == "إضافة وارد"
        else "صادر"
    )

    icon = "📥" if doc_type == "وارد" else "📤"

    st.markdown(
        f"""
        <div class="page-title">
            {icon} إضافة {doc_type} جديد
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form(
        f"add_{doc_type}_form",
        clear_on_submit=True
    ):

        doc_number = st.text_input(
            "رقم المستند *",
            placeholder="أدخل رقم المستند"
        )

        doc_date = st.date_input(
            "تاريخ المستند *",
            value=date.today(),
            format="DD/MM/YYYY"
        )

        party = st.text_input(
            "الجهة *",
            placeholder="اسم الجهة"
        )

        subject = st.text_area(
            "الموضوع *",
            placeholder="اكتب موضوع المستند",
            height=120
        )

        uploaded_file = st.file_uploader(
            "إرفاق ملف PDF",
            type=["pdf"],
            help="يمكنك إرفاق نسخة PDF من المستند"
        )

        save_button = st.form_submit_button(
            f"💾 حفظ {doc_type}",
            use_container_width=True
        )

    if save_button:

        if not doc_number.strip():

            st.error(
                "⚠️ يرجى إدخال رقم المستند."
            )

        elif not party.strip():

            st.error(
                "⚠️ يرجى إدخال الجهة."
            )

        elif not subject.strip():

            st.error(
                "⚠️ يرجى إدخال الموضوع."
            )

        else:

            file_path = save_uploaded_file(
                uploaded_file,
                doc_type
            )

            add_document(
                doc_type=doc_type,
                doc_number=doc_number.strip(),
                doc_date=doc_date.strftime("%d/%m/%Y"),
                party=party.strip(),
                subject=subject.strip(),
                file_path=file_path
            )

            st.success(
                f"✅ تم حفظ {doc_type} بنجاح."
            )

            st.balloons()


# =========================================================
# السجلات
# =========================================================

elif st.session_state.page == "السجلات":

    st.markdown(
        '<div class="page-title">📋 السجلات</div>',
        unsafe_allow_html=True
    )

    filter_value = st.selectbox(
        "نوع السجل",
        [
            "الكل",
            "وارد",
            "صادر"
        ],
        index=0
    )

    search_value = st.text_input(
        "🔎 بحث داخل السجلات",
        placeholder="رقم المستند أو الجهة أو الموضوع أو التاريخ"
    )

    rows = get_documents(
        doc_type=filter_value,
        search_text=search_value.strip()
    )

    st.info(
        f"عدد النتائج: {len(rows)}"
    )

    if not rows:

        st.warning(
            "لا توجد بيانات مطابقة."
        )

    for row in rows:

        display_document_card(row)

        col1, col2, col3 = st.columns(3)

        with col1:

            if row["file_path"]:

                file_path = Path(row["file_path"])

                if file_path.exists():

                    with open(
                        file_path,
                        "rb"
                    ) as file:

                        st.download_button(
                            "📄 تحميل PDF",
                            data=file.read(),
                            file_name=file_path.name,
                            mime="application/pdf",
                            key=f"records_pdf_{row['id']}",
                            use_container_width=True
                        )

        with col2:

            if st.button(
                "✏️ تعديل",
                key=f"records_edit_{row['id']}",
                use_container_width=True
            ):

                st.session_state.edit_id = row["id"]

                go_to("تعديل")

        with col3:

            if st.button(
                "🗑️ حذف",
                key=f"records_delete_{row['id']}",
                use_container_width=True
            ):

                st.session_state.delete_id = row["id"]

                go_to("تأكيد الحذف")


# =========================================================
# البحث
# =========================================================

elif st.session_state.page == "البحث":

    st.markdown(
        '<div class="page-title">🔎 البحث</div>',
        unsafe_allow_html=True
    )

    search_value = st.text_input(
        "ابحث عن مستند",
        placeholder="رقم المستند - الجهة - الموضوع - التاريخ"
    )

    if search_value.strip():

        rows = get_documents(
            search_text=search_value.strip()
        )

        st.info(
            f"تم العثور على {len(rows)} نتيجة."
        )

        for row in rows:

            display_document_card(row)

            col1, col2, col3 = st.columns(3)

            with col1:

                if row["file_path"]:

                    file_path = Path(row["file_path"])

                    if file_path.exists():

                        with open(
                            file_path,
                            "rb"
                        ) as file:

                            st.download_button(
                                "📄 تحميل PDF",
                                data=file.read(),
                                file_name=file_path.name,
                                mime="application/pdf",
                                key=f"search_pdf_{row['id']}",
                                use_container_width=True
                            )

            with col2:

                if st.button(
                    "✏️ تعديل",
                    key=f"search_edit_{row['id']}",
                    use_container_width=True
                ):

                    st.session_state.edit_id = row["id"]

                    go_to("تعديل")

            with col3:

                if st.button(
                    "🗑️ حذف",
                    key=f"search_delete_{row['id']}",
                    use_container_width=True
                ):

                    st.session_state.delete_id = row["id"]

                    go_to("تأكيد الحذف")

    else:

        st.info(
            "اكتب كلمة البحث لعرض النتائج."
        )


# =========================================================
# تعديل مستند
# =========================================================

elif st.session_state.page == "تعديل":

    st.markdown(
        '<div class="page-title">✏️ تعديل المستند</div>',
        unsafe_allow_html=True
    )

    edit_id = st.session_state.get(
        "edit_id"
    )

    if not edit_id:

        st.warning(
            "لم يتم اختيار مستند للتعديل."
        )

        if st.button(
            "العودة للسجلات",
            use_container_width=True
        ):

            go_to("السجلات")

    else:

        row = get_document(edit_id)

        if not row:

            st.error(
                "المستند غير موجود."
            )

        else:

            with st.form(
                "edit_document_form"
            ):

                st.markdown(
                    f"""
                    <div style="
                        color:#17365d;
                        font-size:17px;
                        font-weight:900;
                        margin-bottom:12px;
                    ">
                        تعديل {row["doc_type"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                doc_number = st.text_input(
                    "رقم المستند *",
                    value=row["doc_number"]
                )

                try:

                    old_date = datetime.strptime(
                        row["doc_date"],
                        "%d/%m/%Y"
                    ).date()

                except Exception:

                    old_date = date.today()

                doc_date = st.date_input(
                    "تاريخ المستند *",
                    value=old_date,
                    format="DD/MM/YYYY"
                )

                party = st.text_input(
                    "الجهة *",
                    value=row["party"]
                )

                subject = st.text_area(
                    "الموضوع *",
                    value=row["subject"],
                    height=120
                )

                if row["file_path"]:

                    current_file = Path(
                        row["file_path"]
                    )

                    if current_file.exists():

                        st.success(
                            f"📎 الملف الحالي: {current_file.name}"
                        )

                new_file = st.file_uploader(
                    "استبدال ملف PDF",
                    type=["pdf"]
                )

                save_edit = st.form_submit_button(
                    "💾 حفظ التعديلات",
                    use_container_width=True
                )

            if save_edit:

                if not doc_number.strip():

                    st.error(
                        "⚠️ يرجى إدخال رقم المستند."
                    )

                elif not party.strip():

                    st.error(
                        "⚠️ يرجى إدخال الجهة."
                    )

                elif not subject.strip():

                    st.error(
                        "⚠️ يرجى إدخال الموضوع."
                    )

                else:

                    new_file_path = None

                    if new_file:

                        old_file_path = row["file_path"]

                        new_file_path = save_uploaded_file(
                            new_file,
                            row["doc_type"]
                        )

                        if old_file_path:

                            delete_old_file(
                                old_file_path
                            )

                    update_document(
                        document_id=edit_id,
                        doc_number=doc_number.strip(),
                        doc_date=doc_date.strftime(
                            "%d/%m/%Y"
                        ),
                        party=party.strip(),
                        subject=subject.strip(),
                        new_file_path=new_file_path
                    )

                    st.success(
                        "✅ تم تحديث المستند بنجاح."
                    )

                    st.session_state.pop(
                        "edit_id",
                        None
                    )

                    st.session_state.page = "السجلات"

                    st.rerun()


# =========================================================
# تأكيد الحذف
# =========================================================

elif st.session_state.page == "تأكيد الحذف":

    st.markdown(
        '<div class="page-title">🗑️ تأكيد الحذف</div>',
        unsafe_allow_html=True
    )

    delete_id = st.session_state.get(
        "delete_id"
    )

    if not delete_id:

        st.warning(
            "لم يتم اختيار مستند للحذف."
        )

        if st.button(
            "العودة للسجلات",
            use_container_width=True
        ):

            go_to("السجلات")

    else:

        row = get_document(delete_id)

        if not row:

            st.error(
                "المستند غير موجود."
            )

        else:

            display_document_card(row)

            st.warning(
                "⚠️ هل أنت متأكد من حذف هذا المستند؟ "
                "سيتم أيضاً حذف ملف PDF المرتبط به إن وجد."
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "❌ إلغاء",
                    use_container_width=True
                ):

                    st.session_state.pop(
                        "delete_id",
                        None
                    )

                    go_to("السجلات")

            with col2:

                if st.button(
                    "🗑️ نعم، حذف المستند",
                    use_container_width=True
                ):

                    delete_document(
                        delete_id
                    )

                    st.session_state.pop(
                        "delete_id",
                        None
                    )

                    st.success(
                        "✅ تم حذف المستند بنجاح."
                    )

                    st.session_state.page = "السجلات"

                    st.rerun()


# =========================================================
# الفوتر
# =========================================================

st.markdown(
    """
    <div class="app-footer">

        <div class="footer-main">
            الأكاديمية المهنية للمعلمين - فرع الجيزة
        </div>

        <div class="footer-credit">
            ✦ تصميم وتنفيذ أحمد الجنزوري ✦
        </div>

    </div>
    """,
    unsafe_allow_html=True
)
