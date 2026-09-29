import streamlit as st
import sqlite3
from pathlib import Path
from datetime import date, datetime
from html import escape


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

LOGO_PATH = BASE_DIR / "logo.png"

INCOMING_DIR.mkdir(parents=True, exist_ok=True)
OUTGOING_DIR.mkdir(parents=True, exist_ok=True)


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

    /* ========================================================
       الإعداد العام
       ======================================================== */

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
        max-width: 900px !important;
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


    /* ========================================================
       شاشة الدخول
       ======================================================== */

    .login-logo-space {
        width: 100%;
        text-align: center;
        margin: 0 auto 8px auto;
    }

    .login-main-title {
        width: 100%;
        text-align: center !important;
        color: #17365d;
        font-size: 30px;
        font-weight: 900;
        line-height: 1.5;
        margin: 0 auto 3px auto;
    }

    .login-sub-title {
        width: 100%;
        text-align: center !important;
        color: #294d7c;
        font-size: 20px;
        font-weight: 700;
        line-height: 1.5;
        margin: 0 auto 18px auto;
    }


    /* ========================================================
       رأس البرنامج
       ======================================================== */

    .main-title {
        width: 100%;
        text-align: center !important;
        color: #17365d;
        font-size: 27px;
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
        margin: 0 auto 18px auto;
    }


    /* ========================================================
       عناوين الأقسام
       ======================================================== */

    .section-title {
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

        font-size: 20px;
        font-weight: 800;

        text-align: right;
    }


    /* ========================================================
       بطاقة بيانات المستند
       ======================================================== */

    .document-card {
        width: 100%;
        box-sizing: border-box;

        background: #ffffff;

        border: 1px solid #d9e1ea;

        border-radius: 13px;

        margin: 0 0 10px 0;

        overflow: hidden;

        box-shadow:
            0 2px 8px rgba(0, 0, 0, 0.06);

        direction: rtl;
        text-align: right;
    }


    /* رأس البطاقة */

    .document-card-header {
        display: flex;

        justify-content: space-between;
        align-items: center;

        gap: 10px;

        background: #f3f7fb;

        border-bottom: 1px solid #dce4ed;

        padding: 12px 15px;
    }

    .document-card-title {
        color: #17365d;

        font-size: 18px;

        font-weight: 900;

        line-height: 1.5;
    }

    .document-type-badge {
        background: #17365d;

        color: white;

        border-radius: 20px;

        padding: 4px 13px;

        font-size: 13px;

        font-weight: 800;

        white-space: nowrap;
    }


    /* جسم البطاقة */

    .document-card-body {
        padding: 13px;
    }


    /* شبكة البيانات */

    .document-grid {
        width: 100%;

        display: grid;

        grid-template-columns:
            minmax(0, 1fr)
            minmax(0, 1fr);

        gap: 9px;

        direction: rtl;
    }


    /* خانة البيانات */

    .document-field {
        background: #f8fafc;

        border: 1px solid #e5eaf0;

        border-radius: 9px;

        padding: 9px 11px;

        min-width: 0;

        box-sizing: border-box;

        direction: rtl;

        text-align: right;
    }

    .document-field-label {
        color: #687586;

        font-size: 12px;

        font-weight: 700;

        margin-bottom: 3px;

        line-height: 1.5;
    }

    .document-field-value {
        color: #17365d;

        font-size: 15px;

        font-weight: 800;

        line-height: 1.7;

        word-break: break-word;

        overflow-wrap: anywhere;
    }


    /* موضوع المستند */

    .document-subject {
        grid-column: 1 / -1;

        background: #f8fafc;

        border: 1px solid #e5eaf0;

        border-radius: 9px;

        padding: 10px 11px;

        box-sizing: border-box;

        direction: rtl;

        text-align: right;
    }

    .document-subject-value {
        color: #17365d;

        font-size: 15px;

        font-weight: 700;

        line-height: 1.9;

        word-break: break-word;

        overflow-wrap: anywhere;

        white-space: normal;
    }


    /* ملف PDF */

    .document-file {
        margin-top: 10px;

        background: #fff8e8;

        border: 1px solid #f0dfad;

        border-radius: 9px;

        padding: 9px 11px;

        color: #765d16;

        font-size: 14px;

        font-weight: 700;

        line-height: 1.7;

        direction: rtl;

        text-align: right;

        word-break: break-word;

        overflow-wrap: anywhere;
    }

    .document-no-file {
        margin-top: 10px;

        background: #f5f6f8;

        border: 1px solid #e2e5e9;

        border-radius: 9px;

        padding: 9px 11px;

        color: #68707a;

        font-size: 14px;

        font-weight: 700;

        direction: rtl;

        text-align: right;
    }


    /* ========================================================
       Expander
       ======================================================== */

    div[data-testid="stExpander"] {
        border-radius: 10px !important;

        border: 1px solid #dce3eb !important;

        background: white !important;

        margin-bottom: 12px !important;

        direction: rtl !important;

        text-align: right !important;
    }

    div[data-testid="stExpander"] > details {
        direction: rtl !important;
        text-align: right !important;
    }

    div[data-testid="stExpander"] summary {
        direction: rtl !important;
        text-align: right !important;
    }

    div[data-testid="stExpander"] summary p {
        direction: rtl !important;
        text-align: right !important;

        font-weight: 800 !important;

        color: #17365d !important;
    }


    /* ========================================================
       الحقول
       ======================================================== */

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {
        direction: rtl !important;
        text-align: right !important;
    }

    div[data-testid="stDateInput"] input {
        direction: rtl !important;
        text-align: right !important;
    }

    div[data-baseweb="select"] {
        direction: rtl !important;
    }

    section[data-testid="stFileUploader"] {
        direction: rtl;
        text-align: right;
    }


    /* ========================================================
       الأزرار
       ======================================================== */

    .stButton > button {
        width: 100%;

        border-radius: 8px;

        min-height: 42px;

        font-weight: 700;
    }

    div[data-testid="stDownloadButton"] button {
        width: 100% !important;

        border-radius: 8px !important;

        min-height: 42px !important;

        font-weight: 700 !important;
    }


    /* ========================================================
       التنبيهات
       ======================================================== */

    div[data-testid="stAlert"] {
        direction: rtl;
        text-align: right;
    }


    /* ========================================================
       الفوتر
       ======================================================== */

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


    /* ========================================================
       الموبايل
       ======================================================== */

    @media (max-width: 600px) {

        .block-container {
            width: 94% !important;
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

        .document-grid {
            grid-template-columns: 1fr;
        }

        .document-subject {
            grid-column: auto;
        }

        .document-card-header {
            padding: 10px;
        }

        .document-card-title {
            font-size: 16px;
        }

        .document-type-badge {
            font-size: 11px;
            padding: 3px 9px;
        }

        .document-card-body {
            padding: 10px;
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

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

if "delete_id" not in st.session_state:
    st.session_state.delete_id = None


# ============================================================
# دالة عرض الشعار
# ============================================================

def show_logo(width=150):

    if LOGO_PATH.exists():

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:

            st.image(
                str(LOGO_PATH),
                width=width
            )

    else:

        st.markdown(
            """
            <div style="
                width:100%;
                text-align:center;
                font-size:70px;
                margin:5px auto 10px auto;
            ">
                📁
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# شاشة تسجيل الدخول
# ============================================================

if not st.session_state.authenticated:

    show_logo(180)

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

    # ========================================================
    # نموذج تسجيل الدخول
    # الضغط على Enter يعمل هنا مباشرة
    # ========================================================

    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:

        with st.form(
            key="login_form",
            clear_on_submit=False,
            enter_to_submit=True
        ):

            password = st.text_input(
                "🔐 كلمة المرور",
                type="password",
                placeholder="أدخل كلمة المرور ثم اضغط Enter",
                key="login_password"
            )

            login_clicked = st.form_submit_button(
                "🔓 تسجيل الدخول",
                type="primary"
            )


    if login_clicked:

        if password == APP_PASSWORD:

            st.session_state.authenticated = True

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
            ✦ تصميم وتنفيذ أحمد الجنزوري - مدير الفرع ✦
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# قاعدة البيانات
# ============================================================

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


# ============================================================
# الترقيم التلقائي
# ============================================================

def get_next_document_number(doc_type):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT MAX(CAST(doc_number AS INTEGER))
        FROM documents
        WHERE doc_type = ?
        """,
        (doc_type,)
    ).fetchone()

    conn.close()

    max_number = row[0]

    if doc_type == "وارد":
        start_number = 961
    else:
        start_number = 1160

    if max_number is None or max_number < start_number:
        return str(start_number)

    return str(max_number + 1)


# ============================================================
# وظائف الملفات
# ============================================================

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

    original_name = Path(
        uploaded_file.name
    ).name

    safe_name = f"{timestamp}_{original_name}"

    file_path = folder / safe_name

    with open(file_path, "wb") as file:

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

    if doc_type and doc_type != "الكل":

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

        search_value = f"%{search_text}%"

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

        file_path = row["file_path"]

        if file_path:

            delete_old_file(
                file_path
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
# الانتقال بين الصفحات
# ============================================================

def go_to(page):

    st.session_state.page = page

    st.rerun()


# ============================================================
# عرض بطاقة المستند
# ============================================================

def render_document_card(row):

    doc_type = str(
        row["doc_type"] or ""
    )

    doc_number = str(
        row["doc_number"] or ""
    )

    doc_date = str(
        row["doc_date"] or ""
    )

    party = str(
        row["party"] or ""
    )

    subject = str(
        row["subject"] or ""
    )

    icon = (
        "📥"
        if doc_type == "وارد"
        else "📤"
    )

    # حماية النصوص القادمة من قاعدة البيانات
    doc_type_html = escape(doc_type)
    doc_number_html = escape(doc_number)
    doc_date_html = escape(doc_date)
    party_html = escape(party)
    subject_html = escape(subject)

    if row["file_path"]:

        file_name = Path(
            row["file_path"]
        ).name

        file_name_html = escape(
            file_name
        )

        file_html = f"""
            <div class="document-file">
                📎 يوجد ملف PDF مرفق:
                <b>{file_name_html}</b>
            </div>
        """

    else:

        file_html = """
            <div class="document-no-file">
                📄 لا يوجد ملف PDF مرفق
            </div>
        """


    st.markdown(
        f"""
        <div class="document-card">

            <!-- رأس البطاقة -->

            <div class="document-card-header">

                <div class="document-card-title">
                    {icon} بيانات المستند
                </div>

                <div class="document-type-badge">
                    {doc_type_html}
                </div>

            </div>


            <!-- جسم البطاقة -->

            <div class="document-card-body">

                <div class="document-grid">

                    <!-- رقم المستند -->

                    <div class="document-field">

                        <div class="document-field-label">
                            رقم المستند
                        </div>

                        <div class="document-field-value">
                            {doc_number_html}
                        </div>

                    </div>


                    <!-- التاريخ -->

                    <div class="document-field">

                        <div class="document-field-label">
                            تاريخ المستند
                        </div>

                        <div class="document-field-value">
                            {doc_date_html}
                        </div>

                    </div>


                    <!-- الجهة -->

                    <div class="document-field">

                        <div class="document-field-label">
                            الجهة / الطرف
                        </div>

                        <div class="document-field-value">
                            {party_html}
                        </div>

                    </div>


                    <!-- نوع المعاملة -->

                    <div class="document-field">

                        <div class="document-field-label">
                            نوع المعاملة
                        </div>

                        <div class="document-field-value">
                            {doc_type_html}
                        </div>

                    </div>


                    <!-- الموضوع -->

                    <div class="document-subject">

                        <div class="document-field-label">
                            موضوع المستند
                        </div>

                        <div class="document-subject-value">
                            {subject_html}
                        </div>

                    </div>

                </div>


                <!-- ملف PDF -->

                {file_html}

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# تحميل PDF
# ============================================================

def render_pdf_download(
    row,
    key_prefix
):

    if not row["file_path"]:

        return


    file_path = Path(
        row["file_path"]
    )


    if not file_path.exists():

        st.warning(
            "⚠️ الملف المرفق غير موجود في الأرشيف."
        )

        return


    try:

        with open(
            file_path,
            "rb"
        ) as pdf_file:

            pdf_data = pdf_file.read()


        st.download_button(
            "📥 تحميل PDF",
            data=pdf_data,
            file_name=file_path.name,
            mime="application/pdf",
            key=f"{key_prefix}_pdf_{row['id']}",
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"❌ تعذر قراءة ملف PDF: {e}"
        )


# ============================================================
# رأس البرنامج الداخلي
# ============================================================

show_logo(145)

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
# الصفحة الرئيسية
# ============================================================

if st.session_state.page == "الرئيسية":

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
            key="add_incoming_home"
        ):

            go_to("إضافة وارد")


    with col2:

        if st.button(
            "📋 عرض الوارد",
            key="view_incoming_home"
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
            key="add_outgoing_home"
        ):

            go_to("إضافة صادر")


    with col2:

        if st.button(
            "📋 عرض الصادر",
            key="view_outgoing_home"
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
        "ابحث برقم المستند أو الجهة أو الموضوع أو التاريخ",
        value="",
        placeholder="اكتب كلمة البحث هنا..."
    )


    if st.button(
        "🔎 تنفيذ البحث",
        type="primary",
        key="search_home"
    ):

        st.session_state.search_query = search_text

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

    title_icon = (
        "📥"
        if doc_type == "وارد"
        else "📤"
    )


    st.markdown(
        f"""
        <div class="section-title">
            {title_icon} إضافة مستند {doc_type} جديد
        </div>
        """,
        unsafe_allow_html=True
    )


    with st.form(
        key=f"add_form_{doc_type}"
    ):

        doc_number = get_next_document_number(
            doc_type
        )

        st.text_input(
            "رقم المستند",
            value=doc_number,
            disabled=True
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
            height=100
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
                type="primary"
            )


        with col2:

            cancel_clicked = st.form_submit_button(
                "↩️ إلغاء"
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
                "الجهة / الطرف مطلوب."
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
                    f"✅ تم حفظ المستند {doc_type} بنجاح."
                )


                st.session_state.page = "الرئيسية"

                st.rerun()


            except Exception as e:

                st.error(
                    f"❌ حدث خطأ أثناء الحفظ: {e}"
                )


# ============================================================
# عرض السجلات
# ============================================================

elif st.session_state.page == "السجلات":

    st.markdown(
        """
        <div class="section-title">
            📋 سجلات الوارد والصادر
        </div>
        """,
        unsafe_allow_html=True
    )


    default_filter = st.session_state.get(
        "view_filter",
        "الكل"
    )


    filter_options = [
        "الكل",
        "وارد",
        "صادر"
    ]


    if default_filter not in filter_options:

        default_filter = "الكل"


    selected_filter = st.selectbox(
        "نوع السجل",
        filter_options,
        index=filter_options.index(
            default_filter
        )
    )


    # حفظ الاختيار الحالي
    st.session_state.view_filter = selected_filter


    rows = get_documents(
        doc_type=selected_filter
    )


    st.write(
        f"📊 عدد السجلات: **{len(rows)}**"
    )


    if not rows:

        st.info(
            "لا توجد سجلات متاحة."
        )


    else:

        for row in rows:

            icon = (
                "📥"
                if row["doc_type"] == "وارد"
                else "📤"
            )


            # ------------------------------------------------
            # عنوان مختصر للـ Expander
            # لا يتم وضع الموضوع هنا
            # ------------------------------------------------

            expander_title = (
                f"{icon} "
                f"{row['doc_type']} "
                f"— رقم {row['doc_number']} "
                f"— {row['doc_date']}"
            )


            with st.expander(
                expander_title,
                expanded=False
            ):

                # ============================================
                # بطاقة البيانات الجديدة
                # ============================================

                render_document_card(
                    row
                )


                # ============================================
                # تحميل PDF
                # ============================================

                if row["file_path"]:

                    render_pdf_download(
                        row,
                        "records"
                    )


                # ============================================
                # أزرار التعديل والحذف
                # ============================================

                col1, col2 = st.columns(2)


                with col1:

                    if st.button(
                        "✏️ تعديل المستند",
                        key=f"edit_{row['id']}"
                    ):

                        st.session_state.edit_id = row["id"]

                        go_to("تعديل")


                with col2:

                    if st.button(
                        "🗑️ حذف المستند",
                        key=f"delete_{row['id']}"
                    ):

                        st.session_state.delete_id = row["id"]

                        go_to("تأكيد الحذف")


    st.markdown("<br>", unsafe_allow_html=True)


    if st.button(
        "🏠 العودة للرئيسية",
        key="back_from_records"
    ):

        go_to("الرئيسية")


# ============================================================
# البحث
# ============================================================

elif st.session_state.page == "البحث":

    st.markdown(
        """
        <div class="section-title">
            🔎 البحث في الأرشيف
        </div>
        """,
        unsafe_allow_html=True
    )


    search_text = st.text_input(
        "كلمة البحث",
        value=st.session_state.search_query,
        placeholder="رقم المستند / الجهة / الموضوع / التاريخ"
    )


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "🔎 بحث",
            type="primary",
            key="search_again"
        ):

            st.session_state.search_query = search_text

            st.rerun()


    with col2:

        if st.button(
            "🏠 الرئيسية",
            key="back_search"
        ):

            go_to("الرئيسية")


    if st.session_state.search_query:

        rows = get_documents(
            search_text=st.session_state.search_query
        )


        st.markdown(
            """
            <div class="section-title">
                📊 نتائج البحث
            </div>
            """,
            unsafe_allow_html=True
        )


        st.write(
            f"عدد النتائج: **{len(rows)}**"
        )


        if not rows:

            st.warning(
                "لم يتم العثور على نتائج مطابقة."
            )


        else:

            for row in rows:

                icon = (
                    "📥"
                    if row["doc_type"] == "وارد"
                    else "📤"
                )


                title = (
                    f"{icon} "
                    f"{row['doc_type']} "
                    f"— رقم {row['doc_number']} "
                    f"— {row['doc_date']}"
                )


                with st.expander(
                    title,
                    expanded=False
                ):

                    render_document_card(
                        row
                    )


                    if row["file_path"]:

                        render_pdf_download(
                            row,
                            "search"
                        )


                    col1, col2 = st.columns(2)


                    with col1:

                        if st.button(
                            "✏️ تعديل المستند",
                            key=f"search_edit_{row['id']}"
                        ):

                            st.session_state.edit_id = row["id"]

                            go_to("تعديل")


                    with col2:

                        if st.button(
                            "🗑️ حذف المستند",
                            key=f"search_delete_{row['id']}"
                        ):

                            st.session_state.delete_id = row["id"]

                            go_to("تأكيد الحذف")


# ============================================================
# تعديل مستند
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
            "🏠 الرئيسية"
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
                "🏠 الرئيسية"
            ):

                go_to("الرئيسية")


        else:

            st.markdown(
                f"""
                <div class="section-title">
                    ✏️ تعديل مستند {escape(str(row["doc_type"]))}
                </div>
                """,
                unsafe_allow_html=True
            )


            with st.form(
                key=f"edit_form_{document_id}"
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
                    height=100
                )


                st.write(
                    "📎 الملف الحالي:"
                )


                if row["file_path"]:

                    old_file = Path(
                        row["file_path"]
                    )


                    if old_file.exists():

                        st.info(
                            old_file.name
                        )

                    else:

                        st.warning(
                            "الملف الحالي غير موجود."
                        )


                else:

                    st.info(
                        "لا يوجد ملف مرفق حاليًا."
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
                        type="primary"
                    )


                with col2:

                    cancel_edit = st.form_submit_button(
                        "↩️ إلغاء"
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

                        old_file_path = row["file_path"]


                        if new_file:

                            new_file_path = save_uploaded_file(
                                new_file,
                                row["doc_type"]
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


                        st.session_state.page = "السجلات"

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
        <div class="section-title">
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
            "🏠 الرئيسية"
        ):

            go_to("الرئيسية")


    else:

        st.warning(
            f"""
            ⚠️ هل أنت متأكد من حذف المستند؟

            **النوع:** {row["doc_type"]}

            **رقم المستند:** {row["doc_number"]}

            **التاريخ:** {row["doc_date"]}

            **الجهة:** {row["party"]}

            **الموضوع:** {row["subject"]}

            سيتم حذف السجل والملف المرفق إن وجد.
            """
        )


        col1, col2 = st.columns(2)


        with col1:

            if st.button(
                "🗑️ نعم، حذف المستند",
                type="primary"
            ):

                try:

                    delete_document(
                        document_id
                    )


                    st.success(
                        "✅ تم حذف المستند بنجاح."
                    )


                    st.session_state.page = "السجلات"

                    st.rerun()


                except Exception as e:

                    st.error(
                        f"❌ حدث خطأ أثناء الحذف: {e}"
                    )


        with col2:

            if st.button(
                "↩️ إلغاء"
            ):

                go_to("السجلات")


# ============================================================
# الفوتر
# ============================================================

st.markdown(
    """
    <div class="custom-footer">

        الأكاديمية المهنية للمعلمين - فرع الجيزة

        <br>

        ✦ تصميم وتنفيذ أحمد الجنزوري - مدير الفرع ✦

    </div>
    """,
    unsafe_allow_html=True
)
