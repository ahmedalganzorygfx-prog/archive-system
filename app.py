import streamlit as st
import sqlite3
import base64
from pathlib import Path
from datetime import date, datetime


# =========================================================
# إعداد الصفحة
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

LOGO_PATH = BASE_DIR / "logo.png"

INCOMING_DIR.mkdir(parents=True, exist_ok=True)
OUTGOING_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# كلمة المرور
# =========================================================

APP_PASSWORD = "1234"


# =========================================================
# تحويل الصورة إلى Base64
# =========================================================

def get_image_base64(image_path):
    if not image_path.exists():
        return None

    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       RTL
       ===================================================== */

    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
    }

    .stApp {
        direction: rtl;
    }

    /* =====================================================
       إخفاء Header و Footer
       ===================================================== */

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* =====================================================
       المحتوى الرئيسي
       ===================================================== */

    .block-container {
        max-width: 900px !important;
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
    }

    /* =====================================================
       شعار تسجيل الدخول
       ===================================================== */

    .login-logo-container {
        text-align: center;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    .login-logo-container img {
        width: 180px;
        height: 180px;
        object-fit: contain;
    }

    /* =====================================================
       الشعار الداخلي
       ===================================================== */

    .internal-logo-container {
        text-align: center;
        margin-top: 5px;
        margin-bottom: 8px;
    }

    .internal-logo-container img {
        width: 145px;
        height: 145px;
        object-fit: contain;
    }

    /* =====================================================
       العناوين
       ===================================================== */

    .main-title {
        text-align: center;
        font-size: 26px;
        font-weight: 800;
        margin-top: 5px;
        margin-bottom: 5px;
    }

    .main-subtitle {
        text-align: center;
        font-size: 21px;
        font-weight: 700;
        margin-bottom: 20px;
    }

    /* =====================================================
       عنوان القسم
       ===================================================== */

    .section-title {
        font-size: 22px;
        font-weight: 800;
        text-align: center;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    /* =====================================================
       البطاقات
       ===================================================== */

    .info-card {
        padding: 18px;
        border-radius: 16px;
        margin-bottom: 18px;
        border: 1px solid #e0e0e0;
        background: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }

    /* =====================================================
       عنوان السجل
       ===================================================== */

    .record-title {
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 15px;
        text-align: right;
    }

    /* =====================================================
       بيانات السجل
       ===================================================== */

    .record-line {
        font-size: 17px;
        line-height: 2;
        margin-bottom: 4px;
        text-align: right;
    }

    /* =====================================================
       الفوتر
       ===================================================== */

    .custom-footer {
        text-align: center;
        margin-top: 35px;
        padding-top: 15px;
        border-top: 1px solid #e5e5e5;
        color: #666;
        font-size: 14px;
    }

    /* =====================================================
       النماذج
       ===================================================== */

    div[data-testid="stForm"] {
        direction: rtl;
        text-align: right;
    }

    /* =====================================================
       الأزرار
       ===================================================== */

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 700;
    }

    /* =====================================================
       رفع الملفات
       ===================================================== */

    section[data-testid="stFileUploader"] {
        direction: rtl;
        text-align: right;
    }

    /* =====================================================
       Expander
       ===================================================== */

    div[data-testid="stExpander"] {
        direction: rtl;
        text-align: right;
    }

    /* =====================================================
       الرسائل
       ===================================================== */

    .stAlert {
        direction: rtl;
        text-align: right;
    }

    /* =====================================================
       Selectbox
       ===================================================== */

    div[data-baseweb="select"] {
        direction: rtl;
        text-align: right;
    }

    /* =====================================================
       الموبايل
       ===================================================== */

    @media (max-width: 768px) {

        .login-logo-container img {
            width: 140px;
            height: 140px;
        }

        .internal-logo-container img {
            width: 115px;
            height: 115px;
        }

        .main-title {
            font-size: 21px;
        }

        .main-subtitle {
            font-size: 18px;
        }

        .record-line {
            font-size: 15px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# Session State
# =========================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "page" not in st.session_state:
    st.session_state.page = "الرئيسية"

if "search_query" not in st.session_state:
    st.session_state.search_query = ""


# =========================================================
# شاشة تسجيل الدخول
# =========================================================

if not st.session_state.authenticated:

    logo_base64 = get_image_base64(LOGO_PATH)

    if logo_base64:
        st.markdown(
            f"""
            <div class="login-logo-container">
                <img src="data:image/png;base64,{logo_base64}">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="
                text-align:center;
                font-size:80px;
                margin-bottom:10px;
            ">
                📁
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="main-title">
            الأكاديمية المهنية للمعلمين – فرع الجيزة
        </div>

        <div class="main-subtitle">
            المنظومة الرقمية للوارد والصادر
        </div>
        """,
        unsafe_allow_html=True
    )

    password = st.text_input(
        "🔐 كلمة المرور",
        type="password"
    )

    if st.button("دخول", use_container_width=True):

        if password == APP_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()

        else:
            st.error("❌ كلمة المرور غير صحيحة")

    st.markdown(
        """
        <div class="custom-footer">
            ✦ تصميم وتنفيذ أحمد الجنزوري ✦
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# =========================================================
# قاعدة البيانات
# =========================================================

def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_type TEXT NOT NULL,
            doc_number TEXT NOT NULL,
            doc_date TEXT NOT NULL,
            party TEXT NOT NULL,
            subject TEXT NOT NULL,
            file_path TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


init_db()


# =========================================================
# تحديد مجلد الأرشيف
# =========================================================

def get_archive_folder(doc_type):

    if doc_type == "وارد":
        return INCOMING_DIR

    return OUTGOING_DIR


# =========================================================
# حفظ الملف
# =========================================================

def save_uploaded_file(uploaded_file, doc_type):

    if uploaded_file is None:
        return None

    folder = get_archive_folder(doc_type)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    safe_name = uploaded_file.name.replace("/", "_").replace("\\", "_")

    file_name = f"{timestamp}_{safe_name}"

    file_path = folder / file_name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return str(file_path)


# =========================================================
# جلب المستندات
# =========================================================

def get_documents(doc_type=None):

    conn = get_connection()

    cursor = conn.cursor()

    if doc_type:

        cursor.execute(
            """
            SELECT
                id,
                doc_type,
                doc_number,
                doc_date,
                party,
                subject,
                file_path,
                created_at
            FROM documents
            WHERE doc_type = ?
            ORDER BY id DESC
            """,
            (doc_type,)
        )

    else:

        cursor.execute(
            """
            SELECT
                id,
                doc_type,
                doc_number,
                doc_date,
                party,
                subject,
                file_path,
                created_at
            FROM documents
            ORDER BY id DESC
            """
        )

    rows = cursor.fetchall()

    conn.close()

    columns = [
        "id",
        "doc_type",
        "doc_number",
        "doc_date",
        "party",
        "subject",
        "file_path",
        "created_at"
    ]

    return [
        dict(zip(columns, row))
        for row in rows
    ]


# =========================================================
# مستند واحد
# =========================================================

def get_document(document_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            doc_type,
            doc_number,
            doc_date,
            party,
            subject,
            file_path,
            created_at
        FROM documents
        WHERE id = ?
        """,
        (document_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if not row:
        return None

    columns = [
        "id",
        "doc_type",
        "doc_number",
        "doc_date",
        "party",
        "subject",
        "file_path",
        "created_at"
    ]

    return dict(zip(columns, row))


# =========================================================
# حذف المستند
# =========================================================

def delete_document(document_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM documents WHERE id = ?",
        (document_id,)
    )

    conn.commit()

    conn.close()


# =========================================================
# تعديل المستند
# =========================================================

def update_document(
    document_id,
    doc_type,
    doc_number,
    doc_date,
    party,
    subject,
    file_path
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE documents
        SET
            doc_type = ?,
            doc_number = ?,
            doc_date = ?,
            party = ?,
            subject = ?,
            file_path = ?
        WHERE id = ?
        """,
        (
            doc_type,
            doc_number,
            doc_date,
            party,
            subject,
            file_path,
            document_id
        )
    )

    conn.commit()

    conn.close()


# =========================================================
# حذف الملف القديم
# =========================================================

def delete_old_file(file_path):

    if file_path:

        path = Path(file_path)

        if path.exists():

            try:
                path.unlink()
            except:
                pass


# =========================================================
# الانتقال بين الصفحات
# =========================================================

def go_to(page):

    st.session_state.page = page
    st.rerun()


# =========================================================
# الهيدر الداخلي
# =========================================================

logo_base64 = get_image_base64(LOGO_PATH)

if logo_base64:

    st.markdown(
        f"""
        <div class="internal-logo-container">
            <img src="data:image/png;base64,{logo_base64}">
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.warning("لم يتم العثور على ملف الشعار logo.png")


st.markdown(
    """
    <div class="main-title">
        الأكاديمية المهنية للمعلمين – فرع الجيزة
    </div>

    <div class="main-subtitle">
        المنظومة الرقمية للوارد والصادر
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# الصفحة الرئيسية
# =========================================================

if st.session_state.page == "الرئيسية":

    st.markdown(
        """
        <div class="section-title">
            🏠 الرئيسية
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # الوارد
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="info-card">

            <div class="record-title">
                📥 الوارد
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "➕ إضافة وارد",
            key="add_incoming",
            use_container_width=True
        ):
            go_to("إضافة وارد")

    with col2:

        if st.button(
            "📋 عرض الوارد",
            key="view_incoming",
            use_container_width=True
        ):
            go_to("سجلات الوارد")


    # -----------------------------------------------------
    # الصادر
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="info-card">

            <div class="record-title">
                📤 الصادر
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "➕ إضافة صادر",
            key="add_outgoing",
            use_container_width=True
        ):
            go_to("إضافة صادر")

    with col2:

        if st.button(
            "📋 عرض الصادر",
            key="view_outgoing",
            use_container_width=True
        ):
            go_to("سجلات الصادر")


    # -----------------------------------------------------
    # البحث
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="info-card">

            <div class="record-title">
                🔎 البحث
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    search_text = st.text_input(
        "اكتب رقم المستند أو الجهة أو الموضوع",
        key="home_search"
    )

    if st.button(
        "🔎 تنفيذ البحث",
        key="home_search_button",
        use_container_width=True
    ):

        st.session_state.search_query = search_text

        go_to("البحث")


# =========================================================
# إضافة وارد / صادر
# =========================================================

elif st.session_state.page in ["إضافة وارد", "إضافة صادر"]:

    doc_type = (
        "وارد"
        if st.session_state.page == "إضافة وارد"
        else "صادر"
    )

    icon = "📥" if doc_type == "وارد" else "📤"

    st.markdown(
        f"""
        <div class="section-title">
            {icon} إضافة {doc_type}
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form(
        key=f"add_form_{doc_type}"
    ):

        doc_number = st.text_input(
            "رقم المستند"
        )

        doc_date = st.date_input(
            "تاريخ المستند",
            value=date.today()
        )

        party = st.text_input(
            "الجهة / الطرف"
        )

        subject = st.text_area(
            "موضوع المستند"
        )

        uploaded_file = st.file_uploader(
            "إرفاق ملف PDF",
            type=["pdf"]
        )

        submitted = st.form_submit_button(
            f"💾 حفظ {doc_type}",
            use_container_width=True
        )

        if submitted:

            if not doc_number.strip():

                st.error("يرجى إدخال رقم المستند")

            elif not party.strip():

                st.error("يرجى إدخال الجهة / الطرف")

            elif not subject.strip():

                st.error("يرجى إدخال موضوع المستند")

            else:

                file_path = save_uploaded_file(
                    uploaded_file,
                    doc_type
                )

                conn = get_connection()

                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO documents
                    (
                        doc_type,
                        doc_number,
                        doc_date,
                        party,
                        subject,
                        file_path,
                        created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        doc_type,
                        doc_number.strip(),
                        doc_date.strftime("%d/%m/%Y"),
                        party.strip(),
                        subject.strip(),
                        file_path,
                        datetime.now().strftime(
                            "%d/%m/%Y %H:%M:%S"
                        )
                    )
                )

                conn.commit()

                conn.close()

                st.success(
                    f"✅ تم حفظ المستند بنجاح ضمن {doc_type}"
                )

                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "🏠 العودة للرئيسية",
        key=f"back_add_{doc_type}",
        use_container_width=True
    ):
        go_to("الرئيسية")


# =========================================================
# السجلات
# =========================================================

elif st.session_state.page in [
    "السجلات",
    "سجلات الوارد",
    "سجلات الصادر"
]:

    if st.session_state.page == "سجلات الوارد":

        doc_type_filter = "وارد"

    elif st.session_state.page == "سجلات الصادر":

        doc_type_filter = "صادر"

    else:

        doc_type_filter = None


    title = (
        "📥 سجلات الوارد"
        if doc_type_filter == "وارد"
        else
        "📤 سجلات الصادر"
        if doc_type_filter == "صادر"
        else
        "📋 السجلات"
    )

    st.markdown(
        f"""
        <div class="section-title">
            {title}
        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # فلتر السجلات
    # -----------------------------------------------------

    if doc_type_filter is None:

        selected_filter = st.selectbox(
            "نوع المستند",
            [
                "الكل",
                "الوارد",
                "الصادر"
            ]
        )

        if selected_filter == "الوارد":
            actual_filter = "وارد"

        elif selected_filter == "الصادر":
            actual_filter = "صادر"

        else:
            actual_filter = None

    else:

        actual_filter = doc_type_filter


    documents = get_documents(actual_filter)


    st.info(
        f"عدد السجلات: {len(documents)}"
    )


    if not documents:

        st.warning("لا توجد سجلات حتى الآن.")

    else:

        for row in documents:

            icon = (
                "📥"
                if row["doc_type"] == "وارد"
                else "📤"
            )

            title_text = (
                f'{icon} {row["doc_type"]} - '
                f'رقم {row["doc_number"]} - '
                f'{row["subject"]}'
            )

            with st.expander(title_text):

                # =================================================
                # عرض البيانات
                # =================================================

                st.markdown(
                    """
                    <div class="record-title">
                        📥 بيانات المستند
                    </div>

                    <div class="record-line">
                        <b>النوع:</b>
                        {doc_type}
                    </div>

                    <div class="record-line">
                        <b>رقم المستند:</b>
                        {doc_number}
                    </div>

                    <div class="record-line">
                        <b>التاريخ:</b>
                        {doc_date}
                    </div>

                    <div class="record-line">
                        <b>الجهة:</b>
                        {party}
                    </div>

                    <div class="record-line">
                        <b>الموضوع:</b>
                        {subject}
                    </div>
                    """.format(
                        doc_type=row["doc_type"],
                        doc_number=row["doc_number"],
                        doc_date=row["doc_date"],
                        party=row["party"],
                        subject=row["subject"]
                    ),
                    unsafe_allow_html=True
                )


                # -------------------------------------------------
                # الملف
                # -------------------------------------------------

                if row["file_path"]:

                    file_path = Path(row["file_path"])

                    if file_path.exists():

                        with open(
                            file_path,
                            "rb"
                        ) as f:

                            st.download_button(
                                "📄 تحميل ملف PDF",
                                data=f.read(),
                                file_name=file_path.name,
                                mime="application/pdf",
                                key=f"download_{row['id']}",
                                use_container_width=True
                            )

                    else:

                        st.warning(
                            "ملف PDF غير موجود."
                        )


                # -------------------------------------------------
                # أزرار التعديل والحذف
                # -------------------------------------------------

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "✏️ تعديل",
                        key=f"edit_{row['id']}",
                        use_container_width=True
                    ):

                        st.session_state.edit_id = row["id"]

                        go_to("تعديل")


                with col2:

                    if st.button(
                        "🗑️ حذف",
                        key=f"delete_{row['id']}",
                        use_container_width=True
                    ):

                        st.session_state.delete_id = row["id"]

                        go_to("تأكيد الحذف")


    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "🏠 العودة للرئيسية",
        key="back_records",
        use_container_width=True
    ):

        go_to("الرئيسية")


# =========================================================
# البحث
# =========================================================

elif st.session_state.page == "البحث":

    st.markdown(
        """
        <div class="section-title">
            🔎 البحث في السجلات
        </div>
        """,
        unsafe_allow_html=True
    )


    search_query = st.text_input(
        "رقم المستند أو الجهة أو الموضوع",
        value=st.session_state.search_query,
        key="search_page_input"
    )


    if st.button(
        "🔎 بحث",
        key="search_page_button",
        use_container_width=True
    ):

        st.session_state.search_query = search_query


    query = st.session_state.search_query.strip()


    if query:

        all_documents = get_documents()

        results = []

        for row in all_documents:

            if (
                query.lower() in str(
                    row["doc_number"]
                ).lower()
                or
                query.lower() in str(
                    row["party"]
                ).lower()
                or
                query.lower() in str(
                    row["subject"]
                ).lower()
                or
                query.lower() in str(
                    row["doc_type"]
                ).lower()
            ):

                results.append(row)


        st.info(
            f"عدد النتائج: {len(results)}"
        )


        if not results:

            st.warning(
                "لم يتم العثور على نتائج."
            )

        else:

            for row in results:

                icon = (
                    "📥"
                    if row["doc_type"] == "وارد"
                    else "📤"
                )

                title_text = (
                    f'{icon} {row["doc_type"]} - '
                    f'رقم {row["doc_number"]} - '
                    f'{row["subject"]}'
                )

                with st.expander(title_text):

                    # =============================================
                    # عرض بيانات المستند بدون شرطات
                    # =============================================

                    st.markdown(
                        """
                        <div class="record-title">
                            📥 بيانات المستند
                        </div>

                        <div class="record-line">
                            <b>النوع:</b>
                            {doc_type}
                        </div>

                        <div class="record-line">
                            <b>رقم المستند:</b>
                            {doc_number}
                        </div>

                        <div class="record-line">
                            <b>التاريخ:</b>
                            {doc_date}
                        </div>

                        <div class="record-line">
                            <b>الجهة:</b>
                            {party}
                        </div>

                        <div class="record-line">
                            <b>الموضوع:</b>
                            {subject}
                        </div>
                        """.format(
                            doc_type=row["doc_type"],
                            doc_number=row["doc_number"],
                            doc_date=row["doc_date"],
                            party=row["party"],
                            subject=row["subject"]
                        ),
                        unsafe_allow_html=True
                    )


                    # ---------------------------------------------
                    # تحميل PDF
                    # ---------------------------------------------

                    if row["file_path"]:

                        file_path = Path(
                            row["file_path"]
                        )

                        if file_path.exists():

                            with open(
                                file_path,
                                "rb"
                            ) as f:

                                st.download_button(
                                    "📄 تحميل ملف PDF",
                                    data=f.read(),
                                    file_name=file_path.name,
                                    mime="application/pdf",
                                    key=f"search_download_{row['id']}",
                                    use_container_width=True
                                )

                        else:

                            st.warning(
                                "ملف PDF غير موجود."
                            )


    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "🏠 العودة للرئيسية",
        key="back_from_search_results",
        use_container_width=True
    ):

        go_to("الرئيسية")


# =========================================================
# تعديل المستند
# =========================================================

elif st.session_state.page == "تعديل":

    document_id = st.session_state.get(
        "edit_id"
    )

    row = get_document(document_id)


    if not row:

        st.error(
            "المستند غير موجود."
        )

        if st.button(
            "🏠 العودة للرئيسية",
            use_container_width=True
        ):
            go_to("الرئيسية")

    else:

        st.markdown(
            """
            <div class="section-title">
                ✏️ تعديل المستند
            </div>
            """,
            unsafe_allow_html=True
        )


        with st.form(
            key=f"edit_form_{document_id}"
        ):

            doc_type = st.selectbox(
                "نوع المستند",
                ["وارد", "صادر"],
                index=(
                    0
                    if row["doc_type"] == "وارد"
                    else 1
                )
            )

            doc_number = st.text_input(
                "رقم المستند",
                value=row["doc_number"]
            )

            try:

                old_date = datetime.strptime(
                    row["doc_date"],
                    "%d/%m/%Y"
                ).date()

            except:

                old_date = date.today()


            doc_date = st.date_input(
                "تاريخ المستند",
                value=old_date
            )

            party = st.text_input(
                "الجهة / الطرف",
                value=row["party"]
            )

            subject = st.text_area(
                "موضوع المستند",
                value=row["subject"]
            )

            new_file = st.file_uploader(
                "استبدال ملف PDF",
                type=["pdf"]
            )


            submitted = st.form_submit_button(
                "💾 حفظ التعديلات",
                use_container_width=True
            )


            if submitted:

                if not doc_number.strip():

                    st.error(
                        "يرجى إدخال رقم المستند"
                    )

                elif not party.strip():

                    st.error(
                        "يرجى إدخال الجهة / الطرف"
                    )

                elif not subject.strip():

                    st.error(
                        "يرجى إدخال موضوع المستند"
                    )

                else:

                    old_file_path = row["file_path"]

                    final_file_path = old_file_path


                    # ---------------------------------------------
                    # إذا تم رفع ملف جديد
                    # ---------------------------------------------

                    if new_file:

                        new_path = save_uploaded_file(
                            new_file,
                            doc_type
                        )

                        final_file_path = new_path

                        if (
                            old_file_path
                            and
                            old_file_path != new_path
                        ):

                            delete_old_file(
                                old_file_path
                            )


                    # ---------------------------------------------
                    # تحديث البيانات
                    # ---------------------------------------------

                    update_document(
                        document_id,
                        doc_type,
                        doc_number.strip(),
                        doc_date.strftime(
                            "%d/%m/%Y"
                        ),
                        party.strip(),
                        subject.strip(),
                        final_file_path
                    )


                    st.success(
                        "✅ تم تحديث المستند بنجاح"
                    )

                    go_to("السجلات")


        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "🏠 العودة للرئيسية",
            key="back_edit",
            use_container_width=True
        ):

            go_to("الرئيسية")


# =========================================================
# تأكيد الحذف
# =========================================================

elif st.session_state.page == "تأكيد الحذف":

    document_id = st.session_state.get(
        "delete_id"
    )

    row = get_document(document_id)


    if not row:

        st.error(
            "المستند غير موجود."
        )

        if st.button(
            "🏠 العودة للرئيسية",
            use_container_width=True
        ):

            go_to("الرئيسية")

    else:

        st.markdown(
            """
            <div class="section-title">
                🗑️ تأكيد حذف المستند
            </div>
            """,
            unsafe_allow_html=True
        )


        st.warning(
            "هل أنت متأكد من رغبتك في حذف هذا المستند؟"
        )


        # =====================================================
        # بيانات المستند
        # =====================================================

        st.markdown(
            """
            <div class="info-card">

                <div class="record-line">
                    <b>النوع:</b>
                    {doc_type}
                </div>

                <div class="record-line">
                    <b>رقم المستند:</b>
                    {doc_number}
                </div>

                <div class="record-line">
                    <b>التاريخ:</b>
                    {doc_date}
                </div>

                <div class="record-line">
                    <b>الجهة:</b>
                    {party}
                </div>

                <div class="record-line">
                    <b>الموضوع:</b>
                    {subject}
                </div>

            </div>
            """.format(
                doc_type=row["doc_type"],
                doc_number=row["doc_number"],
                doc_date=row["doc_date"],
                party=row["party"],
                subject=row["subject"]
            ),
            unsafe_allow_html=True
        )


        col1, col2 = st.columns(2)


        with col1:

            if st.button(
                "🗑️ نعم، حذف المستند",
                key="confirm_delete",
                use_container_width=True
            ):

                delete_old_file(
                    row["file_path"]
                )

                delete_document(
                    document_id
                )

                st.success(
                    "✅ تم حذف المستند بنجاح"
                )

                go_to("الرئيسية")


        with col2:

            if st.button(
                "❌ إلغاء",
                key="cancel_delete",
                use_container_width=True
            ):

                go_to("الرئيسية")


# =========================================================
# الفوتر
# =========================================================

st.markdown(
    """
    <div class="custom-footer">

        <div>
            الأكاديمية المهنية للمعلمين - فرع الجيزة
        </div>

        <div>
            ✦ تصميم وتنفيذ أحمد الجنزوري ✦
        </div>

    </div>
    """,
    unsafe_allow_html=True
)
