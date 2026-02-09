

# main.py

import sys
import logging
from visualize_data import visualize_data
from haashi_pkg.utility import Logger


logger = Logger(level=logging.INFO)
if len(sys.argv) > 1:
    if "-d" or "--debug" in sys.argv:
        logger = Logger(level=logging.DEBUG)


def main(logger: Logger = logger) -> None:
    visualize_data(logger=logger)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Main process interrupted.")
        sys.exit(0)
    except Exception as e:
        logger.error(exception=e, save_to_json=True)
        sys.exit(0)
