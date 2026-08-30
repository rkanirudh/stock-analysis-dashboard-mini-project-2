📈 Data-Driven Stock Analysis Dashboard

Executive Summary

This project is a Data-Driven Stock Analysis Platform designed to organize, analyze, and visualize historical market data for Nifty 50 constituent stocks.

The project combines Python, Pandas, SQLAlchemy, Streamlit, Plotly, and Microsoft Power BI.

The dataset contains 14,200 daily stock records covering 50 Nifty 50 companies, with historical data from October 2023 to November 2024.

The project provides:

A Python + Streamlit analytics application

A Microsoft Power BI interactive dashboard

📊 Project Objectives

The main objective is to transform raw stock-market data into meaningful financial insights.

The analysis includes:

Stock price trends

Daily market movements

Moving averages

Monthly performance

Yearly returns

Stock volatility

Risk vs. return analysis

Sector-level analysis

Trading volume analysis

Top gainers and losers

Stock return correlations

🗂️ Project Structure

stock-analysis-dashboard-mini-project-2/
│
├── analysis/
├── data/
│   ├── extracted_csv/
│   └── processed/
│       └── cleaned_stock.csv
├── database/
│   ├── connection.py
│   ├── fetch_data.py
│   ├── insert_data.py
│   └── __init__.py
├── extraction/
├── notebooks/
├── powerbi/
│   └── Stock_Analysis12.pbix
├── reports/
├── streamlit_app/
│   ├── app.py
│   └── pages/
├── utils/
├── visualization/
├── config.py
├── logger.py
├── main.py
├── requirements.txt
├── test_connection.py
└── README.md

📁 Dataset

The project uses historical stock-market data for 50 Nifty 50 companies.

Metric

Value

Companies

50

Total Records

14,200

Start Date

2023-10-03

End Date

2024-11-22

Processed dataset:

data/processed/cleaned_stock.csv

Individual company datasets:

data/extracted_csv/

📈 Power BI Dashboard

The completed Power BI dashboard is available at:

powerbi/Stock_Analysis12.pbix

The .pbix file contains the completed Power BI report, data model, calculations, relationships, filters, and visualizations.

Dashboard Pages

1. Executive Dashboard

Total Companies

Total Records

Average Closing Price

Average Yearly Return

Top 10 Gainers

Top 10 Losers

Overall Market Summary

2. Stock Analysis

Stock/Ticker selection

Date filtering

Closing price analysis

20-Day Moving Average

50-Day Moving Average

Volatility

Interactive price trend analysis

3. Sector Analysis

Companies by sector

Average closing price by sector

Average trading volume by sector

Sector comparison

4. Monthly Analysis

Monthly closing-price trends

Monthly trading volume

Average monthly close

Monthly performance comparison

5. Risk & Correlation

Risk vs. Return analysis

Stock volatility ranking

Yearly return comparison

Stock correlation analysis

Cross-stock Pearson correlation matrix

🖥️ Streamlit Application

Main application:

streamlit_app/app.py

Run on macOS / Linux

source venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app/app.py

Run on Windows

venv\Scriptsctivate
pip install -r requirements.txt
streamlit run streamlit_app/app.py

🗄️ Database

Database-related components are located in:

database/
├── connection.py
├── fetch_data.py
└── insert_data.py

The data-fetching workflow supports the processed CSV dataset used by the analytics application.

🧹 Data Processing Pipeline

Raw Stock Data
      ↓
Data Extraction
      ↓
Data Cleaning
      ↓
Data Transformation
      ↓
Processed Dataset
      ↓
Exploratory Data Analysis
      ↓
Financial Analysis
      ↓
Visualization
      ↓
Streamlit + Power BI

The processed dataset contains:

Ticker

Open Price

High Price

Low Price

Close Price

Volume

Trade Date

Month

📊 Analytical Techniques

Moving Averages

MA20

MA50

Returns

Daily and yearly returns are analyzed to understand stock performance.

Volatility

Volatility is used as a measure of stock price risk.

Risk vs Return

Stocks are compared based on risk/volatility and investment return.

Correlation

Pearson correlation is used to identify relationships between stock returns.

Sector Analysis

Companies are grouped and compared at the sector level.

🛠️ Technologies Used

Technology

Purpose

Python

Data processing and analytics

Pandas

Data manipulation

NumPy

Numerical computation

SQLAlchemy

Database connectivity

MySQL

Data storage

Streamlit

Interactive Python dashboard

Plotly

Interactive visualizations

Power BI

Business intelligence dashboard

Jupyter Notebook

Exploratory analysis

Git & GitHub

Version control

📌 Power BI Report

The completed Power BI report is:

powerbi/Stock_Analysis12.pbix

Open the file using Power BI Desktop on Windows to view and interact with the complete dashboard.

Note: .pbix is the native Power BI Desktop report format.

🔒 Git Ignore

The repository excludes unnecessary generated and environment-specific files:

__pycache__/
*.pyc
*.pyo
*.pyd

venv/
.venv/

.env
*.env

.DS_Store
**/.DS_Store

logs/
*.log

.ipynb_checkpoints/

.vscode/
.idea/

👨‍💻 Author

Anirudh R K

Data Analytics / Python / Power BI Project

🎯 Project Outcome

This project demonstrates an end-to-end data analytics workflow:

Data Collection
      ↓
Data Cleaning
      ↓
Data Processing
      ↓
Exploratory Data Analysis
      ↓
Financial Analysis
      ↓
Interactive Visualization
      ↓
Streamlit Dashboard
      ↓
Power BI Dashboard

The final result is an interactive stock-market analytics solution for exploring Nifty 50 stock performance, trends, risk, returns, sectors, trading volume, and correlations.