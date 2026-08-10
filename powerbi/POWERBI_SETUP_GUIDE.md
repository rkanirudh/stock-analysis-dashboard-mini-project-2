# 📊 Power BI Desktop Setup Guide — Nifty 50 Stock Analysis Dashboard

> **Why no .pbix file?**
> `.pbix` files contain a proprietary binary VertiPaq/Analysis Services data model that can only be created and saved by Power BI Desktop itself — no tool outside Power BI can write this binary format. This guide gives you **everything pre-written** so you can build the full dashboard in Power BI Desktop in under 20 minutes.

---

## 📁 Project File Locations

All CSV data files are in:
```
/Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/reports/
```

Available CSVs:
| File | Table Name | Rows |
|------|-----------|------|
| `daily_return.csv` | Fact_DailyReturn | 14,200 |
| `moving_average.csv` | Fact_MovingAverage | 14,200 |
| `dim_company.csv` *(built via M)* | Dim_Company | 50 |
| `yearly_return.csv` | Yearly_Return | 50 |
| `risk_return_analysis.csv` | Risk_Return_Analysis | 50 |
| `volatility.csv` | Volatility | 50 |
| `sector_analysis.csv` | Sector_Analysis | 20 |
| `monthly_analysis.csv` | Monthly_Analysis | 12 |
| `correlation_matrix.csv` | Correlation_Matrix | 50 |
| `top_gainers.csv` | Top_Gainers | 10 |
| `top_losers.csv` | Top_Losers | 10 |
| `market_summary.csv` | Market_Summary | 8 |

---

## 🚀 STEP 1: Open Power BI Desktop & Apply Theme

1. Launch **Power BI Desktop**
2. Go to **View → Themes → Browse for themes**
3. Select the theme file:
   ```
   /Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/powerbi/theme/finance_theme.json
   ```
4. Click **Apply**

---

## 🔗 STEP 2: Load All 12 Tables via Power Query

Go to **Home → Transform Data** to open Power Query Editor.

For **each table below**, click **Home → New Source → Blank Query**, then paste the M code into **View → Advanced Editor**.

---

### Table 1: `Dim_Company` (Master Dimension)

```powerquery
let
    FilePath = "/Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/reports/yearly_return.csv",
    Source = Csv.Document(
        File.Contents(FilePath),
        [Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Removed Other Columns" = Table.SelectColumns(#"Promoted Headers", {"ticker"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Other Columns", {{"ticker","Ticker"}}),
    #"Removed Duplicates" = Table.Distinct(#"Renamed Columns"),
    #"Added Sector" = Table.AddColumn(#"Removed Duplicates", "Sector", each
        if [Ticker]="HDFCBANK" or [Ticker]="ICICIBANK" or [Ticker]="SBIN" or [Ticker]="AXISBANK" or [Ticker]="KOTAKBANK" or [Ticker]="INDUSINDBK" then "Banking"
        else if [Ticker]="BAJFINANCE" or [Ticker]="BAJAJFINSV" or [Ticker]="SHRIRAMFIN" then "Financial Services"
        else if [Ticker]="SBILIFE" or [Ticker]="HDFCLIFE" then "Insurance"
        else if [Ticker]="TCS" or [Ticker]="INFY" or [Ticker]="HCLTECH" or [Ticker]="TECHM" or [Ticker]="WIPRO" then "Information Technology"
        else if [Ticker]="SUNPHARMA" or [Ticker]="DRREDDY" or [Ticker]="CIPLA" then "Pharmaceuticals"
        else if [Ticker]="APOLLOHOSP" then "Healthcare"
        else if [Ticker]="MARUTI" or [Ticker]="TATAMOTORS" or [Ticker]="M&M" or [Ticker]="HEROMOTOCO" or [Ticker]="BAJAJ-AUTO" or [Ticker]="EICHERMOT" then "Automobile"
        else if [Ticker]="RELIANCE" or [Ticker]="ONGC" or [Ticker]="BPCL" or [Ticker]="COALINDIA" then "Energy"
        else if [Ticker]="NTPC" or [Ticker]="POWERGRID" then "Power"
        else if [Ticker]="TATASTEEL" or [Ticker]="JSWSTEEL" or [Ticker]="HINDALCO" then "Metals"
        else if [Ticker]="ULTRACEMCO" or [Ticker]="GRASIM" then "Cement"
        else if [Ticker]="LT" then "Construction"
        else if [Ticker]="HINDUNILVR" or [Ticker]="ITC" or [Ticker]="NESTLEIND" or [Ticker]="BRITANNIA" or [Ticker]="TATACONSUM" then "FMCG"
        else if [Ticker]="TRENT" then "Retail"
        else if [Ticker]="BHARTIARTL" then "Telecommunication"
        else if [Ticker]="ASIANPAINT" then "Paints"
        else if [Ticker]="TITAN" then "Consumer Durables"
        else if [Ticker]="BEL" then "Capital Goods"
        else if [Ticker]="ADANIPORTS" then "Infrastructure"
        else if [Ticker]="ADANIENT" then "Diversified"
        else "Other",
        type text
    ),
    #"Added Company Name" = Table.AddColumn(#"Added Sector", "CompanyName", each [Ticker] & " Ltd.", type text),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Company Name",{{"Ticker",type text},{"Sector",type text},{"CompanyName",type text}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type",{{"Ticker",Order.Ascending}})
in
    #"Sorted Rows"
```

---

### Table 2: `Fact_DailyReturn`

```powerquery
let
    FilePath = "/Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/reports/daily_return.csv",
    Source = Csv.Document(File.Contents(FilePath),[Delimiter=",",Columns=4,Encoding=65001,QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    #"Renamed Columns" = Table.RenameColumns(#"Promoted Headers",{{"ticker","Ticker"},{"trade_date","TradeDate"},{"close_price","ClosePrice"},{"Daily_Return (%)","DailyReturnPct"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"Ticker",type text},{"TradeDate",type date},{"ClosePrice",Currency.Type},{"DailyReturnPct",type number}}),
    #"Replaced Nulls" = Table.ReplaceValue(#"Changed Type",null,0.0,Replacer.ReplaceValue,{"DailyReturnPct"}),
    #"Sorted Rows" = Table.Sort(#"Replaced Nulls",{{"Ticker",Order.Ascending},{"TradeDate",Order.Ascending}})
in
    #"Sorted Rows"
```

---

### Table 3: `Fact_MovingAverage`

```powerquery
let
    FilePath = "/Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/reports/moving_average.csv",
    Source = Csv.Document(File.Contents(FilePath),[Delimiter=",",Columns=5,Encoding=65001,QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    #"Renamed Columns" = Table.RenameColumns(#"Promoted Headers",{{"ticker","Ticker"},{"trade_date","TradeDate"},{"close_price","ClosePrice"},{"MA20","MA20"},{"MA50","MA50"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"Ticker",type text},{"TradeDate",type date},{"ClosePrice",Currency.Type},{"MA20",Currency.Type},{"MA50",Currency.Type}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type",{{"Ticker",Order.Ascending},{"TradeDate",Order.Ascending}})
in
    #"Sorted Rows"
```

---

### Table 4: `Yearly_Return`

```powerquery
let
    FilePath = "/Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/reports/yearly_return.csv",
    Source = Csv.Document(File.Contents(FilePath),[Delimiter=",",Columns=4,Encoding=65001,QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    #"Renamed Columns" = Table.RenameColumns(#"Promoted Headers",{{"ticker","Ticker"},{"First Close","FirstClose"},{"Last Close","LastClose"},{"Yearly Return (%)","YearlyReturnPct"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"Ticker",type text},{"FirstClose",Currency.Type},{"LastClose",Currency.Type},{"YearlyReturnPct",type number}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type",{{"YearlyReturnPct",Order.Descending}})
in
    #"Sorted Rows"
```

---

### Table 5: `Risk_Return_Analysis`

```powerquery
let
    FilePath = "/Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/reports/risk_return_analysis.csv",
    Source = Csv.Document(File.Contents(FilePath),[Delimiter=",",Columns=3,Encoding=65001,QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    #"Renamed Columns" = Table.RenameColumns(#"Promoted Headers",{{"ticker","Ticker"},{"Yearly_Return","YearlyReturnPct"},{"Volatility","VolatilityPct"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"Ticker",type text},{"YearlyReturnPct",type number},{"VolatilityPct",type number}}),
    #"Added Risk Level" = Table.AddColumn(#"Changed Type","RiskLevel", each
        if [VolatilityPct] >= 2.0 then "High Risk"
        else if [VolatilityPct] >= 1.5 then "Moderate Risk"
        else "Low Risk",
        type text
    )
in
    #"Added Risk Level"
```

---

### Table 6: `Volatility`

```powerquery
let
    FilePath = "/Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/reports/volatility.csv",
    Source = Csv.Document(File.Contents(FilePath),[Delimiter=",",Columns=3,Encoding=65001,QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    #"Removed Index" = Table.RemoveColumns(#"Promoted Headers",{"Column1"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Index",{{"ticker","Ticker"},{"volatility","Volatility"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"Ticker",type text},{"Volatility",type number}}),
    #"Added VolPct" = Table.AddColumn(#"Changed Type","VolatilityPct", each [Volatility]*100, type number),
    #"Sorted Rows" = Table.Sort(#"Added VolPct",{{"Volatility",Order.Descending}})
in
    #"Sorted Rows"
```

---

### Table 7: `Sector_Analysis`

```powerquery
let
    FilePath = "/Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/reports/sector_analysis.csv",
    Source = Csv.Document(File.Contents(FilePath),[Delimiter=",",Columns=4,Encoding=65001,QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    #"Renamed Columns" = Table.RenameColumns(#"Promoted Headers",{{"sector","Sector"},{"Companies","CompanyCount"},{"Average_Close","AverageClose"},{"Average_Volume","AverageVolume"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"Sector",type text},{"CompanyCount",Int64.Type},{"AverageClose",Currency.Type},{"AverageVolume",type number}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type",{{"Sector",Order.Ascending}})
in
    #"Sorted Rows"
```

---

### Table 8: `Monthly_Analysis`

```powerquery
let
    FilePath = "/Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/reports/monthly_analysis.csv",
    Source = Csv.Document(File.Contents(FilePath),[Delimiter=",",Columns=4,Encoding=65001,QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    #"Renamed Columns" = Table.RenameColumns(#"Promoted Headers",{{"month_number","MonthNumber"},{"month_name","MonthName"},{"average_close_price","AverageClose"},{"average_volume","AverageVolume"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"MonthNumber",Int64.Type},{"MonthName",type text},{"AverageClose",Currency.Type},{"AverageVolume",Int64.Type}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type",{{"MonthNumber",Order.Ascending}})
in
    #"Sorted Rows"
```

---

### Table 9: `Top_Gainers`

```powerquery
let
    FilePath = "/Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/reports/top_gainers.csv",
    Source = Csv.Document(File.Contents(FilePath),[Delimiter=",",Columns=2,Encoding=65001,QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    #"Renamed Columns" = Table.RenameColumns(#"Promoted Headers",{{"Ticker","Ticker"},{"Yearly_Return","YearlyReturnPct"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"Ticker",type text},{"YearlyReturnPct",type number}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type",{{"YearlyReturnPct",Order.Descending}})
in
    #"Sorted Rows"
```

---

### Table 10: `Top_Losers`

```powerquery
let
    FilePath = "/Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/reports/top_losers.csv",
    Source = Csv.Document(File.Contents(FilePath),[Delimiter=",",Columns=2,Encoding=65001,QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    #"Renamed Columns" = Table.RenameColumns(#"Promoted Headers",{{"Ticker","Ticker"},{"Yearly_Return","YearlyReturnPct"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"Ticker",type text},{"YearlyReturnPct",type number}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type",{{"YearlyReturnPct",Order.Ascending}})
in
    #"Sorted Rows"
```

---

### Table 11: `Market_Summary`

```powerquery
let
    FilePath = "/Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/reports/market_summary.csv",
    Source = Csv.Document(File.Contents(FilePath),[Delimiter=",",Columns=2,Encoding=65001,QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Metric",type text},{"Value",type text}})
in
    #"Changed Type"
```

---

### Table 12: `Correlation_Matrix`

```powerquery
let
    FilePath = "/Users/anirudh/Desktop/stock-analysis-dashboard-mini-project-2/reports/correlation_matrix.csv",
    Source = Csv.Document(File.Contents(FilePath),[Delimiter=",",Encoding=65001,QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    #"Renamed Ticker Col" = Table.RenameColumns(#"Promoted Headers",{{"ticker","Ticker"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Ticker Col", List.Transform(
        List.Skip(Table.ColumnNames(#"Renamed Ticker Col"),1),
        each {_, type number}
    ) & {{"Ticker", type text}})
in
    #"Changed Type"
```

---

## 🔗 STEP 3: Set Up Data Model Relationships

After loading all tables, go to **Model View** and create these relationships:

```
Dim_Company[Ticker]         ──(1)──→──(*)── Fact_DailyReturn[Ticker]
Dim_Company[Ticker]         ──(1)──→──(*)── Fact_MovingAverage[Ticker]
Dim_Company[Ticker]         ──(1)──→──(1)── Yearly_Return[Ticker]
Dim_Company[Ticker]         ──(1)──→──(1)── Risk_Return_Analysis[Ticker]
Dim_Company[Ticker]         ──(1)──→──(1)── Volatility[Ticker]
Dim_Company[Ticker]         ──(1)──→──(1)── Top_Gainers[Ticker]    (inactive)
Dim_Company[Ticker]         ──(1)──→──(1)── Top_Losers[Ticker]     (inactive)
Dim_Company[Sector]         ──(*)──→──(1)── Sector_Analysis[Sector]
Fact_DailyReturn[TradeDate] ──(*)──→──(1)── Fact_MovingAverage[TradeDate] (inactive)
```

> [!IMPORTANT]
> Set all relationship cross-filter directions to **Single** unless otherwise noted. Cardinality for Fact tables is Many (*).

---

## 📐 STEP 4: Create All DAX Measures

In the **Data view**, click your `Fact_DailyReturn` table, then go to **Home → New Measure** and paste each measure:

### Section 1: Core KPIs
```dax
Total Companies = DISTINCTCOUNT(Dim_Company[Ticker])
```
```dax
Total Records = COUNTROWS(Fact_DailyReturn)
```
```dax
Total Sectors = DISTINCTCOUNT(Dim_Company[Sector])
```

### Section 2: Price & Volume
```dax
Average Closing Price = AVERAGE(Fact_DailyReturn[ClosePrice])
```
```dax
Highest Stock Price = MAX(Fact_DailyReturn[ClosePrice])
```
```dax
Lowest Stock Price = MIN(Fact_DailyReturn[ClosePrice])
```
```dax
Average Trading Volume = AVERAGE(Sector_Analysis[AverageVolume])
```

### Section 3: Return & Risk
```dax
Average Daily Return = AVERAGE(Fact_DailyReturn[DailyReturnPct]) / 100.0
```
```dax
Average Volatility = AVERAGE(Risk_Return_Analysis[VolatilityPct]) / 100.0
```
```dax
Average Yearly Return = AVERAGE(Yearly_Return[YearlyReturnPct]) / 100.0
```

### Section 4: Dynamic Stock Selection (for Stock Analysis page)
```dax
Selected Stock Close =
    IF(
        HASONEVALUE(Dim_Company[Ticker]),
        AVERAGE(Fact_DailyReturn[ClosePrice]),
        BLANK()
    )
```
```dax
Selected MA20 =
    IF(
        HASONEVALUE(Dim_Company[Ticker]),
        AVERAGE(Fact_MovingAverage[MA20]),
        BLANK()
    )
```
```dax
Selected MA50 =
    IF(
        HASONEVALUE(Dim_Company[Ticker]),
        AVERAGE(Fact_MovingAverage[MA50]),
        BLANK()
    )
```
```dax
Selected Stock Daily Return =
    IF(
        HASONEVALUE(Dim_Company[Ticker]),
        AVERAGE(Fact_DailyReturn[DailyReturnPct]) / 100.0,
        BLANK()
    )
```
```dax
Selected Stock Volatility =
    IF(
        HASONEVALUE(Dim_Company[Ticker]),
        SELECTEDVALUE(Volatility[Volatility]),
        BLANK()
    )
```
```dax
Selected Stock Yearly Return =
    IF(
        HASONEVALUE(Dim_Company[Ticker]),
        SELECTEDVALUE(Yearly_Return[YearlyReturnPct]) / 100.0,
        BLANK()
    )
```

### Section 5: Executive Leaderboard
```dax
Top Gainer Return =
    MAXX(
        TOPN(1, ALL(Yearly_Return), Yearly_Return[YearlyReturnPct], DESC),
        Yearly_Return[YearlyReturnPct]
    ) / 100.0
```
```dax
Top Loser Return =
    MINX(
        TOPN(1, ALL(Yearly_Return), Yearly_Return[YearlyReturnPct], ASC),
        Yearly_Return[YearlyReturnPct]
    ) / 100.0
```

### Section 6: Risk Segmentation
```dax
High Risk Stocks Count =
    CALCULATE(
        COUNTROWS(Risk_Return_Analysis),
        Risk_Return_Analysis[VolatilityPct] >= 2.0
    )
```
```dax
Low Risk Stocks Count =
    CALCULATE(
        COUNTROWS(Risk_Return_Analysis),
        Risk_Return_Analysis[VolatilityPct] < 1.5
    )
```
```dax
Moderate Risk Stocks Count =
    CALCULATE(
        COUNTROWS(Risk_Return_Analysis),
        Risk_Return_Analysis[VolatilityPct] >= 1.5,
        Risk_Return_Analysis[VolatilityPct] < 2.0
    )
```
```dax
Stock Risk Status =
    VAR CurrentVol = AVERAGE(Volatility[Volatility]) * 100
    RETURN
    SWITCH(
        TRUE(),
        CurrentVol >= 2.5, "⚠️ High Volatility",
        CurrentVol >= 1.8, "⚡ Moderate Volatility",
        "✅ Low Volatility"
    )
```

---

## 🎨 STEP 5: Build the 4 Report Pages

Create 4 pages in the Report View. Canvas size: **1280 × 720px** (File → Page Setup → Custom).

---

### PAGE 1 — Executive Overview

| Visual | Type | Fields | Position (X,Y,W,H) |
|--------|------|--------|---------------------|
| Header Text Box | Text Box | "Nifty 50 Market Analysis — Executive Overview" | 10,10,1260,50 |
| KPI Card | Card | `[Total Companies]` | 10,70,295,85 |
| KPI Card | Card | `[Total Records]` | 320,70,295,85 |
| KPI Card | Card | `[Average Closing Price]` | 630,70,295,85 |
| KPI Card | Card | `[Average Yearly Return]` — format `+0.00%` | 940,70,330,85 |
| Top 10 Gainers | Clustered Bar | Y: `Top_Gainers[Ticker]`, X: `Top_Gainers[YearlyReturnPct]` | 10,170,400,530 |
| Top 10 Losers | Clustered Bar | Y: `Top_Losers[Ticker]`, X: `Top_Losers[YearlyReturnPct]` | 425,170,400,530 |
| Market Summary | Table | `Market_Summary[Metric]`, `Market_Summary[Value]` | 840,170,430,530 |

**Color settings:**
- Gainers bar → Data color: `#10B981`
- Losers bar → Conditional formatting by value (negative = `#EF4444`, positive = `#F59E0B`)

---

### PAGE 2 — Sector Analysis

| Visual | Type | Fields | Position |
|--------|------|--------|----------|
| Header Text Box | Text Box | "Sector Performance & Constituent Distribution" | 10,10,1260,50 |
| Companies by Sector | Clustered Bar | Y: `Sector_Analysis[Sector]`, X: `Sector_Analysis[CompanyCount]` | 10,70,615,305 |
| Avg Close by Sector | Clustered Column | X: `Sector_Analysis[Sector]`, Y: `Sector_Analysis[AverageClose]` | 640,70,630,305 |
| Avg Volume by Sector | Clustered Column | X: `Sector_Analysis[Sector]`, Y: `Sector_Analysis[AverageVolume]` | 10,390,615,310 |
| Sector Grid | Matrix | Rows: `Sector`, Values: `CompanyCount`, `AverageClose`, `AverageVolume` | 640,390,630,310 |

---

### PAGE 3 — Monthly Trends

| Visual | Type | Fields | Position |
|--------|------|--------|----------|
| Header Text Box | Text Box | "Monthly Price Trends & Volume Dynamics" | 10,10,1260,50 |
| Combo Chart | Line & Stacked Column | X: `Monthly_Analysis[MonthName]`, Column: `AverageVolume`, Line: `AverageClose` | 10,70,1260,325 |
| Monthly Close Bar | Clustered Column | X: `MonthName`, Y: `AverageClose` | 10,410,615,280 |
| Monthly Matrix | Matrix | Rows: `MonthName`, Values: `AverageClose`, `AverageVolume` | 640,410,630,280 |

> [!TIP]
> For the Combo Chart X-axis, set **Sort by column** on `MonthName` to `MonthNumber` (Ascending) so months appear Jan→Dec.

---

### PAGE 4 — Risk & Return

| Visual | Type | Fields | Position |
|--------|------|--------|----------|
| Header Text Box | Text Box | "Risk vs Return & Stock Correlation Analysis" | 10,10,1260,50 |
| KPI Card | Card | `[High Risk Stocks Count]` | 10,70,295,85 |
| KPI Card | Card | `[Moderate Risk Stocks Count]` | 320,70,295,85 |
| KPI Card | Card | `[Low Risk Stocks Count]` | 630,70,295,85 |
| KPI Card | Card | `[Top Gainer Return]` — format `+0.0%` | 940,70,330,85 |
| Risk vs Return Scatter | Scatter | X: `VolatilityPct`, Y: `YearlyReturnPct`, Details: `Dim_Company[Ticker]`, Legend: `Dim_Company[Sector]` | 10,170,615,300 |
| Volatility Ranking | Clustered Bar | Y: `Volatility[Ticker]`, X: `Volatility[VolatilityPct]` | 640,170,630,300 |
| Correlation Heatmap | Matrix | Rows: `Correlation_Matrix[Ticker]`, Values: all 50 ticker columns | 10,485,1260,225 |

**Conditional Formatting for Heatmap:**
- Select Matrix → Format → Cell elements → Background color → Rules
- Min = `#F87171` (Coral Red), Mid = `#F1F5F9` (Gray), Max = `#1E3A8A` (Navy Blue)

---

## ✅ STEP 6: Final Formatting Checklist

- [ ] Apply `finance_theme.json` theme (Step 1)
- [ ] All 12 tables loaded without errors in Power Query
- [ ] All 9 model relationships created in Model View
- [ ] All 23 DAX measures created with correct formats
- [ ] Page 1: 4 KPI Cards + 2 bar charts + 1 summary table
- [ ] Page 2: 2 bar charts + 1 column chart + 1 sector matrix
- [ ] Page 3: 1 combo chart + 1 column chart + 1 monthly matrix
- [ ] Page 4: 4 KPI Cards + scatter plot + volatility bar + heatmap
- [ ] Monthly Analysis X-axis sorted by MonthNumber
- [ ] Heatmap conditional formatting applied (Red→Gray→Blue)
- [ ] Save file: **File → Save As → `Nifty50_Stock_Dashboard.pbix`**

---

## 🎨 Color Reference

| Purpose | Color Hex |
|---------|-----------|
| Background | `#0F172A` |
| Card Background | `#1E293B` |
| Accent Blue | `#0EA5E9` |
| Gain (Positive) | `#10B981` |
| Loss (Negative) | `#EF4444` |
| Amber (Highlight) | `#F59E0B` |
| Purple | `#8B5CF6` |
| Muted Gray | `#64748B` |

---

*Data covers **Oct 2023 – Nov 2024** | 50 Nifty 50 stocks | 14,200 daily observations | 20 industry sectors*
