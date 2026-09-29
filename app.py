
import streamlit as st
import sqlite3
import shutil
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

.block-container {
    max-width: 850px;
    width: 95%;
    padding-top: 1rem;
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

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
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
    """حفظ ملف PDF داخل مجلد الأرشيف."""

    if uploaded_file is None:
        return None

    folder = get_archive_folder(doc_type)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    original_name = Path(uploaded_file.name).name
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
            width=160
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
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ إضافة صادر جديد", key="add_outgoing"):
            go_to("إضافة صادر")
            st.rerun()

    with col2:
        if st.button("📋 عرض السجلات", key="view_all"):
            go_to("عرض السجلات")
            st.rerun()

    st.markdown(
        '<div class="section-title">🔎 البحث في الأرشيف</div>',
        unsafe_allow_html=True
    )

    search_text = st.text_input(
        "ابحث برقم الخطاب أو الجهة أو الموضوع",
        key="main_search"
    )

    if st.button("بحث", key="main_search_button", type="primary"):
        st.session_state.search_query = search_text
        go_to("نتائج البحث")
        st.rerun()


# ==========================================
# إضافة مستند وارد أو صادر
# ==========================================

elif st.session_state.page in ["إضافة وارد", "إضافة صادر"]:

    doc_type = (
        "وارد"
        if st.session_state.page == "إضافة وارد"
        else "صادر"
    )

    st.markdown(
        f'<div class="section-title">➕ تسجيل {doc_type} جديد</div>',
        unsafe_allow_html=True
    )

    with st.form("add_document_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:
            doc_number = st.text_input(
                "رقم الخطاب *",
                placeholder="أدخل رقم الخطاب"
            )

        with col2:
            doc_date = st.date_input(
                "تاريخ الخطاب *",
                value=date.today(),
                format="YYYY/MM/DD"
            )

        col1, col2 = st.columns(2)

        with col1:
            party = st.text_input(
                "الجهة *",
                placeholder="اسم الجهة"
            )

        with col2:
            subject = st.text_input(
                "موضوع الخطاب *",
                placeholder="موضوع الخطاب"
            )

        uploaded_file = st.file_uploader(
            "إرفاق ملف الخطاب PDF (اختياري)",
            type=["pdf"],
            help="يمكن إرفاق نسخة PDF من الخطاب"
        )

        submitted = st.form_submit_button(
            "💾 حفظ المستند",
            type="primary",
            use_container_width=True
        )

        if submitted:

            if not doc_number.strip():
                st.error("من فضلك أدخل رقم الخطاب.")

            elif not party.strip():
                st.error("من فضلك أدخل اسم الجهة.")

            elif not subject.strip():
                st.error("من فضلك أدخل موضوع الخطاب.")

            else:
                file_path = None

                try:
                    file_path = save_uploaded_file(
                        uploaded_file,
                        doc_type
                    )

                    conn = get_connection()

                    conn.execute("""
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
                    """, (
                        doc_type,
                        doc_number.strip(),
                        doc_date.strftime("%Y-%m-%d"),
                        party.strip(),
                        subject.strip(),
                        file_path
                    ))

                    conn.commit()
                    conn.close()

                    st.success(
                        f"تم حفظ الخطاب {doc_type} بنجاح."
                    )

                    st.session_state.page = "الرئيسية"
                    st.rerun()

                except Exception as e:
                    st.error(f"حدث خطأ أثناء الحفظ: {e}")

                    # تنظيف الملف إذا فشلت عملية الحفظ
                    if file_path:
                        try:
                            Path(file_path).unlink(missing_ok=True)
                        except OSError:
                            pass

    if st.button("⬅️ العودة للرئيسية"):
        go_to("الرئيسية")
        st.rerun()


# ==========================================
# عرض السجلات
# ==========================================

elif st.session_state.page == "عرض السجلات":

    st.markdown(
        '<div class="section-title">📋 جميع السجلات</div>',
        unsafe_allow_html=True
    )

    filter_type = st.selectbox(
        "نوع المستند",
        ["الكل", "وارد", "صادر"]
    )

    selected_type = (
        None if filter_type == "الكل"
        else filter_type
    )

    rows = get_documents(selected_type)

    if rows:

        for row in rows:

            with st.expander(
                f"{row['doc_type']} | رقم {row['doc_number']} | {row['party']}"
            ):

                st.write(f"**رقم الخطاب:** {row['doc_number']}")
                st.write(f"**التاريخ:** {row['doc_date']}")
                st.write(f"**الجهة:** {row['party']}")
                st.write(f"**الموضوع:** {row['subject']}")

                if row["file_path"]:
                    file_path = Path(row["file_path"])

                    if file_path.exists():
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label="📥 تنزيل ملف الخطاب",
                                data=f.read(),
                                file_name=file_path.name,
                                mime="application/pdf",
                                key=f"download_{row['id']}"
                            )
                    else:
                        st.warning("ملف الخطاب غير موجود في الأرشيف.")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        "✏️ تعديل",
                        key=f"edit_{row['id']}"
                    ):
                        st.session_state.edit_id = row["id"]
                        go_to("تعديل مستند")
                        st.rerun()

                with col2:
                    if st.button(
                        "🗑️ حذف",
                        key=f"delete_{row['id']}"
                    ):
                        st.session_state.delete_id = row["id"]
                        go_to("تأكيد الحذف")
                        st.rerun()

    else:
        st.info("لا توجد سجلات مسجلة حتى الآن.")

    if st.button("⬅️ العودة للرئيسية"):
        go_to("الرئيسية")
        st.rerun()


# ==========================================
# نتائج البحث
# ==========================================

elif st.session_state.page == "نتائج البحث":

    st.markdown(
        '<div class="section-title">🔎 نتائج البحث</div>',
        unsafe_allow_html=True
    )

    search_query = st.session_state.get(
        "search_query", ""
    )

    rows = get_documents(search_text=search_query)

    if rows:

        st.success(f"عدد النتائج: {len(rows)}")

        for row in rows:

            with st.expander(
                f"{row['doc_type']} | {row['doc_number']} | {row['party']}"
            ):

                st.write(f"**التاريخ:** {row['doc_date']}")
                st.write(f"**الجهة:** {row['party']}")
                st.write(f"**الموضوع:** {row['subject']}")

                if row["file_path"]:
                    file_path = Path(row["file_path"])

                    if file_path.exists():
                        with open(file_path, "rb") as f:
                            st.download_button(
                                "📥 تنزيل الخطاب",
                                data=f.read(),
                                file_name=file_path.name,
                                mime="application/pdf",
                                key=f"search_download_{row['id']}"
                            )

    else:
        st.warning("لا توجد نتائج مطابقة للبحث.")

    if st.button("⬅️ العودة للرئيسية"):
        go_to("الرئيسية")
        st.rerun()


# ==========================================
# تعديل مستند
# ==========================================

elif st.session_state.page == "تعديل مستند":

    doc_id = st.session_state.get("edit_id")

    conn = get_connection()

    row = conn.execute(
        "SELECT * FROM documents WHERE id = ?",
        (doc_id,)
    ).fetchone()

    conn.close()

    st.markdown(
        '<div class="section-title">✏️ تعديل بيانات المستند</div>',
        unsafe_allow_html=True
    )

    if row:

        with st.form("edit_document_form"):

            col1, col2 = st.columns(2)

            with col1:
                new_number = st.text_input(
                    "رقم الخطاب",
                    value=row["doc_number"]
                )

            with col2:
                try:
                    current_date = date.fromisoformat(
                        row["doc_date"]
                    )
                except ValueError:
                    current_date = date.today()

                new_date = st.date_input(
                    "تاريخ الخطاب",
                    value=current_date,
                    format="YYYY/MM/DD"
                )

            new_party = st.text_input(
                "الجهة",
                value=row["party"]
            )

            new_subject = st.text_input(
                "موضوع الخطاب",
                value=row["subject"]
            )

            new_file = st.file_uploader(
                "استبدال ملف PDF (اختياري)",
                type=["pdf"]
            )

            save_changes = st.form_submit_button(
                "💾 حفظ التعديلات",
                type="primary",
                use_container_width=True
            )

            if save_changes:

                if not new_number.strip() or not new_party.strip() or not new_subject.strip():
                    st.error("يرجى استكمال جميع البيانات المطلوبة.")

                else:
                    old_file_path = row["file_path"]
                    updated_file_path = old_file_path

                    try:
                        if new_file is not None:
                            updated_file_path = save_uploaded_file(
                                new_file,
                                row["doc_type"]
                            )

                        conn = get_connection()

                        conn.execute("""
                            UPDATE documents
                            SET doc_number = ?,
                                doc_date = ?,
                                party = ?,
                                subject = ?,
                                file_path = ?
                            WHERE id = ?
                        """, (
                            new_number.strip(),
                            new_date.strftime("%Y-%m-%d"),
                            new_party.strip(),
                            new_subject.strip(),
                            updated_file_path,
                            doc_id
                        ))

                        conn.commit()
                        conn.close()

                        # حذف الملف القديم بعد نجاح تحديث قاعدة البيانات
                        if new_file is not None and old_file_path:
                            old_path = Path(old_file_path)

                            try:
                                if (
                                    old_path.exists()
                                    and ARCHIVE_DIR.resolve() in old_path.resolve().parents
                                ):
                                    old_path.unlink()
                            except OSError:
                                pass

                        st.success("تم تعديل المستند بنجاح.")

                        go_to("عرض السجلات")
                        st.rerun()

                    except Exception as e:
                        st.error(f"حدث خطأ أثناء التعديل: {e}")

    else:
        st.error("المستند غير موجود.")

    if st.button("⬅️ العودة للسجلات"):
        go_to("عرض السجلات")
        st.rerun()


# ==========================================
# تأكيد حذف مستند
# ==========================================

elif st.session_state.page == "تأكيد الحذف":

    doc_id = st.session_state.get("delete_id")

    st.markdown(
        '<div class="section-title">🗑️ حذف مستند</div>',
        unsafe_allow_html=True
    )

    st.warning(
        "هل أنت متأكد من حذف هذا المستند وملف PDF المرتبط به؟ "
        "لا يمكن التراجع عن هذه العملية."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "نعم، حذف المستند",
            type="primary"
        ):
            delete_document(doc_id)

            st.success("تم حذف المستند بنجاح.")

            go_to("عرض السجلات")
            st.rerun()

    with col2:
        if st.button("إلغاء"):
            go_to("عرض السجلات")
            st.rerun()


# ==========================================
# الفوتر
# ==========================================

st.markdown("""
<div class="footer">
✦ تصميم وتنفيذ أحمد الجنزوري ✦
</div>
""", unsafe_allow_html=True)
