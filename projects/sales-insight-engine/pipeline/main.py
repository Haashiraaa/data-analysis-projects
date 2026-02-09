
# main.py

from clean_data import clean_data
from visualize_data import visualize_data
from haashi_pkg.utility import Logger
import sys
import logging


logger = Logger(level=logging.INFO)

if len(sys.argv) > 1:
    if "-d" or "--debug" in sys.argv:
        logger = Logger(level=logging.DEBUG)


def main(logger: Logger = logger) -> None:
    clean_data(logger=logger)
    visualize_data(logger=logger)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n\nProgram terminated by user")
        sys.exit(0)
    except Exception as e:
        logger.error(exception=e, save_to_json=True,)
        sys.exit(1)
