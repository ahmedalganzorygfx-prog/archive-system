import streamlit as st
import sqlite3
import os
import shutil
from datetime import datetime
import pandas as pd

# --- 1. إعدادات الصفحة والتصميم ---
st.set_page_config(
    page_title="المنظومة الرقمية للوارد والصادر - الأكاديمية المهنية للمعلمين فرع الجيزة",
    page_icon="📂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تطبيق تنسيق RTL والنمط البصري (CSS)
st.markdown("""
    
""", unsafe_allow_html=True)

# --- 2. إعداد مجلد الملفات وقاعدة البيانات المحليّة ---
ARCHIVE_FOLDER = "Archive_Files"
if not os.path.exists(ARCHIVE_FOLDER):
    os.makedirs(ARCHIVE_FOLDER)

def get_db_connection():
    conn = sqlite3.connect("archive_system.db", check_same_thread=False)
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_type TEXT NOT NULL,
            doc_number TEXT NOT NULL,
            doc_date TEXT NOT NULL,
            party TEXT NOT NULL,
            subject TEXT,
            file_path TEXT
        )
    ''')
    conn.commit()

init_db()

# --- 3. عرض الترويسة العلوية واللوجو بالمنتصف ---
col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
with col_l2:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=130)
    else:
        st.markdown("
