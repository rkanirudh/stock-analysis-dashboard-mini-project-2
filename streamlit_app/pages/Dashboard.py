"""
Dashboard.py

Interactive market overview dashboard for Nifty 50 stocks.

Data Source:
MySQL stock_data table through SQLAlchemy.

Author  : Anirudh R K
Project : Stock Analysis Dashboard
"""

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------
# PROJECT ROOT
# ---------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# ---------------------------------------------------
# DATABASE IMPORT
# ---------------------------------------------------

from database.fetch_data import fetch_stock_data


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Market Dashboard",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------

st.title("📊 Nifty 50 Market Dashboard")

st.write(
    "Interactive overview of Nifty 50 stock performance, "
    "trading activity, returns, and market trends."
)

st.markdown("---")


# ---------------------------------------------------
# LOAD DATA FROM MYSQL
# ---------------------------------------------------

@st.cache_data
def load_stock_data():

    df = fetch_stock_data()

    df["trade_date"] = pd.to_datetime(
        df["trade_date"],
        errors="coerce"
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
            errors="coerce"
        )

    df = df.dropna(
        subset=[
            "ticker",
            "trade_date",
            "close_price"
        ]
    )

    return df.sort_values(
        ["ticker", "trade_date"]
    ).reset_index(drop=True)


try:

    stock_data = load_stock_data()

except Exception as error:

    st.error(
        "Unable to load stock market data from MySQL."
    )

    st.exception(error)

    st.stop()


# ---------------------------------------------------
# DATA VALIDATION
# ---------------------------------------------------

if stock_data.empty:

    st.warning(
        "The stock_data table does not contain any records."
    )

    st.stop()


# ---------------------------------------------------
# GLOBAL INFORMATION
# ---------------------------------------------------

stocks = sorted(
    stock_data["ticker"]
    .dropna()
    .unique()
    .tolist()
)

minimum_date = stock_data[
    "trade_date"
].min().date()

maximum_date = stock_data[
    "trade_date"
].max().date()


# ---------------------------------------------------
# FILTERS
# ---------------------------------------------------

st.subheader("🎛️ Market Filters")

filter_col1, filter_col2 = st.columns(
    [2, 1]
)


with filter_col1:

    selected_stocks = st.multiselect(
        "Select Stocks",
        options=stocks,
        default=stocks
    )


with filter_col2:

    selected_dates = st.date_input(
        "Trading Period",
        value=(
            minimum_date,
            maximum_date
        ),
        min_value=minimum_date,
        max_value=maximum_date
    )


# ---------------------------------------------------
# VALIDATE FILTERS
# ---------------------------------------------------

if not selected_stocks:

    st.warning(
        "Select at least one stock to continue."
    )

    st.stop()


if isinstance(selected_dates, tuple):

    if len(selected_dates) == 2:

        start_date = pd.Timestamp(
            selected_dates[0]
        )

        end_date = pd.Timestamp(
            selected_dates[1]
        )

    else:

        start_date = pd.Timestamp(
            selected_dates[0]
        )

        end_date = pd.Timestamp(
            selected_dates[0]
        )

else:

    start_date = pd.Timestamp(
        selected_dates
    )

    end_date = pd.Timestamp(
        selected_dates
    )


# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------

filtered_data = stock_data[
    (
        stock_data["ticker"]
        .isin(selected_stocks)
    )
    &
    (
        stock_data["trade_date"]
        >= start_date
    )
    &
    (
        stock_data["trade_date"]
        <= end_date
    )
].copy()


if filtered_data.empty:

    st.warning(
        "No stock records are available for the selected filters."
    )

    st.stop()


st.caption(
    f"Showing {len(filtered_data):,} records "
    f"from {start_date.date()} to {end_date.date()}."
)

st.markdown("---")


# ---------------------------------------------------
# CALCULATE STOCK RETURNS
# ---------------------------------------------------

performance = (
    filtered_data
    .sort_values(
        ["ticker", "trade_date"]
    )
    .groupby("ticker")
    .agg(
        start_price=(
            "close_price",
            "first"
        ),
        end_price=(
            "close_price",
            "last"
        ),
        highest_price=(
            "high_price",
            "max"
        ),
        lowest_price=(
            "low_price",
            "min"
        ),
        average_close=(
            "close_price",
            "mean"
        ),
        average_volume=(
            "volume",
            "mean"
        ),
        total_volume=(
            "volume",
            "sum"
        ),
        records=(
            "close_price",
            "count"
        )
    )
    .reset_index()
)


performance["return_percent"] = (
    (
        performance["end_price"]
        - performance["start_price"]
    )
    /
    performance["start_price"]
    * 100
)


performance["return_percent"] = (
    performance["return_percent"]
    .replace(
        [float("inf"), float("-inf")],
        pd.NA
    )
)


# ---------------------------------------------------
# MARKET KPIs
# ---------------------------------------------------

st.subheader("📌 Market Overview")


total_companies = (
    filtered_data["ticker"]
    .nunique()
)

total_records = len(
    filtered_data
)

highest_price = (
    filtered_data["high_price"]
    .max()
)

lowest_price = (
    filtered_data["low_price"]
    .min()
)

average_close = (
    filtered_data["close_price"]
    .mean()
)

average_volume = (
    filtered_data["volume"]
    .mean()
)

top_return = (
    performance["return_percent"]
    .max()
)

lowest_return = (
    performance["return_percent"]
    .min()
)


k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Companies",
    f"{total_companies:,}"
)

k2.metric(
    "Stock Records",
    f"{total_records:,}"
)

k3.metric(
    "Highest Price",
    f"{highest_price:,.2f}"
)

k4.metric(
    "Lowest Price",
    f"{lowest_price:,.2f}"
)


k5, k6, k7, k8 = st.columns(4)

k5.metric(
    "Average Close",
    f"{average_close:,.2f}"
)

k6.metric(
    "Average Volume",
    f"{average_volume:,.0f}"
)

k7.metric(
    "Best Return",
    f"{top_return:.2f}%"
)

k8.metric(
    "Lowest Return",
    f"{lowest_return:.2f}%"
)


st.markdown("---")


# ---------------------------------------------------
# MARKET PERFORMANCE
# ---------------------------------------------------

st.subheader("🏆 Market Performance")


valid_performance = (
    performance
    .dropna(
        subset=["return_percent"]
    )
    .sort_values(
        "return_percent",
        ascending=False
    )
)


left, right = st.columns(2)


# ---------------------------------------------------
# TOP GAINERS
# ---------------------------------------------------

with left:

    st.markdown(
        "### 📈 Top 10 Performing Stocks"
    )

    top_gainers = (
        valid_performance
        .head(10)
        .sort_values(
            "return_percent"
        )
    )

    fig_gainers = px.bar(
        top_gainers,
        x="return_percent",
        y="ticker",
        orientation="h",
        labels={
            "ticker": "Stock",
            "return_percent": "Return (%)"
        },
        title="Top 10 Stocks by Return"
    )

    fig_gainers.update_layout(
        yaxis_title="Stock",
        xaxis_title="Return (%)",
        height=500
    )

    st.plotly_chart(
        fig_gainers,
        width="stretch"
    )


# ---------------------------------------------------
# LOWEST PERFORMERS
# ---------------------------------------------------

with right:

    st.markdown(
        "### 📉 Lowest 10 Performing Stocks"
    )

    lowest_performers = (
        valid_performance
        .tail(10)
        .sort_values(
            "return_percent"
        )
    )

    fig_losers = px.bar(
        lowest_performers,
        x="return_percent",
        y="ticker",
        orientation="h",
        labels={
            "ticker": "Stock",
            "return_percent": "Return (%)"
        },
        title="Lowest 10 Stocks by Return"
    )

    fig_losers.update_layout(
        yaxis_title="Stock",
        xaxis_title="Return (%)",
        height=500
    )

    st.plotly_chart(
        fig_losers,
        width="stretch"
    )


st.markdown("---")


# ---------------------------------------------------
# MARKET INDEX TREND
# ---------------------------------------------------

st.subheader("📈 Overall Market Trend")

st.caption(
    "The chart represents the average closing price "
    "of the selected stocks for each trading day."
)


market_trend = (
    filtered_data
    .groupby(
        "trade_date",
        as_index=False
    )
    .agg(
        average_close=(
            "close_price",
            "mean"
        )
    )
)


fig_market = px.line(
    market_trend,
    x="trade_date",
    y="average_close",
    labels={
        "trade_date": "Trading Date",
        "average_close": "Average Closing Price"
    },
    title="Average Market Closing Price"
)


fig_market.update_layout(
    height=500
)


st.plotly_chart(
    fig_market,
    width="stretch"
)


st.markdown("---")


# ---------------------------------------------------
# TRADING VOLUME
# ---------------------------------------------------

st.subheader("💰 Trading Activity")


volume_summary = (
    filtered_data
    .groupby(
        "ticker",
        as_index=False
    )
    .agg(
        total_volume=(
            "volume",
            "sum"
        )
    )
    .sort_values(
        "total_volume",
        ascending=False
    )
    .head(15)
)


fig_volume = px.bar(
    volume_summary,
    x="ticker",
    y="total_volume",
    labels={
        "ticker": "Stock",
        "total_volume": "Total Trading Volume"
    },
    title="Top 15 Stocks by Trading Volume"
)


fig_volume.update_layout(
    height=500,
    xaxis_tickangle=-45
)


st.plotly_chart(
    fig_volume,
    width="stretch"
)


st.markdown("---")


# ---------------------------------------------------
# RETURN DISTRIBUTION
# ---------------------------------------------------

st.subheader("📊 Stock Return Distribution")


fig_distribution = px.histogram(
    valid_performance,
    x="return_percent",
    nbins=20,
    labels={
        "return_percent": "Return (%)"
    },
    title="Distribution of Stock Returns"
)


fig_distribution.update_layout(
    xaxis_title="Return (%)",
    yaxis_title="Number of Stocks",
    height=450
)


st.plotly_chart(
    fig_distribution,
    width="stretch"
)


st.markdown("---")


# ---------------------------------------------------
# PRICE VS VOLUME
# ---------------------------------------------------

st.subheader("🔬 Price vs Trading Volume")


fig_scatter = px.scatter(
    performance,
    x="average_volume",
    y="average_close",
    hover_name="ticker",
    size="records",
    labels={
        "average_volume": "Average Trading Volume",
        "average_close": "Average Closing Price",
        "records": "Trading Records"
    },
    title="Average Price vs Average Trading Volume"
)


fig_scatter.update_layout(
    height=550
)


st.plotly_chart(
    fig_scatter,
    width="stretch"
)


st.markdown("---")


# ---------------------------------------------------
# STOCK PERFORMANCE TABLE
# ---------------------------------------------------

st.subheader("📋 Stock Performance Summary")


performance_table = performance[
    [
        "ticker",
        "start_price",
        "end_price",
        "highest_price",
        "lowest_price",
        "average_close",
        "average_volume",
        "return_percent"
    ]
].copy()


performance_table.columns = [
    "Stock",
    "Start Price",
    "End Price",
    "Highest Price",
    "Lowest Price",
    "Average Close",
    "Average Volume",
    "Return (%)"
]


numeric_round_columns = [
    "Start Price",
    "End Price",
    "Highest Price",
    "Lowest Price",
    "Average Close",
    "Average Volume",
    "Return (%)"
]


performance_table[
    numeric_round_columns
] = performance_table[
    numeric_round_columns
].round(2)


performance_table = (
    performance_table
    .sort_values(
        "Return (%)",
        ascending=False
    )
)


st.dataframe(
    performance_table,
    width="stretch",
    hide_index=True
)


# ---------------------------------------------------
# DOWNLOAD
# ---------------------------------------------------

csv_data = performance_table.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇️ Download Performance Report",
    data=csv_data,
    file_name="nifty50_performance_report.csv",
    mime="text/csv"
)


st.markdown("---")


# ---------------------------------------------------
# DATA EXPLORER
# ---------------------------------------------------

with st.expander(
    "🔎 Explore Filtered Stock Records"
):

    display_data = (
        filtered_data[
            [
                "ticker",
                "trade_date",
                "open_price",
                "high_price",
                "low_price",
                "close_price",
                "volume"
            ]
        ]
        .sort_values(
            ["trade_date", "ticker"],
            ascending=[
                False,
                True
            ]
        )
    )


    st.dataframe(
        display_data,
        width="stretch",
        hide_index=True
    )


# ---------------------------------------------------
# DASHBOARD INFORMATION
# ---------------------------------------------------

with st.expander(
    "ℹ️ Dashboard Information"
):

    st.markdown(
        """
        **Data Source:** MySQL `stock_data` table

        **Dashboard calculations:**

        - Stock return = percentage change between the first and
          last closing price in the selected period.
        - Market trend = average closing price across selected stocks.
        - Trading activity = total traded volume by company.
        - Highest and lowest prices use daily high and low values.
        - All calculations respond dynamically to the selected
          stocks and trading period.

        **Technology Stack**

        Python • Pandas • MySQL • SQLAlchemy • Plotly • Streamlit
        """
    )


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Nifty 50 Stock Analysis Dashboard | "
    "MySQL • SQLAlchemy • Pandas • Plotly • Streamlit"
)