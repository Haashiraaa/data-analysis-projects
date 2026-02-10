

# clean_data.py

"""Clean retail sales data and prepare for analysis."""

import sys
import logging
from typing import Optional, Union, List

from pandas import DataFrame, Series
from haashi_pkg.utility import Logger
from haashi_pkg.data_engine import (
    DataAnalyzer,
    DataLoader,
    DataSaver,
    DataValidationError
)


def validate_numeric_columns(
    df: DataFrame,
    columns: Union[str, List[str]],
    analyzer: DataAnalyzer,
    logger: Logger
) -> None:
    """Validate that numeric columns are non-negative."""
    cols_to_check = [columns] if isinstance(columns, str) else columns

    for col in cols_to_check:
        try:
            analyzer.validate_numeric_non_negative(df, col)
            logger.debug(f"✓ Column '{col}' validated")
        except DataValidationError as e:
            logger.error(
                f"Validation failed for column '{col}'",
                exception=e,
                save_to_json=True
            )


def inspect_missing_data(
    df: DataFrame,
    analyzer: DataAnalyzer,
    logger: Logger
) -> None:
    """Log missing value counts for all columns."""
    all_columns = list(df.columns)
    missing_counts = analyzer.count_missing(df, all_columns)

    total_missing = sum(missing_counts)
    if total_missing > 0:
        logger.debug(f"Missing values found: {total_missing} total")
        for col, count in zip(all_columns, missing_counts):
            if count > 0:
                logger.debug(f"  {col}: {count} missing")
    else:
        logger.debug("No missing values found")


def clean_data(
    filepath: str = "data/retail_sales.csv",
    savepath: str = "data/cleaned_retail_sales.parquet",
    logger: Optional[Logger] = None
) -> None:
    """
    Clean retail sales data and save as Parquet.

    Steps:
    - Load CSV data
    - Fill missing categories/regions with 'Unknown'
    - Convert data types
    - Remove invalid rows (negative/zero prices or quantities)
    - Calculate revenue and add sale month
    - Validate cleaned data
    - Save as Parquet
    """
    if logger is None:
        logger = Logger(level=logging.INFO)

    logger.info(f"Loading data from {filepath}")

    # Load data
    loader = DataLoader(filepath, logger=logger)
    sales_df = loader.load_csv_single()

    logger.info(f"Loaded {len(sales_df)} records")

    # Initialize analyzer
    analyzer = DataAnalyzer(logger=logger)

    # Initial inspection
    logger.debug("Performing initial data inspection")
    inspect_missing_data(sales_df, analyzer, logger)

    # Cleaning operations
    logger.debug("Starting data cleaning...")

    # Rename column
    sales_df = sales_df.rename(columns={"product_id": "raw_id"})

    # Fill missing categorical values
    logger.debug("Filling missing categorical values")
    sales_df["category"] = sales_df.category.fillna("Unknown")
    sales_df["region"] = sales_df.region.fillna("Unknown")

    # Convert data types
    logger.debug("Converting data types")
    sales_df["sale_date"] = analyzer.convert_datetime(
        Series(sales_df["sale_date"]))
    sales_df["category"] = sales_df["category"].astype("category")
    sales_df["region"] = sales_df["region"].astype("category")

    # Remove invalid rows
    logger.debug("Removing invalid rows (negative or zero values)")
    invalid_rows = DataFrame(
        sales_df[(sales_df.price <= 0) | (sales_df.quantity <= 0)]
    )

    if len(invalid_rows) > 0:
        logger.debug(f"Dropping {len(invalid_rows)} invalid rows")
        sales_df = sales_df.drop(invalid_rows.index)

    # Calculate derived columns
    logger.debug("Calculating revenue and sale month")
    sales_df["revenue"] = sales_df.price * sales_df.quantity
    sales_df["sale_month"] = sales_df.sale_date.dt.to_period("M")

    # Sort by date
    sales_df = sales_df.sort_values(by="sale_date")

    # Final validation
    logger.debug("Validating cleaned data")
    validate_numeric_columns(
        sales_df, ["price", "quantity", "revenue"], analyzer, logger
    )

    logger.info(f"Cleaning completed: {len(sales_df)} records retained")
    logger.info(
        f"Date range: {sales_df['sale_date'].min()} to {sales_df['sale_date'].max()}")
    logger.info(f"Total revenue: ${sales_df['revenue'].sum():,.2f}")

    # Save cleaned data
    logger.debug(f"Saving to {savepath}")
    saver = DataSaver(logger=logger)
    saver.save_parquet_default(sales_df, savepath)

    logger.info(f"Data saved to {savepath}")


def main() -> None:
    """Run cleaning as standalone script."""
    logger = Logger(level=logging.INFO)

    try:
        logger.info("Starting retail sales data cleaning...")
        clean_data(logger=logger)
        logger.info("Cleaning completed successfully")

    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user")
        sys.exit(0)

    except Exception as e:
        logger.error(exception=e, save_to_json=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
