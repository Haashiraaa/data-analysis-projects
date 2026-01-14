

# setup_data.py

import pandas as pd
from typing import List, Dict, Union
from haashi_pkg.data_engine.dataengine import DataEngine


de = DataEngine()
ValueLike = Union[List[str], List[int], List[float]]


# ------------------------------------
# Data Setup
# ------------------------------------

def setup_data() -> tuple[pd.DataFrame, pd.DataFrame]:

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

    weekly_steps_df = pd.DataFrame(weekly_steps)
    user_metrics_df = pd.DataFrame(user_metrics)

    de.inspect_dataframe(weekly_steps_df, verbose=False)
    de.inspect_dataframe(user_metrics_df, verbose=False)

    return weekly_steps_df, user_metrics_df
