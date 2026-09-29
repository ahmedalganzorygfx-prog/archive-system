import streamlit as st
import sqlite3
from pathlib import Path
from datetime import date, datetime


# ============================================================
# إعدادات الصفحة
# ============================================================

st.set_page_config(
    page_title="منظومة الوارد والصادر",
    page_icon="📁",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================================
# المسارات
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "documents.db"

ARCHIVE_DIR = BASE_DIR / "Archive_Files"
INCOMING_DIR = ARCHIVE_DIR / "Incoming"
OUTGOING_DIR = ARCHIVE_DIR / "Outgoing"


# ============================================================
# البحث عن الشعار
# ============================================================

def find_logo():

    candidates = [
        BASE_DIR / "logo.png",
        BASE_DIR / "logo.PNG",
        BASE_DIR / "logo.jpg",
        BASE_DIR / "logo.jpeg",
        BASE_DIR / "شعار.png",
        BASE_DIR / "شعار.jpg"
    ]

    for logo in candidates:

        if logo.exists():
            return logo

    return None


LOGO_PATH = find_logo()


# ============================================================
# إنشاء المجلدات
# ============================================================

INCOMING_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTGOING_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# إعدادات النظام
# ============================================================

APP_PASSWORD = "1234"


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       الصفحة العامة
       ====================================================== */

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

        background: #f5f7fa;

    }


    .block-container {

        max-width: 950px !important;

        width: 94% !important;

        padding-top: 8px !important;
        padding-bottom: 25px !important;

        margin: 0 auto !important;

    }


    /* ======================================================
       إخفاء عناصر Streamlit
       ====================================================== */

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


    /* ======================================================
       الخط
       ====================================================== */

    body,
    .stApp,
    input,
    textarea,
    button,
    select {

        font-family:
            Tahoma,
            Arial,
            sans-serif !important;

    }


    /* ======================================================
       شاشة الدخول
       ====================================================== */

    .login-container {

        width: 100%;

        display: flex;
        flex-direction: column;

        align-items: center;

        text-align: center;

        padding-top: 3px;
        padding-bottom: 20px;

        margin: 0 auto;

    }


    .login-main-title {

        width: 100%;

        text-align: center !important;

        color: #17365d;

        font-size: 29px;
        font-weight: 900;

        line-height: 1.5;

        margin: 0 auto 3px auto;

    }


    .login-sub-title {

        width: 100%;

        text-align: center !important;

        color: #294d7c;

        font-size: 19px;
        font-weight: 700;

        line-height: 1.5;

        margin: 0 auto 18px auto;

    }


    .login-box {

        width: 100%;

        max-width: 430px;

        margin: 0 auto;

        text-align: right;

    }


    /* ======================================================
       العنوان الداخلي
       ====================================================== */

    .internal-logo-space {

        width: 100%;

        display: flex;

        justify-content: center;

        align-items: center;

        margin: 0 auto 4px auto;

        padding: 0;

    }


    .main-title {

        width: 100%;

        text-align: center !important;

        color: #17365d;

        font-size: 26px;
        font-weight: 900;

        line-height: 1.5;

        margin: 0 auto 2px auto;

    }


    .sub-title {

        width: 100%;

        text-align: center !important;

        color: #294d7c;

        font-size: 18px;
        font-weight: 600;

        line-height: 1.5;

        margin: 0 auto 17px auto;

    }


    /* ======================================================
       عناوين الأقسام
       ====================================================== */

    .section-title {

        width: 100%;

        box-sizing: border-box;

        background: linear-gradient(
            90deg,
            #17365d,
            #294d7c
        );

        color: white;

        border-radius: 10px;

        padding: 10px 15px;

        margin-top: 12px;
        margin-bottom: 12px;

        font-size: 19px;

        font-weight: 800;

        text-align: right;

    }


    /* ======================================================
       البطاقات الرئيسية
       ====================================================== */

    .info-card {

        width: 100%;

        box-sizing: border-box;

        background: white;

        border-radius: 13px;

        padding: 16px;

        margin-bottom: 12px;

        border: 1px solid #dfe5ec;

        box-shadow:
            0 2px 8px rgba(0, 0, 0, 0.06);

    }


    /* ======================================================
       بطاقة بيانات المستند
       ====================================================== */

    .document-card {

        width: 100%;

        box-sizing: border-box;

        background: #ffffff;

        border: 1px solid #dce3eb;

        border-radius: 14px;

        padding: 16px;

        margin: 5px 0 10px 0;

        box-shadow:
            0 2px 8px rgba(0,0,0,0.05);

        direction: rtl;

    }


    /* ======================================================
       عنوان البطاقة
       ====================================================== */

    .document-card-header {

        width: 100%;

        display: flex;

        align-items: center;

        justify-content: space-between;

        gap: 10px;

        padding-bottom: 11px;

        margin-bottom: 13px;

        border-bottom: 2px solid #edf1f5;

        box-sizing: border-box;

    }


    .document-card-title {

        color: #17365d;

        font-size: 18px;

        font-weight: 900;

        text-align: right;

    }


    .document-type-badge {

        display: inline-block;

        padding: 5px 12px;

        border-radius: 20px;

        background: #edf4ff;

        color: #17365d;

        font-size: 13px;

        font-weight: 800;

        white-space: nowrap;

    }


    /* ======================================================
       شبكة البيانات
       ====================================================== */

    .document-grid {

        width: 100%;

        display: grid;

        grid-template-columns:
            repeat(2, minmax(0, 1fr));

        gap: 10px;

    }


    .document-field {

        min-width: 0;

        box-sizing: border-box;

        background: #f7f9fc;

        border: 1px solid #e8edf3;

        border-radius: 9px;

        padding: 11px;

    }


    .document-field-label {

        color: #707b8c;

        font-size: 12px;

        font-weight: 700;

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


    /* ======================================================
       الموضوع
       ====================================================== */

    .document-subject {

        grid-column: 1 / -1;

        box-sizing: border-box;

        background: #f7f9fc;

        border: 1px solid #e8edf3;

        border-radius: 9px;

        padding: 12px;

    }


    .document-subject-value {

        color: #26364d;

        font-size: 15px;

        font-weight: 700;

        line-height: 1.9;

        word-break: break-word;

        overflow-wrap: anywhere;

        text-align: right;

    }


    /* ======================================================
       ملف PDF
       ====================================================== */

    .pdf-status {

        width: 100%;

        box-sizing: border-box;

        margin-top: 10px;

        padding: 10px 12px;

        border-radius: 9px;

        background: #f5f8fc;

        border: 1px solid #e2e8f0;

        color: #526174;

        font-size: 13px;

        font-weight: 700;

        text-align: right;

    }


    /* ======================================================
       عنوان الصفحة
       ====================================================== */

    .page-title {

        width: 100%;

        text-align: center;

        color: #17365d;

        font-size: 23px;

        font-weight: 900;

        margin: 5px 0 15px 0;

    }


    /* ======================================================
       الإحصائيات
       ====================================================== */

    .stat-card {

        background: #ffffff;

        border: 1px solid #dfe5ec;

        border-radius: 12px;

        padding: 14px;

        text-align: center;

        box-shadow:
            0 2px 7px rgba(0,0,0,0.04);

    }


    .stat-title {

        color: #6b7280;

        font-size: 12px;

        font-weight: 700;

    }


    .stat-number {

        color: #17365d;

        font-size: 25px;

        font-weight: 900;

        margin-top: 3px;

    }


    /* ======================================================
       الفوتر
       ====================================================== */

    .custom-footer {

        width: 100%;

        text-align: center;

        color: #6b7280;

        font-size: 13px;

        margin-top: 25px;

        padding-top: 10px;

        border-top: 1px solid #e5e7eb;

        line-height: 1.8;

    }


    /* ======================================================
       الحقول
       ====================================================== */

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {

        direction: rtl;

        text-align: right;

    }


    div[data-testid="stDateInput"] input {

        direction: rtl;

        text-align: right;

    }


    /* ======================================================
       الأزرار
       ====================================================== */

    .stButton > button {

        width: 100%;

        border-radius: 8px !important;

        min-height: 42px;

        font-weight: 700;

    }


    .stDownloadButton > button {

        width: 100%;

        border-radius: 8px !important;

        min-height: 42px;

        font-weight: 700;

    }


    /* ======================================================
       رفع الملفات
       ====================================================== */

    section[data-testid="stFileUploader"] {

        direction: rtl;

        text-align: right;

    }


    /* ======================================================
       الرسائل
       ====================================================== */

    div[data-testid="stAlert"] {

        direction: rtl;

        text-align: right;

    }


    /* ======================================================
       Selectbox
       ====================================================== */

    div[data-baseweb="select"] {

        direction: rtl;

        text-align: right;

    }


    /* ======================================================
       Expander
       ====================================================== */

    div[data-testid="stExpander"] {

        border-radius: 10px !important;

        border: 1px solid #dfe5ec !important;

        background: white !important;

        margin-bottom: 10px !important;

    }


    /* ======================================================
       الموبايل
       ====================================================== */

    @media (max-width: 600px) {

        .block-container {

            width: 95% !important;

            padding-top: 5px !important;

        }


        .login-main-title {

            font-size: 22px;

        }


        .login-sub-title {

            font-size: 16px;

        }


        .main-title {

            font-size: 21px;

        }


        .sub-title {

            font-size: 16px;

        }


        .section-title {

            font-size: 17px;

        }


        .page-title {

            font-size: 20px;

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


        .document-card-header {

            flex-direction: column;

            align-items: flex-start;

        }


        .document-card-title {

            font-size: 16px;

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


# ============================================================
# Session State
# ============================================================

if "authenticated" not in st.session_state:

    st.session_state.authenticated = False


if "page" not in st.session_state:

    st.session_state.page = "الرئيسية"


if "search_query" not in st.session_state:

    st.session_state.search_query = ""


if "view_filter" not in st.session_state:

    st.session_state.view_filter = "الكل"


# ============================================================
# دالة الاتصال بقاعدة البيانات
# ============================================================

def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# ============================================================
# إنشاء قاعدة البيانات
# ============================================================

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


# ============================================================
# دالة عرض الشعار
# ============================================================

def show_logo(width=150):

    if LOGO_PATH is None:

        st.warning(
            "⚠️ لم يتم العثور على الشعار. "
            "ضع ملف logo.png بجوار app.py"
        )

        return

    try:

        left, center, right = st.columns(
            [1, 2, 1]
        )

        with center:

            st.image(
                str(LOGO_PATH),
                width=width
            )

    except Exception as e:

        st.warning(
            f"تعذر عرض الشعار: {e}"
        )


# ============================================================
# وظائف الملفات
# ============================================================

def get_archive_folder(doc_type):

    if doc_type == "وارد":

        return INCOMING_DIR

    return OUTGOING_DIR


def save_uploaded_file(
    uploaded_file,
    doc_type
):

    if uploaded_file is None:

        return None

    folder = get_archive_folder(
        doc_type
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    original_name = Path(
        uploaded_file.name
    ).name

    safe_name = (
        f"{timestamp}_{original_name}"
    )

    file_path = folder / safe_name

    with open(
        file_path,
        "wb"
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )

    return str(file_path)


def delete_old_file(file_path):

    if not file_path:

        return

    try:

        path = Path(
            file_path
        ).resolve()

        archive_root = ARCHIVE_DIR.resolve()

        if (
            archive_root in path.parents
            and path.exists()
        ):

            path.unlink()

    except Exception:

        pass


# ============================================================
# وظائف قاعدة البيانات
# ============================================================

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

    if (
        doc_type
        and doc_type != "الكل"
    ):

        query += """
            AND doc_type = ?
        """

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

        search_value = (
            f"%{search_text}%"
        )

        params.extend(
            [
                search_value,
                search_value,
                search_value,
                search_value
            ]
        )


    query += """
        ORDER BY id DESC
    """


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


# ============================================================
# التنقل
# ============================================================

def go_to(page):

    st.session_state.page = page

    st.rerun()


# ============================================================
# دالة عرض المستند بشكل منظم
# ============================================================

def display_document_card(
    row,
    show_actions=True,
    prefix="record"
):

    doc_type = row["doc_type"]

    if doc_type == "وارد":

        icon = "📥"

    else:

        icon = "📤"


    # --------------------------------------------------------
    # البطاقة
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="document-card">

            <div class="document-card-header">

                <div class="document-card-title">
                    {icon} بيانات المستند
                </div>

                <div class="document-type-badge">
                    {doc_type}
                </div>

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
                        تاريخ المستند
                    </div>

                    <div class="document-field-value">
                        {row["doc_date"]}
                    </div>

                </div>


                <div class="document-field">

                    <div class="document-field-label">
                        الجهة / الطرف
                    </div>

                    <div class="document-field-value">
                        {row["party"]}
                    </div>

                </div>


                <div class="document-field">

                    <div class="document-field-label">
                        نوع المعاملة
                    </div>

                    <div class="document-field-value">
                        {doc_type}
                    </div>

                </div>


                <div class="document-subject">

                    <div class="document-field-label">
                        موضوع المستند
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


    # --------------------------------------------------------
    # حالة الملف
    # --------------------------------------------------------

    if row["file_path"]:

        file_path = Path(
            row["file_path"]
        )

        if file_path.exists():

            st.markdown(
                f"""
                <div class="pdf-status">
                    📎 يوجد ملف PDF مرفق:
                    <b>{file_path.name}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

            with open(
                file_path,
                "rb"
            ) as pdf_file:

                pdf_data = pdf_file.read()


            st.download_button(
                "📥 تحميل ملف PDF",
                data=pdf_data,
                file_name=file_path.name,
                mime="application/pdf",
                key=f"{prefix}_download_{row['id']}",
                use_container_width=True
            )

        else:

            st.warning(
                "⚠️ يوجد ملف مسجل في قاعدة البيانات "
                "ولكنه غير موجود داخل مجلد الأرشيف."
            )

    else:

        st.markdown(
            """
            <div class="pdf-status">
                📄 لا يوجد ملف PDF مرفق بهذا المستند.
            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # أزرار التحكم
    # --------------------------------------------------------

    if show_actions:

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "✏️ تعديل المستند",
                key=f"{prefix}_edit_{row['id']}",
                use_container_width=True
            ):

                st.session_state.edit_id = (
                    row["id"]
                )

                go_to("تعديل")


        with col2:

            if st.button(
                "🗑️ حذف المستند",
                key=f"{prefix}_delete_{row['id']}",
                use_container_width=True
            ):

                st.session_state.delete_id = (
                    row["id"]
                )

                go_to("تأكيد الحذف")


# ============================================================
# تسجيل الدخول
# ============================================================

if not st.session_state.authenticated:

    st.markdown(
        '<div class="login-container">',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # الشعار
    # --------------------------------------------------------

    show_logo(175)


    # --------------------------------------------------------
    # العنوان
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="login-main-title">
            الأكاديمية المهنية للمعلمين – فرع الجيزة
        </div>

        <div class="login-sub-title">
            المنظومة الرقمية للوارد والصادر
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # تسجيل الدخول
    #
    # استخدام st.form يسمح بالضغط على Enter
    # --------------------------------------------------------

    st.markdown(
        '<div class="login-box">',
        unsafe_allow_html=True
    )


    with st.form(
        "login_form",
        clear_on_submit=False
    ):

        password = st.text_input(
            "🔐 كلمة المرور",
            type="password",
            placeholder="أدخل كلمة المرور ثم اضغط Enter"
        )


        login_clicked = st.form_submit_button(
            "🔓 تسجيل الدخول",
            type="primary",
            use_container_width=True
        )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # التحقق من كلمة المرور
    # --------------------------------------------------------

    if login_clicked:

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
        <div class="custom-footer">

            الأكاديمية المهنية للمعلمين - فرع الجيزة

            <br>

            ✦ تصميم وتنفيذ أحمد الجنزوري ✦

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    st.stop()


# ============================================================
# رأس البرنامج بعد تسجيل الدخول
# ============================================================

show_logo(135)


st.markdown(
    """
    <div class="main-title">
        الأكاديمية المهنية للمعلمين – فرع الجيزة
    </div>

    <div class="sub-title">
        المنظومة الرقمية للوارد والصادر
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# القائمة الرئيسية
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    if st.button(
        "🏠 الرئيسية",
        key="menu_home",
        use_container_width=True
    ):

        go_to("الرئيسية")


with col2:

    if st.button(
        "📥 إضافة وارد",
        key="menu_incoming",
        use_container_width=True
    ):

        go_to("إضافة وارد")


with col3:

    if st.button(
        "📤 إضافة صادر",
        key="menu_outgoing",
        use_container_width=True
    ):

        go_to("إضافة صادر")


with col4:

    if st.button(
        "📋 السجلات",
        key="menu_records",
        use_container_width=True
    ):

        go_to("السجلات")


col1, col2 = st.columns(2)


with col1:

    if st.button(
        "🔎 البحث",
        key="menu_search",
        use_container_width=True
    ):

        go_to("البحث")


with col2:

    if st.button(
        "🚪 تسجيل الخروج",
        key="menu_logout",
        use_container_width=True
    ):

        st.session_state.authenticated = False

        st.session_state.page = "الرئيسية"

        st.rerun()


st.divider()


# ============================================================
# الرئيسية
# ============================================================

if st.session_state.page == "الرئيسية":

    st.markdown(
        '<div class="page-title">🏠 الرئيسية</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # الإحصائيات
    # --------------------------------------------------------

    all_docs = get_documents()

    incoming_count = sum(
        1
        for row in all_docs
        if row["doc_type"] == "وارد"
    )

    outgoing_count = sum(
        1
        for row in all_docs
        if row["doc_type"] == "صادر"
    )


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
                    {incoming_count}
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
                    {outgoing_count}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # الوارد
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="section-title">
            📥 سجل الوارد
        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "➕ إضافة وارد جديد",
            key="home_add_incoming",
            use_container_width=True
        ):

            go_to("إضافة وارد")


    with col2:

        if st.button(
            "📋 عرض الوارد",
            key="home_view_incoming",
            use_container_width=True
        ):

            st.session_state.view_filter = "وارد"

            go_to("السجلات")


    # --------------------------------------------------------
    # الصادر
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="section-title">
            📤 سجل الصادر
        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "➕ إضافة صادر جديد",
            key="home_add_outgoing",
            use_container_width=True
        ):

            go_to("إضافة صادر")


    with col2:

        if st.button(
            "📋 عرض الصادر",
            key="home_view_outgoing",
            use_container_width=True
        ):

            st.session_state.view_filter = "صادر"

            go_to("السجلات")


    # --------------------------------------------------------
    # البحث
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="section-title">
            🔎 البحث في الأرشيف
        </div>
        """,
        unsafe_allow_html=True
    )


    search_text = st.text_input(
        "رقم المستند أو الجهة أو الموضوع أو التاريخ",
        placeholder="اكتب كلمة البحث هنا...",
        key="home_search_input"
    )


    if st.button(
        "🔎 تنفيذ البحث",
        type="primary",
        key="home_search_button",
        use_container_width=True
    ):

        st.session_state.search_query = (
            search_text.strip()
        )

        go_to("البحث")


# ============================================================
# إضافة وارد / صادر
# ============================================================

elif st.session_state.page in [
    "إضافة وارد",
    "إضافة صادر"
]:

    doc_type = (
        "وارد"
        if st.session_state.page == "إضافة وارد"
        else "صادر"
    )


    icon = (
        "📥"
        if doc_type == "وارد"
        else "📤"
    )


    st.markdown(
        f"""
        <div class="page-title">
            {icon} إضافة مستند {doc_type}
        </div>
        """,
        unsafe_allow_html=True
    )


    with st.form(
        f"add_form_{doc_type}"
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
            "الجهة / الطرف *",
            placeholder="أدخل اسم الجهة"
        )


        subject = st.text_area(
            "موضوع المستند *",
            placeholder="أدخل موضوع المستند",
            height=110
        )


        uploaded_file = st.file_uploader(
            "إرفاق ملف PDF",
            type=["pdf"],
            help="يمكنك اختيار ملف PDF لأرشفته مع المستند."
        )


        col1, col2 = st.columns(2)


        with col1:

            save_clicked = st.form_submit_button(
                "💾 حفظ المستند",
                type="primary",
                use_container_width=True
            )


        with col2:

            cancel_clicked = st.form_submit_button(
                "↩️ إلغاء",
                use_container_width=True
            )


    if cancel_clicked:

        go_to("الرئيسية")


    if save_clicked:

        errors = []


        if not doc_number.strip():

            errors.append(
                "رقم المستند مطلوب."
            )


        if not party.strip():

            errors.append(
                "الجهة / الطرف مطلوبة."
            )


        if not subject.strip():

            errors.append(
                "موضوع المستند مطلوب."
            )


        if errors:

            for error in errors:

                st.error(
                    f"❌ {error}"
                )


        else:

            try:

                file_path = save_uploaded_file(
                    uploaded_file,
                    doc_type
                )


                conn = get_connection()


                conn.execute(
                    """
                    INSERT INTO documents (

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
                        doc_number.strip(),
                        doc_date.strftime(
                            "%d/%m/%Y"
                        ),
                        party.strip(),
                        subject.strip(),
                        file_path
                    )
                )


                conn.commit()

                conn.close()


                st.success(
                    f"✅ تم حفظ مستند {doc_type} بنجاح."
                )


                st.session_state.page = "الرئيسية"

                st.rerun()


            except Exception as e:

                st.error(
                    f"❌ حدث خطأ أثناء الحفظ: {e}"
                )


# ============================================================
# السجلات
# ============================================================

elif st.session_state.page == "السجلات":

    st.markdown(
        """
        <div class="page-title">
            📋 سجلات الوارد والصادر
        </div>
        """,
        unsafe_allow_html=True
    )


    filter_options = [
        "الكل",
        "وارد",
        "صادر"
    ]


    default_filter = st.session_state.get(
        "view_filter",
        "الكل"
    )


    if default_filter not in filter_options:

        default_filter = "الكل"


    selected_filter = st.selectbox(
        "نوع السجل",
        filter_options,
        index=filter_options.index(
            default_filter
        ),
        key="records_filter"
    )


    rows = get_documents(
        doc_type=selected_filter
    )


    st.markdown(
        f"""
        <div class="info-card">

            <div style="
                color:#17365d;
                font-size:16px;
                font-weight:900;
                text-align:right;
            ">
                📊 عدد السجلات: {len(rows)}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    if not rows:

        st.info(
            "📭 لا توجد سجلات متاحة."
        )


    else:

        for row in rows:

            icon = (
                "📥"
                if row["doc_type"] == "وارد"
                else "📤"
            )


            # ------------------------------------------------
            # عنوان مختصر قبل البطاقة
            # ------------------------------------------------

            st.markdown(
                f"""
                <div style="
                    color:#6b7280;
                    font-size:12px;
                    font-weight:700;
                    margin:5px 0 3px 0;
                    text-align:right;
                ">
                    سجل رقم {row["id"]}
                </div>
                """,
                unsafe_allow_html=True
            )


            # ------------------------------------------------
            # البطاقة الجديدة
            # ------------------------------------------------

            display_document_card(
                row,
                show_actions=True,
                prefix="records"
            )


    if st.button(
        "🏠 العودة للرئيسية",
        key="records_home",
        use_container_width=True
    ):

        go_to("الرئيسية")


# ============================================================
# البحث
# ============================================================

elif st.session_state.page == "البحث":

    st.markdown(
        """
        <div class="page-title">
            🔎 البحث في الأرشيف
        </div>
        """,
        unsafe_allow_html=True
    )


    search_text = st.text_input(
        "كلمة البحث",
        value=st.session_state.search_query,
        placeholder="رقم المستند / الجهة / الموضوع / التاريخ",
        key="search_page_input"
    )


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "🔎 بحث",
            type="primary",
            key="search_page_button",
            use_container_width=True
        ):

            st.session_state.search_query = (
                search_text.strip()
            )

            st.rerun()


    with col2:

        if st.button(
            "🏠 الرئيسية",
            key="search_home_button",
            use_container_width=True
        ):

            go_to("الرئيسية")


    if st.session_state.search_query:

        rows = get_documents(
            search_text=
            st.session_state.search_query
        )


        st.markdown(
            f"""
            <div class="section-title">
                📊 نتائج البحث: {len(rows)}
            </div>
            """,
            unsafe_allow_html=True
        )


        if not rows:

            st.warning(
                "⚠️ لم يتم العثور على نتائج مطابقة."
            )


        else:

            for row in rows:

                display_document_card(
                    row,
                    show_actions=True,
                    prefix="search"
                )


# ============================================================
# تعديل المستند
# ============================================================

elif st.session_state.page == "تعديل":

    document_id = st.session_state.get(
        "edit_id"
    )


    if not document_id:

        st.error(
            "❌ لم يتم تحديد المستند."
        )

        if st.button(
            "🏠 الرئيسية",
            use_container_width=True
        ):

            go_to("الرئيسية")


    else:

        row = get_document(
            document_id
        )


        if not row:

            st.error(
                "❌ المستند غير موجود."
            )

            if st.button(
                "🏠 الرئيسية",
                use_container_width=True
            ):

                go_to("الرئيسية")


        else:

            icon = (
                "📥"
                if row["doc_type"] == "وارد"
                else "📤"
            )


            st.markdown(
                f"""
                <div class="page-title">
                    {icon} تعديل مستند {row["doc_type"]}
                </div>
                """,
                unsafe_allow_html=True
            )


            with st.form(
                f"edit_form_{document_id}"
            ):

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
                    "الجهة / الطرف *",
                    value=row["party"]
                )


                subject = st.text_area(
                    "موضوع المستند *",
                    value=row["subject"],
                    height=110
                )


                if row["file_path"]:

                    old_file = Path(
                        row["file_path"]
                    )


                    if old_file.exists():

                        st.success(
                            f"📎 الملف الحالي: {old_file.name}"
                        )

                    else:

                        st.warning(
                            "⚠️ الملف الحالي غير موجود."
                        )

                else:

                    st.info(
                        "📄 لا يوجد ملف PDF حالي."
                    )


                new_file = st.file_uploader(
                    "استبدال ملف PDF",
                    type=["pdf"],
                    key=f"new_pdf_{document_id}"
                )


                col1, col2 = st.columns(2)


                with col1:

                    save_edit = st.form_submit_button(
                        "💾 حفظ التعديلات",
                        type="primary",
                        use_container_width=True
                    )


                with col2:

                    cancel_edit = st.form_submit_button(
                        "↩️ إلغاء",
                        use_container_width=True
                    )


            if cancel_edit:

                go_to("السجلات")


            if save_edit:

                errors = []


                if not doc_number.strip():

                    errors.append(
                        "رقم المستند مطلوب."
                    )


                if not party.strip():

                    errors.append(
                        "الجهة / الطرف مطلوبة."
                    )


                if not subject.strip():

                    errors.append(
                        "موضوع المستند مطلوب."
                    )


                if errors:

                    for error in errors:

                        st.error(
                            f"❌ {error}"
                        )


                else:

                    try:

                        new_file_path = None

                        old_file_path = (
                            row["file_path"]
                        )


                        if new_file:

                            new_file_path = (
                                save_uploaded_file(
                                    new_file,
                                    row["doc_type"]
                                )
                            )


                        update_document(
                            document_id=document_id,
                            doc_number=doc_number.strip(),
                            doc_date=doc_date.strftime(
                                "%d/%m/%Y"
                            ),
                            party=party.strip(),
                            subject=subject.strip(),
                            new_file_path=new_file_path
                        )


                        if (
                            new_file_path
                            and old_file_path
                        ):

                            delete_old_file(
                                old_file_path
                            )


                        st.success(
                            "✅ تم تحديث المستند بنجاح."
                        )


                        st.session_state.page = (
                            "السجلات"
                        )


                        st.rerun()


                    except Exception as e:

                        st.error(
                            f"❌ حدث خطأ أثناء التعديل: {e}"
                        )


# ============================================================
# تأكيد الحذف
# ============================================================

elif st.session_state.page == "تأكيد الحذف":

    document_id = st.session_state.get(
        "delete_id"
    )


    row = (
        get_document(document_id)
        if document_id
        else None
    )


    st.markdown(
        """
        <div class="page-title">
            🗑️ حذف المستند
        </div>
        """,
        unsafe_allow_html=True
    )


    if not row:

        st.error(
            "❌ المستند غير موجود."
        )


        if st.button(
            "🏠 العودة للسجلات",
            use_container_width=True
        ):

            go_to("السجلات")


    else:

        # عرض البيانات كاملة قبل الحذف
        display_document_card(
            row,
            show_actions=False,
            prefix="delete_preview"
        )


        st.warning(
            "⚠️ هل أنت متأكد من حذف هذا المستند؟ "
            "سيتم حذف السجل وملف PDF المرتبط به إن وجد."
        )


        col1, col2 = st.columns(2)


        with col1:

            if st.button(
                "🗑️ نعم، حذف المستند",
                type="primary",
                key="confirm_delete",
                use_container_width=True
            ):

                try:

                    delete_document(
                        document_id
                    )


                    st.success(
                        "✅ تم حذف المستند بنجاح."
                    )


                    st.session_state.page = (
                        "السجلات"
                    )


                    st.rerun()


                except Exception as e:

                    st.error(
                        f"❌ حدث خطأ أثناء الحذف: {e}"
                    )


        with col2:

            if st.button(
                "↩️ إلغاء",
                key="cancel_delete",
                use_container_width=True
            ):

                go_to("السجلات")


# ============================================================
# الفوتر
# ============================================================

st.markdown(
    """
    <div class="custom-footer">

        <b>
            الأكاديمية المهنية للمعلمين - فرع الجيزة
        </b>

        <br>

        ✦ تصميم وتنفيذ أحمد الجنزوري ✦

    </div>
    """,
    unsafe_allow_html=True
)
