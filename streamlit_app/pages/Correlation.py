"""
Correlation.py

Stock Correlation Analysis page for the
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
# project/streamlit_app/pages/Correlation.py
#
# parents[0] -> pages
# parents[1] -> streamlit_app
# parents[2] -> project root

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
    page_title="Correlation Analysis",
    page_icon="🔗",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🔗 Stock Correlation Analysis")

st.markdown(
    """
    Analyze relationships between **Nifty 50 stocks**
    using their **daily percentage returns**.

    Correlation values range from **-1 to +1**:

    - **+1** → Strong positive relationship
    - **0** → Little or no linear relationship
    - **-1** → Strong negative relationship
    """
)

st.divider()


# ============================================================
# LOAD DATA FROM MYSQL
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

    df["close_price"] = pd.to_numeric(
        df["close_price"],
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
        "Unable to load stock market data from MySQL."
    )

    st.exception(error)

    st.stop()


if stock_data.empty:

    st.warning(
        "The stock_data table does not contain any records."
    )

    st.stop()


# ============================================================
# BASIC DATA INFORMATION
# ============================================================

stocks = sorted(
    stock_data["ticker"]
    .dropna()
    .unique()
    .tolist()
)

total_records = len(stock_data)

total_companies = len(stocks)

total_days = stock_data[
    "trade_date"
].nunique()

start_date = stock_data[
    "trade_date"
].min()

end_date = stock_data[
    "trade_date"
].max()


# ============================================================
# KPI SECTION
# ============================================================

st.subheader("📊 Dataset Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Companies",
    f"{total_companies:,}"
)

c2.metric(
    "Stock Records",
    f"{total_records:,}"
)

c3.metric(
    "Trading Days",
    f"{total_days:,}"
)

c4.metric(
    "Period",
    f"{start_date:%b %Y} – {end_date:%b %Y}"
)

st.divider()


# ============================================================
# CREATE CLOSING PRICE MATRIX
# ============================================================

price_matrix = stock_data.pivot_table(
    index="trade_date",
    columns="ticker",
    values="close_price",
    aggfunc="mean"
)

price_matrix = price_matrix.sort_index()


# ============================================================
# DAILY RETURNS
# ============================================================

returns = price_matrix.pct_change(
    fill_method=None
)

returns = returns.replace(
    [float("inf"), float("-inf")],
    pd.NA
)

returns = returns.dropna(
    how="all"
)


# ============================================================
# CORRELATION MATRIX
# ============================================================

correlation_matrix = returns.corr(
    method="pearson"
)


if correlation_matrix.empty:

    st.error(
        "Correlation matrix could not be calculated."
    )

    st.stop()


# ============================================================
# CORRELATION HEATMAP
# ============================================================

st.subheader("🔥 Nifty 50 Correlation Heatmap")

st.caption(
    "Correlation is calculated using daily percentage returns "
    "rather than raw stock prices."
)


fig_heatmap = px.imshow(
    correlation_matrix,
    x=correlation_matrix.columns,
    y=correlation_matrix.index,
    color_continuous_scale="RdBu_r",
    zmin=-1,
    zmax=1,
    aspect="auto",
    title="Nifty 50 Daily Return Correlation Matrix"
)


fig_heatmap.update_layout(
    height=900,
    xaxis_title="Stock",
    yaxis_title="Stock",
    margin=dict(
        l=20,
        r=20,
        t=70,
        b=20
    )
)


fig_heatmap.update_xaxes(
    tickangle=90
)


st.plotly_chart(
    fig_heatmap,
    width="stretch"
)

st.divider()


# ============================================================
# INDIVIDUAL STOCK CORRELATION
# ============================================================

st.subheader("🔎 Individual Stock Correlation")

selected_stock = st.selectbox(
    "Select Stock",
    stocks,
    key="correlation_selected_stock"
)


stock_correlation = (
    correlation_matrix[selected_stock]
    .drop(
        labels=[selected_stock],
        errors="ignore"
    )
    .dropna()
    .sort_values(
        ascending=False
    )
)


if stock_correlation.empty:

    st.warning(
        "Not enough data to calculate correlation "
        "for this stock."
    )

    st.stop()


# ============================================================
# STRONGEST / WEAKEST RELATIONSHIPS
# ============================================================

strongest_stock = stock_correlation.idxmax()

strongest_value = stock_correlation.max()

weakest_stock = stock_correlation.idxmin()

weakest_value = stock_correlation.min()


c1, c2, c3 = st.columns(3)


c1.metric(
    "Selected Stock",
    selected_stock
)


c2.metric(
    "Highest Correlation",
    strongest_stock,
    f"{strongest_value:.3f}"
)


c3.metric(
    "Lowest Correlation",
    weakest_stock,
    f"{weakest_value:.3f}"
)


st.divider()


# ============================================================
# TOP POSITIVE / LOWEST CORRELATIONS
# ============================================================

left, right = st.columns(2)


# ------------------------------------------------------------
# POSITIVE
# ------------------------------------------------------------

with left:

    st.subheader(
        "📈 Most Positively Correlated"
    )

    positive = (
        stock_correlation
        .head(10)
        .reset_index()
    )

    positive.columns = [
        "Stock",
        "Correlation"
    ]


    fig_positive = px.bar(
        positive,
        x="Stock",
        y="Correlation",
        title=(
            f"Stocks Most Correlated "
            f"with {selected_stock}"
        ),
        text_auto=".3f"
    )


    fig_positive.update_layout(
        xaxis_title="Stock",
        yaxis_title="Correlation",
        yaxis_range=[
            min(0, positive["Correlation"].min()),
            1
        ]
    )


    st.plotly_chart(
        fig_positive,
        width="stretch"
    )


# ------------------------------------------------------------
# LOWEST
# ------------------------------------------------------------

with right:

    st.subheader(
        "📉 Least Correlated"
    )

    lowest = (
        stock_correlation
        .tail(10)
        .sort_values()
        .reset_index()
    )

    lowest.columns = [
        "Stock",
        "Correlation"
    ]


    fig_lowest = px.bar(
        lowest,
        x="Stock",
        y="Correlation",
        title=(
            f"Stocks Least Correlated "
            f"with {selected_stock}"
        ),
        text_auto=".3f"
    )


    fig_lowest.update_layout(
        xaxis_title="Stock",
        yaxis_title="Correlation"
    )


    st.plotly_chart(
        fig_lowest,
        width="stretch"
    )


st.divider()


# ============================================================
# COMPARE TWO STOCKS
# ============================================================

st.subheader("⚖️ Compare Two Stocks")

col1, col2 = st.columns(2)


with col1:

    stock1 = st.selectbox(
        "Stock 1",
        stocks,
        index=0,
        key="correlation_stock_1"
    )


with col2:

    default_index = (
        1
        if len(stocks) > 1
        else 0
    )

    stock2 = st.selectbox(
        "Stock 2",
        stocks,
        index=default_index,
        key="correlation_stock_2"
    )


# ============================================================
# CORRELATION COEFFICIENT
# ============================================================

correlation_value = correlation_matrix.loc[
    stock1,
    stock2
]


st.metric(
    "Correlation Coefficient",
    f"{correlation_value:.4f}"
)


# ============================================================
# CORRELATION INTERPRETATION
# ============================================================

if stock1 == stock2:

    interpretation = (
        "A stock compared with itself always has "
        "a correlation of 1."
    )

elif correlation_value >= 0.70:

    interpretation = (
        "Strong Positive Correlation"
    )

elif correlation_value >= 0.40:

    interpretation = (
        "Moderate Positive Correlation"
    )

elif correlation_value > -0.40:

    interpretation = (
        "Weak / Low Correlation"
    )

elif correlation_value > -0.70:

    interpretation = (
        "Moderate Negative Correlation"
    )

else:

    interpretation = (
        "Strong Negative Correlation"
    )


st.info(
    f"**{stock1} vs {stock2}:** "
    f"{interpretation}"
)


# ============================================================
# NORMALIZED STOCK PERFORMANCE
# ============================================================

st.subheader(
    "📈 Normalized Performance Comparison"
)


comparison = price_matrix[
    [stock1, stock2]
].dropna().copy()


if not comparison.empty:

    # Prevent duplicate columns when same stock selected
    comparison = comparison.loc[
        :,
        ~comparison.columns.duplicated()
    ]


    normalized = (
        comparison
        / comparison.iloc[0]
        * 100
    )


    normalized = (
        normalized
        .reset_index()
        .melt(
            id_vars="trade_date",
            var_name="Stock",
            value_name="Normalized Price"
        )
    )


    fig_compare = px.line(
        normalized,
        x="trade_date",
        y="Normalized Price",
        color="Stock",
        title=(
            f"{stock1} vs {stock2} "
            "— Normalized Performance"
        )
    )


    fig_compare.update_layout(
        xaxis_title="Trading Date",
        yaxis_title="Normalized Price (Base = 100)",
        hovermode="x unified"
    )


    st.plotly_chart(
        fig_compare,
        width="stretch"
    )

else:

    st.warning(
        "No overlapping trading data is available "
        "for these two stocks."
    )


st.divider()


# ============================================================
# ROLLING CORRELATION
# ============================================================

st.subheader("📅 Rolling Correlation Analysis")

st.caption(
    "Shows how the relationship between the two stocks "
    "changes over time."
)


rolling_window = st.slider(
    "Rolling Window (Trading Days)",
    min_value=10,
    max_value=90,
    value=30,
    step=5
)


if stock1 != stock2:

    pair_returns = returns[
        [stock1, stock2]
    ].dropna()


    if len(pair_returns) >= rolling_window:

        rolling_corr = (
            pair_returns[stock1]
            .rolling(
                window=rolling_window
            )
            .corr(
                pair_returns[stock2]
            )
            .dropna()
            .reset_index()
        )


        rolling_corr.columns = [
            "Trading Date",
            "Correlation"
        ]


        fig_rolling = px.line(
            rolling_corr,
            x="Trading Date",
            y="Correlation",
            title=(
                f"{rolling_window}-Day Rolling Correlation: "
                f"{stock1} vs {stock2}"
            )
        )


        fig_rolling.update_layout(
            yaxis_range=[-1, 1],
            yaxis_title="Correlation",
            xaxis_title="Trading Date"
        )


        st.plotly_chart(
            fig_rolling,
            width="stretch"
        )

    else:

        st.warning(
            "Not enough overlapping records for the "
            "selected rolling window."
        )

else:

    st.info(
        "Select two different stocks to view "
        "rolling correlation."
    )


st.divider()


# ============================================================
# CORRELATION DISTRIBUTION
# ============================================================

st.subheader("📊 Correlation Distribution")

upper_triangle = []

columns = correlation_matrix.columns


for i in range(len(columns)):

    for j in range(i + 1, len(columns)):

        value = correlation_matrix.iloc[
            i,
            j
        ]

        if pd.notna(value):

            upper_triangle.append(
                {
                    "Stock 1": columns[i],
                    "Stock 2": columns[j],
                    "Correlation": value
                }
            )


pairs_df = pd.DataFrame(
    upper_triangle
)


if not pairs_df.empty:

    fig_distribution = px.histogram(
        pairs_df,
        x="Correlation",
        nbins=30,
        title="Distribution of Nifty 50 Stock Correlations"
    )


    fig_distribution.update_layout(
        xaxis_title="Correlation Coefficient",
        yaxis_title="Number of Stock Pairs"
    )


    st.plotly_chart(
        fig_distribution,
        width="stretch"
    )


# ============================================================
# STRONGEST STOCK PAIRS
# ============================================================

st.subheader("🏆 Strongest Stock Relationships")


if not pairs_df.empty:

    strongest_pairs = (
        pairs_df
        .sort_values(
            "Correlation",
            ascending=False
        )
        .head(10)
        .copy()
    )


    strongest_pairs[
        "Correlation"
    ] = strongest_pairs[
        "Correlation"
    ].round(4)


    st.dataframe(
        strongest_pairs,
        width="stretch",
        hide_index=True
    )


st.divider()


# ============================================================
# CORRELATION MATRIX TABLE
# ============================================================

with st.expander(
    "📋 View Complete Correlation Matrix"
):

    st.dataframe(
        correlation_matrix.round(3),
        width="stretch"
    )


# ============================================================
# SELECTED STOCK TABLE
# ============================================================

with st.expander(
    f"📊 View {selected_stock} Correlations"
):

    correlation_table = (
        stock_correlation
        .reset_index()
    )


    correlation_table.columns = [
        "Stock",
        "Correlation"
    ]


    correlation_table[
        "Correlation"
    ] = correlation_table[
        "Correlation"
    ].round(4)


    st.dataframe(
        correlation_table,
        width="stretch",
        hide_index=True
    )


# ============================================================
# METHODOLOGY
# ============================================================

with st.expander(
    "ℹ️ About Correlation Analysis"
):

    st.markdown(
        """
        ### How this analysis works

        **1. Closing Price Matrix**

        Daily closing prices are organized by trading date
        and company.

        **2. Daily Returns**

        Percentage change in closing price is calculated for
        each stock.

        **3. Pearson Correlation**

        Correlation is calculated between the daily returns
        of every pair of stocks.

        ### Interpretation

        | Correlation | Interpretation |
        |---|---|
        | 0.70 to 1.00 | Strong positive |
        | 0.40 to 0.69 | Moderate positive |
        | -0.39 to 0.39 | Weak / low |
        | -0.69 to -0.40 | Moderate negative |
        | -1.00 to -0.70 | Strong negative |

        Correlation measures statistical co-movement and
        **does not imply causation**.
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