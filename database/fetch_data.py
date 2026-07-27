"""
fetch_data.py

Fetches stock market data from MySQL using SQLAlchemy.

Author: Anirudh R K
Project: Stock Analysis Dashboard
"""

import pandas as pd
from sqlalchemy import text

from database.connection import get_engine
from logger import get_logger


logger = get_logger(__name__)


def fetch_stock_data():
    """Fetch all stock records from MySQL."""

    engine = get_engine()

    query = text("""
        SELECT
            ticker,
            trade_date,
            open_price,
            high_price,
            low_price,
            close_price,
            volume
        FROM stock_data
        ORDER BY ticker, trade_date
    """)

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    logger.info(f"Fetched {len(df)} stock records.")

    return df


def fetch_market_summary():
    """Calculate overall market statistics using SQL."""

    engine = get_engine()

    query = text("""
        SELECT
            COUNT(*) AS total_records,
            COUNT(DISTINCT ticker) AS total_companies,
            MIN(trade_date) AS start_date,
            MAX(trade_date) AS end_date,
            MAX(high_price) AS highest_price,
            MIN(low_price) AS lowest_price,
            ROUND(AVG(close_price), 2) AS average_close,
            ROUND(AVG(volume), 2) AS average_volume
        FROM stock_data
    """)

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    logger.info("Market summary fetched successfully.")

    return df


def fetch_company_summary():
    """Calculate company-wise statistics using SQL."""

    engine = get_engine()

    query = text("""
        SELECT
            ticker,
            ROUND(AVG(close_price), 2) AS average_close,
            MAX(high_price) AS highest_price,
            MIN(low_price) AS lowest_price,
            ROUND(AVG(volume), 2) AS average_volume
        FROM stock_data
        GROUP BY ticker
        ORDER BY ticker
    """)

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    logger.info(
        f"Fetched company summary for {len(df)} companies."
    )

    return df


def main():

    print("\n========== SQL DATABASE TEST ==========\n")

    # Test 1 - Stock data
    stock_data = fetch_stock_data()

    print("First 5 records:")
    print(stock_data.head())

    print("\nTotal Records:", len(stock_data))

    # Test 2 - Market summary
    print("\n========== MARKET SUMMARY ==========\n")

    market_summary = fetch_market_summary()

    print(market_summary.to_string(index=False))

    # Test 3 - Company summary
    print("\n========== COMPANY SUMMARY ==========\n")

    company_summary = fetch_company_summary()

    print(company_summary.head(10).to_string(index=False))


if __name__ == "__main__":
    main()