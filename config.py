"""
config.py

Central configuration file for the Stock Analysis Dashboard project.

This module stores all project paths and reusable constants.
"""

from pathlib import Path

# ==========================================================
# PROJECT ROOT
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent


# ==========================================================
# DATA DIRECTORIES
# ==========================================================

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

EXTRACTED_CSV_DIR = DATA_DIR / "extracted_csv"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

SECTOR_FILE = DATA_DIR / "sector.csv"


# ==========================================================
# DATABASE
# ==========================================================

DATABASE_NAME = "stock_analysis"


# ==========================================================
# LOG DIRECTORY
# ==========================================================

LOG_DIR = PROJECT_ROOT / "logs"

LOG_FILE = LOG_DIR / "stock_analysis.log"


# ==========================================================
# STREAMLIT
# ==========================================================

STREAMLIT_DIR = PROJECT_ROOT / "streamlit_app"


# ==========================================================
# REPORTS
# ==========================================================

REPORTS_DIR = PROJECT_ROOT / "reports"

SCREENSHOT_DIR = PROJECT_ROOT / "screenshots"


# ==========================================================
# CREATE IMPORTANT DIRECTORIES
# ==========================================================

EXTRACTED_CSV_DIR.mkdir(parents=True, exist_ok=True)

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

LOG_DIR.mkdir(parents=True, exist_ok=True)

# =====================================================
# Database Configuration
# =====================================================

DB_USERNAME = "root"
DB_PASSWORD = "rkas@2005"
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_NAME = "stock_analysis"