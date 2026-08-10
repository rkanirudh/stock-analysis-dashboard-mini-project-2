# Power BI Data Dictionary - Stock Analysis Dashboard

## Overview
This document provides a comprehensive data dictionary for all 11 CSV datasets and dimension models supporting the **Data-Driven Stock Analysis Power BI Dashboard**. It outlines column metadata, Power BI data types, null counts, business descriptions, and primary/foreign key classifications.

---

## Workspace Datasets Summary

| Dataset / Table Name | Row Count | Column Count | Primary Key / Foreign Keys | Description |
| :--- | :--- | :--- | :--- | :--- |
| `dim_company` | 50 | 3 | `ticker` (PK) | Master ticker dimension with company name and sector mapping |
| `daily_return` | 14,200 | 4 | (`ticker`, `trade_date`) (PK) | Fact table containing daily closing prices and percentage daily returns |
| `moving_average` | 14,200 | 5 | (`ticker`, `trade_date`) (PK) | Fact table containing 20-day (MA20) and 50-day (MA50) moving averages |
| `risk_return_analysis` | 50 | 3 | `ticker` (FK to `dim_company`) | Calculated annualized risk (volatility %) and return summary per ticker |
| `yearly_return` | 50 | 4 | `ticker` (FK to `dim_company`) | First close, last close, and total yearly percentage return per ticker |
| `volatility` | 50 | 3 | `ticker` (FK to `dim_company`) | Daily standard deviation / volatility coefficient per ticker |
| `sector_analysis` | 20 | 4 | `sector` (PK) | Aggregated close price, trading volume, and company count per sector |
| `monthly_analysis` | 12 | 4 | `month_number` (PK) | Average closing price and average trading volume aggregated by month |
| `correlation_matrix` | 50 | 51 | `ticker` (PK) | Cross-asset daily return correlation matrix for all 50 Nifty 50 stocks |
| `top_gainers` | 10 | 2 | `Ticker` (FK to `dim_company`) | Top 10 performing stocks ranked by highest yearly percentage return |
| `top_losers` | 10 | 2 | `Ticker` (FK to `dim_company`) | Top 10 worst performing stocks ranked by lowest yearly percentage return |
| `market_summary` | 8 | 2 | `Metric` (PK) | High-level system metadata metrics and summary indicators |

---

## Detailed Data Dictionaries

### 1. `Dim_Company` (Master Dimension)
- **Source**: Constructed from dataset tickers and Nifty 50 sector mapping.
- **Granularity**: One record per stock ticker.

| Column Name | Power BI Data Type | M Type | Description | Null Count | Key Type | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ticker` | Text | `type text` | Unique stock symbol / ticker (e.g., RELIANCE, TCS) | 0 | Primary Key | `RELIANCE` |
| `company_name` | Text | `type text` | Full commercial company name | 0 | Attribute | `Reliance Industries Ltd.` |
| `sector` | Text | `type text` | Industry sector classification | 0 | Foreign Key | `Energy` |

---

### 2. `Fact_DailyReturn` (`daily_return.csv`)
- **Source**: `./reports/daily_return.csv`
- **Granularity**: Daily stock observation (Ticker + Date). Total rows: 14,200 (50 tickers × 284 trading days).

| Column Name | Power BI Data Type | M Type | Description | Null Count | Key Type | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ticker` | Text | `type text` | Stock ticker symbol | 0 | Foreign Key | `ADANIENT` |
| `trade_date` | Date | `type date` | Trading date (YYYY-MM-DD) | 0 | Foreign Key | `2023-10-03` |
| `close_price` | Fixed Decimal (Currency) | `Currency.Type` | Daily adjusted closing price in INR (₹) | 0 | Fact Measure | `2387.25` |
| `Daily_Return (%)` | Percentage / Decimal | `Percentage.Type` | Percentage change in close price relative to previous trading day | 50 | Fact Measure | `3.25%` (0.0325) |

*Note: The 50 null values in `Daily_Return (%)` correspond to the baseline first trading day for each of the 50 stocks (no prior closing price to compute return).*

---

### 3. `Fact_MovingAverage` (`moving_average.csv`)
- **Source**: `./reports/moving_average.csv`
- **Granularity**: Daily stock observation (Ticker + Date). Total rows: 14,200.

| Column Name | Power BI Data Type | M Type | Description | Null Count | Key Type | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ticker` | Text | `type text` | Stock ticker symbol | 0 | Foreign Key | `ADANIENT` |
| `trade_date` | Date | `type date` | Trading date (YYYY-MM-DD) | 0 | Foreign Key | `2023-10-03` |
| `close_price` | Fixed Decimal (Currency) | `Currency.Type` | Daily closing price in INR | 0 | Fact Measure | `2387.25` |
| `MA20` | Fixed Decimal (Currency) | `Currency.Type` | 20-day Simple Moving Average of close price | 950 | Fact Measure | `2393.57` |
| `MA50` | Fixed Decimal (Currency) | `Currency.Type` | 50-day Simple Moving Average of close price | 2,450 | Fact Measure | `2397.83` |

*Note: Null values occur during initial warmup window periods (first 19 trading days for MA20 = 50 × 19 = 950 nulls; first 49 trading days for MA50 = 50 × 49 = 2,450 nulls).*

---

### 4. `Risk_Return_Analysis` (`risk_return_analysis.csv`)
- **Source**: `./reports/risk_return_analysis.csv`
- **Granularity**: One record per stock ticker (50 rows).

| Column Name | Power BI Data Type | M Type | Description | Null Count | Key Type | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ticker` | Text | `type text` | Stock ticker symbol | 0 | Primary Key / Foreign Key | `TRENT` |
| `Yearly_Return` | Percentage / Decimal | `Percentage.Type` | Total percentage return over the 1-year analysis period | 0 | Metric | `223.09%` (223.09) |
| `Volatility` | Percentage / Decimal | `Percentage.Type` | Annualized daily return volatility percentage | 0 | Metric | `2.31%` (2.31) |

---

### 5. `Yearly_Return` (`yearly_return.csv`)
- **Source**: `./reports/yearly_return.csv`
- **Granularity**: One record per stock ticker (50 rows).

| Column Name | Power BI Data Type | M Type | Description | Null Count | Key Type | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ticker` | Text | `type text` | Stock ticker symbol | 0 | Primary Key / Foreign Key | `TRENT` |
| `First Close` | Fixed Decimal (Currency) | `Currency.Type` | Stock close price on the first trading day of the dataset period | 0 | Metric | `2059.10` |
| `Last Close` | Fixed Decimal (Currency) | `Currency.Type` | Stock close price on the last trading day of the dataset period | 0 | Metric | `6652.80` |
| `Yearly Return (%)` | Percentage / Decimal | `Percentage.Type` | Calculated net percentage return over the period | 0 | Metric | `223.09%` |

---

### 6. `Volatility` (`volatility.csv`)
- **Source**: `./reports/volatility.csv`
- **Granularity**: One record per stock ticker (50 rows).

| Column Name | Power BI Data Type | M Type | Description | Null Count | Key Type | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Unnamed: 0` | Whole Number | `Int64.Type` | Original row index (Removed in Power Query transformation) | 0 | Index (Drop) | `0` |
| `ticker` | Text | `type text` | Stock ticker symbol | 0 | Primary Key / Foreign Key | `ADANIENT` |
| `volatility` | Decimal Number | `type number` | Standard deviation of daily returns (expressed as standard decimal) | 0 | Metric | `0.0286` (2.86%) |

---

### 7. `Sector_Analysis` (`sector_analysis.csv`)
- **Source**: `./reports/sector_analysis.csv`
- **Granularity**: One record per industry sector (20 rows).

| Column Name | Power BI Data Type | M Type | Description | Null Count | Key Type | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `sector` | Text | `type text` | Industry sector name | 0 | Primary Key | `Cement` |
| `Companies` | Whole Number | `Int64.Type` | Count of Nifty 50 constituent companies in sector | 0 | Attribute | `2` |
| `Average_Close` | Fixed Decimal (Currency) | `Currency.Type` | Average closing price across sector constituents | 0 | Metric | `6310.31` |
| `Average_Volume` | Decimal Number / Int | `type number` | Average daily trading volume across sector constituents | 0 | Metric | `576606.57` |

---

### 8. `Monthly_Analysis` (`monthly_analysis.csv`)
- **Source**: `./reports/monthly_analysis.csv`
- **Granularity**: One record per calendar month (12 rows).

| Column Name | Power BI Data Type | M Type | Description | Null Count | Key Type | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `month_number` | Whole Number | `Int64.Type` | Calendar month index (1 to 12) | 0 | Primary Key | `1` |
| `month_name` | Text | `type text` | Calendar month name (January through December) | 0 | Attribute | `January` |
| `average_close_price` | Fixed Decimal (Currency) | `Currency.Type` | Average closing price across all stocks in month | 0 | Metric | `2290.99` |
| `average_volume` | Whole Number | `Int64.Type` | Average trading volume across all stocks in month | 0 | Metric | `7019825` |

---

### 9. `Correlation_Matrix` (`correlation_matrix.csv`)
- **Source**: `./reports/correlation_matrix.csv`
- **Granularity**: 50 × 50 matrix of stock-to-stock daily return Pearson correlation coefficients.

| Column Name | Power BI Data Type | M Type | Description | Null Count | Key Type | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ticker` | Text | `type text` | Reference stock ticker symbol | 0 | Primary Key | `ADANIENT` |
| `[ADANIENT ... WIPRO]` (50 cols) | Decimal Number | `type number` | Pearson correlation coefficient ranging from -1.0 to +1.0 | 0 | Matrix Values | `0.85` |

---

### 10. `Top_Gainers` (`top_gainers.csv`) & `Top_Losers` (`top_losers.csv`)
- **Source**: `./reports/top_gainers.csv` and `./reports/top_losers.csv`
- **Granularity**: Top 10 ranked records (10 rows each).

| Column Name | Power BI Data Type | M Type | Description | Null Count | Key Type | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Ticker` | Text | `type text` | Stock ticker symbol | 0 | Foreign Key | `TRENT` / `INDUSINDBK` |
| `Yearly_Return` | Percentage / Decimal | `Percentage.Type` | Yearly return percentage | 0 | Metric | `223.09%` / `-30.46%` |

---

### 11. `Market_Summary` (`market_summary.csv`)
- **Source**: `./reports/market_summary.csv`
- **Granularity**: Key-value summary pairs (8 rows).

| Column Name | Power BI Data Type | M Type | Description | Null Count | Key Type | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Metric` | Text | `type text` | Summary indicator name | 0 | Key | `Total Records` |
| `Value` | Text | `type text` | String/Numeric value of indicator | 0 | Value | `14200` |
