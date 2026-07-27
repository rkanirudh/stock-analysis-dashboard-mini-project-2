"""
sector_analysis.py

Performs sector-wise analysis of Nifty 50 stocks.

Author : Anirudh R K
Project : Stock Analysis Dashboard
"""

import pandas as pd

from database.connection import get_engine
from utils.sector_mapping import SECTOR_MAPPING


def main():

    engine = get_engine()

    query = """
    SELECT
        ticker,
        close_price,
        volume
    FROM stock_data;
    """

    # Read data from MySQL
    df = pd.read_sql(query, engine)

    # ---------------------------------------------------
    # Clean ticker names
    # ---------------------------------------------------

    df["ticker"] = (
        df["ticker"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # ---------------------------------------------------
    # Map ticker to sector
    # ---------------------------------------------------

    df["sector"] = df["ticker"].map(SECTOR_MAPPING)

    # ---------------------------------------------------
    # Check for unmapped tickers
    # ---------------------------------------------------

    missing = df[df["sector"].isna()]["ticker"].unique()

    if len(missing) > 0:
        print("\nUnmapped Tickers:")
        print(missing)

    # ---------------------------------------------------
    # Remove rows without sector
    # ---------------------------------------------------

    df = df.dropna(subset=["sector"])

    # ---------------------------------------------------
    # Sector-wise aggregation
    # ---------------------------------------------------

    sector_summary = (
        df.groupby("sector")
        .agg(
            Companies=("ticker", "nunique"),
            Average_Close=("close_price", "mean"),
            Average_Volume=("volume", "mean"),
        )
        .round(2)
        .sort_values(
            by="Average_Close",
            ascending=False
        )
    )

    print("\n========== SECTOR ANALYSIS ==========\n")
    print(sector_summary)

    # ---------------------------------------------------
    # Save Report
    # ---------------------------------------------------

    sector_summary.to_csv(
        "reports/sector_analysis.csv"
    )

    print("\nSector analysis saved to reports/sector_analysis.csv")


if __name__ == "__main__":
    main()