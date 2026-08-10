# Data-Driven Stock Analysis: Power BI Solution & Analytics Platform

## Executive Summary
This repository contains the complete **Microsoft Power BI Analytics Platform & Architecture** for **Data-Driven Stock Analysis: Organizing, Cleaning, and Visualizing Market Trends**.

The solution analyzes daily market movements, moving averages (MA20/MA50), price volatility, annual percentage returns, cross-asset correlations, and sector performance across **Nifty 50 constituent stocks** (14,200 daily records).

---

## Workspace & Project Folder Structure

```
.
├── reports/                         # Core CSV market datasets (11 files)
│   ├── correlation_matrix.csv
│   ├── daily_return.csv
│   ├── market_summary.csv
│   ├── monthly_analysis.csv
│   ├── moving_average.csv
│   ├── risk_return_analysis.csv
│   ├── sector_analysis.csv
│   ├── top_gainers.csv
│   ├── top_losers.csv
│   ├── volatility.csv
│   └── yearly_return.csv
│
└── powerbi/                         # Power BI Solution Architecture
    ├── assets/                      # Graphic assets & blueprint diagrams
    │
    ├── dax/
    │   └── measures.dax             # Production DAX measure repository (23 measures)
    │
    ├── documentation/
    │   ├── data_dictionary.md       # Comprehensive column metadata, data types, nulls
    │   ├── data_model.md            # Star schema architecture, keys, cardinality
    │   └── build_steps.md           # Step-by-step PBIX build manual for Power BI Desktop
    │
    ├── power_query/                 # 12 Modular Power Query M Scripts
    │   ├── correlation_matrix.m
    │   ├── daily_return.m
    │   ├── dim_company.m            # Dynamic Master Ticker & Sector Dimension
    │   ├── market_summary.m
    │   ├── monthly_analysis.m
    │   ├── moving_average.m
    │   ├── risk_return_analysis.m
    │   ├── sector_analysis.m
    │   ├── top_gainers.m
    │   ├── top_losers.m
    │   ├── volatility.m
    │   └── yearly_return.m
    │
    ├── report_design/
    │   └── dashboard_spec.md        # Layout grid & visual spec for all 5 report pages
    │
    └── theme/
        └── finance_theme.json       # Custom Financial Power BI Theme JSON
```

---

## Power BI Data Model Architecture (Star Schema)

The solution uses a **Star Schema Design** centered around `Dim_Company` and `Dim_Date`:

```
               +--------------------+
               |      Dim_Date      |
               +---------+----------+
                         |
           +-------------+-------------+
           | 1:*                       | 1:*
           v                           v
+------------------+       +-------------------+
| Fact_DailyReturn |       |Fact_MovingAverage |
+------------------+       +-------------------+
           ^                           ^
           | *:1                       | *:1
           +-------------+-------------+
                         |
               +---------+----------+
               |    Dim_Company     |
               +----+----+-----+----+
                    |    |     |
            1:1     |    | 1:1 | 1:1
   +----------------+    |     +----------------+
   |                     v                      |
+--+------------------+ +--+---------------+ +--+-------------------+
| Risk_Return_Analysis| |  Yearly_Return   | |    Volatility        |
+---------------------+ +------------------+ +----------------------+
```

### Relationship Summary

| Parent Table (1) | Child Table (*) | Relationship Type | Cross-Filter Direction | Key Column |
| :--- | :--- | :--- | :--- | :--- |
| `Dim_Company` | `Fact_DailyReturn` | One to Many (`1:*`) | Single | `Ticker` |
| `Dim_Company` | `Fact_MovingAverage` | One to Many (`1:*`) | Single | `Ticker` |
| `Dim_Date` | `Fact_DailyReturn` | One to Many (`1:*`) | Single | `TradeDate` |
| `Dim_Date` | `Fact_MovingAverage` | One to Many (`1:*`) | Single | `TradeDate` |
| `Dim_Company` | `Risk_Return_Analysis` | One to One (`1:1`) | Both | `Ticker` |
| `Dim_Company` | `Yearly_Return` | One to One (`1:1`) | Both | `Ticker` |
| `Dim_Company` | `Volatility` | One to One (`1:1`) | Both | `Ticker` |
| `Sector_Analysis` | `Dim_Company` | One to Many (`1:*`) | Single | `Sector` |

---

## Report Page Architecture (5 Interactive Pages)

1. **Page 1: Executive Dashboard**
   - High-level KPIs: Total Companies, Total Records, Avg Closing Price, Avg Yearly Return.
   - Top 10 Gainers & Top 10 Losers Horizontal Bar Leaderboards.
   - System Market Summary Matrix Table.

2. **Page 2: Stock Analysis (Technical Trends)**
   - Searchable Ticker Slicer & Date Range Slider.
   - Interactive KPI Cards: Current Close, MA20, MA50, Volatility.
   - Technical Price Trend Line Chart displaying Close Price vs 20-Day & 50-Day Moving Averages.

3. **Page 3: Sector Analysis**
   - Companies by Sector Bar Chart.
   - Average Closing Price by Sector Column Chart.
   - Average Daily Trading Volume by Sector Column Chart.
   - Sector Comparative Matrix Grid.

4. **Page 4: Monthly Analysis**
   - Monthly Combo Line & Column Chart (Average Volume Bars + Average Close Navy Line).
   - Monthly Close Price Breakdown Column Chart.
   - Monthly Performance Breakdown Grid.

5. **Page 5: Risk & Correlation**
   - Risk vs Return Scatter Plot (Volatility % vs Yearly Return %).
   - Stock Volatility Ranking Bar Chart.
   - 50 × 50 Cross-Asset Return Pearson Correlation Heatmap Matrix with diverging color scales.

---

## How to Build the PBIX in Power BI Desktop

For complete step-by-step instructions, refer to **[build_steps.md](file:///Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/powerbi/documentation/build_steps.md)**.

### Quick Start Checklist:
1. Open **Microsoft Power BI Desktop**.
2. Go to **Transform Data** (Power Query Editor).
3. Create new Blank Queries and paste the M script content from `powerbi/power_query/*.m` into the **Advanced Editor**.
4. Apply & Load data.
5. In **Model View**, establish the relationships documented in `powerbi/documentation/data_model.md`.
6. Add measures from `powerbi/dax/measures.dax`.
7. Import `powerbi/theme/finance_theme.json` via **View** > **Browse for themes**.
8. Build visuals following `powerbi/report_design/dashboard_spec.md`.
9. Save report as `Stock_Analysis_Dashboard.pbix`.

---

## Documentation Links

- **[Data Dictionary](file:///Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/powerbi/documentation/data_dictionary.md)**: Metadata, null counts, data types.
- **[Data Model Spec](file:///Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/powerbi/documentation/data_model.md)**: Cardinality, filtering logic, ER diagram.
- **[DAX Measures](file:///Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/powerbi/dax/measures.dax)**: Measure code repository.
- **[Visual Specification](file:///Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/powerbi/report_design/dashboard_spec.md)**: Page-by-page visual layouts.
- **[Build Steps Guide](file:///Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/powerbi/documentation/build_steps.md)**: Step-by-step PBIX creation guide.
- **[Finance Theme JSON](file:///Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/powerbi/theme/finance_theme.json)**: Custom Power BI color palette.
