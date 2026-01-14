

# clean_data.py

import logging

from haashi_pkg.data_engine.dataloader import DataLoader
from haashi_pkg.data_engine.dataengine import DataEngine
from haashi_pkg.data_engine.datasaver import DataSaver
from haashi_pkg.utility.utils import Utility
from pandas import DataFrame

USE_FAKE_DATA: bool = True


if USE_FAKE_DATA:
    FILEPATH: str = "dataset/sample_bank_statement_2025.xlsx"
else:
    FILEPATH: str = "dataset/bank_statement_2025.xlsx"

SAVEPATH: str = "cleaned_data/cleaned_bank_statement_2025.parquet"

MASKING_RULES = {
    "Transfer": "Transfers",
    "Mobile|Airtime|SMS|USSD": "Phone & Data",
    "Electricity": "Electricity bill",
    "Card|Merchant": "Purchases",
}

# Initializtion

dl = DataLoader(FILEPATH)
de = DataEngine()
ds = DataSaver()
ut = Utility(level=logging.INFO)


def mask_description(
    df: DataFrame, col: str, pattern: str, generic_desc: str
) -> None:
    df.loc[df[col].str.contains(pattern, na=False), col] = generic_desc


def drop_description(
    df: DataFrame, col: str, pattern: str
) -> DataFrame:
    rows_to_drop = df[df[col].str.contains(pattern, na=False)]
    return df.drop(rows_to_drop.index)


def clean_data() -> None:

    # load data
    if USE_FAKE_DATA:
        bank_st_df = dl.load_excel_single(skip_rows=0)
    else:
        bank_st_df = dl.load_excel_single(skip_rows=6)

    # inspect data
    de.inspect_dataframe(bank_st_df, verbose=False)

    # ---------------------
    # Cleaning
    # ---------------------

    bank_st_df = de.normalize_column_names(bank_st_df)

    bank_st_df.columns = bank_st_df.columns.str.replace(" ", "_")
    bank_st_df = bank_st_df[bank_st_df["credit(₦)"] == "--"]
    bank_st_df = bank_st_df.drop(columns=[
        "value_date",
        "channel",
        "credit(₦)",
        "balance_after(₦)",
        "transaction_reference",
    ])

    bank_st_df = bank_st_df.rename(columns={"trans._date": "trans_date"})

    # ---------------------
    # Dropping descriptions
    # ---------------------

    num_pattern: str = "8051021438|9058929223|8111016740|9037527321"
    save_pattern: str = "Save|OWealth|Fixed"

    bank_st_df = drop_description(bank_st_df, "description", num_pattern)
    bank_st_df = drop_description(bank_st_df, "description", save_pattern)

    # -----------------
    # Masking
    # -----------------

    for desc, generic_desc in MASKING_RULES.items():
        mask_description(bank_st_df, "description", desc, generic_desc)

    ut.debug(bank_st_df.description.unique())

    # -----------------
    # Conversions
    # -----------------

    bank_st_df["trans_date"] = de.convert_datetime(bank_st_df["trans_date"])
    bank_st_df["description"] = bank_st_df["description"].astype("category")
    bank_st_df["debit(₦)"] = de.convert_numeric(bank_st_df["debit(₦)"])

    # New column
    bank_st_df["trans_month"] = bank_st_df["trans_date"].dt.to_period("M")

    # Final inspection
    de.inspect_dataframe(bank_st_df, verbose=False)

    # Save data
    ds.save_parquet_compressed(bank_st_df, SAVEPATH)


if __name__ == "__main__":
    clean_data()
