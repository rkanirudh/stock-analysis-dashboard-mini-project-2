"""
moving_average.py

Calculates the 20-Day and 50-Day Moving Average
for every stock.

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

    # Calculate Moving Averages
    df["MA20"] = (
        df.groupby("ticker")["close_price"]
        .transform(
            lambda x: x.rolling(window=20).mean()
        )
    )

    df["MA50"] = (
        df.groupby("ticker")["close_price"]
        .transform(
            lambda x: x.rolling(window=50).mean()
        )
    )

    # Round values
    df["MA20"] = df["MA20"].round(2)
    df["MA50"] = df["MA50"].round(2)

    # Display first few calculated rows
    print("\n========== MOVING AVERAGE ANALYSIS ==========\n")

    print(
        df[
            [
                "ticker",
                "trade_date",
                "close_price",
                "MA20",
                "MA50",
            ]
        ].head(30)
    )

    # Save report
    df.to_csv(
        "reports/moving_average.csv",
        index=False
    )

    print(
        "\nMoving Average report saved to reports/moving_average.csv"
    )


if __name__ == "__main__":
    main()