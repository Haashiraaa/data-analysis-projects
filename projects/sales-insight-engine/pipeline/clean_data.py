

# clean_data.py

import sys
import logging
from pandas import DataFrame, Series
from haashi_pkg.data_engine import (
    DataValidationError,
    DataAnalyzer,
    DataLoader,
    DataSaver,
)
from haashi_pkg.utility import Logger


# pyright: basic


logger = Logger(level=logging.INFO)
analyze = DataAnalyzer(logger)


def inspection_and_validation(
    df: DataFrame,
    cols: list[str] | str,
    logger: Logger,
    start_inspect: bool = True
) -> None:

    if start_inspect:

        all_columns: list[str] = [col for col in df.columns]
        missing_vals = analyze.count_missing(df, all_columns)
        logger.debug(
            "Missing values found for each column: " + str(missing_vals)
        )

        if isinstance(cols, list):
            for col in cols:
                try:
                    analyze.validate_numeric_non_negative(df, col)
                except DataValidationError as e:
                    logger.error(
                        "Validation failed for column " + col,
                        exception=e,
                        save_to_json=True,
                        context="validating numeric non-negative"
                    )
        else:
            try:
                analyze.validate_numeric_non_negative(df, cols)
            except DataValidationError as e:
                logger.error(
                    "Validation failed for column " + cols,
                    exception=e,
                    save_to_json=True,
                    context="validating numeric non-negative"
                )


def clean_data(
    filepath: str = "data/retail_sales.csv",
    savepath: str = "data/cleaned_retail_sales.parquet",
    logger: Logger = logger
) -> None:

    sales_df = DataLoader(filepath, logger=logger).load_csv_single()

    # ====================
    #  Initial Inspection
    # ====================

    analyze.inspect_dataframe(sales_df, verbose=False)

    inspection_and_validation(
        sales_df, ["price", "quantity"], logger, start_inspect=False
    )

    # ================
    # Cleaning
    # ================

    sales_df = sales_df.rename(columns={"product_id": "raw_id"})

    sales_df["category"] = sales_df.category.fillna("Unknown")
    sales_df["region"] = sales_df.region.fillna("Unknown")

    for col in ["category", "region", "sale_date"]:
        if col == "sale_date":
            sales_df[col] = analyze.convert_datetime(Series(sales_df[col]))
        else:
            sales_df[col] = sales_df[col].astype("category")

    neg_or_zero = sales_df[
        (sales_df.price <= 0) | (sales_df.quantity <= 0)
    ]

    sales_df = sales_df.drop(neg_or_zero.index)

    sales_df["revenue"] = sales_df.price * sales_df.quantity
    sales_df["sale_month"] = sales_df.sale_date.dt.to_period("M")
    sales_df = sales_df.sort_values(by="sale_date")

    # ====================
    #  Final Inspection
    # ====================

    analyze.inspect_dataframe(sales_df, verbose=False)

    inspection_and_validation(
        sales_df, ["price", "quantity"], logger, start_inspect=False
    )

    # ================
    # Saving
    # ================
    DataSaver(logger=logger).save_parquet_default(sales_df, savepath)


if __name__ == "__main__":
    try:
        clean_data()
    except KeyboardInterrupt:
        logger.info("\n\nProgram terminated by user")
        sys.exit(1)
