

# sample_data_generator.py

import pandas as pd
import numpy as np
import sys
from datetime import datetime, timedelta


def generate_sample_bank_statement(num_transactions: int = 100) -> None:
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

    df = df.sort_values("Trans. Date").reset_index(drop=True)
    df.to_excel("data/sample_bank_statement_2025.xlsx", index=False)
    print("Sample data generated!")


if __name__ == "__main__":
    try:
        generate_sample_bank_statement()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
