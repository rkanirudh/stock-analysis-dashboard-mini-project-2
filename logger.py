"""
logger.py

Reusable logging configuration for the project.

Author : Anirudh
Project: Stock Analysis Dashboard
"""

import logging

from config import LOG_FILE


def get_logger(name: str) -> logging.Logger:
    """
    Create and return a reusable logger.

    Parameters
    ----------
    name : str
        Logger name.

    Returns
    -------
    logging.Logger
    """

    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
    )

    # --------------------------------------------
    # Console Handler
    # --------------------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # --------------------------------------------
    # File Handler
    # --------------------------------------------

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger