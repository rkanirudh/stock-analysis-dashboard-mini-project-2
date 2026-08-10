// ==============================================================================
// Power Query M Script: Risk_Return_Analysis
// Source Dataset: risk_return_analysis.csv
// Description: Loads risk vs return metrics per stock (Yearly Return % and Volatility %),
//              converts data types, and prepares dataset for Scatter Plot visual.
// ==============================================================================

let
    FilePath = "C:\StockAnalysis\reports\risk_return_analysis.csv",
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
    #"Renamed Columns" = Table.RenameColumns(
        #"Promoted Headers",
        {
            {"ticker", "Ticker"},
            {"Yearly_Return", "YearlyReturnPct"},
            {"Volatility", "VolatilityPct"}
        }
    ),
    #"Changed Type" = Table.TransformColumnTypes(
        #"Renamed Columns",
        {
            {"Ticker", type text},
            {"YearlyReturnPct", type number},
            {"VolatilityPct", type number}
        }
    ),
    #"Sorted Rows" = Table.Sort(#"Changed Type", {{"Ticker", Order.Ascending}})
in
    #"Sorted Rows"
