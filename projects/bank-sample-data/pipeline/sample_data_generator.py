

# sample_data_generator.py

"""
Sample Bank Statement Data Generator

This module generates fake bank statement data for testing and demonstration
purposes. Creates realistic-looking transaction records with random dates,
descriptions, and amounts.

Functions:
    generate_sample_bank_statement: Generate fake bank statement Excel file
"""

import sys
import logging
from typing import Optional
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
from haashi_pkg.utility import Logger, FileHandler


def generate_sample_bank_statement(
    num_transactions: int = 100,
    save_path: str = "data/sample_bank_statement_2025.xlsx",
    logger: Optional[Logger] = None
) -> None:
    """
    Generate fake bank statement data and save as Excel file.
    """
    # Initialize logger if not provided
    if logger is None:
        logger = Logger(level=logging.INFO)

    logger.info(f"Generating {num_transactions} sample bank transactions...")

    # Set random seed for reproducibility
    np.random.seed(42)

    # Generate random dates in 2025
    logger.debug("Generating random transaction dates")
    start_date = datetime(2025, 1, 1)
    dates = [
        start_date + timedelta(days=np.random.randint(0, 365))
        for _ in range(num_transactions)
    ]

    # Define realistic transaction descriptions
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

    # Generate random transaction amounts (₦500 to ₦50,000)
    logger.debug("Generating random transaction amounts")
    debits = np.random.randint(500, 50000, num_transactions)

    # Create DataFrame
    logger.debug("Creating DataFrame")
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

    # Sort by date
    logger.debug("Sorting transactions by date")
    df = df.sort_values("Trans. Date").reset_index(drop=True)

    # Ensure directory exists
    logger.debug(f"Ensuring directory exists for {save_path}")
    file_handler = FileHandler(logger=logger)
    validated_path = str(file_handler.ensure_writable_path(save_path))

    # Save to Excel
    logger.debug(f"Saving to {validated_path}")
    df.to_excel(validated_path, index=False)

    # Calculate summary stats
    total_amount = df["Debit(₦)"].sum()
    avg_amount = df["Debit(₦)"].mean()
    date_range = f"{df['Trans. Date'].min().strftime('%Y-%m-%d')} to {df['Trans. Date'].max().strftime('%Y-%m-%d')}"

    logger.info(f"Sample data generated and saved to {validated_path}")
    logger.info(f"  Transactions: {num_transactions}")
    logger.info(f"  Date range: {date_range}")
    logger.info(f"  Total debits: ₦{total_amount:,}")
    logger.info(f"  Average transaction: ₦{avg_amount:,.2f}")


def main() -> None:
    """Run sample data generator as standalone script."""
    logger = Logger(level=logging.INFO)

    try:
        logger.info("Starting sample data generation...")
        generate_sample_bank_statement(logger=logger)
        logger.info("Generation completed successfully")

    except KeyboardInterrupt:
        logger.info("\n\nProcess interrupted by user")
        sys.exit(0)

    except Exception as e:
        logger.error(exception=e, save_to_json=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
