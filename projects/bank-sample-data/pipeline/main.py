

# main.py

from haashi_pkg.utility import Logger
from clean_data import clean_data
from sample_data_generator import generate_sample_bank_statement
from visualize_data import visualize_data
import sys
import logging


logger = Logger(level=logging.INFO)
if len(sys.argv) > 1:
    if "-d" or "--debug" in sys.argv:
        logger = Logger(level=logging.DEBUG)


def main(logger: Logger = logger) -> None:
    generate_sample_bank_statement(logger=logger)
    clean_data(logger=logger)
    visualize_data(logger=logger)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(exception=e, save_to_json=True)
        sys.exit(1)
