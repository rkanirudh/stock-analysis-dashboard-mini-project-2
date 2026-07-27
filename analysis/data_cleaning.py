"""
data_cleaning.py

Reads all extracted stock CSV files,
merges them into a single DataFrame,
cleans the data,
and saves the final cleaned dataset.

Author : Anirudh R K
Project : Stock Analysis Dashboard
"""

from typing import List

import pandas as pd

from config import EXTRACTED_CSV_DIR, PROCESSED_DATA_DIR
from logger import get_logger


logger = get_logger(__name__)


# =====================================================
# Load CSV Files
# =====================================================

def load_csv_files() -> List[pd.DataFrame]:
    """
    Load all extracted stock CSV files.

    Returns
    -------
    List[pd.DataFrame]
    """

    dataframes = []

    csv_files = sorted(EXTRACTED_CSV_DIR.glob("*.csv"))

    logger.info(f"Found {len(csv_files)} CSV files.")

    for file in csv_files:

        dataframe = pd.read_csv(file)

        dataframes.append(dataframe)

        logger.info(f"Loaded {file.name}")

    return dataframes


# =====================================================
# Merge DataFrames
# =====================================================

def merge_dataframes(dataframes: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Merge all stock DataFrames into one DataFrame.
    """

    merged_df = pd.concat(
        dataframes,
        ignore_index=True
    )

    logger.info(
        f"Merged {len(dataframes)} DataFrames."
    )

    logger.info(
        f"Total Rows : {len(merged_df)}"
    )

    return merged_df


# =====================================================
# Clean Data
# =====================================================

def clean_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Clean merged stock data.
    """

    logger.info("Cleaning data...")

    initial_rows = len(dataframe)

    # Remove duplicate rows
    dataframe.drop_duplicates(inplace=True)

    # Remove rows with missing values
    dataframe.dropna(inplace=True)

    # Convert Date column
    dataframe["date"] = pd.to_datetime(dataframe["date"])

    # Convert numeric columns

    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    for column in numeric_columns:

        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce"
        )

    # Remove rows created after datatype conversion

    dataframe.dropna(inplace=True)

    # Sort

    dataframe.sort_values(
        by=["Ticker", "date"],
        inplace=True
    )

    dataframe.reset_index(
        drop=True,
        inplace=True
    )

    logger.info(
        f"Removed {initial_rows-len(dataframe)} invalid rows."
    )

    logger.info(
        f"Final Rows : {len(dataframe)}"
    )

    return dataframe


# =====================================================
# Save Cleaned Data
# =====================================================

def save_cleaned_data(dataframe: pd.DataFrame) -> None:
    """
    Save cleaned stock dataset.
    """

    output_file = (
        PROCESSED_DATA_DIR /
        "cleaned_stock.csv"
    )

    dataframe.to_csv(
        output_file,
        index=False
    )

    logger.info(
        f"Saved cleaned dataset : {output_file.name}"
    )


# =====================================================
# Main
# =====================================================

def main():

    logger.info("=" * 60)
    logger.info("Starting Data Cleaning")
    logger.info("=" * 60)

    dataframes = load_csv_files()

    merged_df = merge_dataframes(dataframes)

    cleaned_df = clean_data(merged_df)

    save_cleaned_data(cleaned_df)

    logger.info("=" * 60)
    logger.info("Data Cleaning Completed Successfully")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()