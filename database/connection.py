"""
connection.py

Creates and returns a reusable SQLAlchemy engine
for the Stock Analysis Dashboard MySQL database.

Author : Anirudh R K
Project : Stock Analysis Dashboard
"""

from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from config import (
    DB_USERNAME,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME,
)

from logger import get_logger


# ---------------------------------------------------------
# Logger
# ---------------------------------------------------------

logger = get_logger(__name__)


# ---------------------------------------------------------
# Database URL
# ---------------------------------------------------------

# Encode password safely in case it contains special
# characters such as @, #, %, &, etc.
encoded_password = quote_plus(DB_PASSWORD)

DATABASE_URL = (
    f"mysql+pymysql://{DB_USERNAME}:{encoded_password}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# ---------------------------------------------------------
# Create Database Engine
# ---------------------------------------------------------

def get_engine() -> Engine:
    """
    Create and return a reusable SQLAlchemy engine.

    Returns:
        Engine: SQLAlchemy database engine.
    """

    try:
        engine = create_engine(
            DATABASE_URL,
            echo=False,
            future=True,
            pool_pre_ping=True,
        )

        logger.info("Database engine created successfully.")

        return engine

    except Exception as error:
        logger.error(
            f"Failed to create database engine: {error}"
        )
        raise