# sample_data_generator.py

import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from haashi_pkg.utility.utils import Utility


ut = Utility(level=logging.WARNING)


def generate_sample_bank_statement(num_transactions: int = 100) -> pd.DataFrame:
    """Generate fake bank statement data for demo purposes."""

    np.random.seed(42)  # Reproducible fake data

    # Random dates in 2025
    start_date = datetime(2025, 1, 1)
    dates = [start_date + timedelta(days=np.random.randint(0, 365))
             for _ in range(num_transactions)]

    # Random transaction types
    descriptions = [
        "Transfer to John Doe",
        "POS Merchant Purchase - Sample Store",
        "Mobile Data - Sample Telco",
        "Electricity Bill - Sample Disco",
        "ATM Card Withdrawal",
        "Online Merchant Purchase - Sample Site",
        "Airtime Recharge",
        "USSD Charge",
    ]

    # Random amounts
    debits = np.random.randint(500, 50000, num_transactions)

    df = pd.DataFrame({
        "Trans. Date": dates,
        "Value Date": dates,
        "Description": np.random.choice(descriptions, num_transactions),
        "Debit(₦)": debits,
        "Credit(₦)": ["--"] * num_transactions,
        "Balance After(₦)": ["--"] * num_transactions,
        "Channel": ["Mobile"] * num_transactions,
        "Transaction Reference": [f"REF{i:06d}" for i in range(num_transactions)]
    })

    return df.sort_values("Trans. Date").reset_index(drop=True)


if __name__ == "__main__":
    # Generate and save sample data
    sample_df = generate_sample_bank_statement(150)
    path = ut.ensure_writable_path("dataset/sample_bank_statement_2025.xlsx")
    sample_df.to_excel(path, index=False)
    print("Sample data generated!")

