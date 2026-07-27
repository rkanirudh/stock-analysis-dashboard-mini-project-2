"""
volatility.py

Calculates stock volatility using
the standard deviation of daily returns.

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

    df = pd.read_sql(query, engine)

    # Daily Return
    df["daily_return"] = (
        df.groupby("ticker")["close_price"]
          .pct_change()
    )

    # Volatility
    volatility = (
        df.groupby("ticker")["daily_return"]
          .std()
          .reset_index()
    )

    volatility.rename(
        columns={
            "daily_return": "volatility"
        },
        inplace=True
    )

    volatility["volatility"] = (
        volatility["volatility"]
        .round(4)
    )

    volatility = volatility.sort_values(
        by="volatility",
        ascending=False
    )

    print("\n========== VOLATILITY ANALYSIS ==========\n")
    print(volatility)

    volatility.to_csv(
        "reports/volatility.csv"
    )

    print("\nVolatility analysis saved to reports/volatility .csv")



if __name__ == "__main__":
    main()