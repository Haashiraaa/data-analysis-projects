
# main.py

from clean_data import clean_data
from visualize_data import visualize_data
from haashi_pkg.utility.utils import Utility
import sys
import logging


FILEPATH: str = "data/retail_sales.csv"
SAVEPATH: str = "data/cleaned_retail_sales.parquet"
PLOTPATH: str = "data/plots/retail_sales_plots.png"


def main():
    clean_data(FILEPATH, SAVEPATH)
    print("Data cleaned and saved to " + SAVEPATH)
    print("Analyzing data...")
    print("Plotting data...")
    visualize_data(PLOTPATH)
    print("Data visualized and saved to " + PLOTPATH)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user")
        sys.exit(0)
    except Exception as e:
        print("\n\nSomething went wrong!")
        Utility(logging.INFO).debug(e)
        sys.exit(1)
