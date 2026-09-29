import streamlit as st
import sqlite3
import base64
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

LOGO_PATH = BASE_DIR / "logo.png"

INCOMING_DIR.mkdir(parents=True, exist_ok=True)
OUTGOING_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# إعدادات النظام
# ============================================================

APP_PASSWORD = "1234"


# ============================================================
# دالة تحويل الصورة إلى Base64
# ============================================================

def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception:
        return None


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    
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


# ============================================================
# شاشة تسجيل الدخول
# ============================================================

if not st.session_state.authenticated:

    logo_base64 = None

    if LOGO_PATH.exists():
        logo_base64 = get_image_base64(LOGO_PATH)

    st.markdown(
        '
