"""
app.py

Main landing page for the Nifty 50 Stock Analysis Dashboard.

Author  : Anirudh R K
Project : Stock Analysis Dashboard
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# PROJECT ROOT
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# ============================================================
# DATABASE IMPORTS
# ============================================================

from database.fetch_data import (
    fetch_stock_data,
    fetch_market_summary,
    fetch_company_summary,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Nifty 50 Stock Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(ttl=600)
def load_data():

    stocks = fetch_stock_data()
    market = fetch_market_summary()
    companies = fetch_company_summary()

    stocks["trade_date"] = pd.to_datetime(
        stocks["trade_date"],
        errors="coerce",
    )

    return stocks, market, companies


try:

    stock_data, market_summary, company_summary = load_data()

except Exception as error:

    st.error(
        "Unable to connect to the stock analytics database."
    )

    st.exception(error)

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.title("📈 Nifty 50 Stock Analytics Platform")

st.markdown(
    """
    ### Data-Driven Stock Market Analysis Dashboard

    Interactive analytics platform for exploring **Nifty 50 market
    performance, stock trends, sector distribution, correlations,
    returns and risk metrics** using historical market data.
    """
)

st.caption(
    "Python • Pandas • MySQL • SQLAlchemy • Plotly • Streamlit"
)

st.markdown("---")


# ============================================================
# MARKET OVERVIEW
# ============================================================

st.header("📊 Market Overview")


total_companies = (
    stock_data["ticker"]
    .nunique()
)

total_records = len(stock_data)

start_date = stock_data["trade_date"].min()

end_date = stock_data["trade_date"].max()

highest_price = stock_data["high_price"].max()

lowest_price = stock_data["low_price"].min()

average_close = stock_data["close_price"].mean()

average_volume = stock_data["volume"].mean()


# ============================================================
# KPI ROW 1
# ============================================================

c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "Companies",
    f"{total_companies:,}",
)


c2.metric(
    "Market Records",
    f"{total_records:,}",
)


c3.metric(
    "Highest Price",
    f"₹{highest_price:,.2f}",
)


c4.metric(
    "Lowest Price",
    f"₹{lowest_price:,.2f}",
)


# ============================================================
# KPI ROW 2
# ============================================================

c5, c6, c7, c8 = st.columns(4)


c5.metric(
    "Average Closing Price",
    f"₹{average_close:,.2f}",
)


c6.metric(
    "Average Daily Volume",
    f"{average_volume:,.0f}",
)


c7.metric(
    "Start Date",
    start_date.strftime("%d %b %Y"),
)


c8.metric(
    "End Date",
    end_date.strftime("%d %b %Y"),
)


st.markdown("---")


# ============================================================
# PLATFORM MODULES
# ============================================================

st.header("🧭 Analytics Modules")

st.write(
    "Use the navigation menu on the left to explore the "
    "different analytical modules."
)


# ============================================================
# DASHBOARD
# ============================================================

with st.container(border=True):

    st.subheader("📊 Dashboard")

    st.write(
        """
        Get a complete overview of Nifty 50 market performance,
        including major KPIs, top-performing stocks, market
        trends, volatility and return analysis.
        """
    )

    st.page_link(
        "pages/Dashboard.py",
        label="Open Market Dashboard",
        icon="📊",
    )


# ============================================================
# STOCK ANALYSIS
# ============================================================

with st.container(border=True):

    st.subheader("🔎 Individual Stock Analysis")

    st.write(
        """
        Perform detailed analysis of individual Nifty 50 stocks
        using historical prices, OHLC candlesticks, moving
        averages, trading volume, returns and drawdown.
        """
    )

    st.page_link(
        "pages/Stock_Analysis.py",
        label="Open Stock Analysis",
        icon="🔎",
    )


# ============================================================
# CORRELATION
# ============================================================

with st.container(border=True):

    st.subheader("🔗 Correlation Analysis")

    st.write(
        """
        Examine relationships between Nifty 50 stocks using
        daily-return correlation matrices and compare how
        different stocks move relative to one another.
        """
    )

    st.page_link(
        "pages/Correlation.py",
        label="Open Correlation Analysis",
        icon="🔗",
    )


# ============================================================
# MONTHLY
# ============================================================

with st.container(border=True):

    st.subheader("📅 Monthly Market Analysis")

    st.write(
        """
        Explore monthly market trends and understand how
        stock prices and returns change across different
        months of the year.
        """
    )

    st.page_link(
        "pages/Monthly.py",
        label="Open Monthly Analysis",
        icon="📅",
    )


# ============================================================
# SECTOR
# ============================================================

with st.container(border=True):

    st.subheader("🏭 Sector Analysis")

    st.write(
        """
        Analyze the sector composition of Nifty 50 companies
        and compare sector-level market performance.
        """
    )

    st.page_link(
        "pages/Sector.py",
        label="Open Sector Analysis",
        icon="🏭",
    )


st.markdown("---")


# ============================================================
# DATASET INFORMATION
# ============================================================

st.header("🗄️ Dataset Information")


info1, info2, info3 = st.columns(3)


info1.metric(
    "Nifty 50 Companies",
    total_companies,
)


info2.metric(
    "Historical Records",
    f"{total_records:,}",
)


trading_days = (
    stock_data["trade_date"]
    .nunique()
)


info3.metric(
    "Trading Days",
    f"{trading_days:,}",
)


st.write(
    f"""
    The dataset contains historical market information from
    **{start_date.strftime("%d %B %Y")}** to
    **{end_date.strftime("%d %B %Y")}**.
    """
)


# ============================================================
# DATA PIPELINE
# ============================================================

st.markdown("---")

st.header("⚙️ Analytics Architecture")

st.code(
    """
Raw YAML Stock Files
        │
        ▼
YAML Extraction
        │
        ▼
Data Cleaning & Validation
        │
        ▼
Pandas Data Processing
        │
        ▼
MySQL Database
        │
        ▼
SQLAlchemy Data Access Layer
        │
        ▼
Analytics Engine
        │
        ├── Market Analysis
        ├── Return Analysis
        ├── Volatility Analysis
        ├── Correlation Analysis
        ├── Monthly Analysis
        └── Sector Analysis
        │
        ▼
Streamlit + Plotly Dashboard
"""
)


# ============================================================
# TECHNOLOGY STACK
# ============================================================

st.markdown("---")

st.header("🛠️ Technology Stack")


tech1, tech2, tech3 = st.columns(3)


with tech1:

    st.subheader("Data Engineering")

    st.write(
        """
        • Python  
        • Pandas  
        • YAML  
        • Data Cleaning  
        • ETL Processing
        """
    )


with tech2:

    st.subheader("Database")

    st.write(
        """
        • MySQL  
        • SQL  
        • SQLAlchemy  
        • Relational Data Modeling  
        • Query Processing
        """
    )


with tech3:

    st.subheader("Analytics & UI")

    st.write(
        """
        • Streamlit  
        • Plotly  
        • Statistical Analysis  
        • Financial Analytics  
        • Interactive Visualization
        """
    )


# ============================================================
# DATABASE STATUS
# ============================================================

st.markdown("---")

st.header("🟢 System Status")


s1, s2, s3 = st.columns(3)


s1.success("MySQL Connected")

s2.success("Dataset Loaded")

s3.success("Analytics Ready")


# ============================================================
# SAMPLE DATABASE DATA
# ============================================================

with st.expander("🗄️ Preview Database Records"):

    preview = stock_data[
        [
            "ticker",
            "trade_date",
            "open_price",
            "high_price",
            "low_price",
            "close_price",
            "volume",
        ]
    ].head(20)

    st.dataframe(
        preview,
        width="stretch",
        hide_index=True,
    )


# ============================================================
# COMPANY SUMMARY
# ============================================================

with st.expander("🏢 Preview Company Summary"):

    st.dataframe(
        company_summary.head(20),
        width="stretch",
        hide_index=True,
    )


# ============================================================
# PROJECT INFORMATION
# ============================================================

st.markdown("---")

st.header("💼 Project Overview")

st.markdown(
    """
    **Project:** Data-Driven Stock Analysis: Organizing, Cleaning
    and Visualizing Market Trends

    **Domain:** Finance / Data Analytics

    **Objective:** Build an end-to-end analytical application
    capable of processing historical Nifty 50 market data,
    storing structured information in MySQL and generating
    interactive financial insights.

    The application demonstrates a complete workflow from
    **raw data → cleaning → SQL storage → statistical analysis
    → interactive visualization**.
    """
)


# ============================================================
# DISCLAIMER
# ============================================================

st.info(
    "ℹ️ This dashboard is an educational data analytics project "
    "based on historical market data. It does not provide "
    "financial or investment advice."
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Nifty 50 Stock Analytics Platform | "
    "Developed by Anirudh R K | "
    "Python • Pandas • MySQL • SQLAlchemy • Plotly • Streamlit"
)