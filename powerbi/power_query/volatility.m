// ==============================================================================
// Power Query M Script: Volatility
// Source Dataset: volatility.csv
// Description: Loads daily return standard deviation per stock, drops redundant
//              row index column (`Unnamed: 0`), and formats volatility decimals.
// ==============================================================================

let
    FilePath = "C:\StockAnalysis\reports\volatility.csv",
    Source = Csv.Document(
        File.Contents(FilePath),
        [
            Delimiter = ",",
            Columns = 3,
            Encoding = 65001,
            QuoteStyle = QuoteStyle.None
        ]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    
    // Drop raw index column
    #"Removed Columns" = Table.RemoveColumns(#"Promoted Headers", {"Unnamed: 0"}),
    
    #"Renamed Columns" = Table.RenameColumns(
        #"Removed Columns",
        {
            {"ticker", "Ticker"},
            {"volatility", "Volatility"}
        }
    ),
    #"Changed Type" = Table.TransformColumnTypes(
        #"Renamed Columns",
        {
            {"Ticker", type text},
            {"Volatility", type number}
        }
    ),
    #"Sorted Rows" = Table.Sort(#"Changed Type", {{"Volatility", Order.Descending}})
in
    #"Sorted Rows"
