

# setup_data.py

"""Setup fitness tracker data for visualization."""

import sys
import logging
from typing import Optional, Tuple

from pandas import DataFrame
from haashi_pkg.utility import Logger
from haashi_pkg.data_engine import DataAnalyzer


def setup_data(
    logger: Optional[Logger] = None,
    can_return: bool = True
) -> Optional[Tuple[DataFrame, DataFrame]]:
    """
    Create sample fitness tracker data for dashboard.

    Returns weekly steps data and user metrics (calories, sleep).
    """
    if logger is None:
        logger = Logger(level=logging.INFO)

    logger.debug("Setting up fitness tracker data...")

    # Initialize analyzer
    analyzer = DataAnalyzer(logger=logger)

    # Days of the week
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    # Weekly steps for each user
    weekly_steps = {
        'days': days,
        'alex': [8500, 9000, 12000, 10000, 9500, 13000, 12500],
        'bree': [7000, 7500, 8200, 8800, 9100, 10000, 11000],
        'carlos': [6000, 7200, 8000, 8500, 9000, 9500, 9700]
    }

    # User metrics: calories and sleep
    user_metrics = {
        'users': ['Alex', 'Bree', 'Carlos'],
        'calories': [3500, 3100, 2900],
        'average_sleep_hours': [7.1, 6.8, 8.0]
    }

    # Create DataFrames
    weekly_steps_df = DataFrame(weekly_steps)
    user_metrics_df = DataFrame(user_metrics)

    logger.debug(f"Created weekly steps data: {len(weekly_steps_df)} days")
    logger.debug(f"Created user metrics: {len(user_metrics_df)} users")

    # Validate data structure
    analyzer.validate_columns_exist(
        weekly_steps_df,
        ['days', 'alex', 'bree', 'carlos']
    )
    analyzer.validate_columns_exist(
        user_metrics_df,
        ['users', 'calories', 'average_sleep_hours']
    )

    logger.info("Data setup completed")
    logger.info(f"  Users: {len(user_metrics_df)}")
    logger.info(
        f"  Total steps tracked: {weekly_steps_df[['alex', 'bree', 'carlos']].sum().sum():,}")

    if can_return:
        return weekly_steps_df, user_metrics_df

    return None


def main() -> None:
    """Run data setup as standalone script."""
    logger = Logger(level=logging.INFO)

    try:
        logger.info("Starting fitness data setup...")
        setup_data(logger=logger, can_return=False)
        logger.info("Setup completed")

    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user")
        sys.exit(0)

    except Exception as e:
        logger.error(exception=e, save_to_json=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
