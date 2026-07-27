"""
Sector.py

Sector-wise analysis for the Nifty 50
Stock Analysis Dashboard.

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

# Current:
# project/streamlit_app/pages/Sector.py
#
# parents[0] = pages
# parents[1] = streamlit_app
# parents[2] = project root

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# ============================================================
# PROJECT IMPORTS
# ============================================================

from database.fetch_data import fetch_stock_data


# ============================================================
# SECTOR MAPPING IMPORT
# ============================================================

try:
    from utils.sector_mapping import SECTOR_MAPPING
except ImportError:
    SECTOR_MAPPING = {}


# ============================================================
# FALLBACK SECTOR MAPPING
# ============================================================

# Used only if utils/sector_mapping.py does not contain
# SECTOR_MAPPING.

FALLBACK_SECTOR_MAPPING = {

    "ADANIENT": "Diversified",
    "ADANIPORTS": "Infrastructure",

    "APOLLOHOSP": "Healthcare",

    "ASIANPAINT": "Consumer Durables",

    "AXISBANK": "Banking",

    "BAJAJ-AUTO": "Automobile",
    "BAJAJFINSV": "Financial Services",
    "BAJFINANCE": "Financial Services",

    "BEL": "Defence",

    "BHARTIARTL": "Telecommunication",

    "BPCL": "Energy",

    "BRITANNIA": "FMCG",

    "CIPLA": "Pharmaceuticals",

    "COALINDIA": "Metals & Mining",

    "DRREDDY": "Pharmaceuticals",

    "EICHERMOT": "Automobile",

    "GRASIM": "Cement",

    "HCLTECH": "Information Technology",

    "HDFCBANK": "Banking",
    "HDFCLIFE": "Insurance",

    "HEROMOTOCO": "Automobile",

    "HINDALCO": "Metals",

    "HINDUNILVR": "FMCG",

    "ICICIBANK": "Banking",

    "INDUSINDBK": "Banking",

    "INFY": "Information Technology",

    "ITC": "FMCG",

    "JSWSTEEL": "Metals",

    "KOTAKBANK": "Banking",

    "LT": "Infrastructure",

    "M&M": "Automobile",

    "MARUTI": "Automobile",

    "NESTLEIND": "FMCG",

    "NTPC": "Power",

    "ONGC": "Energy",

    "POWERGRID": "Power",

    "RELIANCE": "Energy",

    "SBILIFE": "Insurance",

    "SBIN": "Banking",

    "SHRIRAMFIN": "Financial Services",

    "SUNPHARMA": "Pharmaceuticals",

    "TATACONSUM": "FMCG",

    "TATAMOTORS": "Automobile",

    "TATASTEEL": "Metals",

    "TCS": "Information Technology",

    "TECHM": "Information Technology",

    "TITAN": "Consumer Durables",

    "TRENT": "Retail",

    "ULTRACEMCO": "Cement",

    "WIPRO": "Information Technology"
}


if not SECTOR_MAPPING:
    SECTOR_MAPPING = FALLBACK_SECTOR_MAPPING


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Sector Analysis",
    page_icon="🏭",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🏭 Sector Analysis")

st.markdown(
    """
    Analyze the **Nifty 50 market by sector** using historical
    price, return, volatility and trading-volume data.
    """
)

st.divider()


# ============================================================
# LOAD MYSQL DATA
# ============================================================

@st.cache_data(ttl=600)
def load_stock_data():

    df = fetch_stock_data()

    if df.empty:
        return df

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    df["trade_date"] = pd.to_datetime(
        df["trade_date"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # NUMERIC COLUMNS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # REMOVE INVALID RECORDS
    # --------------------------------------------------------

    df = df.dropna(
        subset=[
            "ticker",
            "trade_date",
            "close_price"
        ]
    )

    df = df.sort_values(
        [
            "ticker",
            "trade_date"
        ]
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
# ADD SECTOR INFORMATION
# ============================================================

stock_data["sector"] = (
    stock_data["ticker"]
    .map(SECTOR_MAPPING)
    .fillna("Other")
)


# ============================================================
# BASIC VARIABLES
# ============================================================

stocks = sorted(
    stock_data["ticker"]
    .unique()
    .tolist()
)


sectors = sorted(
    stock_data["sector"]
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
# SECTOR COMPANY INFORMATION
# ============================================================

company_sector = (
    stock_data[
        [
            "ticker",
            "sector"
        ]
    ]
    .drop_duplicates()
)


sector_company_count = (
    company_sector
    .groupby(
        "sector",
        as_index=False
    )
    .agg(
        companies=(
            "ticker",
            "nunique"
        )
    )
    .sort_values(
        "companies",
        ascending=False
    )
)


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📊 Sector Overview")


largest_sector_row = (
    sector_company_count.iloc[0]
)


c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "Companies",
    f"{len(stocks):,}"
)


c2.metric(
    "Sectors",
    f"{len(sectors):,}"
)


c3.metric(
    "Largest Sector",
    largest_sector_row["sector"],
    f"{int(largest_sector_row['companies'])} companies"
)


c4.metric(
    "Period",
    f"{start_date:%b %Y} – {end_date:%b %Y}"
)


st.divider()


# ============================================================
# SECTOR DISTRIBUTION
# ============================================================

st.subheader("🥧 Nifty 50 Sector Distribution")

left, right = st.columns([1.5, 1])


# ------------------------------------------------------------
# DONUT CHART
# ------------------------------------------------------------

with left:

    fig_distribution = px.pie(
        sector_company_count,
        names="sector",
        values="companies",
        hole=0.45,
        title="Companies by Sector"
    )


    fig_distribution.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )


    fig_distribution.update_layout(
        height=600
    )


    st.plotly_chart(
        fig_distribution,
        width="stretch"
    )


# ------------------------------------------------------------
# BAR CHART
# ------------------------------------------------------------

with right:

    fig_sector_count = px.bar(
        sector_company_count,
        x="companies",
        y="sector",
        orientation="h",
        title="Number of Companies"
    )


    fig_sector_count.update_layout(
        xaxis_title="Companies",
        yaxis_title="Sector",
        height=600
    )


    st.plotly_chart(
        fig_sector_count,
        width="stretch"
    )


st.divider()


# ============================================================
# CALCULATE DAILY STOCK RETURNS
# ============================================================

stock_data["daily_return"] = (
    stock_data
    .groupby("ticker")[
        "close_price"
    ]
    .pct_change(
        fill_method=None
    )
)


# ============================================================
# COMPANY PERFORMANCE
# ============================================================

company_performance = (
    stock_data
    .groupby(
        [
            "ticker",
            "sector"
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
        ),
        volatility=(
            "daily_return",
            "std"
        )
    )
)


# ============================================================
# TOTAL STOCK RETURN
# ============================================================

company_performance[
    "return_pct"
] = (
    (
        company_performance["last_close"]
        -
        company_performance["first_close"]
    )
    /
    company_performance["first_close"]
    *
    100
)


company_performance[
    "volatility_pct"
] = (
    company_performance[
        "volatility"
    ]
    * 100
)


# ============================================================
# SECTOR PERFORMANCE
# ============================================================

sector_performance = (
    company_performance
    .groupby(
        "sector",
        as_index=False
    )
    .agg(
        companies=(
            "ticker",
            "nunique"
        ),
        average_return=(
            "return_pct",
            "mean"
        ),
        average_volatility=(
            "volatility_pct",
            "mean"
        ),
        average_close=(
            "average_close",
            "mean"
        ),
        average_volume=(
            "average_volume",
            "mean"
        ),
        total_volume=(
            "total_volume",
            "sum"
        )
    )
)


sector_performance = (
    sector_performance
    .sort_values(
        "average_return",
        ascending=False
    )
)


# ============================================================
# BEST / WORST SECTOR
# ============================================================

st.subheader("🏆 Sector Performance Overview")


best_sector = (
    sector_performance.iloc[0]
)


worst_sector = (
    sector_performance.iloc[-1]
)


most_volatile_sector = (
    sector_performance.loc[
        sector_performance[
            "average_volatility"
        ].idxmax()
    ]
)


most_active_sector = (
    sector_performance.loc[
        sector_performance[
            "total_volume"
        ].idxmax()
    ]
)


c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "Best Performing Sector",
    best_sector["sector"],
    f"{best_sector['average_return']:.2f}%"
)


c2.metric(
    "Lowest Performing Sector",
    worst_sector["sector"],
    f"{worst_sector['average_return']:.2f}%"
)


c3.metric(
    "Most Volatile Sector",
    most_volatile_sector["sector"],
    f"{most_volatile_sector['average_volatility']:.2f}%"
)


c4.metric(
    "Highest Trading Activity",
    most_active_sector["sector"]
)


st.divider()


# ============================================================
# SECTOR RETURN ANALYSIS
# ============================================================

st.subheader("📈 Sector Return Analysis")


fig_return = px.bar(
    sector_performance,
    x="sector",
    y="average_return",
    title="Average Historical Return by Sector",
    text_auto=".2f"
)


fig_return.update_layout(
    xaxis_title="Sector",
    yaxis_title="Average Return (%)",
    xaxis_tickangle=-45
)


st.plotly_chart(
    fig_return,
    width="stretch"
)


st.divider()


# ============================================================
# SECTOR VOLATILITY
# ============================================================

st.subheader("⚡ Sector Volatility")


volatility_sorted = (
    sector_performance
    .sort_values(
        "average_volatility",
        ascending=False
    )
)


fig_volatility = px.bar(
    volatility_sorted,
    x="sector",
    y="average_volatility",
    title="Average Daily Volatility by Sector",
    text_auto=".2f"
)


fig_volatility.update_layout(
    xaxis_title="Sector",
    yaxis_title="Volatility (%)",
    xaxis_tickangle=-45
)


st.plotly_chart(
    fig_volatility,
    width="stretch"
)


st.divider()


# ============================================================
# RISK RETURN ANALYSIS
# ============================================================

st.subheader("🎯 Sector Risk vs Return")

st.caption(
    "Compare historical return against daily volatility "
    "for each sector."
)


fig_risk_return = px.scatter(
    sector_performance,
    x="average_volatility",
    y="average_return",
    size="companies",
    text="sector",
    hover_name="sector",
    hover_data={
        "companies": True,
        "average_volatility": ":.2f",
        "average_return": ":.2f",
        "average_close": ":.2f"
    },
    title="Sector Risk-Return Profile"
)


fig_risk_return.update_traces(
    textposition="top center"
)


fig_risk_return.update_layout(
    height=650,
    xaxis_title="Average Volatility (%)",
    yaxis_title="Average Return (%)"
)


st.plotly_chart(
    fig_risk_return,
    width="stretch"
)


st.divider()


# ============================================================
# SECTOR TRADING VOLUME
# ============================================================

st.subheader("📦 Sector Trading Activity")


volume_sorted = (
    sector_performance
    .sort_values(
        "total_volume",
        ascending=False
    )
)


fig_volume = px.bar(
    volume_sorted,
    x="sector",
    y="total_volume",
    title="Total Historical Trading Volume by Sector"
)


fig_volume.update_layout(
    xaxis_title="Sector",
    yaxis_title="Trading Volume",
    xaxis_tickangle=-45
)


st.plotly_chart(
    fig_volume,
    width="stretch"
)


st.divider()


# ============================================================
# SECTOR DRILL-DOWN
# ============================================================

st.subheader("🔎 Sector Drill-Down")


selected_sector = st.selectbox(
    "Select Sector",
    sectors,
    key="sector_selection"
)


selected_sector_data = (
    company_performance[
        company_performance[
            "sector"
        ]
        == selected_sector
    ]
    .copy()
)


selected_sector_data = (
    selected_sector_data
    .sort_values(
        "return_pct",
        ascending=False
    )
)


# ============================================================
# SELECTED SECTOR KPI
# ============================================================

sector_company_total = len(
    selected_sector_data
)


sector_average_return = (
    selected_sector_data[
        "return_pct"
    ].mean()
)


sector_average_volatility = (
    selected_sector_data[
        "volatility_pct"
    ].mean()
)


sector_best_company = (
    selected_sector_data.iloc[0]
)


c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "Sector",
    selected_sector
)


c2.metric(
    "Companies",
    sector_company_total
)


c3.metric(
    "Average Return",
    f"{sector_average_return:.2f}%"
)


c4.metric(
    "Top Stock",
    sector_best_company["ticker"],
    f"{sector_best_company['return_pct']:.2f}%"
)


st.divider()


# ============================================================
# COMPANIES IN SELECTED SECTOR
# ============================================================

st.subheader(
    f"🏢 {selected_sector} Companies"
)


fig_company_return = px.bar(
    selected_sector_data,
    x="ticker",
    y="return_pct",
    title=(
        f"{selected_sector} — Company Returns"
    ),
    text_auto=".2f"
)


fig_company_return.update_layout(
    xaxis_title="Stock",
    yaxis_title="Return (%)"
)


st.plotly_chart(
    fig_company_return,
    width="stretch"
)


# ============================================================
# COMPANY RISK RETURN
# ============================================================

st.subheader(
    f"⚡ {selected_sector} Company Risk vs Return"
)


fig_company_risk = px.scatter(
    selected_sector_data,
    x="volatility_pct",
    y="return_pct",
    text="ticker",
    size="average_volume",
    hover_name="ticker",
    title=(
        f"{selected_sector} — Risk Return Comparison"
    )
)


fig_company_risk.update_traces(
    textposition="top center"
)


fig_company_risk.update_layout(
    height=600,
    xaxis_title="Volatility (%)",
    yaxis_title="Return (%)"
)


st.plotly_chart(
    fig_company_risk,
    width="stretch"
)


st.divider()


# ============================================================
# SECTOR PRICE TREND
# ============================================================

st.subheader(
    f"📅 {selected_sector} Historical Trend"
)


sector_tickers = (
    selected_sector_data[
        "ticker"
    ]
    .tolist()
)


sector_history = (
    stock_data[
        stock_data[
            "ticker"
        ].isin(sector_tickers)
    ]
    .copy()
)


daily_sector = (
    sector_history
    .groupby(
        "trade_date",
        as_index=False
    )
    .agg(
        average_close=(
            "close_price",
            "mean"
        ),
        trading_volume=(
            "volume",
            "sum"
        )
    )
)


fig_sector_trend = px.line(
    daily_sector,
    x="trade_date",
    y="average_close",
    title=(
        f"{selected_sector} Average Closing Price Trend"
    )
)


fig_sector_trend.update_layout(
    xaxis_title="Trading Date",
    yaxis_title="Average Closing Price",
    hovermode="x unified"
)


st.plotly_chart(
    fig_sector_trend,
    width="stretch"
)


st.divider()


# ============================================================
# COMPARE TWO SECTORS
# ============================================================

st.subheader("⚖️ Compare Two Sectors")


col1, col2 = st.columns(2)


with col1:

    sector1 = st.selectbox(
        "Sector 1",
        sectors,
        index=0,
        key="sector_compare_1"
    )


with col2:

    default_index = (
        1
        if len(sectors) > 1
        else 0
    )

    sector2 = st.selectbox(
        "Sector 2",
        sectors,
        index=default_index,
        key="sector_compare_2"
    )


comparison_data = (
    sector_performance[
        sector_performance[
            "sector"
        ].isin(
            [
                sector1,
                sector2
            ]
        )
    ]
    .copy()
)


# ============================================================
# RETURN COMPARISON
# ============================================================

left, right = st.columns(2)


with left:

    fig_compare_return = px.bar(
        comparison_data,
        x="sector",
        y="average_return",
        title="Return Comparison",
        text_auto=".2f"
    )


    fig_compare_return.update_layout(
        xaxis_title="Sector",
        yaxis_title="Return (%)"
    )


    st.plotly_chart(
        fig_compare_return,
        width="stretch"
    )


with right:

    fig_compare_risk = px.bar(
        comparison_data,
        x="sector",
        y="average_volatility",
        title="Volatility Comparison",
        text_auto=".2f"
    )


    fig_compare_risk.update_layout(
        xaxis_title="Sector",
        yaxis_title="Volatility (%)"
    )


    st.plotly_chart(
        fig_compare_risk,
        width="stretch"
    )


st.divider()


# ============================================================
# SECTOR NORMALIZED PERFORMANCE
# ============================================================

st.subheader("📈 Sector Performance Comparison")


def build_sector_daily_series(sector_name):

    tickers = (
        company_sector[
            company_sector[
                "sector"
            ]
            == sector_name
        ][
            "ticker"
        ]
        .tolist()
    )

    data = stock_data[
        stock_data[
            "ticker"
        ].isin(tickers)
    ]

    daily = (
        data
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

    daily["sector"] = sector_name

    return daily


sector1_daily = build_sector_daily_series(
    sector1
)

sector2_daily = build_sector_daily_series(
    sector2
)


sector_comparison = pd.concat(
    [
        sector1_daily,
        sector2_daily
    ],
    ignore_index=True
)


sector_comparison = (
    sector_comparison
    .sort_values(
        [
            "sector",
            "trade_date"
        ]
    )
)


sector_comparison[
    "normalized_price"
] = (
    sector_comparison
    .groupby(
        "sector"
    )[
        "average_close"
    ]
    .transform(
        lambda x:
        x / x.iloc[0] * 100
    )
)


fig_sector_comparison = px.line(
    sector_comparison,
    x="trade_date",
    y="normalized_price",
    color="sector",
    title=(
        f"{sector1} vs {sector2} "
        "— Normalized Performance"
    )
)


fig_sector_comparison.update_layout(
    xaxis_title="Trading Date",
    yaxis_title="Normalized Price (Base = 100)",
    hovermode="x unified"
)


st.plotly_chart(
    fig_sector_comparison,
    width="stretch"
)


st.divider()


# ============================================================
# SECTOR TABLE
# ============================================================

st.subheader("📋 Sector Summary")


sector_table = (
    sector_performance.copy()
)


round_columns = [
    "average_return",
    "average_volatility",
    "average_close",
    "average_volume"
]


for column in round_columns:

    sector_table[column] = (
        sector_table[column]
        .round(2)
    )


st.dataframe(
    sector_table,
    width="stretch",
    hide_index=True
)


# ============================================================
# EXPANDERS
# ============================================================

with st.expander(
    f"🏢 View {selected_sector} Company Data"
):

    display_columns = [
        "ticker",
        "first_close",
        "last_close",
        "return_pct",
        "volatility_pct",
        "average_volume"
    ]


    sector_company_table = (
        selected_sector_data[
            display_columns
        ]
        .copy()
    )


    for column in [
        "first_close",
        "last_close",
        "return_pct",
        "volatility_pct",
        "average_volume"
    ]:

        sector_company_table[column] = (
            sector_company_table[
                column
            ].round(2)
        )


    st.dataframe(
        sector_company_table,
        width="stretch",
        hide_index=True
    )


with st.expander(
    "🗂️ View Company Sector Mapping"
):

    mapping_table = (
        company_sector
        .sort_values(
            [
                "sector",
                "ticker"
            ]
        )
    )


    st.dataframe(
        mapping_table,
        width="stretch",
        hide_index=True
    )


# ============================================================
# METHODOLOGY
# ============================================================

with st.expander(
    "ℹ️ About Sector Analysis"
):

    st.markdown(
        """
        ### Sector Analysis

        Stocks are grouped according to their business sector
        and historical market behaviour is compared across
        those groups.

        **Sector Return**

        Calculated using the historical first and last closing
        prices of each company and then aggregated by sector.

        **Volatility**

        Calculated using the standard deviation of daily
        percentage returns. Higher volatility indicates larger
        historical price fluctuations.

        **Risk vs Return**

        The scatter plot compares historical return with
        volatility. This helps visualize sectors that produced
        higher returns relative to their historical variability.

        **Normalized Performance**

        Sector values are rebased to 100 so sectors with very
        different stock-price levels can be compared on the
        same chart.

        These results represent historical data analysis and
        are not investment recommendations.
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