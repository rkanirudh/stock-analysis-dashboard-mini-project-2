"""
daily_return.py

Calculates the Daily Return (%) for every stock.

Author : Anirudh R K
Project : Stock Analysis Dashboard
"""

import pandas as pd

from database.connection import get_engine


def main():

    engine = get_engine()

    query = """
    SELECT
        ticker,
        trade_date,
        close_price
    FROM stock_data
    ORDER BY
        ticker,
        trade_date;
    """

    # Read data from MySQL
    df = pd.read_sql(query, engine)

    # Convert trade_date to datetime
    df["trade_date"] = pd.to_datetime(df["trade_date"])

    # ----------------------------------------------------
    # Calculate Daily Return (%)
    # ----------------------------------------------------

    df["Daily_Return (%)"] = (
        df.groupby("ticker")["close_price"]
        .pct_change()
        * 100
    )

    # Round values
    df["Daily_Return (%)"] = (
        df["Daily_Return (%)"]
        .round(2)
    )

    # ----------------------------------------------------
    # Display Result
    # ----------------------------------------------------

    print("\n========== DAILY RETURN ANALYSIS ==========\n")

    print(
        df[
            [
                "ticker",
                "trade_date",
                "close_price",
                "Daily_Return (%)",
            ]
        ].head(30)
    )

    # ----------------------------------------------------
    # Save Report
    # ----------------------------------------------------

    df.to_csv(
        "reports/daily_return.csv",
        index=False
    )

    print(
        "\nDaily Return report saved to reports/daily_return.csv"
    )


if __name__ == "__main__":
    main()