"""
insert_data.py

Loads cleaned_stock.csv into MySQL stock_data table.

Author: Anirudh R K
"""

import pandas as pd

from database.connection import get_engine
from config import PROCESSED_DATA_DIR
from logger import get_logger


logger = get_logger(__name__)


def load_csv():
    csv_path = PROCESSED_DATA_DIR / "cleaned_stock.csv"

    df = pd.read_csv(csv_path)

    logger.info(f"Loaded {len(df)} rows.")

    return df


def prepare_dataframe(df):

    df = df.rename(
        columns={
            "Ticker": "ticker",
            "date": "trade_date",
            "open": "open_price",
            "high": "high_price",
            "low": "low_price",
            "close": "close_price",
        }
    )

    if "month" in df.columns:
        df = df.drop(columns=["month"])

    df["trade_date"] = pd.to_datetime(df["trade_date"])

    return df


def insert_into_mysql(df):

    engine = get_engine()

    df.to_sql(
        name="stock_data",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000,
    )

    logger.info(f"{len(df)} rows inserted successfully.")


def main():

    logger.info("=" * 60)
    logger.info("Starting Data Insertion")
    logger.info("=" * 60)

    df = load_csv()
    df = prepare_dataframe(df)

    insert_into_mysql(df)

    logger.info("=" * 60)
    logger.info("Data Insertion Completed")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()