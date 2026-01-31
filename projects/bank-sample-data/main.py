

# main.py

from haashi_pkg.utility.utils import Utility
from clean_data import clean_data
from sample_data_generator import generate_sample_bank_statement
from visualize_data import visualize_data
import sys
import logging


def main() -> None:
    try:
        print("\nGenerating sample data...")
        generate_sample_bank_statement()
        print("Cleaning data...")
        clean_data()
        print("Analyzing data...")
        print("Visualizing data...")
        visualize_data()
    except Exception as e:
        print("\nSomething went wrong!")
        Utility(logging.INFO).info(e)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
