"""
Stock_Analysis.py

Individual Nifty 50 Stock Analysis Dashboard.

Project : Stock Analysis Dashboard
Author  : Anirudh R K
"""

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PROJECT ROOT
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# ============================================================
# DATABASE IMPORT
# ============================================================

from database.fetch_data import fetch_stock_data


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Stock Analysis",
    page_icon="🔎",
    layout="wide",
)


# ============================================================
# HEADER
# ============================================================

st.title("🔎 Individual Stock Analysis")

st.write(
    "Explore historical price movement, trading volume, returns, "
    "moving averages, volatility and risk for individual Nifty 50 stocks."
)

st.markdown("---")


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(ttl=600)
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
        subset=["ticker", "trade_date", "close_price"]
    )

    return df


try:

    stock_data = load_stock_data()

except Exception as error:

    st.error("Unable to load stock market data from MySQL.")

    st.exception(error)

    st.stop()


# ============================================================
# STOCK SELECTOR
# ============================================================

stocks = sorted(
    stock_data["ticker"]
    .dropna()
    .unique()
    .tolist()
)


st.subheader("🎯 Select Stock")

selected_stock = st.selectbox(
    "Choose a Nifty 50 Stock",
    stocks,
)


# ============================================================
# FILTER STOCK
# ============================================================

stock = (
    stock_data[
        stock_data["ticker"] == selected_stock
    ]
    .copy()
    .sort_values("trade_date")
)


if stock.empty:

    st.warning("No data available for the selected stock.")

    st.stop()


# ============================================================
# DATE FILTER
# ============================================================

min_date = stock["trade_date"].min().date()
max_date = stock["trade_date"].max().date()


date_range = st.date_input(
    "Select Analysis Period",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)


if len(date_range) == 2:

    start_date, end_date = date_range

    stock = stock[
        (
            stock["trade_date"].dt.date >= start_date
        )
        &
        (
            stock["trade_date"].dt.date <= end_date
        )
    ].copy()


if stock.empty:

    st.warning(
        "No stock records are available for the selected date range."
    )

    st.stop()


# ============================================================
# CALCULATIONS
# ============================================================

stock["daily_return"] = (
    stock["close_price"]
    .pct_change(fill_method=None)
    * 100
)


stock["MA_20"] = (
    stock["close_price"]
    .rolling(20)
    .mean()
)


stock["MA_50"] = (
    stock["close_price"]
    .rolling(50)
    .mean()
)


stock["MA_100"] = (
    stock["close_price"]
    .rolling(100)
    .mean()
)


stock["cumulative_max"] = (
    stock["close_price"]
    .cummax()
)


stock["drawdown"] = (
    (
        stock["close_price"]
        / stock["cumulative_max"]
    )
    - 1
) * 100


# ============================================================
# KPI CALCULATIONS
# ============================================================

latest_close = stock["close_price"].iloc[-1]

first_close = stock["close_price"].iloc[0]

highest_price = stock["high_price"].max()

lowest_price = stock["low_price"].min()

average_close = stock["close_price"].mean()

average_volume = stock["volume"].mean()


period_return = (
    (
        latest_close
        / first_close
    )
    - 1
) * 100


daily_volatility = (
    stock["daily_return"]
    .std()
)


max_drawdown = (
    stock["drawdown"]
    .min()
)


# ============================================================
# STOCK OVERVIEW
# ============================================================

st.markdown("---")

st.subheader(f"📊 {selected_stock} Market Overview")


c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "Latest Close",
    f"₹{latest_close:,.2f}"
)


c2.metric(
    "Period Return",
    f"{period_return:.2f}%"
)


c3.metric(
    "Highest Price",
    f"₹{highest_price:,.2f}"
)


c4.metric(
    "Lowest Price",
    f"₹{lowest_price:,.2f}"
)


c5, c6, c7, c8 = st.columns(4)


c5.metric(
    "Average Close",
    f"₹{average_close:,.2f}"
)


c6.metric(
    "Average Volume",
    f"{average_volume:,.0f}"
)


c7.metric(
    "Daily Volatility",
    (
        f"{daily_volatility:.2f}%"
        if pd.notna(daily_volatility)
        else "N/A"
    )
)


c8.metric(
    "Maximum Drawdown",
    (
        f"{max_drawdown:.2f}%"
        if pd.notna(max_drawdown)
        else "N/A"
    )
)


# ============================================================
# PRICE TREND
# ============================================================

st.markdown("---")

st.subheader("📈 Closing Price Trend")


fig_price = px.line(
    stock,
    x="trade_date",
    y="close_price",
    title=f"{selected_stock} Closing Price",
)


fig_price.update_layout(
    xaxis_title="Trading Date",
    yaxis_title="Closing Price (₹)",
    hovermode="x unified",
)


st.plotly_chart(
    fig_price,
    width="stretch",
)


# ============================================================
# CANDLESTICK CHART
# ============================================================

st.markdown("---")

st.subheader("🕯️ Candlestick Analysis")


fig_candle = go.Figure(
    data=[
        go.Candlestick(
            x=stock["trade_date"],
            open=stock["open_price"],
            high=stock["high_price"],
            low=stock["low_price"],
            close=stock["close_price"],
            name=selected_stock,
        )
    ]
)


fig_candle.update_layout(
    title=f"{selected_stock} OHLC Candlestick Chart",
    xaxis_title="Trading Date",
    yaxis_title="Stock Price (₹)",
    xaxis_rangeslider_visible=False,
    height=600,
)


st.plotly_chart(
    fig_candle,
    width="stretch",
)


# ============================================================
# MOVING AVERAGE ANALYSIS
# ============================================================

st.markdown("---")

st.subheader("📉 Moving Average Analysis")


fig_ma = go.Figure()


fig_ma.add_trace(
    go.Scatter(
        x=stock["trade_date"],
        y=stock["close_price"],
        mode="lines",
        name="Closing Price",
    )
)


fig_ma.add_trace(
    go.Scatter(
        x=stock["trade_date"],
        y=stock["MA_20"],
        mode="lines",
        name="20-Day MA",
    )
)


fig_ma.add_trace(
    go.Scatter(
        x=stock["trade_date"],
        y=stock["MA_50"],
        mode="lines",
        name="50-Day MA",
    )
)


fig_ma.add_trace(
    go.Scatter(
        x=stock["trade_date"],
        y=stock["MA_100"],
        mode="lines",
        name="100-Day MA",
    )
)


fig_ma.update_layout(
    title=f"{selected_stock} Moving Average Trend",
    xaxis_title="Trading Date",
    yaxis_title="Stock Price (₹)",
    hovermode="x unified",
)


st.plotly_chart(
    fig_ma,
    width="stretch",
)


# ============================================================
# TRADING VOLUME
# ============================================================

st.markdown("---")

st.subheader("📊 Trading Volume")


fig_volume = px.bar(
    stock,
    x="trade_date",
    y="volume",
    title=f"{selected_stock} Daily Trading Volume",
)


fig_volume.update_layout(
    xaxis_title="Trading Date",
    yaxis_title="Volume",
)


st.plotly_chart(
    fig_volume,
    width="stretch",
)


# ============================================================
# DAILY RETURN ANALYSIS
# ============================================================

st.markdown("---")

st.subheader("💹 Daily Return Analysis")


return_data = stock.dropna(
    subset=["daily_return"]
)


if not return_data.empty:

    fig_return = px.bar(
        return_data,
        x="trade_date",
        y="daily_return",
        title=f"{selected_stock} Daily Percentage Return",
    )


    fig_return.add_hline(
        y=0,
        line_dash="dash",
    )


    fig_return.update_layout(
        xaxis_title="Trading Date",
        yaxis_title="Daily Return (%)",
    )


    st.plotly_chart(
        fig_return,
        width="stretch",
    )

else:

    st.info(
        "Not enough records to calculate daily returns."
    )


# ============================================================
# RETURN DISTRIBUTION
# ============================================================

st.markdown("---")

st.subheader("📊 Return Distribution")


if not return_data.empty:

    fig_hist = px.histogram(
        return_data,
        x="daily_return",
        nbins=40,
        title=f"{selected_stock} Daily Return Distribution",
    )


    fig_hist.update_layout(
        xaxis_title="Daily Return (%)",
        yaxis_title="Frequency",
    )


    st.plotly_chart(
        fig_hist,
        width="stretch",
    )


# ============================================================
# DRAWDOWN ANALYSIS
# ============================================================

st.markdown("---")

st.subheader("⚠️ Drawdown Analysis")


fig_drawdown = px.area(
    stock,
    x="trade_date",
    y="drawdown",
    title=f"{selected_stock} Historical Drawdown",
)


fig_drawdown.update_layout(
    xaxis_title="Trading Date",
    yaxis_title="Drawdown (%)",
)


st.plotly_chart(
    fig_drawdown,
    width="stretch",
)


# ============================================================
# RISK & PERFORMANCE SUMMARY
# ============================================================

st.markdown("---")

st.subheader("⚖️ Risk & Performance Summary")


risk_summary = pd.DataFrame(
    {
        "Metric": [
            "Starting Close",
            "Latest Close",
            "Period Return",
            "Highest Price",
            "Lowest Price",
            "Average Closing Price",
            "Average Trading Volume",
            "Daily Volatility",
            "Maximum Drawdown",
        ],

        "Value": [
            f"₹{first_close:,.2f}",
            f"₹{latest_close:,.2f}",
            f"{period_return:.2f}%",
            f"₹{highest_price:,.2f}",
            f"₹{lowest_price:,.2f}",
            f"₹{average_close:,.2f}",
            f"{average_volume:,.0f}",
            (
                f"{daily_volatility:.2f}%"
                if pd.notna(daily_volatility)
                else "N/A"
            ),
            (
                f"{max_drawdown:.2f}%"
                if pd.notna(max_drawdown)
                else "N/A"
            ),
        ],
    }
)


st.dataframe(
    risk_summary,
    width="stretch",
    hide_index=True,
)


# ============================================================
# HISTORICAL DATA TABLE
# ============================================================

st.markdown("---")

st.subheader("📋 Historical Stock Data")


display_columns = [
    "trade_date",
    "open_price",
    "high_price",
    "low_price",
    "close_price",
    "volume",
    "daily_return",
    "MA_20",
    "MA_50",
    "MA_100",
]


display_data = stock[
    display_columns
].copy()


display_data.columns = [
    "Date",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "Daily Return (%)",
    "MA 20",
    "MA 50",
    "MA 100",
]


st.dataframe(
    display_data.sort_values(
        "Date",
        ascending=False,
    ),
    width="stretch",
    hide_index=True,
)


# ============================================================
# DOWNLOAD DATA
# ============================================================

st.markdown("---")

st.subheader("📥 Export Stock Data")


csv_data = stock.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label=f"Download {selected_stock} Analysis CSV",
    data=csv_data,
    file_name=f"{selected_stock}_stock_analysis.csv",
    mime="text/csv",
)


# ============================================================
# ANALYSIS INFORMATION
# ============================================================

with st.expander("ℹ️ Understanding the Analysis"):

    st.markdown(
        """
        **Closing Price**
        
        The final traded price of the stock for a trading day.

        **Moving Average**

        Moving averages smooth short-term price fluctuations and
        help identify the overall trend.

        **20-Day MA**

        Represents the short-term market trend.

        **50-Day MA**

        Commonly used to identify medium-term trends.

        **100-Day MA**

        Provides a broader view of the stock's price direction.

        **Daily Return**

        Percentage change in closing price from the previous
        trading day.

        **Volatility**

        Measures how much daily returns fluctuate. Higher
        volatility generally indicates greater price uncertainty.

        **Maximum Drawdown**

        Measures the largest percentage decline from a previous
        peak during the selected period.

        **Candlestick Chart**

        Shows Open, High, Low and Close prices for every trading
        session.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Nifty 50 Stock Analysis Dashboard | "
    "MySQL • SQLAlchemy • Pandas • Plotly • Streamlit"
)