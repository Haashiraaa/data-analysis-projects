

# analyze_data.py


"""
Analyze Bank Statement Data

This module performs aggregation and analysis on cleaned bank statement data,
calculating monthly spending totals and category breakdowns.

Functions:
    aggregations: Aggregate transaction data by month and category
"""

import sys
import logging
from typing import Optional, Tuple

from pandas import DataFrame
from haashi_pkg.utility import Logger
from haashi_pkg.data_engine import DataLoader, DataAnalyzer


# Type alias for return value
AggregationResult = Tuple[DataFrame, DataFrame, float, int, float]


def aggregations(
    filepath: str = "data/cleaned_bank_statement_2025.parquet",
    logger: Optional[Logger] = None,
    can_return: bool = True
) -> Optional[AggregationResult]:
    """
    Aggregate bank statement data by month and category.

    Calculates monthly spending totals, spending by category, median monthly
    spending, transaction count, and maximum single expense.

    Returns:
        Tuple containing:
            - monthly_spending: DataFrame with total spending per month
            - spend_by_category: DataFrame with total spending per category
            - monthly_avg: Median monthly spending amount
            - transaction_count: Total number of transactions
            - max_expense: Largest single transaction amount

        Returns None if can_return is False. 
    """
    # Initialize logger if not provided
    if logger is None:
        logger = Logger(level=logging.INFO)

    logger.debug(f"Loading data from {filepath}")

    # Initialize analyzer and load data
    analyzer = DataAnalyzer(logger=logger)
    loader = DataLoader(filepath, logger=logger)
    bank_st_df = loader.load_parquet_single()

    logger.debug(f"Loaded {len(bank_st_df)} transactions")
    logger.debug("Performing aggregations...")

    # Aggregate by month
    monthly_spending = (
        analyzer.aggregate(bank_st_df, "debit(₦)", "trans_month", "sum")
        .reset_index()
        .rename(columns={
            "trans_month": "months",
            "debit(₦)": "total_spending",
        })
        .sort_values("months")
    )

    logger.debug(f"Calculated spending across {len(monthly_spending)} months")

    # Aggregate by category
    spend_by_category = (
        analyzer.aggregate(bank_st_df, "debit(₦)", "description", "sum")
        .reset_index()
        .rename(columns={
            "description": "category",
            "debit(₦)": "total_spending",
        })
        .sort_values("total_spending", ascending=False)
    )

    logger.debug(
        f"Calculated spending across {len(spend_by_category)} categories")

    # Calculate summary statistics
    monthly_avg = float(monthly_spending.total_spending.median())
    max_expense = float(bank_st_df["debit(₦)"].max())
    transaction_count = len(bank_st_df)

    logger.info("Aggregations completed successfully")
    logger.info(f"  Median monthly spending: ₦{monthly_avg:,.2f}")
    logger.info(f"  Total transactions: {transaction_count}")
    logger.info(f"  Largest expense: ₦{max_expense:,.2f}")

    if can_return:
        return (
            monthly_spending,
            spend_by_category,
            monthly_avg,
            transaction_count,
            max_expense
        )

    return None


def main() -> None:
    """Run aggregations as standalone script."""
    logger = Logger(level=logging.INFO)

    try:
        logger.info("Starting bank statement analysis...")
        aggregations(logger=logger, can_return=False)
        logger.info("Analysis completed successfully")

    except KeyboardInterrupt:
        logger.info("\n\nProcess interrupted by user")
        sys.exit(0)

    except Exception as e:
        logger.error(exception=e, save_to_json=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
