

# clean_data.py

import logging
import sys
from haashi_pkg.data_engine import DataLoader, DataAnalyzer, DataSaver
from haashi_pkg.utility import Logger
from pandas import DataFrame


# Initializtion
logger = Logger(level=logging.INFO)


def mask_description(
    df: DataFrame, col: str, pattern: str, generic_desc: str
) -> None:
    df.loc[df[col].str.contains(pattern, na=False), col] = generic_desc


def drop_description(
    df: DataFrame, col: str, pattern: str
) -> DataFrame:
    rows_to_drop = DataFrame(df[df[col].str.contains(pattern, na=False)])
    return df.drop(rows_to_drop.index)


def clean_data(
    filepath: str = "data/sample_bank_statement_2025.xlsx",
    savepath: str = "data/cleaned_bank_statement_2025.parquet",
    USE_FAKE_DATA: bool = True,
    logger: Logger = logger
) -> None:

    MASKING_MAP = {
        "Transfer": "Transfers",
        "Mobile|Airtime|SMS|USSD": "Phone & Data",
        "Electricity": "Electricity bill",
        "Card|Merchant": "Purchases",
    }

    file_path: str = (
        filepath if USE_FAKE_DATA else "data/bank_statement_2025.xlsx"
    )

    rows_to_skip: int = 0 if USE_FAKE_DATA else 6

    # load data
    logger.debug("Loading data...")
    bank_st_df = DataFrame(
        DataLoader(file_path, logger=logger)
        .load_excel_single(skip_rows=rows_to_skip)
    )

    logger.debug("Cleaning data...")
    analyze = DataAnalyzer(logger=logger)

    # inspect data
    analyze.inspect_dataframe(bank_st_df, verbose=False)

    # ---------------------
    # Cleaning
    # ---------------------

    bank_st_df = analyze.normalize_column_names(bank_st_df)

    bank_st_df.columns = bank_st_df.columns.str.replace(" ", "_")
    bank_st_df = bank_st_df[bank_st_df["credit(₦)"] == "--"]
    bank_st_df = bank_st_df.drop(columns=[
        "value_date",
        "channel",
        "credit(₦)",
        "balance_after(₦)",
        "transaction_reference",
    ])

    bank_st_df = DataFrame(
        bank_st_df.rename(columns={"trans._date": "trans_date"})
    )

    # ---------------------
    # Dropping descriptions
    # ---------------------

    num_pattern: str = "8051021438|9058929223|8111016740|9037527321"
    string_pattern: str = "Save|OWealth|Fixed"

    bank_st_df = drop_description(bank_st_df, "description", num_pattern)
    bank_st_df = drop_description(bank_st_df, "description", string_pattern)

    # -----------------
    # Masking
    # -----------------

    for desc, generic_desc in MASKING_MAP.items():
        mask_description(bank_st_df, "description", desc, generic_desc)

    # -----------------
    # Conversions
    # -----------------

    bank_st_df["trans_date"] = analyze.convert_datetime(
        bank_st_df["trans_date"])
    bank_st_df["description"] = bank_st_df["description"].astype("category")
    bank_st_df["debit(₦)"] = analyze.convert_numeric(bank_st_df["debit(₦)"])

    # New column
    bank_st_df["trans_month"] = bank_st_df["trans_date"].dt.to_period("M")

    # Final inspection
    analyze.inspect_dataframe(bank_st_df, verbose=False)

    # Save data
    DataSaver(logger=logger).save_parquet_compressed(bank_st_df, savepath)


if __name__ == "__main__":
    try:
        clean_data()
    except KeyboardInterrupt:
        logger.info("\n\nInterrupted by user")
        sys.exit(0)
