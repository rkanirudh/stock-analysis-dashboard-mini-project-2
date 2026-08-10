# Power BI Dashboard Visual Specification & Report Design

## Overview
This document provides complete layout specs, visual dimensions, chart configurations, field mappings, interaction behavior, and formatting rules for all **5 Report Pages** in the **Data-Driven Stock Analysis Power BI Solution**.

- **Canvas Size**: 16:9 Widescreen (1280 × 720 px)
- **Theme Palette**: Financial Dark Blue (`#0F172A`), Slate (`#1E293B`), Accent Blue (`#0EA5E9`), Gain Green (`#10B981`), Loss Red (`#EF4444`), Muted Gray (`#64748B`).
- **Typography**: Segoe UI / Inter (Bold Headings 14-20pt, Data Values 20-28pt, Labels 9-11pt).

---

## PAGE 1: EXECUTIVE DASHBOARD

### Purpose
High-level market summary for C-suite executives and analysts, featuring market KPIs, top gainers, top losers, and baseline metadata.

```
+-----------------------------------------------------------------------------------+
| HEADER BANNER: NIFTY 50 EXECUTIVE MARKET DASHBOARD | Date Range Slicer            |
+-------------------+-------------------+-------------------+-----------------------+
| KPI CARD 1        | KPI CARD 2        | KPI CARD 3        | KPI CARD 4            |
| Total Companies   | Total Records     | Avg Close Price   | Avg Yearly Return     |
+-------------------+-------------------+-------------------+-----------------------+
| VISUAL 1.1        | VISUAL 1.2        | VISUAL 1.3                                |
| Top 10 Gainers    | Top 10 Losers     | Market Summary Key Metrics Table          |
| (Horizontal Bar)  | (Horizontal Bar)  | (Metric Name | Value | Description)      |
+-------------------+-------------------+-------------------------------------------+
```

### Visual Specifications

#### 1. Header Banner & Slicers
- **Position**: X: 10, Y: 10, W: 1260, H: 60
- **Type**: Header Shape with Text Title + Date Slicer
- **Title**: `Nifty 50 Market Analysis - Executive Overview`

#### 2. Top KPI Cards
- **Card 1 (Total Companies)**: X: 10, Y: 80, W: 300, H: 90 | Measure: `[Total Companies]` | Format: `#`
- **Card 2 (Total Records)**: X: 325, Y: 80, W: 300, H: 90 | Measure: `[Total Records]` | Format: `#,##0`
- **Card 3 (Avg Close Price)**: X: 640, Y: 80, W: 300, H: 90 | Measure: `[Average Closing Price]` | Format: `₹#,##0.00`
- **Card 4 (Avg Yearly Return)**: X: 955, Y: 80, W: 315, H: 90 | Measure: `[Average Yearly Return]` | Format: `+0.00%` (Color: Green if >0)

#### 3. Visual 1.1: Top 10 Gainers Bar Chart
- **Position**: X: 10, Y: 185, W: 400, H: 515
- **Visual Type**: Clustered Horizontal Bar Chart
- **Y-Axis**: `Top_Gainers[Ticker]` (Sorted by `YearlyReturnPct` Descending)
- **X-Axis**: `Top_Gainers[YearlyReturnPct]`
- **Data Color**: Emerald Green (`#10B981`)
- **Data Labels**: On (Format: `0.0%`)
- **Title**: `Top 10 Gainer Stocks (1-Year Return %)`

#### 4. Visual 1.2: Top 10 Losers Bar Chart
- **Position**: X: 425, Y: 185, W: 400, H: 515
- **Visual Type**: Clustered Horizontal Bar Chart
- **Y-Axis**: `Top_Losers[Ticker]` (Sorted by `YearlyReturnPct` Ascending)
- **X-Axis**: `Top_Losers[YearlyReturnPct]`
- **Data Color**: Crimson Red (`#EF4444`)
- **Data Labels**: On (Format: `0.0%`)
- **Title**: `Top 10 Loser Stocks (1-Year Return %)`

#### 5. Visual 1.3: Market Summary Table
- **Position**: X: 840, Y: 185, W: 430, H: 515
- **Visual Type**: Grid Matrix / Table Visual
- **Values**: `Market_Summary[Metric]`, `Market_Summary[Value]`
- **Formatting**: Alternating row shading (Slate Gray background), bold metric names.
- **Title**: `Market Summary & Dataset Indicators`

---

## PAGE 2: STOCK ANALYSIS (TECHNICAL PRICE TRENDS)

### Purpose
Deep-dive single-stock analysis featuring interactive ticker selection, moving averages (MA20/MA50), daily returns, and price volatility.

```
+-----------------------------------------------------------------------------------+
| SLICER: Select Ticker (Dropdown/Searchable) | Date Range Filter                   |
+-------------------+-------------------+-------------------+-----------------------+
| KPI CARD: Close   | KPI CARD: MA20    | KPI CARD: MA50    | KPI CARD: Volatility  |
| [Selected Close]  | [Selected MA20]   | [Selected MA50]   | [Selected Volatility] |
+-------------------+-------------------+-------------------+-----------------------+
| MAIN LINE CHART                                                                   |
| X-Axis: TradeDate                                                                 |
| Y-Axis: Close Price (Solid Blue), MA20 (Orange), MA50 (Purple)                   |
| Tooltips: TradeDate, Close, MA20, MA50, Daily Return %                            |
+-----------------------------------------------------------------------------------+
```

### Visual Specifications

#### 1. Slicer Controls
- **Ticker Slicer**: X: 10, Y: 10, W: 400, H: 60 | Field: `Dim_Company[Ticker]` (Single-select dropdown with Search bar enabled).
- **Date Range Slicer**: X: 425, Y: 10, W: 845, H: 60 | Field: `Dim_Date[Date]` (Between Slider).

#### 2. Selected Stock KPI Cards
- **Close Price Card**: X: 10, Y: 80, W: 300, H: 90 | Measure: `[Selected Stock Close]` | Title: `Current Close Price`
- **MA20 Card**: X: 325, Y: 80, W: 300, H: 90 | Measure: `[Selected MA20]` | Title: `20-Day Moving Average`
- **MA50 Card**: X: 640, Y: 80, W: 300, H: 90 | Measure: `[Selected MA50]` | Title: `50-Day Moving Average`
- **Volatility Card**: X: 955, Y: 80, W: 315, H: 90 | Measure: `[Selected Stock Volatility]` | Title: `Annualized Volatility`

#### 3. Main Trend Line Chart
- **Position**: X: 10, Y: 185, W: 1260, H: 515
- **Visual Type**: Line Chart
- **X-Axis**: `Fact_MovingAverage[TradeDate]` (Continuous Date hierarchy)
- **Y-Axis Values**:
  1. `Fact_MovingAverage[ClosePrice]` (Stroke: Solid, Color: `#0EA5E9`, Width: 3px)
  2. `Fact_MovingAverage[MA20]` (Stroke: Dashed, Color: `#F59E0B`, Width: 2px)
  3. `Fact_MovingAverage[MA50]` (Stroke: Dotted, Color: `#8B5CF6`, Width: 2px)
- **Tooltips**: `Fact_DailyReturn[DailyReturnPct]`, `Fact_DailyReturn[ClosePrice]`
- **Title**: `Stock Price Trend vs 20-Day & 50-Day Moving Averages`

---

## PAGE 3: SECTOR ANALYSIS

### Purpose
Comparative analysis of sector representation, average close price, trading volume, and company distribution across sectors.

```
+-----------------------------------------------------------------------------------+
| HEADER: SECTOR PERFORMANCE & CONSTITUENT DISTRIBUTION                              |
+-----------------------------------+-----------------------------------------------+
| VISUAL 3.1                        | VISUAL 3.2                                    |
| Companies by Sector               | Average Closing Price by Sector               |
| (Horizontal Bar Chart)            | (Clustered Column Chart)                      |
+-----------------------------------+-----------------------------------------------+
| VISUAL 3.3                        | VISUAL 3.4                                    |
| Average Trading Volume by Sector  | Sector Performance Grid                       |
| (Clustered Column Chart)          | (Sector | Companies | Avg Close | Avg Volume) |
+-----------------------------------+-----------------------------------------------+
```

### Visual Specifications

#### 1. Visual 3.1: Companies by Sector
- **Position**: X: 10, Y: 80, W: 615, H: 300
- **Visual Type**: Horizontal Clustered Bar Chart
- **Y-Axis**: `Sector_Analysis[Sector]` (Sorted by `CompanyCount` Descending)
- **X-Axis**: `Sector_Analysis[CompanyCount]`
- **Color**: Slate Blue (`#1E293B`)
- **Title**: `Number of Constituent Companies by Sector`

#### 2. Visual 3.2: Average Close Price by Sector
- **Position**: X: 640, Y: 80, W: 630, H: 300
- **Visual Type**: Vertical Clustered Column Chart
- **X-Axis**: `Sector_Analysis[Sector]`
- **Y-Axis**: `Sector_Analysis[AverageClose]`
- **Format**: `₹#,##0.00`
- **Color**: Teal Blue (`#0284C7`)
- **Title**: `Average Stock Closing Price by Sector (INR ₹)`

#### 3. Visual 3.3: Average Trading Volume by Sector
- **Position**: X: 10, Y: 395, W: 615, H: 305
- **Visual Type**: Vertical Clustered Column Chart
- **X-Axis**: `Sector_Analysis[Sector]`
- **Y-Axis**: `Sector_Analysis[AverageVolume]`
- **Format**: `#,##0` (In Millions / Thousands)
- **Color**: Purple Accent (`#7C3AED`)
- **Title**: `Average Daily Trading Volume by Sector`

#### 4. Visual 3.4: Sector Performance Grid
- **Position**: X: 640, Y: 395, W: 630, H: 305
- **Visual Type**: Table / Matrix Visual
- **Rows**: `Sector_Analysis[Sector]`
- **Values**: `[Total Companies]`, `[Average Closing Price]`, `[Average Trading Volume]`
- **Title**: `Sector Comparative Performance Matrix`

---

## PAGE 4: MONTHLY ANALYSIS

### Purpose
Seasonal performance evaluation mapping monthly average closing prices, trading volume fluctuations, and month-over-month price trends.

```
+-----------------------------------------------------------------------------------+
| HEADER: MONTHLY PRICE TRENDS & VOLUME DYNAMICS                                    |
+-----------------------------------------------------------------------------------+
| VISUAL 4.1: COMBO CHART (MONTHLY CLOSE & VOLUME TREND)                           |
| Shared X-Axis: MonthName (Ordered January to December via MonthNumber)            |
| Column Y-Axis: AverageVolume (Light Blue Bars)                                    |
| Line Y-Axis: AverageClose (Dark Navy Line with Data Markers)                      |
+-----------------------------------+-----------------------------------------------+
| VISUAL 4.2                        | VISUAL 4.3                                    |
| Monthly Closing Price Bar Chart   | Monthly Performance Grid                      |
| (Column Chart sorted chronologically)| (Month | Avg Close | Avg Volume | YoY Trend)|
+-----------------------------------+-----------------------------------------------+
```

### Visual Specifications

#### 1. Visual 4.1: Monthly Combo Line & Column Chart
- **Position**: X: 10, Y: 80, W: 1260, H: 330
- **Visual Type**: Line and Stacked Column Chart
- **Shared X-Axis**: `Monthly_Analysis[MonthName]` (Sort column set to `Monthly_Analysis[MonthNumber]` Ascending)
- **Column Values**: `Monthly_Analysis[AverageVolume]` (Color: Light Cyan `#38BDF8`, Transparency: 30%)
- **Line Values**: `Monthly_Analysis[AverageClose]` (Color: Dark Navy `#0F172A`, Line width: 3px, Markers: On)
- **Title**: `Monthly Average Close Price vs Average Volume Trend`

#### 2. Visual 4.2: Monthly Close Price Breakdown
- **Position**: X: 10, Y: 425, W: 615, H: 275
- **Visual Type**: Clustered Column Chart
- **X-Axis**: `Monthly_Analysis[MonthName]`
- **Y-Axis**: `Monthly_Analysis[AverageClose]`
- **Data Labels**: On (Format: `₹#,##0`)
- **Title**: `Average Closing Price by Month`

#### 3. Visual 4.3: Monthly Matrix Grid
- **Position**: X: 640, Y: 425, W: 630, H: 275
- **Visual Type**: Matrix Table
- **Rows**: `Monthly_Analysis[MonthName]`
- **Values**: `Monthly_Analysis[AverageClose]`, `Monthly_Analysis[AverageVolume]`
- **Conditional Formatting**: Background color gradient on `AverageClose` (Light Blue to Dark Blue).
- **Title**: `Monthly Breakdown Performance Table`

---

## PAGE 5: RISK & CORRELATION

### Purpose
Risk-reward evaluation combining risk-return scatter plots, volatility rankings, cross-stock correlation heatmaps, and high/low risk stock segmentation.

```
+-----------------------------------------------------------------------------------+
| HEADER: RISK VS RETURN & STOCK CORRELATION MATRIX                                 |
+-----------------------------------+-----------------------------------------------+
| VISUAL 5.1                        | VISUAL 5.2                                    |
| Risk vs Return Scatter Plot       | Top Volatile Stocks Ranking                   |
| X: Volatility %, Y: Yearly Return %| (Horizontal Bar Chart sorted by Volatility)   |
| Details: Ticker                   |                                               |
+-----------------------------------+-----------------------------------------------+
| VISUAL 5.3: CROSS-STOCK CORRELATION MATRIX HEATMAP                                |
| Matrix Visual: Ticker (Rows) vs 50 Ticker Columns (Values)                        |
| Conditional Formatting: Red (-1.0) to Blue (+1.0) Diverging Color Scale            |
+-----------------------------------------------------------------------------------+
```

### Visual Specifications

#### 1. Visual 5.1: Risk vs Return Scatter Plot
- **Position**: X: 10, Y: 80, W: 615, H: 300
- **Visual Type**: Scatter Chart
- **X-Axis**: `Risk_Return_Analysis[VolatilityPct]` (Title: `Annualized Volatility (%)`)
- **Y-Axis**: `Risk_Return_Analysis[YearlyReturnPct]` (Title: `Yearly Return (%)`)
- **Details**: `Dim_Company[Ticker]`
- **Legend**: `Dim_Company[Sector]`
- **Tooltips**: `Ticker`, `YearlyReturnPct`, `VolatilityPct`
- **Title**: `Risk vs Return Distribution (Scatter Plot)`

#### 2. Visual 5.2: Volatility Ranking Bar Chart
- **Position**: X: 640, Y: 80, W: 630, H: 300
- **Visual Type**: Horizontal Clustered Bar Chart
- **Y-Axis**: `Volatility[Ticker]` (Sorted by `Volatility` Descending)
- **X-Axis**: `Volatility[Volatility]`
- **Data Colors**: Gradient from Amber (`#F59E0B`) to Red (`#EF4444`) based on risk level.
- **Title**: `Stock Volatility Ranking (Standard Deviation)`

#### 3. Visual 5.3: Correlation Matrix Heatmap
- **Position**: X: 10, Y: 395, W: 1260, H: 305
- **Visual Type**: Matrix Table
- **Rows**: `Correlation_Matrix[Ticker]`
- **Values**: All 50 Stock Ticker Columns (`[ADANIENT ... WIPRO]`)
- **Conditional Formatting**: Background Color Rules (Diverging Color Scale):
  - Minimum (-1.0): Coral Red (`#F87171`)
  - Midpoint (0.0): Neutral Gray (`#F1F5F9`)
  - Maximum (+1.0): Deep Navy Blue (`#1E3A8A`)
- **Title**: `Nifty 50 Cross-Asset Return Correlation Heatmap Matrix`

---

## Interactive Filtering & Cross-Highlighting Rules

1. **Global Ticker Selection**:
   - Selecting a stock ticker on any page filters corresponding visuals on that page.
   - Slicing on Page 2 (`Stock Analysis`) dynamically updates all 6 top cards and technical MA trend lines simultaneously.

2. **Sector Drill-Through**:
   - Right-clicking a sector bar in Page 3 (`Sector Analysis`) enables drill-through to Page 2 pre-filtered for tickers in that sector.

3. **Correlation Matrix Highlighting**:
   - Selecting a ticker row in Page 5 correlation heatmap cross-highlights that company's position in the Risk-Return scatter plot.
