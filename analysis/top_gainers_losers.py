"""
top_gainers_losers.py

Finds the Top 10 Gainers and Top 10 Losers
based on yearly stock returns.

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
    ORDER BY ticker, trade_date;
    """

    df = pd.read_sql(query, engine)

    # First closing price
    first_close = (
        df.groupby("ticker")["close_price"]
        .first()
    )

    # Last closing price
    last_close = (
        df.groupby("ticker")["close_price"]
        .last()
    )

    yearly_return = (
        (last_close - first_close)
        / first_close
    ) * 100

    yearly_return = yearly_return.round(2)

    result = yearly_return.reset_index()

    result.columns = [
        "Ticker",
        "Yearly_Return"
    ]

    gainers = (
        result.sort_values(
            by="Yearly_Return",
            ascending=False
        )
        .head(10)
    )

    losers = (
        result.sort_values(
            by="Yearly_Return",
            ascending=True
        )
        .head(10)
    )

    print("\n========== TOP 10 GAINERS ==========\n")
    print(gainers.to_string(index=False))

    print("\n========== TOP 10 LOSERS ==========\n")
    print(losers.to_string(index=False))

    gainers.to_csv(
        "reports/top_gainers.csv",
        index=False
    )

    losers.to_csv(
        "reports/top_losers.csv",
        index=False
    )

    print("\nReports saved to reports/top_gainers.csv")
    print("Reports saved to reports/top_losers.csv")


if __name__ == "__main__":
    main()