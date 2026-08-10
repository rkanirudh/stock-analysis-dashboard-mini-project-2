// ==============================================================================
// Power Query M Script: Dim_Company
// Description: Builds the master company dimension by extracting distinct tickers
//              and mapping each ticker to its respective Nifty 50 industry sector.
// ==============================================================================

let
    // 1. Source distinct tickers from yearly_return dataset
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
    #"Removed Other Columns" = Table.SelectColumns(#"Promoted Headers", {"ticker"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Other Columns", {{"ticker", "Ticker"}}),
    #"Removed Duplicates" = Table.Distinct(#"Renamed Columns"),
    
    // 2. Add Sector mapping via Conditional Column logic
    #"Added Sector" = Table.AddColumn(#"Removed Duplicates", "Sector", each 
        if [Ticker] = "HDFCBANK" or [Ticker] = "ICICIBANK" or [Ticker] = "SBIN" or [Ticker] = "AXISBANK" or [Ticker] = "KOTAKBANK" or [Ticker] = "INDUSINDBK" then "Banking"
        else if [Ticker] = "BAJFINANCE" or [Ticker] = "BAJAJFINSV" or [Ticker] = "SHRIRAMFIN" then "Financial Services"
        else if [Ticker] = "SBILIFE" or [Ticker] = "HDFCLIFE" then "Insurance"
        else if [Ticker] = "TCS" or [Ticker] = "INFY" or [Ticker] = "HCLTECH" or [Ticker] = "TECHM" or [Ticker] = "WIPRO" then "Information Technology"
        else if [Ticker] = "SUNPHARMA" or [Ticker] = "DRREDDY" or [Ticker] = "CIPLA" then "Pharmaceuticals"
        else if [Ticker] = "APOLLOHOSP" then "Healthcare"
        else if [Ticker] = "MARUTI" or [Ticker] = "TATAMOTORS" or [Ticker] = "M&M" or [Ticker] = "HEROMOTOCO" or [Ticker] = "BAJAJ-AUTO" or [Ticker] = "EICHERMOT" then "Automobile"
        else if [Ticker] = "RELIANCE" or [Ticker] = "ONGC" or [Ticker] = "BPCL" or [Ticker] = "COALINDIA" then "Energy"
        else if [Ticker] = "NTPC" or [Ticker] = "POWERGRID" then "Power"
        else if [Ticker] = "TATASTEEL" or [Ticker] = "JSWSTEEL" or [Ticker] = "HINDALCO" then "Metals"
        else if [Ticker] = "ULTRACEMCO" or [Ticker] = "GRASIM" then "Cement"
        else if [Ticker] = "LT" then "Construction"
        else if [Ticker] = "HINDUNILVR" or [Ticker] = "ITC" or [Ticker] = "NESTLEIND" or [Ticker] = "BRITANNIA" or [Ticker] = "TATACONSUM" then "FMCG"
        else if [Ticker] = "TRENT" then "Retail"
        else if [Ticker] = "BHARTIARTL" then "Telecommunication"
        else if [Ticker] = "ASIANPAINT" then "Paints"
        else if [Ticker] = "TITAN" then "Consumer Durables"
        else if [Ticker] = "BEL" then "Capital Goods"
        else if [Ticker] = "ADANIPORTS" then "Infrastructure"
        else if [Ticker] = "ADANIENT" then "Diversified"
        else "Other",
        type text
    ),

    // 3. Add Full Company Name for enhanced visualization tooltips
    #"Added Company Name" = Table.AddColumn(#"Added Sector", "CompanyName", each 
        [Ticker] & " Ltd.", type text
    ),

    // 4. Set final Data Types and Sort
    #"Changed Type" = Table.TransformColumnTypes(
        #"Added Company Name",
        {
            {"Ticker", type text},
            {"Sector", type text},
            {"CompanyName", type text}
        }
    ),
    #"Sorted Rows" = Table.Sort(#"Changed Type", {{"Ticker", Order.Ascending}})
in
    #"Sorted Rows"
