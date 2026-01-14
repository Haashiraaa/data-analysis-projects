
# analyze_data.py


from haashi_pkg.data_engine.dataloader import DataLoader
from haashi_pkg.data_engine.dataengine import DataEngine
from pandas import DataFrame


FILE_PATH = "cleaned_data/cleaned_bank_statement_2025.parquet"

dl = DataLoader(FILE_PATH)
de = DataEngine()

ReturnLike = tuple[DataFrame, DataFrame, float, int, float]


def load_data() -> DataFrame:
    return dl.load_parquet_single()


def aggregations() -> ReturnLike:
    bank_st_df = load_data()

    monthly_spending = (
        de.aggregate(bank_st_df, "debit(₦)", "trans_month", "sum")
        .reset_index()
        .rename(columns={
            "trans_month": "months",
            "debit(₦)": "total_spending",
        })
        .sort_values("months")
    )

    spend_by_category = (
        de.aggregate(bank_st_df, "debit(₦)", "description", "sum")
        .reset_index()
        .rename(columns={
            "description": "category",
            "debit(₦)": "total_spending",
        })
        .sort_values("total_spending", ascending=False)
    )

    monthly_avg = float(monthly_spending.total_spending.median())
    max_expense = bank_st_df["debit(₦)"].max()

    return (
        monthly_spending,
        spend_by_category,
        monthly_avg,
        len(bank_st_df),
        max_expense
    )


"""

if __name__ == "__main__":
    aggregations()
"""
