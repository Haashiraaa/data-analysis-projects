
# clean_data.py

import logging
import sys
from haashi_pkg.data_engine.dataloader import DataLoader
from haashi_pkg.data_engine.dataengine import DataEngine
from haashi_pkg.utility.utils import Utility
from pandas import DataFrame
from typing import Optional

FILEPATH = "4150697.csv"
DEBUG = False

dl = DataLoader(FILEPATH)
de = DataEngine()
ut = Utility(level=logging.INFO)


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


def clean_data() -> Optional[tuple[DataFrame, str, str, str]]:

    weather_data_df = dl.load_csv_single()

    # Initial inspection of dataset -> First 5 rows
    de.inspect_dataframe(weather_data_df, verbose=False)

    weather_data_df = de.normalize_column_names(weather_data_df)

    # Converting Date column
    weather_data_df["date"] = de.convert_datetime(weather_data_df["date"])

    # Dropping missing rows
    # Initial inspection of missing rows
    num_missing = de.count_missing(
        weather_data_df, [col for col in weather_data_df.columns]
    )

    missing_rows = weather_data_df[weather_data_df.isna().any(axis=1)]
    weather_data_df = weather_data_df.drop(missing_rows.index)

    # Final inspection of missing rows
    num_missing = de.count_missing(
        weather_data_df, [col for col in weather_data_df.columns]
    )

    weather_data_df = weather_data_df.sort_values("date")

    station_name, start_str, end_str = get_station_labels(
        weather_data_df, "name", "date"
    )

    # Final inspection of dataset
    de.inspect_dataframe(weather_data_df, verbose=False)

    ut.debug(num_missing)
    ut.debug(missing_rows)
    ut.debug(station_name)
    ut.debug(start_str)
    ut.debug(end_str)

    if not DEBUG:
        return (
            weather_data_df[["date", "tmax", "tmin"]],
            station_name,
            start_str,
            end_str
        )


if __name__ == "__main__":
    try:
        clean_data()
    except KeyboardInterrupt:
        print("\nCleaning process interrupted.")
        sys.exit(0)
