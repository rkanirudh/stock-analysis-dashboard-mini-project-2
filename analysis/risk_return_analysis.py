import pandas as pd

from database.connection import get_engine


def load_data():

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

    return df
def calculate_daily_return(df):

    df["daily_return"] = (
        df.groupby("ticker")["close_price"]
        .pct_change()
    )

    return df
def calculate_yearly_return(df):

    yearly = (
        df.groupby("ticker")
        .agg(
            First_Close=("close_price", "first"),
            Last_Close=("close_price", "last")
        )
    )

    yearly["Yearly_Return"] = (
        (yearly["Last_Close"] - yearly["First_Close"])
        / yearly["First_Close"]
    ) * 100

    return yearly
def calculate_volatility(df):

    volatility = (
        df.groupby("ticker")["daily_return"]
        .std()
        * 100
    )

    volatility = volatility.rename("Volatility")

    return volatility
def prepare_report(yearly, volatility):

    report = yearly.join(volatility)

    report = report[
        ["Yearly_Return", "Volatility"]
    ]

    report = report.sort_values(
        by="Yearly_Return",
        ascending=False
    )

    return report.round(2)
def main():

    df = load_data()

    df = calculate_daily_return(df)

    yearly = calculate_yearly_return(df)

    volatility = calculate_volatility(df)

    report = prepare_report(yearly, volatility)

    print("\n========== RISK vs RETURN ==========\n")

    print(report)

    report.to_csv(
        "reports/risk_return_analysis.csv"
    )

    print(
        "\nRisk vs Return report saved to reports/risk_return_analysis.csv"
    )


if __name__ == "__main__":
    main()