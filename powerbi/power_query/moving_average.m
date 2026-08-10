// ==============================================================================
// Power Query M Script: Fact_MovingAverage
// Source Dataset: moving_average.csv
// Description: Loads daily price data and technical indicators (20-day and 50-day
//              Moving Averages), sets currency/date types, and sorts by stock & date.
// ==============================================================================

let
    // 1. File Location Setting
    FilePath = "C:\StockAnalysis\reports\moving_average.csv",
    
    // 2. Import CSV Document
    Source = Csv.Document(
        File.Contents(FilePath),
        [
            Delimiter = ",",
            Columns = 5,
            Encoding = 65001,
            QuoteStyle = QuoteStyle.None
        ]
    ),
    
    // 3. Promote Headers
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    
    // 4. Standardize Column Names
    #"Renamed Columns" = Table.RenameColumns(
        #"Promoted Headers",
        {
            {"ticker", "Ticker"},
            {"trade_date", "TradeDate"},
            {"close_price", "ClosePrice"},
            {"MA20", "MA20"},
            {"MA50", "MA50"}
        }
    ),
    
    // 5. Convert Column Data Types
    #"Changed Type" = Table.TransformColumnTypes(
        #"Renamed Columns",
        {
            {"Ticker", type text},
            {"TradeDate", type date},
            {"ClosePrice", Currency.Type},
            {"MA20", Currency.Type},
            {"MA50", Currency.Type}
        }
    ),
    
    // 6. Chronological Sorting
    #"Sorted Rows" = Table.Sort(
        #"Changed Type",
        {
            {"Ticker", Order.Ascending},
            {"TradeDate", Order.Ascending}
        }
    )
in
    #"Sorted Rows"
