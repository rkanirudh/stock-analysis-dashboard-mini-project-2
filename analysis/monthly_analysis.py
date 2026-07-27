"""
monthly_analysis.py

Calculates month-wise stock statistics.

Author : Anirudh R K
Project : Stock Analysis Dashboard
"""

import pandas as pd

from database.connection import get_engine


def main():

    engine = get_engine()

    query = """
    SELECT
        MONTH(trade_date) AS month_number,
        MONTHNAME(trade_date) AS month_name,
        AVG(close_price) AS average_close_price,
        AVG(volume) AS average_volume
    FROM stock_data
    GROUP BY
        MONTH(trade_date),
        MONTHNAME(trade_date)
    ORDER BY
        MONTH(trade_date);
    """

    df = pd.read_sql(query, engine)

    # Round values
    df["average_close_price"] = (
        df["average_close_price"]
        .round(2)
    )

    df["average_volume"] = (
        df["average_volume"]
        .round(0)
        .astype(int)
    )

    print("\n========== MONTHLY ANALYSIS ==========\n")
    print(df)

    # Save Report
    df.to_csv(
        "reports/monthly_analysis.csv",
        index=False
    )

    print(
        "\nMonthly Analysis report saved to reports/monthly_analysis.csv"
    )


if __name__ == "__main__":
    main()