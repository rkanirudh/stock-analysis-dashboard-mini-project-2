// ==============================================================================
// Power Query M Script: Monthly_Analysis
// Source Dataset: monthly_analysis.csv
// Description: Loads monthly aggregate closing price and volume trends, formats
//              currency/volume integers, and sorts by calendar MonthNumber.
// ==============================================================================

let
    FilePath = "C:\StockAnalysis\reports\monthly_analysis.csv",
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
            {"month_number", "MonthNumber"},
            {"month_name", "MonthName"},
            {"average_close_price", "AverageClose"},
            {"average_volume", "AverageVolume"}
        }
    ),
    #"Changed Type" = Table.TransformColumnTypes(
        #"Renamed Columns",
        {
            {"MonthNumber", Int64.Type},
            {"MonthName", type text},
            {"AverageClose", Currency.Type},
            {"AverageVolume", Int64.Type}
        }
    ),
    #"Sorted Rows" = Table.Sort(#"Changed Type", {{"MonthNumber", Order.Ascending}})
in
    #"Sorted Rows"
