

# clean_data.py

"""Clean weather data and extract metadata."""

import sys
import logging
from typing import Optional, Tuple

from pandas import DataFrame, Series
from haashi_pkg.utility import Logger
from haashi_pkg.data_engine import DataLoader, DataAnalyzer


# pyright: basic


def get_station_labels(
    df: DataFrame,
    name_col: str,
    date_col: str
) -> Tuple[str, str, str]:
    """Extract station name and date range labels from weather data."""
    # Get station name(s)
    station_names = df[name_col].unique().tolist()
    station_name = station_names[0] if len(
        station_names) == 1 else ", ".join(station_names)

    # Get date range
    start_date = df[date_col].min()
    end_date = df[date_col].max()

    start_str = start_date.strftime("%b %Y")
    end_str = end_date.strftime("%b %Y")

    return station_name, start_str, end_str


def clean_data(
    filepath: str = "data/4150697.csv",
    logger: Optional[Logger] = None,
    can_return: bool = True,
) -> Optional[Tuple[DataFrame, str, str, str]]:
    """
    Clean weather data and extract metadata.

    Returns temperature data (date, tmax, tmin) and labels
    (station_name, start_date, end_date).
    """
    if logger is None:
        logger = Logger(level=logging.INFO)

    logger.info(f"Loading weather data from {filepath}")

    # Load data
    loader = DataLoader(filepath, logger=logger)
    weather_df = loader.load_csv_single()

    logger.debug(f"Loaded {len(weather_df)} records")
    logger.debug("Starting data cleaning...")

    # Initialize analyzer
    analyzer = DataAnalyzer(logger=logger)

    # Normalize column names
    weather_df = analyzer.normalize_column_names(weather_df)

    # Convert date column
    logger.debug("Converting date column to datetime")
    weather_df["date"] = analyzer.convert_datetime(Series(weather_df["date"]))

    # Check for missing values
    all_columns = list(weather_df.columns)
    missing_counts = analyzer.count_missing(weather_df, all_columns)
    total_missing = sum(missing_counts)

    if total_missing > 0:
        logger.debug(f"Found {total_missing} missing values")

        # Drop rows with any missing values
        missing_rows = weather_df[weather_df.isna().any(axis=1)]
        logger.debug(f"Dropping {len(missing_rows)} rows with missing data")
        weather_df = weather_df.drop(missing_rows.index)

    # Sort by date
    weather_df = weather_df.sort_values("date")

    # Extract metadata
    station_name, start_str, end_str = get_station_labels(
        weather_df, "name", "date"
    )

    logger.info("Data cleaning completed")
    logger.info(f"  Station: {station_name}")
    logger.info(f"  Date range: {start_str} - {end_str}")
    logger.info(f"  Records: {len(weather_df)}")

    if can_return:
        return (  # type: ignore
            weather_df[["date", "tmax", "tmin"]],
            station_name,
            start_str,
            end_str
        )

    return None


def main() -> None:
    """Run data cleaning as standalone script."""
    logger = Logger(level=logging.INFO)

    try:
        logger.info("Starting weather data cleaning...")
        clean_data(logger=logger, can_return=False)
        logger.info("Cleaning completed")

    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user")
        sys.exit(0)

    except Exception as e:
        logger.error(exception=e, save_to_json=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

