import pandas as pd

from database.connection import get_engine


def main():

    engine = get_engine()

    query = """
    SELECT *
    FROM stock_data;
    """

    df = pd.read_sql(query, engine)

    print("\n========== MARKET SUMMARY ==========\n")

    print(f"Total Records           : {len(df)}")
    print(f"Total Companies         : {df['ticker'].nunique()}")

    print(
        f"Date Range              : "
        f"{df['trade_date'].min()}  to  {df['trade_date'].max()}"
    )

    print(f"Highest Stock Price     : {df['high_price'].max():,.2f}")
    print(f"Lowest Stock Price      : {df['low_price'].min():,.2f}")
    print(f"Average Closing Price   : {df['close_price'].mean():,.2f}")
    print(f"Average Trading Volume  : {df['volume'].mean():,.0f}")

    total_records = len(df)
    total_companies = df["ticker"].nunique()
    start_date = df["trade_date"].min()
    end_date = df["trade_date"].max()
    highest_price = df["high_price"].max()
    lowest_price = df["low_price"].min()
    avg_close = df["close_price"].mean()
    avg_volume = df["volume"].mean()

    summary = pd.DataFrame({
        "Metric": [
            "Total Records",
            "Total Companies",
            "Start Date",
            "End Date",
            "Highest Stock Price",
            "Lowest Stock Price",
            "Average Closing Price",
            "Average Trading Volume"
        ],
        "Value": [
            total_records,
            total_companies,
            start_date,
            end_date,
            highest_price,
            lowest_price,
            round(avg_close, 2),
            round(avg_volume, 2)
        ]
    })

    summary.to_csv(
        "reports/market_summary.csv",
        index=False
    )

    print("\nMarket Summary report saved to reports/market_summary.csv")


if __name__ == "__main__":
    main()