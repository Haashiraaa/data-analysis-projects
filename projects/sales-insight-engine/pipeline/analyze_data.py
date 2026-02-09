

# analyze_data.py


import sys
import logging
from haashi_pkg.data_engine import DataAnalyzer, DataLoader
from haashi_pkg.utility import Logger
from pandas import DataFrame
from typing import Optional


# pyright: basic

logger = Logger(level=logging.INFO)
analyze = DataAnalyzer(logger)

ReturnLike = Optional[
    tuple[DataFrame, DataFrame, DataFrame, DataFrame, str, str]
]


def _01_aggregate_helper_func(
    df: DataFrame,
    target_col_name: str,
    groupby_col_name: str,
    sort_col_name: str,
    new_name: str,
    asc: bool = True
) -> DataFrame:

    return analyze.aggregate(
        df, target_col_name, groupby_col_name, op="sum"
    ).reset_index().sort_values(
        by=sort_col_name, ascending=asc
    ).rename(columns={target_col_name: new_name})


def retail_data_label(df: DataFrame, date_col_name: str) -> tuple[str, ...]:
    start_date = df[date_col_name].min()
    end_date = df[date_col_name].max()

    start_str = start_date.strftime("%b %Y")
    end_str = end_date.strftime("%b %Y")

    return start_str, end_str


def analyze_data(
    filepath: str = "data/cleaned_retail_sales.parquet",
    logger: Logger = logger,
    can_return: bool = True
) -> ReturnLike:

    sales_df = DataLoader(filepath, logger=logger).load_parquet_single()
    analyze.inspect_dataframe(sales_df, verbose=False)

    logger.debug("Analyzing data..")
    # Revenue per category
    revenue_by_cat = _01_aggregate_helper_func(
        sales_df, "revenue", "category", "revenue", "total_revenue", False
    )

    # Revenue per region
    revenue_by_region = _01_aggregate_helper_func(
        sales_df, "revenue", "region", "revenue", "total_revenue", False
    )

    # Revenue per month
    revenue_by_month = _01_aggregate_helper_func(
        sales_df, "revenue", "sale_month", "sale_month", "total_revenue"
    )

    pct_change = revenue_by_month.set_index("sale_month").resample(
        "M"
    )["total_revenue"].sum().pct_change().reset_index()

    revenue_by_month = analyze.merge(
        revenue_by_month, pct_change, "sale_month",
    ).rename(columns={
        "total_revenue_x": "total_revenue",
        "total_revenue_y": "revenue_pct_change"
    }).fillna(0)

    revenue_by_month["revenue_pct_change_pct"] = (
        revenue_by_month.revenue_pct_change * 100
    )

    start_date, end_date = retail_data_label(sales_df, "sale_date")

    logger.info("Data analyzed")

    if can_return:
        return (
            sales_df,
            revenue_by_cat,
            revenue_by_region,
            revenue_by_month,
            start_date,
            end_date,
        )


if __name__ == "__main__":
    try:
        analyze_data(can_return=False)
    except KeyboardInterrupt:
        logger.info("Program terminated by user")
        sys.exit(1)
