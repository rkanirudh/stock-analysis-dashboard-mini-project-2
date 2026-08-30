"""
fetch_data.py

Loads stock market data from the local processed CSV file.

Project:
    Data-Driven Stock Analysis Dashboard

Data source:
    data/processed/cleaned_stock.csv

MySQL is NOT required for the Streamlit dashboard.
"""

from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT PATH
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[1]

DATA_FILE = ROOT_DIR / "data" / "processed" / "cleaned_stock.csv"


# ============================================================
# LOAD STOCK DATA
# ============================================================

def fetch_stock_data():
    """
    Load all stock records from cleaned_stock.csv.

    Returns
    -------
    pandas.DataFrame
        Stock data with standardized column names.
    """

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Stock data file not found:\n{DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    # --------------------------------------------------------
    # Rename columns to match the Streamlit application
    # --------------------------------------------------------

    df = df.rename(
        columns={
            "Ticker": "ticker",
            "close": "close_price",
            "date": "trade_date",
            "high": "high_price",
            "low": "low_price",
            "open": "open_price",
            "volume": "volume",
        }
    )

    # --------------------------------------------------------
    # Validate required columns
    # --------------------------------------------------------

    required_columns = [
        "ticker",
        "trade_date",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # --------------------------------------------------------
    # Convert data types
    # --------------------------------------------------------

    df["trade_date"] = pd.to_datetime(
        df["trade_date"],
        errors="coerce",
    )

    numeric_columns = [
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # --------------------------------------------------------
    # Remove invalid records
    # --------------------------------------------------------

    df = df.dropna(
        subset=[
            "ticker",
            "trade_date",
            "close_price",
        ]
    )

    # --------------------------------------------------------
    # Sort data
    # --------------------------------------------------------

    df = df.sort_values(
        ["ticker", "trade_date"]
    ).reset_index(drop=True)

    return df


# ============================================================
# MARKET SUMMARY
# ============================================================

def fetch_market_summary():
    """
    Calculate overall market statistics.

    Returns
    -------
    pandas.DataFrame
        One-row market summary.
    """

    df = fetch_stock_data()

    summary = pd.DataFrame(
        [
            {
                "total_records": len(df),

                "total_companies": df[
                    "ticker"
                ].nunique(),

                "start_date": df[
                    "trade_date"
                ].min(),

                "end_date": df[
                    "trade_date"
                ].max(),

                "highest_price": df[
                    "high_price"
                ].max(),

                "lowest_price": df[
                    "low_price"
                ].min(),

                "average_close": round(
                    df[
                        "close_price"
                    ].mean(),
                    2,
                ),

                "average_volume": round(
                    df[
                        "volume"
                    ].mean(),
                    2,
                ),
            }
        ]
    )

    return summary


# ============================================================
# COMPANY SUMMARY
# ============================================================

def fetch_company_summary():
    """
    Calculate company-wise stock statistics.

    Returns
    -------
    pandas.DataFrame
        Company-level summary for all tickers.
    """

    df = fetch_stock_data()

    summary = (
        df.groupby("ticker")
        .agg(
            average_close=(
                "close_price",
                "mean",
            ),

            highest_price=(
                "high_price",
                "max",
            ),

            lowest_price=(
                "low_price",
                "min",
            ),

            average_volume=(
                "volume",
                "mean",
            ),
        )
        .reset_index()
    )

    # Round numerical values

    summary["average_close"] = (
        summary["average_close"]
        .round(2)
    )

    summary["highest_price"] = (
        summary["highest_price"]
        .round(2)
    )

    summary["lowest_price"] = (
        summary["lowest_price"]
        .round(2)
    )

    summary["average_volume"] = (
        summary["average_volume"]
        .round(2)
    )

    return (
        summary
        .sort_values("ticker")
        .reset_index(drop=True)
    )


# ============================================================
# TEST
# ============================================================

def main():

    print()
    print("=" * 60)
    print("CSV STOCK DATA TEST")
    print("=" * 60)

    # --------------------------------------------------------
    # Test stock data
    # --------------------------------------------------------

    stock_data = fetch_stock_data()

    print("\nStock Data:")
    print(stock_data.head())

    print(
        "\nTotal Records:",
        len(stock_data),
    )

    print(
        "Total Companies:",
        stock_data["ticker"].nunique(),
    )

    print(
        "Date Range:",
        stock_data["trade_date"].min(),
        "to",
        stock_data["trade_date"].max(),
    )

    # --------------------------------------------------------
    # Test market summary
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("MARKET SUMMARY")
    print("=" * 60)

    market_summary = fetch_market_summary()

    print(
        market_summary.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # Test company summary
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("COMPANY SUMMARY")
    print("=" * 60)

    company_summary = fetch_company_summary()

    print(
        company_summary.head(10).to_string(
            index=False
        )
    )

    print(
        "\nTotal Companies in Summary:",
        len(company_summary),
    )

    print()
    print("=" * 60)
    print("TEST COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print()


# ============================================================
# RUN TEST
# ============================================================

if __name__ == "__main__":
    main()