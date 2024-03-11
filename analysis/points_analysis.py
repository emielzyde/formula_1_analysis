import pandas as pd

from .data_loading import (
    load_drivers_data,
    load_qualifying_data,
    load_races_data,
    load_results_data,
)

DRIVER_COL = 'driver'
DRIVER_ID_COL = 'driverId'
CODE_COL = 'code'
POSITION_COL = 'position'


def process_data():
    """
    Loads the driver and results data and processed the data by:
    1. Adding the driver names to the results data

    Returns
    -------

    """
    drivers_data = load_drivers_data()
    driver_standings_data = load_results_data()
    races_data = load_races_data()

    drivers_and_standings_data = pd.merge(
        driver_standings_data,
        drivers_data[[DRIVER_ID_COL, 'driverRef', 'forename', 'surname', 'code']],
        left_on=DRIVER_ID_COL,
        right_on=DRIVER_ID_COL,
    )

    data_with_race_dates = pd.merge(
        drivers_and_standings_data,
        races_data[['raceId', 'date']],
        left_on='raceId',
        right_on='raceId',

    )

    return data_with_race_dates.sort_values(by='date')


def analyse_data(data: pd.DataFrame, qualifying_data: pd.DataFrame):
    #average_position_data = data.groupby(CODE_COL)[POSITION_COL].notna().mean()
    a=0


if __name__ == '__main__':
    data = process_data()
    analyse_data(data, load_qualifying_data())