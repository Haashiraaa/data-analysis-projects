
# clean_data.py

import logging
import sys
from haashi_pkg.data_engine import DataLoader, DataAnalyzer
from haashi_pkg.utility import Logger
from pandas import DataFrame, Series
from typing import Iterable, Union

# pyright: basic

logger = Logger(level=logging.INFO)


def get_station_labels(
    df: DataFrame, name_col: str, date_col: str
) -> tuple[str, str, str]:

    # get station name/names
    station_name = df[name_col].unique().tolist()

    station_name = station_name[0] if len(
        station_name) == 1 else ", ".join(station_name)

    # get start and end date
    start_date = df[date_col].min()
    end_date = df[date_col].max()

    start_str = start_date.strftime("%b %Y")
    end_str = end_date.strftime("%b %Y")

    return (station_name, start_str, end_str)


def clean_data(
    filepath: str = "data/4150697.csv",
    logger: Logger = logger,
    can_return: bool = True,
) -> Iterable[Union[DataFrame, str]] | None:

    logger.debug("Loading data from file...")
    weather_data_df = DataLoader(filepath, logger=logger).load_csv_single()

    logger.debug("Cleaning data...")
    analyze = DataAnalyzer(logger=logger)

    # Initial inspection of dataset -> First 5 rows
    analyze.inspect_dataframe(weather_data_df, verbose=False)

    weather_data_df = analyze.normalize_column_names(weather_data_df)

    # Converting Date column
    weather_data_df["date"] = analyze.convert_datetime(
        Series(weather_data_df["date"])
    )

    # Dropping missing rows
    # Initial inspection of missing rows
    num_missing = analyze.count_missing(
        weather_data_df, [col for col in weather_data_df.columns]
    )

    missing_rows = weather_data_df[weather_data_df.isna().any(axis=1)]
    weather_data_df = weather_data_df.drop(missing_rows.index)

    # Final inspection of missing rows
    num_missing = analyze.count_missing(
        weather_data_df, [col for col in weather_data_df.columns]
    )

    weather_data_df = weather_data_df.sort_values("date")

    station_name, start_str, end_str = get_station_labels(
        weather_data_df, "name", "date"
    )

    # Final inspection of dataset
    analyze.inspect_dataframe(weather_data_df, verbose=False)

    if can_return:
        return (  # type: ignore
            weather_data_df[["date", "tmax", "tmin"]],
            station_name,
            start_str,
            end_str
        )


if __name__ == "__main__":
    try:
        clean_data(can_return=False)
    except KeyboardInterrupt:
        logger.info("\nCleaning process interrupted.")
        sys.exit(0)
