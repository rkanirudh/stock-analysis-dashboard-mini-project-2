// ==============================================================================
// Power Query M Script: Top_Losers
// Source Dataset: top_losers.csv
// Description: Loads the top 10 worst-performing stocks by yearly percentage return.
// ==============================================================================

let
    FilePath = "C:\StockAnalysis\reports\top_losers.csv",
    Source = Csv.Document(
        File.Contents(FilePath),
        [
            Delimiter = ",",
            Columns = 2,
            Encoding = 65001,
            QuoteStyle = QuoteStyle.None
        ]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    #"Renamed Columns" = Table.RenameColumns(
        #"Promoted Headers",
        {
            {"Ticker", "Ticker"},
            {"Yearly_Return", "YearlyReturnPct"}
        }
    ),
    #"Changed Type" = Table.TransformColumnTypes(
        #"Renamed Columns",
        {
            {"Ticker", type text},
            {"YearlyReturnPct", type number}
        }
    ),
    #"Sorted Rows" = Table.Sort(#"Changed Type", {{"YearlyReturnPct", Order.Ascending}})
in
    #"Sorted Rows"
