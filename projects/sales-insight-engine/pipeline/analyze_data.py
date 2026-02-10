

# analyze_data.py

"""Analyze retail sales data and calculate revenue metrics."""

import sys
import logging
from typing import Optional, Tuple

from pandas import DataFrame
from haashi_pkg.utility import Logger
from haashi_pkg.data_engine import DataAnalyzer, DataLoader


# Type alias for return value
AnalysisResult = Tuple[DataFrame, DataFrame, DataFrame, DataFrame, str, str]


def aggregate_revenue(
    df: DataFrame,
    target_col: str,
    groupby_col: str,
    sort_col: str,
    new_name: str,
    ascending: bool = True,
    analyzer: Optional[DataAnalyzer] = None
) -> DataFrame:
    """Aggregate revenue data by specified column."""
    if analyzer is None:
        analyzer = DataAnalyzer()

    return (
        analyzer.aggregate(df, target_col, groupby_col, op="sum")
        .reset_index()
        .sort_values(by=sort_col, ascending=ascending)
        .rename(columns={target_col: new_name})
    )


def get_date_range_labels(df: DataFrame, date_col: str) -> Tuple[str, str]:
    """Get formatted start and end date labels (e.g., 'Jan 2024')."""
    start_date = df[date_col].min()
    end_date = df[date_col].max()

    return start_date.strftime("%b %Y"), end_date.strftime("%b %Y")


def analyze_data(
    filepath: str = "data/cleaned_retail_sales.parquet",
    logger: Optional[Logger] = None,
    can_return: bool = True
) -> Optional[AnalysisResult]:
    """
    Analyze retail sales data and calculate revenue metrics.

    Aggregates revenue by category, region, and month. Calculates
    month-over-month percentage changes.
    """
    if logger is None:
        logger = Logger(level=logging.INFO)

    logger.debug(f"Loading data from {filepath}")

    # Load data
    loader = DataLoader(filepath, logger=logger)
    sales_df = loader.load_parquet_single()

    logger.debug(f"Loaded {len(sales_df)} sales records")
    logger.debug("Performing revenue aggregations...")

    # Initialize analyzer
    analyzer = DataAnalyzer(logger=logger)

    # Revenue by category
    revenue_by_cat = aggregate_revenue(
        sales_df, "revenue", "category", "revenue",
        "total_revenue", ascending=False, analyzer=analyzer
    )

    # Revenue by region
    revenue_by_region = aggregate_revenue(
        sales_df, "revenue", "region", "revenue",
        "total_revenue", ascending=False, analyzer=analyzer
    )

    # Revenue by month
    revenue_by_month = aggregate_revenue(
        sales_df, "revenue", "sale_month", "sale_month",
        "total_revenue", ascending=True, analyzer=analyzer
    )

    # Calculate month-over-month percentage change
    logger.debug("Calculating month-over-month growth rates")
    pct_change = (
        revenue_by_month.set_index("sale_month")
        .resample("M")["total_revenue"]
        .sum()
        .pct_change()
        .reset_index()
    )

    # Merge percentage change back
    revenue_by_month = (
        analyzer.merge(revenue_by_month, pct_change, "sale_month")
        .rename(columns={
            "total_revenue_x": "total_revenue",
            "total_revenue_y": "revenue_pct_change"
        })
        .fillna(0)
    )

    revenue_by_month["revenue_pct_change_pct"] = (
        revenue_by_month.revenue_pct_change * 100
    )

    # Get date range labels
    start_date, end_date = get_date_range_labels(sales_df, "sale_date")

    logger.info("Analysis completed successfully")
    logger.info(f"  Date range: {start_date} - {end_date}")
    logger.info(f"  Total sales: {len(sales_df):,}")
    logger.info(f"  Categories: {len(revenue_by_cat)}")
    logger.info(f"  Regions: {len(revenue_by_region)}")

    if can_return:
        return (
            sales_df,
            revenue_by_cat,
            revenue_by_region,
            revenue_by_month,
            start_date,
            end_date,
        )

    return None


def main() -> None:
    """Run analysis as standalone script."""
    logger = Logger(level=logging.INFO)

    try:
        logger.info("Starting retail sales analysis...")
        analyze_data(logger=logger, can_return=False)
        logger.info("Analysis completed")

    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user")
        sys.exit(0)

    except Exception as e:
        logger.error(exception=e, save_to_json=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
