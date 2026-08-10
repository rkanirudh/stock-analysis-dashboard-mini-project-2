// ==============================================================================
// Power Query M Script: Fact_DailyReturn
// Source Dataset: daily_return.csv
// Description: Loads daily close prices and percentage daily returns, applies type
//              conversions, replaces null initial returns with 0.0, and sorts rows.
// ==============================================================================

let
    // 1. Parameterized File Path (Update base path if needed)
    FilePath = "C:\StockAnalysis\reports\daily_return.csv",
    
    // 2. Load Raw CSV File
    Source = Csv.Document(
        File.Contents(FilePath),
        [
            Delimiter = ",",
            Columns = 4,
            Encoding = 65001, // UTF-8
            QuoteStyle = QuoteStyle.None
        ]
    ),
    
    // 3. Promote First Row to Column Headers
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    
    // 4. Rename Columns to Standardized Data Model Naming Convention
    #"Renamed Columns" = Table.RenameColumns(
        #"Promoted Headers",
        {
            {"ticker", "Ticker"},
            {"trade_date", "TradeDate"},
            {"close_price", "ClosePrice"},
            {"Daily_Return (%)", "DailyReturnPct"}
        }
    ),
    
    // 5. Transform Column Data Types
    #"Changed Type" = Table.TransformColumnTypes(
        #"Renamed Columns",
        {
            {"Ticker", type text},
            {"TradeDate", type date},
            {"ClosePrice", Currency.Type},
            {"DailyReturnPct", type number}
        }
    ),
    
    // 6. Handle Null Values (First trading day for each ticker has no prior day return)
    #"Replaced Null Returns" = Table.ReplaceValue(
        #"Changed Type",
        null,
        0.0,
        Replacer.ReplaceValue,
        {"DailyReturnPct"}
    ),
    
    // 7. Sort Rows chronologically by Ticker and TradeDate
    #"Sorted Rows" = Table.Sort(
        #"Replaced Null Returns",
        {
            {"Ticker", Order.Ascending},
            {"TradeDate", Order.Ascending}
        }
    )
in
    #"Sorted Rows"
