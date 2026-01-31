

# main.py

from visualize_data import visualize_data
from haashi_pkg.utility.utils import Utility
import sys
import logging

# pyright: basic


def main() -> None:
    try:
        print("\n\nSetting up data...")
        print("Visualizing data...")
        visualize_data()
    except Exception as e:
        print("Something went wrong!")
        Utility(logging.INFO).debug(e)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
