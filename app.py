
import streamlit as st
import sqlite3
import os
import shutil
import html
import uuid
from datetime import datetime
from pathlib import Path

# =========================================================
# 1. إعدادات الصفحة
# =========================================================

st.set_page_config(
    page_title="المنظومة الرقمية للوارد والصادر",
    page_icon="📂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 2. مسارات الملفات
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

DB_NAME = BASE_DIR / "archive_system.db"
ARCHIVE_FOLDER = BASE_DIR / "Archive_Files"
INCOMING_FOLDER = ARCHIVE_FOLDER / "Incoming"
OUTGOING_FOLDER = ARCHIVE_FOLDER / "Outgoing"
LOGO_PATH = BASE_DIR / "logo.png"

for folder in (
    ARCHIVE_FOLDER,
    INCOMING_FOLDER,
    OUTGOING_FOLDER
):
    folder.mkdir(parents=True, exist_ok=True)

# =========================================================
# 3. التصميم والألوان
# =========================================================

st.markdown("""
<style>

/* خلفية الصفحة */
.stApp {
    background-color: #f4f7fb;
    direction: rtl;
}

/* عرض البرنامج */
.block-container {
    max-width: 50vw !important;
    width: 50vw !important;
    margin: auto !important;
    padding-top: 15px !important;
    padding-bottom: 20px !important;
}

/* اللوجو */
.logo-title {
    text-align: center;
    margin: 0 auto;
}

/* العنوان الرئيسي */
.main-title {
    text-align: center;
    direction: rtl;
    color: #183153;
    font-size: 29px;
    font-weight: 800;
    margin-top: 5px;
    margin-bottom: 8px;
}

/* عنوان الفرع */
.branch-title {
    text-align: center;
    direction: rtl;
    color: #52647a;
    font-size: 19px;
    font-weight: bold;
    margin-bottom: 25px;
}

/* عناوين الأقسام */
.section-title {
    background: linear-gradient(135deg, #183153, #315a8a);
    color: white;
    padding: 13px;
    border-radius: 12px;
    text-align: center;
    direction: rtl;
    font-size: 21px;
    font-weight: bold;
    margin: 18px 0;
}

/* الأزرار العامة */
.stButton button,
.stDownloadButton button {
    width: 100%;
    min-height: 45px;
    border-radius: 10px;
    font-weight: bold;
    font-size: 15px;
    transition: all 0.2s ease;
}

/* تأثير المرور */
.stButton button:hover,
.stDownloadButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 12px rgba(0,0,0,0.12);
}

/* زر الوارد */
div[data-testid="stHorizontalBlock"]
> div:nth-child(1)
div[data-testid="stButton"]
button[kind="primary"] {
    background: linear-gradient(135deg, #1565c0, #42a5f5);
    color: white;
    border: none;
}

/* حقول الإدخال */
input, textarea {
    direction: rtl !important;
    text-align: right !important;
    border-radius: 8px !important;
}

/* البطاقات */
.document-card {
    background: white;
    border: 1px solid #dce5ef;
    border-radius: 12px;
    padding: 15px;
    margin-top: 8px;
    margin-bottom: 10px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.04);
    direction: rtl;
    text-align: right;
    line-height: 2;
    overflow-wrap: anywhere;
}

/* الفوتر */
.footer {
    text-align: center;
    direction: rtl;
    color: #64748b;
    border-top: 1px solid #dce5ef;
    padding: 15px 5px;
    margin-top: 30px;
    font-size: 14px;
    font-weight: bold;
}

/* إخفاء العناصر الافتراضية */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* الهاتف والشاشات الصغيرة */
@media (max-width: 900px) {
    .block-container {
        width: 95% !important;
        max-width: 95% !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
    }

    .main-title {
        font-size: 23px;
    }

    .branch-title {
        font-size: 16px;
    }

    .section-title {
        font-size: 18px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# 4. قاعدة البيانات
# =========================================================

def get_db_connection():
    conn = sqlite3.connect(
        str(DB_NAME),
        timeout=30
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
            subject TEXT DEFAULT '',
            file_path TEXT DEFAULT '',
            created_at TEXT
        )
    """)

    # فهرسة لتحسين البحث
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_documents_type
        ON documents(doc_type)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_documents_number
        ON documents(doc_number)
    """)

    conn.commit()
    conn.close()


init_db()

# =========================================================
# 5. الجلسة
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

if "delete_id" not in st.session_state:
    st.session_state.delete_id = None

# =========================================================
# 6. دوال قاعدة البيانات
# =========================================================

def get_documents(doc_type, search_text=""):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT *
        FROM documents
        WHERE doc_type = ?
    """

    params = [doc_type]

    if search_text.strip():
        query += """
            AND (
                doc_number LIKE ?
                OR party LIKE ?
                OR subject LIKE ?
                OR doc_date LIKE ?
            )
        """

        value = f"%{search_text.strip()}%"

        params.extend([
            value,
            value,
            value,
            value
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


def insert_document(
    doc_type,
    doc_number,
    doc_date,
    party,
    subject,
    uploaded_file
):
    file_path = ""

    if uploaded_file is not None:
        folder = (
            INCOMING_FOLDER
            if doc_type == "وارد"
            else OUTGOING_FOLDER
        )

        filename = (
            f"{uuid.uuid4().hex}_"
            f"{Path(uploaded_file.name).name}"
        )

        path = folder / filename

        with open(path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        file_path = str(path)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO documents (
            doc_type,
            doc_number,
            doc_date,
            party,
            subject,
            file_path,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        doc_type,
        doc_number.strip(),
        doc_date.strftime("%Y-%m-%d"),
        party.strip(),
        subject.strip(),
        file_path,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def update_document(
    document_id,
    doc_number,
    doc_date,
    party,
    subject,
    uploaded_file
):
    document = get_document(document_id)

    if not document:
        return False

    old_path = document["file_path"] or ""
    new_path = old_path

    if uploaded_file is not None:
        folder = (
            INCOMING_FOLDER
            if document["doc_type"] == "وارد"
            else OUTGOING_FOLDER
        )

        filename = (
            f"{uuid.uuid4().hex}_"
            f"{Path(uploaded_file.name).name}"
        )

        path = folder / filename

        with open(path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        new_path = str(path)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE documents
        SET
            doc_number = ?,
            doc_date = ?,
            party = ?,
            subject = ?,
            file_path = ?
        WHERE id = ?
    """, (
        doc_number.strip(),
        doc_date.strftime("%Y-%m-%d"),
        party.strip(),
        subject.strip(),
        new_path,
        document_id
    ))

    conn.commit()
    conn.close()

    # حذف الملف القديم بعد نجاح التحديث
    if uploaded_file is not None and old_path:
        try:
            old_file = Path(old_path)
            if old_file.exists():
                old_file.unlink()
        except OSError:
            pass

    return True


def delete_document(document_id):
    document = get_document(document_id)

    if not document:
        return False

    file_path = document["file_path"] or ""

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM documents WHERE id = ?",
        (document_id,)
    )

    conn.commit()
    conn.close()

    if file_path:
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
        except OSError:
            pass

    return True


def get_counts():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT doc_type, COUNT(*) AS total
        FROM documents
        GROUP BY doc_type
    """)

    rows = cursor.fetchall()
    conn.close()

    counts = {
        "وارد": 0,
        "صادر": 0
    }

    for row in rows:
        counts[row["doc_type"]] = row["total"]

    return counts

# =========================================================
# 7. الترويسة واللوجو
# =========================================================

# توسيط اللوجو باستخدام الأعمدة
logo_left, logo_center, logo_right = st.columns(
    [1, 1, 1]
)

with logo_center:
    if LOGO_PATH.exists():
        st.image(
            str(LOGO_PATH),
            width=115
        )
    else:
        st.markdown(
            "<h1 style='text-align:center'>📂</h1>",
            unsafe_allow_html=True
        )

st.markdown("""
<div class="main-title">
    الأكاديمية المهنية للمعلمين – فرع الجيزة
</div>

<div class="branch-title">
    المنظومة الرقمية للوارد والصادر
</div>
""", unsafe_allow_html=True)

# =========================================================
# 8. الصفحة الرئيسية
# =========================================================

if st.session_state.page == "home":

    st.markdown("""
    <div class="section-title">
        اختر نوع المعاملة
    </div>
    """, unsafe_allow_html=True)

    col_in, col_out = st.columns(2)

    with col_in:
        if st.button(
            "📥 الوارد",
            type="primary",
            use_container_width=True,
            key="home_incoming"
        ):
            st.session_state.page = "incoming"
            st.session_state.edit_id = None
            st.session_state.delete_id = None
            st.rerun()

    with col_out:
        if st.button(
            "📤 الصادر",
            type="primary",
            use_container_width=True,
            key="home_outgoing"
        ):
            st.session_state.page = "outgoing"
            st.session_state.edit_id = None
            st.session_state.delete_id = None
            st.rerun()

    counts = get_counts()

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.info(f"📥 إجمالي الوارد: {counts['وارد']}")

    with c2:
        st.success(f"📤 إجمالي الصادر: {counts['صادر']}")

# =========================================================
# 9. شاشة الوارد والصادر
# =========================================================

elif st.session_state.page in ("incoming", "outgoing"):

    current_type = (
        "وارد"
        if st.session_state.page == "incoming"
        else "صادر"
    )

    icon = "📥" if current_type == "وارد" else "📤"

    st.markdown(
        f'<div class="section-title">{icon} سجل {current_type}</div>',
        unsafe_allow_html=True
    )

    top1, top2 = st.columns(2)

    with top1:
        if st.button("🏠 الرئيسية", use_container_width=True):
            st.session_state.page = "home"
            st.session_state.edit_id = None
            st.session_state.delete_id = None
            st.rerun()

    with top2:
        if st.button(
            f"➕ إضافة {current_type} جديد",
            use_container_width=True
        ):
            st.session_state.edit_id = None
            st.rerun()

    # =====================================================
    # نموذج التسجيل والتعديل
    # =====================================================

    edit_document = None

    if st.session_state.edit_id is not None:
        edit_document = get_document(
            st.session_state.edit_id
        )

        if (
            edit_document is None
            or edit_document["doc_type"] != current_type
        ):
            st.session_state.edit_id = None
            edit_document = None

    is_edit = edit_document is not None

    st.markdown(
        f'<div class="section-title">'
        f'{"✏️ تعديل" if is_edit else "➕ تسجيل"} {current_type}'
        f'</div>',
        unsafe_allow_html=True
    )

    default_number = (
        edit_document["doc_number"] if is_edit else ""
    )

    default_party = (
        edit_document["party"] if is_edit else ""
    )

    default_subject = (
        edit_document["subject"] or "" if is_edit else ""
    )

    default_date = datetime.now().date()

    if is_edit:
        try:
            default_date = datetime.strptime(
                edit_document["doc_date"],
                "%Y-%m-%d"
            ).date()
        except (ValueError, TypeError):
            pass

    with st.form(
        key=f"document_form_{current_type}_{st.session_state.edit_id}",
        clear_on_submit=False
    ):

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

        uploaded_file = st.file_uploader(
            "📎 إرفاق ملف PDF",
            type=["pdf"],
            help="اختر ملف PDF الخاص بالخطاب"
        )

        if is_edit and edit_document["file_path"]:
            st.caption(
                "يوجد ملف محفوظ. ارفع ملفًا جديدًا "
                "فقط إذا كنت تريد استبداله."
            )

        submitted = st.form_submit_button(
            "💾 حفظ البيانات",
            type="primary",
            use_container_width=True
        )

    cancel_col, empty_col = st.columns([2, 8])

    with cancel_col:
        if st.button(
            "❌ إلغاء",
            use_container_width=True
        ):
            st.session_state.edit_id = None
            st.rerun()

    if submitted:
        if not doc_number.strip():
            st.error("يرجى إدخال رقم الخطاب.")

        elif not party.strip():
            st.error("يرجى إدخال اسم الجهة.")

        else:
            try:
                if is_edit:
                    success = update_document(
                        st.session_state.edit_id,
                        doc_number,
                        doc_date,
                        party,
                        subject,
                        uploaded_file
                    )

                    if success:
                        st.session_state.edit_id = None
                        st.success("تم تعديل البيانات بنجاح.")
                        st.rerun()

                    else:
                        st.error("السجل غير موجود.")

                else:
                    insert_document(
                        current_type,
                        doc_number,
                        doc_date,
                        party,
                        subject,
                        uploaded_file
                    )

                    st.success("تم تسجيل الخطاب بنجاح.")
                    st.rerun()

            except Exception as e:
                st.error(f"حدث خطأ أثناء الحفظ: {e}")

    # =====================================================
    # البحث
    # =====================================================

    st.markdown("""
    <div class="section-title">
        🔎 البحث في السجلات
    </div>
    """, unsafe_allow_html=True)

    search_text = st.text_input(
        "البحث برقم الخطاب أو التاريخ أو الجهة أو الموضوع",
        placeholder="اكتب كلمة البحث هنا...",
        key=f"search_{current_type}"
    )

    documents = get_documents(
        current_type,
        search_text
    )

    st.markdown(
        f"**عدد السجلات: {len(documents)}**"
    )

    # =====================================================
    # عرض السجلات
    # =====================================================

    if not documents:
        st.info("لا توجد سجلات مطابقة للبحث.")

    for document in documents:

        doc_id = document["id"]

        safe_number = html.escape(
            str(document["doc_number"])
        )

        safe_date = html.escape(
            str(document["doc_date"])
        )

        safe_party = html.escape(
            str(document["party"])
        )

        safe_subject = html.escape(
            str(document["subject"] or "—")
        )

        st.markdown(
            f"""
            <div class="document-card">
                <b>📌 رقم الخطاب:</b> {safe_number}
                <br>
                <b>📅 التاريخ:</b> {safe_date}
                <br>
                <b>🏢 الجهة:</b> {safe_party}
                <br>
                <b>📝 الموضوع:</b> {safe_subject}
            </div>
            """,
            unsafe_allow_html=True
        )

        b1, b2, b3 = st.columns(3)

        with b1:
            file_path = document["file_path"] or ""

            if file_path and Path(file_path).is_file():
                with open(file_path, "rb") as pdf_file:
                    st.download_button(
                        "📄 تنزيل PDF",
                        data=pdf_file.read(),
                        file_name=Path(file_path).name,
                        mime="application/pdf",
                        key=f"download_{doc_id}",
                        use_container_width=True
                    )
            else:
                st.button(
                    "📄 لا يوجد PDF",
                    key=f"no_pdf_{doc_id}",
                    disabled=True,
                    use_container_width=True
                )

        with b2:
            if st.button(
                "✏️ تعديل",
                key=f"edit_{doc_id}",
                use_container_width=True
            ):
                st.session_state.edit_id = doc_id
                st.session_state.delete_id = None
                st.rerun()

        with b3:
            if st.button(
                "🗑️ حذف",
                key=f"delete_{doc_id}",
                use_container_width=True
            ):
                st.session_state.delete_id = doc_id
                st.rerun()

        # =================================================
        # تأكيد الحذف
        # =================================================

        if st.session_state.delete_id == doc_id:

            st.warning(
                "هل أنت متأكد من حذف السجل وملف PDF المرتبط به؟"
            )

            d1, d2 = st.columns(2)

            with d1:
                if st.button(
                    "نعم، حذف نهائي",
                    key=f"confirm_delete_{doc_id}",
                    type="primary",
                    use_container_width=True
                ):
                    try:
                        delete_document(doc_id)
                        st.session_state.delete_id = None
                        st.success("تم حذف السجل.")
                        st.rerun()

                    except Exception as e:
                        st.error(f"تعذر الحذف: {e}")

            with d2:
                if st.button(
                    "إلغاء الحذف",
                    key=f"cancel_delete_{doc_id}",
                    use_container_width=True
                ):
                    st.session_state.delete_id = None
                    st.rerun()

        st.divider()

# =========================================================
# 10. الفوتر
# =========================================================

st.markdown("""
<div class="footer">
    ✦ تصميم وتنفيذ أحمد الجنزوري ✦
</div>
""", unsafe_allow_html=True)
