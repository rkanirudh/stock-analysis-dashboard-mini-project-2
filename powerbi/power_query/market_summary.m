// ==============================================================================
// Power Query M Script: Market_Summary
// Source Dataset: market_summary.csv
// Description: Loads system metadata indicators (Total Records, Total Companies, etc.).
// ==============================================================================

let
    FilePath = "C:\StockAnalysis\reports\market_summary.csv",
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
    #"Changed Type" = Table.TransformColumnTypes(
        #"Promoted Headers",
        {
            {"Metric", type text},
            {"Value", type text}
        }
    )
in
    #"Changed Type"
