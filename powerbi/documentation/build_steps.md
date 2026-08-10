# Step-by-Step Power BI Desktop Build Guide

## Overview
This guide provides explicit, end-to-end instructions for creating the complete **Data-Driven Stock Analysis Power BI Report (`Stock_Analysis_Dashboard.pbix`)** in **Microsoft Power BI Desktop**.

---

## Phase 1: Launch & Environment Setup

1. Open **Microsoft Power BI Desktop**.
2. Click **File** > **Options and settings** > **Options**.
3. Under **Current File** > **Data Load**:
   - Ensure **Autodetect new relationships after data is loaded** is turned **OFF** (to allow manual control over relationship creation).
   - Set **Locale for regional settings** to `English (United States)` or `English (India)`.
4. Click **OK**.

---

## Phase 2: Import Datasets via Power Query (M Scripts)

1. On the **Home** tab, click **Transform Data** to open the **Power Query Editor**.
2. For each of the 12 datasets, follow this exact workflow to import:
   - Click **New Source** > **Blank Query**.
   - Click **Advanced Editor** on the ribbon.
   - Replace the default code snippet with the complete M query content from the corresponding `.m` file in `powerbi/power_query/`:
     - `dim_company` -> Load from `powerbi/power_query/dim_company.m`
     - `daily_return` -> Load from `powerbi/power_query/daily_return.m`
     - `moving_average` -> Load from `powerbi/power_query/moving_average.m`
     - `risk_return_analysis` -> Load from `powerbi/power_query/risk_return_analysis.m`
     - `yearly_return` -> Load from `powerbi/power_query/yearly_return.m`
     - `volatility` -> Load from `powerbi/power_query/volatility.m`
     - `sector_analysis` -> Load from `powerbi/power_query/sector_analysis.m`
     - `monthly_analysis` -> Load from `powerbi/power_query/monthly_analysis.m`
     - `correlation_matrix` -> Load from `powerbi/power_query/correlation_matrix.m`
     - `top_gainers` -> Load from `powerbi/power_query/top_gainers.m`
     - `top_losers` -> Load from `powerbi/power_query/top_losers.m`
     - `market_summary` -> Load from `powerbi/power_query/market_summary.m`
   - *Note*: Ensure the `FilePath` string in each M script points to the exact absolute directory path of your CSV files on your system.
3. Click **Done**.
4. Rename each Query in the left pane to match the model table names (`Dim_Company`, `Fact_DailyReturn`, `Fact_MovingAverage`, etc.).
5. Click **Close & Apply** on the top left ribbon.

---

## Phase 3: Build Calendar Dimension (`Dim_Date`)

1. In Report or Data view, click **New Table** on the **Modeling** tab.
2. Enter the following DAX formula to create a dedicated Calendar dimension:

```dax
Dim_Date = 
VAR MinDate = MIN(Fact_DailyReturn[TradeDate])
VAR MaxDate = MAX(Fact_DailyReturn[TradeDate])
RETURN
ADDCOLUMNS(
    CALENDAR(MinDate, MaxDate),
    "Year", YEAR([Date]),
    "MonthNo", MONTH([Date]),
    "MonthName", FORMAT([Date], "MMMM"),
    "MonthShort", FORMAT([Date], "MMM"),
    "Quarter", "Q" & FORMAT([Date], "Q"),
    "DayOfWeek", FORMAT([Date], "DDD"),
    "IsTradingDay", IF(WEEKDAY([Date], 2) <= 5, 1, 0)
)
```

3. Select `MonthName` column, go to **Column tools** tab, and click **Sort by column** > **MonthNo**.

---

## Phase 4: Create Data Model Relationships

1. Switch to **Model View** (left side icon).
2. Create the following relationships by dragging fields between tables:

| Primary Table (1) | Primary Field | Foreign Table (*) | Foreign Field | Cardinality | Cross Filter Direction |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Dim_Company` | `Ticker` | `Fact_DailyReturn` | `Ticker` | 1 to Many (`1:*`) | Single |
| `Dim_Company` | `Ticker` | `Fact_MovingAverage` | `Ticker` | 1 to Many (`1:*`) | Single |
| `Dim_Date` | `Date` | `Fact_DailyReturn` | `TradeDate` | 1 to Many (`1:*`) | Single |
| `Dim_Date` | `Date` | `Fact_MovingAverage` | `TradeDate` | 1 to Many (`1:*`) | Single |
| `Dim_Company` | `Ticker` | `Risk_Return_Analysis` | `Ticker` | 1 to 1 (`1:1`) | Both |
| `Dim_Company` | `Ticker` | `Yearly_Return` | `Ticker` | 1 to 1 (`1:1`) | Both |
| `Dim_Company` | `Ticker` | `Volatility` | `Ticker` | 1 to 1 (`1:1`) | Both |
| `Sector_Analysis` | `Sector` | `Dim_Company` | `Sector` | 1 to Many (`1:*`) | Single |
| `Dim_Company` | `Ticker` | `Top_Gainers` | `Ticker` | 1 to Many (`1:*`) | Single |
| `Dim_Company` | `Ticker` | `Top_Losers` | `Ticker` | 1 to Many (`1:*`) | Single |
| `Dim_Company` | `Ticker` | `Correlation_Matrix` | `Ticker` | 1 to 1 (`1:1`) | Both |

---

## Phase 5: Add DAX Measures

1. On the **Home** tab, click **Enter Data** to create an empty table named `Key Measures`.
2. Delete `Column1` from `Key Measures`.
3. Right-click `Key Measures` and select **New Measure**.
4. Open `powerbi/dax/measures.dax` and copy/paste each measure formula into the DAX formula bar:
   - `Total Companies`
   - `Total Records`
   - `Average Closing Price`
   - `Average Trading Volume`
   - `Highest Stock Price`
   - `Lowest Stock Price`
   - `Average Daily Return`
   - `Average Volatility`
   - `Average Yearly Return`
   - `Selected Stock Close`
   - `Selected MA20`
   - `Selected MA50`
   - `Selected Stock Volatility`
   - `Selected Stock Yearly Return`
   - `Top Gainer Ticker` & `Top Gainer Return`
   - `Top Loser Ticker` & `Top Loser Return`
5. Apply appropriate formatting (Currency `₹#,##0.00`, Percentage `0.00%`, Integer `#,##0`) to each measure via **Measure tools**.

---

## Phase 6: Apply Power BI Custom Theme

1. Go to the **View** tab on the top ribbon.
2. In the **Themes** section, click the dropdown menu and select **Browse for themes**.
3. Navigate to `powerbi/theme/finance_theme.json` in this workspace.
4. Select the file and click **Open**.
5. Confirm success message: *"Theme imported successfully"*.

---

## Phase 7: Build Report Pages

Create 5 report pages matching `powerbi/report_design/dashboard_spec.md`:

### Page 1: Executive Dashboard
- Rename page tab to `Executive Dashboard`.
- Add 4 Top Card Visuals: `[Total Companies]`, `[Total Records]`, `[Average Closing Price]`, `[Average Yearly Return]`.
- Add Horizontal Bar Chart for **Top 10 Gainers** (`Top_Gainers[Ticker]`, `Top_Gainers[YearlyReturnPct]`).
- Add Horizontal Bar Chart for **Top 10 Losers** (`Top_Losers[Ticker]`, `Top_Losers[YearlyReturnPct]`).
- Add Table Visual for **Market Summary** (`Market_Summary[Metric]`, `Market_Summary[Value]`).

### Page 2: Stock Analysis
- Rename page tab to `Stock Analysis`.
- Add Slicer for `Dim_Company[Ticker]` (Dropdown style with Search box enabled).
- Add 4 Cards for `[Selected Stock Close]`, `[Selected MA20]`, `[Selected MA50]`, `[Selected Stock Volatility]`.
- Add Line Chart:
  - X-Axis: `Fact_MovingAverage[TradeDate]`
  - Y-Axis: `Fact_MovingAverage[ClosePrice]`, `Fact_MovingAverage[MA20]`, `Fact_MovingAverage[MA50]`.

### Page 3: Sector Analysis
- Rename page tab to `Sector Analysis`.
- Add Bar Chart: `Sector_Analysis[Sector]` vs `Sector_Analysis[CompanyCount]`.
- Add Column Chart: `Sector_Analysis[Sector]` vs `Sector_Analysis[AverageClose]`.
- Add Column Chart: `Sector_Analysis[Sector]` vs `Sector_Analysis[AverageVolume]`.
- Add Matrix Table for Sector Comparison.

### Page 4: Monthly Analysis
- Rename page tab to `Monthly Analysis`.
- Add Line & Stacked Column Combo Chart:
  - Shared X-Axis: `Monthly_Analysis[MonthName]`
  - Column Values: `Monthly_Analysis[AverageVolume]`
  - Line Values: `Monthly_Analysis[AverageClose]`.
- Add Column Chart for Monthly Average Close.
- Add Matrix Table for Monthly Breakdown.

### Page 5: Risk & Correlation
- Rename page tab to `Risk & Correlation`.
- Add Scatter Plot:
  - X-Axis: `Risk_Return_Analysis[VolatilityPct]`
  - Y-Axis: `Risk_Return_Analysis[YearlyReturnPct]`
  - Details: `Dim_Company[Ticker]`.
- Add Bar Chart for Volatility Ranking (`Volatility[Ticker]` vs `Volatility[Volatility]`).
- Add Matrix Heatmap for Correlation Matrix (`Correlation_Matrix[Ticker]` vs all stock columns).

---

## Phase 8: Save & Validate

1. Click **File** > **Save As**.
2. Save as `Stock_Analysis_Dashboard.pbix` in your project folder.
3. Validate that cross-filtering works seamlessly when switching tickers and selecting sectors.
