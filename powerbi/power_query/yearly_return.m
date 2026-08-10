// ==============================================================================
// Power Query M Script: Yearly_Return
// Source Dataset: yearly_return.csv
// Description: Loads yearly stock performance summary (First Close, Last Close,
//              and net Percentage Return), converts currency/numeric types, and sorts.
// ==============================================================================

let
    FilePath = "C:\StockAnalysis\reports\yearly_return.csv",
    Source = Csv.Document(
        File.Contents(FilePath),
        [
            Delimiter = ",",
            Columns = 4,
            Encoding = 65001,
            QuoteStyle = QuoteStyle.None
        ]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    #"Renamed Columns" = Table.RenameColumns(
        #"Promoted Headers",
        {
            {"ticker", "Ticker"},
            {"First Close", "FirstClose"},
            {"Last Close", "LastClose"},
            {"Yearly Return (%)", "YearlyReturnPct"}
        }
    ),
    #"Changed Type" = Table.TransformColumnTypes(
        #"Renamed Columns",
        {
            {"Ticker", type text},
            {"FirstClose", Currency.Type},
            {"LastClose", Currency.Type},
            {"YearlyReturnPct", type number}
        }
    ),
    #"Sorted Rows" = Table.Sort(#"Changed Type", {{"YearlyReturnPct", Order.Descending}})
in
    #"Sorted Rows"
