"""
Monthly.py

Monthly Stock Market Analysis page for the
Nifty 50 Stock Analysis Dashboard.

Author  : Anirudh R K
Project : Stock Analysis Dashboard
"""

# ============================================================
# IMPORTS
# ============================================================

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# PROJECT ROOT
# ============================================================

# Current file:
# project/streamlit_app/pages/Monthly.py

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
    page_title="Monthly Analysis",
    page_icon="📅",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("📅 Monthly Market Analysis")

st.markdown(
    """
    Analyze monthly trends across the **Nifty 50 stock dataset**,
    including closing-price movement, trading volume,
    monthly returns, and individual-stock performance.
    """
)

st.divider()


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(ttl=600)
def load_stock_data():

    df = fetch_stock_data()

    if df.empty:
        return df

    df["trade_date"] = pd.to_datetime(
        df["trade_date"],
        errors="coerce"
    )

    numeric_columns = [
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume"
    ]

    for column in numeric_columns:

        if column in df.columns:

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

    df = df.sort_values(
        ["ticker", "trade_date"]
    )

    return df


try:

    stock_data = load_stock_data()

except Exception as error:

    st.error(
        "Unable to load stock data from MySQL."
    )

    st.exception(error)

    st.stop()


if stock_data.empty:

    st.warning(
        "No stock records were found in the database."
    )

    st.stop()


# ============================================================
# CREATE DATE FEATURES
# ============================================================

stock_data["year"] = (
    stock_data["trade_date"].dt.year
)

stock_data["month_number"] = (
    stock_data["trade_date"].dt.month
)

stock_data["month_name"] = (
    stock_data["trade_date"].dt.month_name()
)

stock_data["year_month"] = (
    stock_data["trade_date"]
    .dt.to_period("M")
    .astype(str)
)


# ============================================================
# BASIC INFORMATION
# ============================================================

stocks = sorted(
    stock_data["ticker"]
    .dropna()
    .unique()
    .tolist()
)

years = sorted(
    stock_data["year"]
    .dropna()
    .unique()
    .tolist()
)

start_date = stock_data[
    "trade_date"
].min()

end_date = stock_data[
    "trade_date"
].max()


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📊 Monthly Dataset Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Companies",
    f"{len(stocks):,}"
)

c2.metric(
    "Trading Records",
    f"{len(stock_data):,}"
)

c3.metric(
    "Months Covered",
    stock_data["year_month"].nunique()
)

c4.metric(
    "Period",
    f"{start_date:%b %Y} – {end_date:%b %Y}"
)

st.divider()


# ============================================================
# MONTHLY MARKET AGGREGATION
# ============================================================

monthly_market = (
    stock_data
    .groupby(
        "year_month",
        as_index=False
    )
    .agg(
        average_close=(
            "close_price",
            "mean"
        ),
        highest_price=(
            "high_price",
            "max"
        ),
        lowest_price=(
            "low_price",
            "min"
        ),
        total_volume=(
            "volume",
            "sum"
        )
    )
)


monthly_market[
    "average_close"
] = monthly_market[
    "average_close"
].round(2)


monthly_market[
    "monthly_change_pct"
] = (
    monthly_market["average_close"]
    .pct_change(fill_method=None)
    * 100
)


# ============================================================
# MARKET TREND
# ============================================================

st.subheader("📈 Monthly Market Trend")

st.caption(
    "Average closing price across all companies for each month."
)


fig_market = px.line(
    monthly_market,
    x="year_month",
    y="average_close",
    markers=True,
    title="Average Monthly Closing Price"
)


fig_market.update_layout(
    xaxis_title="Month",
    yaxis_title="Average Closing Price",
    hovermode="x unified"
)


st.plotly_chart(
    fig_market,
    width="stretch"
)

st.divider()


# ============================================================
# MONTH-OVER-MONTH CHANGE
# ============================================================

st.subheader("📊 Month-over-Month Market Change")

monthly_change = monthly_market.dropna(
    subset=["monthly_change_pct"]
).copy()


fig_change = px.bar(
    monthly_change,
    x="year_month",
    y="monthly_change_pct",
    title="Monthly Percentage Change",
    text_auto=".2f"
)


fig_change.update_layout(
    xaxis_title="Month",
    yaxis_title="Change (%)"
)


st.plotly_chart(
    fig_change,
    width="stretch"
)


# ============================================================
# BEST AND WORST MONTH
# ============================================================

if not monthly_change.empty:

    best_month_row = monthly_change.loc[
        monthly_change[
            "monthly_change_pct"
        ].idxmax()
    ]

    worst_month_row = monthly_change.loc[
        monthly_change[
            "monthly_change_pct"
        ].idxmin()
    ]


    c1, c2 = st.columns(2)


    c1.metric(
        "🏆 Best Market Month",
        best_month_row["year_month"],
        f"{best_month_row['monthly_change_pct']:.2f}%"
    )


    c2.metric(
        "📉 Weakest Market Month",
        worst_month_row["year_month"],
        f"{worst_month_row['monthly_change_pct']:.2f}%"
    )


st.divider()


# ============================================================
# MONTHLY TRADING VOLUME
# ============================================================

st.subheader("📦 Monthly Trading Volume")


fig_volume = px.bar(
    monthly_market,
    x="year_month",
    y="total_volume",
    title="Total Trading Volume by Month"
)


fig_volume.update_layout(
    xaxis_title="Month",
    yaxis_title="Trading Volume"
)


st.plotly_chart(
    fig_volume,
    width="stretch"
)

st.divider()


# ============================================================
# MONTHLY HIGH / LOW RANGE
# ============================================================

st.subheader("📈 Monthly Price Range")


price_range = monthly_market[
    [
        "year_month",
        "highest_price",
        "lowest_price"
    ]
].melt(
    id_vars="year_month",
    var_name="Price Type",
    value_name="Price"
)


fig_range = px.line(
    price_range,
    x="year_month",
    y="Price",
    color="Price Type",
    markers=True,
    title="Monthly Highest vs Lowest Market Price"
)


fig_range.update_layout(
    xaxis_title="Month",
    yaxis_title="Stock Price",
    hovermode="x unified"
)


st.plotly_chart(
    fig_range,
    width="stretch"
)

st.divider()


# ============================================================
# INDIVIDUAL STOCK MONTHLY ANALYSIS
# ============================================================

st.subheader("🔎 Individual Stock Monthly Analysis")


selected_stock = st.selectbox(
    "Select Stock",
    stocks,
    key="monthly_selected_stock"
)


selected_data = (
    stock_data[
        stock_data["ticker"]
        == selected_stock
    ]
    .copy()
)


# ============================================================
# MONTHLY STOCK SUMMARY
# ============================================================

monthly_stock = (
    selected_data
    .groupby(
        "year_month",
        as_index=False
    )
    .agg(
        first_close=(
            "close_price",
            "first"
        ),
        last_close=(
            "close_price",
            "last"
        ),
        average_close=(
            "close_price",
            "mean"
        ),
        highest_price=(
            "high_price",
            "max"
        ),
        lowest_price=(
            "low_price",
            "min"
        ),
        average_volume=(
            "volume",
            "mean"
        ),
        total_volume=(
            "volume",
            "sum"
        )
    )
)


# ============================================================
# MONTHLY RETURN
# ============================================================

monthly_stock[
    "monthly_return"
] = (
    (
        monthly_stock["last_close"]
        - monthly_stock["first_close"]
    )
    /
    monthly_stock["first_close"]
    * 100
)


# ============================================================
# SELECTED STOCK KPIS
# ============================================================

if not monthly_stock.empty:

    latest = monthly_stock.iloc[-1]


    best_stock_month = monthly_stock.loc[
        monthly_stock[
            "monthly_return"
        ].idxmax()
    ]


    worst_stock_month = monthly_stock.loc[
        monthly_stock[
            "monthly_return"
        ].idxmin()
    ]


    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "Stock",
        selected_stock
    )


    c2.metric(
        "Latest Monthly Close",
        f"{latest['last_close']:,.2f}"
    )


    c3.metric(
        "Best Month",
        best_stock_month["year_month"],
        f"{best_stock_month['monthly_return']:.2f}%"
    )


    c4.metric(
        "Worst Month",
        worst_stock_month["year_month"],
        f"{worst_stock_month['monthly_return']:.2f}%"
    )


st.divider()


# ============================================================
# STOCK MONTHLY CLOSING TREND
# ============================================================

st.subheader(
    f"📈 {selected_stock} Monthly Price Trend"
)


fig_stock = px.line(
    monthly_stock,
    x="year_month",
    y="last_close",
    markers=True,
    title=(
        f"{selected_stock} Monthly Closing Price"
    )
)


fig_stock.update_layout(
    xaxis_title="Month",
    yaxis_title="Closing Price",
    hovermode="x unified"
)


st.plotly_chart(
    fig_stock,
    width="stretch"
)


# ============================================================
# STOCK MONTHLY RETURNS
# ============================================================

st.subheader(
    f"📊 {selected_stock} Monthly Returns"
)


fig_stock_return = px.bar(
    monthly_stock,
    x="year_month",
    y="monthly_return",
    title=(
        f"{selected_stock} Monthly Return (%)"
    ),
    text_auto=".2f"
)


fig_stock_return.update_layout(
    xaxis_title="Month",
    yaxis_title="Monthly Return (%)"
)


st.plotly_chart(
    fig_stock_return,
    width="stretch"
)

st.divider()


# ============================================================
# MONTHLY PERFORMANCE BY COMPANY
# ============================================================

st.subheader("🏢 Company Monthly Performance")


company_monthly = (
    stock_data
    .groupby(
        [
            "ticker",
            "year_month"
        ],
        as_index=False
    )
    .agg(
        first_close=(
            "close_price",
            "first"
        ),
        last_close=(
            "close_price",
            "last"
        )
    )
)


company_monthly[
    "monthly_return"
] = (
    (
        company_monthly["last_close"]
        - company_monthly["first_close"]
    )
    /
    company_monthly["first_close"]
    * 100
)


available_months = sorted(
    company_monthly[
        "year_month"
    ].unique()
)


selected_month = st.selectbox(
    "Select Month",
    available_months,
    index=len(available_months) - 1,
    key="company_month_selection"
)


selected_month_data = (
    company_monthly[
        company_monthly[
            "year_month"
        ]
        == selected_month
    ]
    .sort_values(
        "monthly_return",
        ascending=False
    )
)


# ============================================================
# TOP / BOTTOM MONTHLY STOCKS
# ============================================================

left, right = st.columns(2)


with left:

    st.subheader("🏆 Top Monthly Performers")

    top_monthly = (
        selected_month_data
        .head(10)
        .copy()
    )


    fig_top = px.bar(
        top_monthly,
        x="ticker",
        y="monthly_return",
        title=(
            f"Top Performers — {selected_month}"
        ),
        text_auto=".2f"
    )


    fig_top.update_layout(
        xaxis_title="Stock",
        yaxis_title="Monthly Return (%)"
    )


    st.plotly_chart(
        fig_top,
        width="stretch"
    )


with right:

    st.subheader("📉 Lowest Monthly Performers")

    bottom_monthly = (
        selected_month_data
        .tail(10)
        .sort_values(
            "monthly_return"
        )
        .copy()
    )


    fig_bottom = px.bar(
        bottom_monthly,
        x="ticker",
        y="monthly_return",
        title=(
            f"Lowest Performers — {selected_month}"
        ),
        text_auto=".2f"
    )


    fig_bottom.update_layout(
        xaxis_title="Stock",
        yaxis_title="Monthly Return (%)"
    )


    st.plotly_chart(
        fig_bottom,
        width="stretch"
    )


st.divider()


# ============================================================
# MONTHLY RETURN HEATMAP
# ============================================================

st.subheader("🔥 Monthly Return Heatmap")

st.caption(
    "Compare monthly percentage returns across all Nifty 50 stocks."
)


monthly_heatmap = company_monthly.pivot_table(
    index="ticker",
    columns="year_month",
    values="monthly_return",
    aggfunc="mean"
)


fig_heatmap = px.imshow(
    monthly_heatmap,
    x=monthly_heatmap.columns,
    y=monthly_heatmap.index,
    color_continuous_scale="RdYlGn",
    aspect="auto",
    title="Nifty 50 Monthly Return Heatmap"
)


fig_heatmap.update_layout(
    height=1000,
    xaxis_title="Month",
    yaxis_title="Stock"
)


st.plotly_chart(
    fig_heatmap,
    width="stretch"
)

st.divider()


# ============================================================
# YEAR FILTER
# ============================================================

st.subheader("🗓️ Year-wise Monthly Analysis")


selected_year = st.selectbox(
    "Select Year",
    years,
    index=len(years) - 1
)


year_data = stock_data[
    stock_data["year"]
    == selected_year
].copy()


year_monthly = (
    year_data
    .groupby(
        [
            "month_number",
            "month_name"
        ],
        as_index=False
    )
    .agg(
        average_close=(
            "close_price",
            "mean"
        ),
        total_volume=(
            "volume",
            "sum"
        )
    )
    .sort_values(
        "month_number"
    )
)


fig_year = px.line(
    year_monthly,
    x="month_name",
    y="average_close",
    markers=True,
    title=(
        f"Monthly Market Trend — {selected_year}"
    )
)


fig_year.update_layout(
    xaxis_title="Month",
    yaxis_title="Average Closing Price"
)


st.plotly_chart(
    fig_year,
    width="stretch"
)

st.divider()


# ============================================================
# TABLES
# ============================================================

st.subheader("📋 Monthly Analysis Tables")


with st.expander(
    "📊 Market Monthly Summary"
):

    market_table = monthly_market.copy()

    market_table[
        "monthly_change_pct"
    ] = market_table[
        "monthly_change_pct"
    ].round(2)

    st.dataframe(
        market_table,
        width="stretch",
        hide_index=True
    )


with st.expander(
    f"📈 {selected_stock} Monthly Summary"
):

    stock_table = monthly_stock.copy()

    numeric_round_columns = [
        "first_close",
        "last_close",
        "average_close",
        "highest_price",
        "lowest_price",
        "average_volume",
        "monthly_return"
    ]

    for column in numeric_round_columns:

        if column in stock_table.columns:

            stock_table[column] = (
                stock_table[column]
                .round(2)
            )


    st.dataframe(
        stock_table,
        width="stretch",
        hide_index=True
    )


with st.expander(
    f"🏢 Company Performance — {selected_month}"
):

    company_table = (
        selected_month_data[
            [
                "ticker",
                "first_close",
                "last_close",
                "monthly_return"
            ]
        ]
        .copy()
    )


    company_table[
        "monthly_return"
    ] = company_table[
        "monthly_return"
    ].round(2)


    st.dataframe(
        company_table,
        width="stretch",
        hide_index=True
    )


# ============================================================
# METHODOLOGY
# ============================================================

with st.expander(
    "ℹ️ About Monthly Analysis"
):

    st.markdown(
        """
        ### Monthly Market Analysis

        This page converts the daily stock-market dataset into
        monthly analytical information.

        **Average Closing Price**  
        Average closing price across the available stock records
        during each month.

        **Monthly Return**  
        Percentage change between the first and last available
        closing price of a stock during a month.

        **Trading Volume**  
        Total number of shares traded during the month.

        **Monthly Return Heatmap**  
        Allows the monthly performance of different Nifty 50
        companies to be compared quickly.

        **Best/Worst Month**  
        Identifies periods with the highest and lowest calculated
        monthly returns.

        These statistics describe historical performance and
        should not be interpreted as investment recommendations.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Nifty 50 Stock Analysis Dashboard | "
    "MySQL • SQLAlchemy • Pandas • Plotly • Streamlit"
)