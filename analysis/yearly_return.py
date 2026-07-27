"""
yearly_return.py

Calculates yearly return for each stock.

Author : Anirudh R K
Project : Stock Analysis Dashboard
"""

import pandas as pd

from database.connection import get_engine


def main():

    engine = get_engine()

    query = """
    SELECT *
    FROM stock_data
    ORDER BY ticker, trade_date;
    """

    df = pd.read_sql(query, engine)

    grouped = df.groupby("ticker")

    first_close = grouped["close_price"].first()
    last_close = grouped["close_price"].last()

    returns = pd.DataFrame({
        "First Close": first_close,
        "Last Close": last_close
    })

    returns["Yearly Return (%)"] = (
        (
            returns["Last Close"]
            - returns["First Close"]
        )
        / returns["First Close"]
    ) * 100

    returns = returns.round(2)

    returns = returns.sort_values(
        by="Yearly Return (%)",
        ascending=False
    )

    print("\n========== YEARLY RETURN ==========\n")
    print(returns.head(10))

    # Save Report
    returns.to_csv(
        "reports/yearly_return.csv",
        index=True
    )

    print("\nYearly Return report saved to reports/yearly_return.csv")


if __name__ == "__main__":
    main()