"""
correlation.py

Calculates the correlation matrix between
all Nifty 50 stocks using closing prices.

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
        trade_date,
        ticker;
    """

    df = pd.read_sql(query, engine)

    pivot_df = df.pivot(
        index="trade_date",
        columns="ticker",
        values="close_price"
    )

    correlation_matrix = pivot_df.corr().round(2)

    print("\n========== CORRELATION MATRIX ==========\n")
    print(correlation_matrix)

    correlation_matrix.to_csv(
        "reports/correlation_matrix.csv"
    )

    print("\nCorrelation matrix saved to reports/correlation_matrix.csv")


if __name__ == "__main__":
    main()