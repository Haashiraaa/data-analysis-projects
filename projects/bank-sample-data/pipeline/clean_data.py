

# clean_data.py

"""
Clean Bank Statement Data

This module cleans raw bank statement data by normalizing column names,
converting data types, masking sensitive information, and removing unwanted
transactions.

Functions:
    mask_description: Replace description patterns with generic labels
    drop_description: Remove transactions matching specific patterns
    clean_data: Main cleaning pipeline for bank statement data
"""

import sys
import logging
from typing import Optional

from pandas import DataFrame
from haashi_pkg.utility import Logger
from haashi_pkg.data_engine import DataLoader, DataAnalyzer, DataSaver


# Configuration: Patterns to mask with generic descriptions
MASKING_MAP = {
    "Transfer": "Transfers",
    "Mobile|Airtime|SMS|USSD": "Phone & Data",
    "Electricity": "Electricity bill",
    "Card|Merchant": "Purchases",
}


def mask_description(
    df: DataFrame,
    col: str,
    pattern: str,
    generic_desc: str
) -> None:
    """
    Replace description patterns with generic labels for privacy/grouping.

    Modifies the DataFrame in-place by masking matching descriptions.

    """
    mask = df[col].str.contains(pattern, na=False)
    df.loc[mask, col] = generic_desc


def drop_description(
    df: DataFrame,
    col: str,
    pattern: str
) -> DataFrame:
    """
    Remove transactions with descriptions matching a pattern.

    Returns a new DataFrame with matching rows removed.

    """
    mask = df[col].str.contains(pattern, na=False)
    rows_to_drop = df[mask]
    return df.drop(rows_to_drop.index)


def clean_data(
    filepath: str = "data/sample_bank_statement_2025.xlsx",
    savepath: str = "data/cleaned_bank_statement_2025.parquet",
    use_fake_data: bool = True,
    logger: Optional[Logger] = None
) -> None:
    """
    Clean raw bank statement data and save as compressed Parquet.

    Performs the following operations:
    1. Loads Excel data (skipping header rows if needed)
    2. Normalizes column names
    3. Filters to debit-only transactions
    4. Removes unnecessary columns
    5. Drops specific transaction types (savings, investments)
    6. Masks sensitive information
    7. Converts data types
    8. Adds derived columns (transaction month)
    9. Saves as compressed Parquet

    """
    # Initialize logger if not provided
    if logger is None:
        logger = Logger(level=logging.INFO)

    # Determine file path and skip rows based on data source
    file_path = filepath if use_fake_data else "data/bank_statement_2025.xlsx"
    rows_to_skip = 0 if use_fake_data else 6

    logger.info(f"Loading data from {file_path}")
    logger.debug(f"Skipping {rows_to_skip} header rows")

    # Load data
    loader = DataLoader(file_path, logger=logger)
    bank_st_df = loader.load_excel_single(skip_rows=rows_to_skip)

    logger.info(f"Loaded {len(bank_st_df)} transactions")
    logger.debug("Starting data cleaning...")

    # Initialize analyzer
    analyzer = DataAnalyzer(logger=logger)

    # Normalize column names
    logger.debug("Normalizing column names")
    bank_st_df = analyzer.normalize_column_names(bank_st_df)
    bank_st_df.columns = bank_st_df.columns.str.replace(" ", "_")

    # Filter to debit transactions only
    logger.debug("Filtering to debit transactions only")
    initial_count = len(bank_st_df)
    bank_st_df = bank_st_df[bank_st_df["credit(₦)"] == "--"]
    logger.debug(f"Kept {len(bank_st_df)}/{initial_count} debit transactions")

    # Drop unnecessary columns
    logger.debug("Removing unnecessary columns")
    columns_to_drop = [
        "value_date",
        "channel",
        "credit(₦)",
        "balance_after(₦)",
        "transaction_reference",
    ]
    bank_st_df = bank_st_df.drop(columns=columns_to_drop)

    # Rename trans._date column
    bank_st_df = bank_st_df.rename(columns={"trans._date": "trans_date"})

    # Drop specific transaction types
    logger.debug("Removing savings and investment transactions")

    # Patterns for transactions to exclude
    phone_numbers = "8051021438|9058929223|8111016740|9037527321"
    keywords = "Save|OWealth|Fixed"

    before_drop = len(bank_st_df)
    bank_st_df = drop_description(bank_st_df, "description", phone_numbers)
    bank_st_df = drop_description(bank_st_df, "description", keywords)
    dropped = before_drop - len(bank_st_df)

    logger.debug(f"Removed {dropped} excluded transactions")

    # Mask sensitive/specific descriptions with generic labels
    logger.debug("Masking transaction descriptions")
    for pattern, generic_desc in MASKING_MAP.items():
        mask_description(bank_st_df, "description", pattern, generic_desc)

    # Convert data types
    logger.debug("Converting data types")
    bank_st_df["trans_date"] = analyzer.convert_datetime(
        bank_st_df["trans_date"])
    bank_st_df["description"] = bank_st_df["description"].astype("category")
    bank_st_df["debit(₦)"] = analyzer.convert_numeric(bank_st_df["debit(₦)"])

    # Add derived column: transaction month
    logger.debug("Adding transaction month column")
    bank_st_df["trans_month"] = bank_st_df["trans_date"].dt.to_period("M")

    # Final validation
    logger.debug("Validating cleaned data")
    analyzer.validate_columns_exist(
        bank_st_df,
        ["trans_date", "description", "debit(₦)", "trans_month"]
    )

    logger.info(f"Cleaning completed: {len(bank_st_df)} transactions retained")
    logger.info(
        f"Date range: {bank_st_df['trans_date'].min()} to {bank_st_df['trans_date'].max()}")
    logger.info(f"Categories: {bank_st_df['description'].nunique()}")

    # Save cleaned data
    logger.debug(f"Saving to {savepath}")
    saver = DataSaver(logger=logger)
    saver.save_parquet_compressed(bank_st_df, savepath)

    logger.info(f"Data cleaned and saved to {savepath}")


def main() -> None:
    """Run data cleaning as standalone script."""
    logger = Logger(level=logging.INFO)

    try:
        logger.info("Starting bank statement cleaning...")
        clean_data(logger=logger)
        logger.info("Cleaning completed successfully")

    except KeyboardInterrupt:
        logger.info("\n\nProcess interrupted by user")
        sys.exit(0)

    except Exception as e:
        logger.error(exception=e, save_to_json=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
