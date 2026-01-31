

# main.py

from visualize_data import visualize_data
from haashi_pkg.utility.utils import Utility
import sys
import logging


FILEPATH = "data/4150697.csv"
PLOT_PATH: str = "data/plots/weather_data.png"


def main() -> None:

    try:
        print("\n\nCleaning data...")
        print("Visualizing data...")
        visualize_data(PLOT_PATH, FILEPATH)
    except Exception as e:
        print("\n\nSomething went wrong.")
        Utility(logging.INFO).debug(e)
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMain process interrupted.")
        sys.exit(0)
