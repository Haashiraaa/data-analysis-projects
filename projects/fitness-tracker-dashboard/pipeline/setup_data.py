

# setup_data.py

import logging
import sys
from pandas import DataFrame
from typing import List, Dict, Union
from haashi_pkg.data_engine import DataAnalyzer
from haashi_pkg.utility import Logger
from typing import Iterable


ValueLike = Union[List[str], List[int], List[float]]
logger = Logger(level=logging.INFO)

# ------------------------------------
# Data Setup
# ------------------------------------


def setup_data(
    logger: Logger = logger,
    can_return: bool = True
) -> Iterable[DataFrame] | None:

    logger.debug('Setting up data...')

    analyze = DataAnalyzer(logger=logger)

    days: list[str] = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    # Weekly steps for each user
    weekly_steps: Dict[str, Union[List[str], List[int]]] = {
        'days': [day for day in days],
        'alex': [8500, 9000, 12000, 10000, 9500, 13000, 12500],
        'bree': [7000, 7500, 8200, 8800, 9100, 10000, 11000],
        'carlos': [6000, 7200, 8000, 8500, 9000, 9500, 9700]
    }

    # Total calories burned per user & Average sleep hours per user
    user_metrics: Dict[str, ValueLike] = {
        'users': ['Alex', 'Bree', 'Carlos'],
        'calories': [3500, 3100, 2900],
        'average_sleep_hours': [7.1, 6.8, 8.0]
    }

    weekly_steps_df = DataFrame(weekly_steps)
    user_metrics_df = DataFrame(user_metrics)

    analyze.inspect_dataframe(weekly_steps_df, verbose=False)
    analyze.inspect_dataframe(user_metrics_df, verbose=False)

    logger.debug("Data setup complete.")

    if can_return:
        return weekly_steps_df, user_metrics_df


if __name__ == '__main__':
    try:
        setup_data(can_return=False)
    except KeyboardInterrupt:
        logger.info('\n\nExiting...')
        sys.exit(0)
