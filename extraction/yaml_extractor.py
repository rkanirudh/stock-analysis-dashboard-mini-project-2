"""
yaml_extractor.py

Reads all YAML files from the raw dataset,
groups records by stock ticker,
and creates one CSV file for each stock.

Author: Anirudh R K
Project: Stock Analysis Dashboard
"""

from pathlib import Path
from typing import Dict, List

import pandas as pd
import yaml

from config import RAW_DATA_DIR, EXTRACTED_CSV_DIR
from logger import get_logger


logger = get_logger(__name__)

REQUIRED_COLUMNS = [
    "Ticker",
    "date",
    "open",
    "high",
    "low",
    "close",
    "volume",
]


# =====================================================
# Create Output Folder
# =====================================================

def create_output_directory() -> None:
    """
    Creates extracted_csv folder if it does not exist.
    """
    EXTRACTED_CSV_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================
# Get All YAML Files
# =====================================================

def get_yaml_files() -> List[Path]:
    """
    Returns a list of all YAML files inside raw dataset.
    """

    yaml_files = sorted(RAW_DATA_DIR.rglob("*.yaml"))

    logger.info(f"Found {len(yaml_files)} YAML files.")

    return yaml_files


# =====================================================
# Read One YAML File
# =====================================================

def read_yaml_file(file_path: Path) -> List[dict]:
    """
    Reads a YAML file.

    Parameters
    ----------
    file_path : Path

    Returns
    -------
    List[dict]
    """

    try:

        with open(file_path, "r", encoding="utf-8") as file:

            data = yaml.safe_load(file)

        return data if data else []

    except Exception as error:

        logger.error(f"Failed to read {file_path.name}")

        logger.error(error)

        return []


# =====================================================
# Validate Record
# =====================================================

def validate_record(record: dict) -> bool:
    """
    Validate required fields.
    """

    for column in REQUIRED_COLUMNS:

        if column not in record:

            return False

    return True


# =====================================================
# Extract Stock Data
# =====================================================

def extract_stock_data(
    yaml_files: List[Path],
) -> Dict[str, List[dict]]:
    """
    Groups stock records by ticker.
    """

    stock_data: Dict[str, List[dict]] = {}

    total_records = 0
    valid_records = 0

    for file in yaml_files:

        records = read_yaml_file(file)

        total_records += len(records)

        for record in records:

            if not validate_record(record):

                continue

            ticker = record["Ticker"]

            stock_data.setdefault(ticker, []).append(record)

            valid_records += 1

    logger.info(f"Total Records : {total_records}")
    logger.info(f"Valid Records : {valid_records}")

    return stock_data


# =====================================================
# Save CSV Files
# =====================================================

def save_csv_files(
    stock_data: Dict[str, List[dict]]
) -> None:
    """
    Saves one CSV file for every stock.
    """

    for ticker, records in stock_data.items():

        dataframe = pd.DataFrame(records)

        dataframe["date"] = pd.to_datetime(dataframe["date"])

        dataframe.sort_values("date", inplace=True)

        output_file = EXTRACTED_CSV_DIR / f"{ticker}.csv"

        dataframe.to_csv(output_file, index=False)

        logger.info(
            f"Saved {ticker}.csv ({len(dataframe)} records)"
        )


# =====================================================
# Main
# =====================================================

def main():

    logger.info("=" * 60)
    logger.info("Starting YAML Extraction")
    logger.info("=" * 60)

    create_output_directory()

    yaml_files = get_yaml_files()

    stock_data = extract_stock_data(yaml_files)

    save_csv_files(stock_data)

    logger.info("=" * 60)
    logger.info("YAML Extraction Completed Successfully")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()