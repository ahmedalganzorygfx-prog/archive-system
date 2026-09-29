import streamlit as st
import sqlite3
import os
import shutil
from datetime import datetime
import pandas as pd

# =========================================================
# 1. إعدادات الصفحة
# =========================================================

st.set_page_config(
    page_title="المنظومة الرقمية للوارد والصادر - الأكاديمية المهنية للمعلمين فرع الجيزة",
    page_icon="📂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 2. CSS - التصميم و RTL
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, Tahoma, sans-serif;
}

/* الصفحة */
.stApp {
    direction: rtl;
    background: #f7f9fc;
}

/* حاوية البرنامج الرئيسية */
.block-container {
    max-width: 50vw !important;
    width: 50vw !important;
    margin: 0 auto !important;
    padding-top: 20px !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
}

/* اللوجو */
.logo-container {
    width: 100%;
    text-align: center;
    margin-top: 5px;
    margin-bottom: 8px;
}

.logo-container img {
    display: block;
    margin: auto;
}

/* العناوين */
.main-title {
    text-align: center;
    direction: rtl;
    font-size: 30px;
    font-weight: bold;
    color: #183153;
    margin-top: 5px;
    margin-bottom: 6px;
}

.branch-title {
    text-align: center;
    direction: rtl;
    font-size: 20px;
    font-weight: bold;
    color: #555;
    margin-bottom: 25px;
}

/* عنوان الأقسام */
.section-title {
    background: linear-gradient(
        135deg,
        #183153,
        #315a8a
    );
    color: white;
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    direction: rtl;
    font-size: 21px;
    font-weight: bold;
    margin-top: 15px;
    margin-bottom: 18px;
}

/* أزرار الوارد والصادر */
.stButton button {
    width: 100%;
    min-height: 55px;
    border-radius: 12px !important;
    border: none !important;
    font-family: Arial, Tahoma, sans-serif !important;
    font-size: 18px !important;
    font-weight: bold !important;
    transition: all 0.2s ease-in-out;
}

/* بطاقات أزرار الصفحة الرئيسية */
div[data-testid="stHorizontalBlock"] .stButton button {
    box-shadow: 0 4px 12px rgba(0,0,0,0.10);
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 7px 18px rgba(0,0,0,0.16);
}

/* الحقول */
input,
textarea {
    direction: rtl !important;
    text-align: right !important;
    border-radius: 8px !important;
}

/* رفع الملفات */
section[data-testid="stFileUploader"] {
    direction: rtl;
}

/* بطاقات المستندات */
.document-card {
    background: white;
    border: 1px solid #e1e7ef;
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    direction: rtl;
    text-align: right;
}

/* الفوتر */
.footer {
    text-align: center;
    direction: rtl;
    margin-top: 35px;
    padding: 15px 5px;
    border-top: 1px solid #dce2e9;
    color: #666;
    font-size: 14px;
    line-height: 1.8;
}

/* إخفاء عناصر Streamlit */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)
# =========================================================
# 3. المجلدات
# =========================================================

ARCHIVE_FOLDER = "Archive_Files"

INCOMING_FOLDER = os.path.join(
    ARCHIVE_FOLDER,
    "Incoming"
)

OUTGOING_FOLDER = os.path.join(
    ARCHIVE_FOLDER,
    "Outgoing"
)

os.makedirs(INCOMING_FOLDER, exist_ok=True)
os.makedirs(OUTGOING_FOLDER, exist_ok=True)


# =========================================================
# 4. قاعدة البيانات
# =========================================================

DB_NAME = "archive_system.db"


def get_db_connection():
    conn = sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_type TEXT NOT NULL,
            doc_number TEXT NOT NULL,
            doc_date TEXT NOT NULL,
            party TEXT NOT NULL,
            subject TEXT,
            file_path TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


# =========================================================
# 5. Session State
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None


# =========================================================
# الترويسة
# =========================================================

st.markdown(
    '<div class="logo-container">',
    unsafe_allow_html=True
)

if os.path.exists("logo.png"):
    st.image(
        "logo.png",
        width=115
    )

st.markdown(
    "</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-title">
        المنظومة الرقمية للوارد والصادر
    </div>

    <div class="branch-title">
        الأكاديمية المهنية للمعلمين – فرع الجيزة
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 7. دوال مساعدة
# =========================================================

def get_documents(doc_type=None, search_text=""):

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT *
        FROM documents
        WHERE 1=1
    """

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
            )
        """

        search_pattern = f"%{search_text}%"

        params.extend([
            search_pattern,
            search_pattern,
            search_pattern
        ])

    query += " ORDER BY id DESC"

    cursor.execute(query, params)

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_document(document_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM documents WHERE id = ?",
        (document_id,)
    )

    row = cursor.fetchone()

    conn.close()

    return row


def delete_document(document_id):

    document = get_document(document_id)

    if not document:
        return False

    file_path = document["file_path"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM documents WHERE id = ?",
        (document_id,)
    )

    conn.commit()
    conn.close()

    # حذف ملف PDF المرتبط
    if file_path and os.path.exists(file_path):

        try:
            os.remove(file_path)
        except Exception:
            pass

    return True


def save_document(
    doc_type,
    doc_number,
    doc_date,
    party,
    subject,
    uploaded_file
):

    if doc_type == "وارد":
        target_folder = INCOMING_FOLDER
    else:
        target_folder = OUTGOING_FOLDER

    file_path = ""

    # حفظ ملف PDF
    if uploaded_file is not None:

        original_name = uploaded_file.name

        safe_name = "".join(
            c for c in original_name
            if c.isalnum() or c in " ._-"
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        file_name = f"{timestamp}_{safe_name}"

        file_path = os.path.join(
            target_folder,
            file_name
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    conn = get_db_connection()
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
            doc_number,
            doc_date,
            party,
            subject,
            file_path,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )

    conn.commit()
    conn.close()


# =========================================================
# أزرار الوارد والصادر
# =========================================================

st.markdown(
    """
    <div class="section-title">
        اختر نوع المعاملة
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        """
        <style>
        div[data-testid="stButton"]
        button[kind="secondary"] {
            background: linear-gradient(
                135deg,
                #1769aa,
                #2196d3
            ) !important;
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "📥  الوارد",
        use_container_width=True,
        key="home_incoming"
    ):
        st.session_state.page = "incoming"
        st.session_state.edit_id = None
        st.rerun()


with col2:

    if st.button(
        "📤  الصادر",
        use_container_width=True,
        key="home_outgoing"
    ):
        st.session_state.page = "outgoing"
        st.session_state.edit_id = None
        st.rerun()
    # إحصائيات
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM documents WHERE doc_type = 'وارد'"
    )

    incoming_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM documents WHERE doc_type = 'صادر'"
    )

    outgoing_count = cursor.fetchone()[0]

    conn.close()

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.info(
            f"📥 إجمالي الوارد: {incoming_count}"
        )

    with c2:
        st.success(
            f"📤 إجمالي الصادر: {outgoing_count}"
        )


# =========================================================
# 9. شاشة الوارد / الصادر
# =========================================================

elif st.session_state.page in [incoming", "outgoing]:

    current_type = (
        "وارد"
        if st.session_state.page == "incoming"
        else "صادر"
    )

    icon = "📥" if current_type == "وارد" else "📤"

    st.markdown(
        f"""
        <div class="section-title">
            {icon} سجل {current_type}
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # أزرار أعلى الصفحة
    # =====================================================

    top1, top2, top3 = st.columns(
        [2, 2, 6]
    )

    with top1:

        if st.button(
            "🏠 الرئيسية",
            use_container_width=True
        ):

            st.session_state.page = "home"
            st.session_state.edit_id = None

            st.rerun()

    with top2:

        if st.button(
            f"➕ إضافة {current_type}",
            use_container_width=True
        ):

            st.session_state.edit_id = None

            st.rerun()

    # =====================================================
    # نموذج الإضافة / التعديل
    # =====================================================

    edit_document = None

    if st.session_state.edit_id:

        edit_document = get_document(
            st.session_state.edit_id
        )

    form_title = (
        f"✏️ تعديل بيانات {current_type}"
        if edit_document
        else f"➕ تسجيل {current_type} جديد"
    )

    st.markdown(
        f"""
        <div class="section-title"
             style="font-size:20px;">
            {form_title}
        </div>
        """,
        unsafe_allow_html=True
    )

    # القيم الافتراضية
    default_number = ""
    default_party = ""
    default_subject = ""
    default_date = datetime.now().date()

    if edit_document:

        default_number = edit_document["doc_number"]
        default_party = edit_document["party"]
        default_subject = edit_document["subject"] or ""

        try:
            default_date = datetime.strptime(
                edit_document["doc_date"],
                "%Y-%m-%d"
            ).date()
        except Exception:
            default_date = datetime.now().date()

    # =====================================================
    # الحقول
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        doc_number = st.text_input(
            "رقم الخطاب *",
            value=default_number,
            placeholder="أدخل رقم الخطاب"
        )

    with col2:

        doc_date = st.date_input(
            "تاريخ الخطاب *",
            value=default_date,
            format="DD/MM/YYYY"
        )

    col3, col4 = st.columns(2)

    with col3:

        party = st.text_input(
            "الجهة *",
            value=default_party,
            placeholder="اسم الجهة"
        )

    with col4:

        subject = st.text_input(
            "موضوع الخطاب",
            value=default_subject,
            placeholder="موضوع الخطاب"
        )

    # =====================================================
    # رفع الملف
    # =====================================================

    uploaded_file = st.file_uploader(
        "📎 إرفاق ملف الخطاب PDF",
        type=["pdf"],
        help="يمكن رفع ملف PDF الخاص بالخطاب"
    )

    if edit_document and edit_document["file_path"]:

        st.caption(
            "📄 يوجد ملف PDF محفوظ حاليًا. "
            "رفع ملف جديد سيستبدل الملف القديم."
        )

    # =====================================================
    # أزرار الحفظ
    # =====================================================

    save_col, cancel_col, empty_col = st.columns(
        [2, 2, 6]
    )

    with save_col:

        save_button = st.button(
            "💾 حفظ البيانات",
            use_container_width=True,
            type="primary"
        )

    with cancel_col:

        cancel_button = st.button(
            "❌ إلغاء",
            use_container_width=True
        )

    # =====================================================
    # إلغاء التعديل
    # =====================================================

    if cancel_button:

        st.session_state.edit_id = None

        st.rerun()

    # =====================================================
    # حفظ
    # =====================================================

    if save_button:

        if not doc_number.strip():

            st.error(
                "⚠️ يرجى إدخال رقم الخطاب."
            )

        elif not party.strip():

            st.error(
                "⚠️ يرجى إدخال اسم الجهة."
            )

        else:

            # =============================================
            # تعديل سجل موجود
            # =============================================

            if edit_document:

                old_file = edit_document["file_path"]

                new_file_path = old_file

                # إذا تم رفع ملف جديد
                if uploaded_file is not None:

                    if current_type == "وارد":
                        target_folder = INCOMING_FOLDER
                    else:
                        target_folder = OUTGOING_FOLDER

                    timestamp = datetime.now().strftime(
                        "%Y%m%d_%H%M%S"
                    )

                    safe_name = "".join(
                        c for c in uploaded_file.name
                        if c.isalnum() or c in " ._-"
                    )

                    new_file_path = os.path.join(
                        target_folder,
                        f"{timestamp}_{safe_name}"
                    )

                    with open(
                        new_file_path,
                        "wb"
                    ) as f:

                        f.write(
                            uploaded_file.getbuffer()
                        )

                    # حذف الملف القديم
                    if (
                        old_file
                        and os.path.exists(old_file)
                        and old_file != new_file_path
                    ):

                        try:
                            os.remove(old_file)
                        except Exception:
                            pass

                conn = get_db_connection()
                cursor = conn.cursor()

                cursor.execute(
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
                        doc_number.strip(),
                        doc_date.strftime("%Y-%m-%d"),
                        party.strip(),
                        subject.strip(),
                        new_file_path,
                        st.session_state.edit_id
                    )
                )

                conn.commit()
                conn.close()

                st.session_state.edit_id = None

                st.success(
                    "✅ تم تعديل البيانات بنجاح."
                )

                st.rerun()

            # =============================================
            # إضافة سجل جديد
            # =============================================

            else:

                save_document(
                    current_type,
                    doc_number.strip(),
                    doc_date.strftime("%Y-%m-%d"),
                    party.strip(),
                    subject.strip(),
                    uploaded_file
                )

                st.success(
                    f"✅ تم تسجيل {current_type} بنجاح."
                )

                st.rerun()

    # =====================================================
    # البحث
    # =====================================================

    st.markdown(
        """
        <div class="section-title"
             style="font-size:20px;">
            🔎 البحث في السجلات
        </div>
        """,
        unsafe_allow_html=True
    )

    search_text = st.text_input(
        "البحث برقم الخطاب أو الجهة أو الموضوع",
        placeholder="اكتب كلمة البحث هنا..."
    )

    documents = get_documents(
        current_type,
        search_text
    )

    st.markdown(
        f"""
        <div style="
            text-align:right;
            direction:rtl;
            font-size:18px;
            font-weight:bold;
            margin:15px 0;
        ">
            عدد السجلات: {len(documents)}
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # عرض السجلات
    # =====================================================

    if not documents:

        st.warning(
            f"لا توجد سجلات في قسم {current_type}."
        )

    else:

        for document in documents:

            with st.container():

                st.markdown(
                    f"""
                    <div class="document-card">
                        <b>📌 رقم الخطاب:</b>
                        {document["doc_number"]}
                        &nbsp;&nbsp; | &nbsp;&nbsp;

                        <b>📅 التاريخ:</b>
                        {document["doc_date"]}
                        <br><br>

                        <b>🏢 الجهة:</b>
                        {document["party"]}
                        <br><br>

                        <b>📝 الموضوع:</b>
                        {document["subject"] or "—"}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                b1, b2, b3, b4 = st.columns(
                    [1.5, 1.5, 1.5, 5]
                )

                with b1:

                    if document["file_path"]:

                        if os.path.exists(
                            document["file_path"]
                        ):

                            with open(
                                document["file_path"],
                                "rb"
                            ) as pdf_file:

                                st.download_button(
                                    "📄 PDF",
                                    data=pdf_file,
                                    file_name=os.path.basename(
                                        document["file_path"]
                                    ),
                                    mime="application/pdf",
                                    key=f"pdf_{document['id']}",
                                    use_container_width=True
                                )

                with b2:

                    if st.button(
                        "✏️ تعديل",
                        key=f"edit_{document['id']}",
                        use_container_width=True
                    ):

                        st.session_state.edit_id = document["id"]

                        st.rerun()

                with b3:

                    if st.button(
                        "🗑️ حذف",
                        key=f"delete_{document['id']}",
                        use_container_width=True
                    ):

                        st.session_state[
                            f"confirm_delete_{document['id']}"
                        ] = True

                        st.rerun()

                # =========================================
                # تأكيد الحذف
                # =========================================

                if st.session_state.get(
                    f"confirm_delete_{document['id']}",
                    False
                ):

                    st.warning(
                        "⚠️ هل أنت متأكد من حذف هذا السجل وملف PDF المرتبط به؟"
                    )

                    d1, d2 = st.columns(2)

                    with d1:

                        if st.button(
                            "نعم، حذف نهائي",
                            key=f"yes_delete_{document['id']}",
                            type="primary",
                            use_container_width=True
                        ):

                            delete_document(
                                document["id"]
                            )

                            st.session_state[
                                f"confirm_delete_{document['id']}"
                            ] = False

                            st.success(
                                "تم حذف السجل بنجاح."
                            )

                            st.rerun()

                    with d2:

                        if st.button(
                            "إلغاء الحذف",
                            key=f"cancel_delete_{document['id']}",
                            use_container_width=True
                        ):

                            st.session_state[
                                f"confirm_delete_{document['id']}"
                            ] = False

                            st.rerun()

                st.divider()


# =========================================================
# 10. نهاية البرنامج
# =========================================================

st.markdown(
    """
    <div style="
        text-align:center;
        direction:rtl;
        margin-top:40px;
        padding:15px;
        color:#666;
        font-size:14px;
    ">
        الأكاديمية المهنية للمعلمين – فرع الجيزة
        <br>
        المنظومة الرقمية للوارد والصادر
    </div>
    """,
    unsafe_allow_html=True
)
