

# clean_data.py

import sys
import logging

from pandas import DataFrame
from haashi_pkg.data_engine.dataengine import (
    DataValidationError,
    DataEngine
)
from haashi_pkg.data_engine.dataloader import DataLoader
from haashi_pkg.data_engine.datasaver import DataSaver
from haashi_pkg.utility.utils import Utility


FILEPATH: str = "_01_csv_files/retail_sales.csv"
SAVEPATH: str = "_02_cleaned_data/retail_sales.parquet"

de = DataEngine()


def inspection_and_validation(
    df: DataFrame,
    cols: list[str] | str,
    start_inspect: bool = True
) -> None:

    if start_inspect:

        all_columns = [col for col in df.columns]
        missing_vals = de.count_missing(df, all_columns)
        Utility(level=logging.INFO).debug(missing_vals)

        if isinstance(cols, list):
            for col in cols:
                try:
                    de.validate_numeric_non_negative(df, col)
                except DataValidationError as dve:
                    Utility(level=logging.INFO).debug(dve)
        else:
            try:
                de.validate_numeric_non_negative(df, cols)
            except DataValidationError as dve:
                Utility(level=logging.INFO).debug(dve)


def clean_data() -> None:

    sales_df = DataLoader(FILEPATH).load_csv_single()

    # ====================
    #  Initial Inspection
    # ====================

    de.inspect_dataframe(sales_df, verbose=False)

    inspection_and_validation(sales_df, ["price", "quantity"], False)

    # ================
    # Cleaning
    # ================

    sales_df = sales_df.rename(columns={"product_id": "raw_id"})

    sales_df["category"] = sales_df.category.fillna("Unknown")
    sales_df["region"] = sales_df.region.fillna("Unknown")

    for col in ["category", "region", "sale_date"]:
        if col == "sale_date":
            sales_df[col] = de.convert_datetime(sales_df[col])
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

    de.inspect_dataframe(sales_df, verbose=False)

    inspection_and_validation(sales_df, ["price", "quantity"], False)

    # ================
    # Saving
    # ================
    DataSaver().save_parquet_default(sales_df, SAVEPATH)


if __name__ == "__main__":
    try:
        clean_data()
    except KeyboardInterrupt:
        print()
        sys.exit(1)
