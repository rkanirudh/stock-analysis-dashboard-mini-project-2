// ==============================================================================
// Power Query M Script: Correlation_Matrix
// Source Dataset: correlation_matrix.csv
// Description: Loads stock-to-stock Pearson correlation matrix (50x50), applies decimal
//              types across all 50 stock columns, and sorts by ticker.
// ==============================================================================

let
    FilePath = "C:\StockAnalysis\reports\correlation_matrix.csv",
    Source = Csv.Document(
        File.Contents(FilePath),
        [
            Delimiter = ",",
            Columns = 51,
            Encoding = 65001,
            QuoteStyle = QuoteStyle.None
        ]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    #"Renamed Columns" = Table.RenameColumns(#"Promoted Headers", {{"ticker", "Ticker"}}),
    
    // Dynamically select all columns except Ticker and transform to type number
    ColumnNames = Table.ColumnNames(#"Renamed Columns"),
    NumericColumns = List.Select(ColumnNames, each _ <> "Ticker"),
    TypeTransformations = List.Transform(NumericColumns, each {_, type number}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns", TypeTransformations),
    #"Sorted Rows" = Table.Sort(#"Changed Type", {{"Ticker", Order.Ascending}})
in
    #"Sorted Rows"
