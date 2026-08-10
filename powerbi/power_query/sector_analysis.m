// ==============================================================================
// Power Query M Script: Sector_Analysis
// Source Dataset: sector_analysis.csv
// Description: Loads sector aggregate metrics (company count, avg close price,
//              avg trading volume), applies standard types, and sorts by sector.
// ==============================================================================

let
    FilePath = "C:\StockAnalysis\reports\sector_analysis.csv",
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
            {"sector", "Sector"},
            {"Companies", "CompanyCount"},
            {"Average_Close", "AverageClose"},
            {"Average_Volume", "AverageVolume"}
        }
    ),
    #"Changed Type" = Table.TransformColumnTypes(
        #"Renamed Columns",
        {
            {"Sector", type text},
            {"CompanyCount", Int64.Type},
            {"AverageClose", Currency.Type},
            {"AverageVolume", type number}
        }
    ),
    #"Sorted Rows" = Table.Sort(#"Changed Type", {{"Sector", Order.Ascending}})
in
    #"Sorted Rows"
