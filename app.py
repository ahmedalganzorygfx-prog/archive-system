import streamlit as st
import sqlite3
import os
import shutil
from datetime import datetime
import pandas as pd

# =========================================================
# 1. إعدادات الصفحة والتصميم
# =========================================================
st.set_page_config(
    page_title="المنظومة الرقمية للوارد والصادر - الأكاديمية المهنية للمعلمين فرع الجيزة",
    page_icon="📂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 2. تنسيق RTL والنمط البصري
# =========================================================
st.markdown("""
<style>
    /* الصفحة بالكامل */
    .stApp {
        direction: rtl;
        text-align: right;
    }

    /* النصوص */
    body, p, div, label, span {
        font-family: Arial, Tahoma, sans-serif;
    }

    /* العناوين */
    h1, h2, h3, h4 {
        text-align: center;
        direction: rtl;
    }

    /* إخفاء بعض عناصر Streamlit الافتراضية */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* الحقول */
    input, textarea, select {
        direction: rtl !important;
        text-align: right !important;
    }

    /* الأزرار */
    .stButton button {
        direction: rtl;
        font-family: Arial, Tahoma, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. إعداد مجلد الملفات وقاعدة البيانات المحلية
# =========================================================
ARCHIVE_FOLDER = "Archive_Files"

if not os.path.exists(ARCHIVE_FOLDER):
    os.makedirs(ARCHIVE_FOLDER)


def get_db_connection():
    conn = sqlite3.connect(
        "archive_system.db",
        check_same_thread=False
    )
    return conn


# =========================================================
# 4. إنشاء قاعدة البيانات والجداول
# =========================================================
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
            file_path TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()

# =========================================================
# 5. الترويسة العلوية واللوجو
# =========================================================
col_l1, col_l2, col_l3 = st.columns([1, 2, 1])

with col_l2:

    if os.path.exists("logo.png"):
        st.image("logo.png", width=130)
    else:
        st.markdown(
            """
            <div style="
                text-align:center;
                font-size:70px;
                margin-bottom:10px;
            ">
                📂
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <h1 style="
            text-align:center;
            margin-top:0;
            margin-bottom:5px;
        ">
            المنظومة الرقمية للوارد والصادر
        </h1>

        <h3 style="
            text-align:center;
            margin-top:0;
        ">
            الأكاديمية المهنية للمعلمين – فرع الجيزة
        </h3>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# 6. رسالة اختبار للتأكد من تشغيل البرنامج
# =========================================================
st.success("تم تشغيل المنظومة بنجاح")

# =========================================================
# 7. اختبار قاعدة البيانات
# =========================================================
conn = get_db_connection()
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM documents")
documents_count = cursor.fetchone()[0]

conn.close()

st.info(f"عدد المستندات المسجلة حاليًا: {documents_count}")
