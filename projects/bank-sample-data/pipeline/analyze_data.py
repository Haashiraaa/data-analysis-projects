
# analyze_data.py

import sys
import logging
from haashi_pkg.utility import Logger
from haashi_pkg.data_engine import DataLoader, DataAnalyzer
from pandas import DataFrame

# pyright: basic


ReturnLike = tuple[DataFrame, DataFrame, float, int, float] | None
logger = Logger(level=logging.INFO)


def aggregations(
    filepath: str = "data/cleaned_bank_statement_2025.parquet",
    logger: Logger = logger,
    can_return: bool = True
) -> ReturnLike:

    analyze = DataAnalyzer(logger=logger)
    bank_st_df = DataLoader(filepath, logger=logger).load_parquet_single()

    logger.debug("Analyzing data...")
    monthly_spending = (
        analyze.aggregate(bank_st_df, "debit(₦)", "trans_month", "sum")
        .reset_index()
        .rename(columns={
            "trans_month": "months",
            "debit(₦)": "total_spending",
        })
        .sort_values("months")
    )

    spend_by_category = (
        analyze.aggregate(bank_st_df, "debit(₦)", "description", "sum")
        .reset_index()
        .rename(columns={
            "description": "category",
            "debit(₦)": "total_spending",
        })
        .sort_values("total_spending", ascending=False)
    )

    monthly_avg = float(monthly_spending.total_spending.median())
    max_expense = bank_st_df["debit(₦)"].max()

    if can_return:
        return (  # type: ignore
            monthly_spending,
            spend_by_category,
            monthly_avg,
            len(bank_st_df),
            max_expense
        )


if __name__ == "__main__":
    try:
        aggregations(can_return=False)
    except KeyboardInterrupt:
        logger.info("\n\nInterrupted by user")
        sys.exit(0)
