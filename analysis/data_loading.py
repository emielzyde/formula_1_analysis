from functools import lru_cache
from pathlib import Path

import pandas as pd

from .constants import DATA_DIRECTORY

ENCODING = 'latin-1'
CIRCUITS_DATA_FILE = 'circuits.csv'
CONSTRUCTORS_DATA_FILE = 'constructors.csv'
CONSTRUCTOR_RESULTS_DATA_FILE = 'constructor_results.csv'
CONSTRUCTOR_STANDINGS_DATA_FILE = 'constructor_standings.csv'
DRIVERS_DATA_FILE = 'drivers.csv'
DRIVER_STANDINGS_FILE = 'driver_standings.csv'
LAP_TIMES_FILE = 'lap_times.csv'
QUALIFYING_DATA_FILE = 'qualifying.csv'
RESULTS_DATA_FILE = 'results.csv'
RACES_DATA_FILE = 'races.csv'
SPRINT_RESULTS_DATA_FILE = 'sprint_results.csv'


@lru_cache(maxsize=1)
def load_drivers_data():
    return pd.read_csv(Path(DATA_DIRECTORY) / DRIVERS_DATA_FILE, encoding=ENCODING)


@lru_cache(maxsize=1)
def load_results_data():
    return pd.read_csv(Path(DATA_DIRECTORY) / RESULTS_DATA_FILE, encoding=ENCODING)


@lru_cache(maxsize=1)
def load_driver_standings_data():
    return pd.read_csv(Path(DATA_DIRECTORY) / DRIVER_STANDINGS_FILE, encoding=ENCODING)


@lru_cache(maxsize=1)
def load_races_data():
    return pd.read_csv(Path(DATA_DIRECTORY) / RACES_DATA_FILE, encoding=ENCODING)


@lru_cache(maxsize=1)
def load_qualifying_data():
    return pd.read_csv(Path(DATA_DIRECTORY) / QUALIFYING_DATA_FILE, encoding=ENCODING)


@lru_cache(maxsize=1)
def load_circuits_data():
    return pd.read_csv(Path(DATA_DIRECTORY) / QUALIFYING_DATA_FILE, encoding=ENCODING)


@lru_cache(maxsize=1)
def load_constructors_data():
    return pd.read_csv(Path(DATA_DIRECTORY) / CONSTRUCTORS_DATA_FILE, encoding=ENCODING)


@lru_cache(maxsize=1)
def load_constructor_results_data():
    return pd.read_csv(
        Path(DATA_DIRECTORY) / CONSTRUCTOR_RESULTS_DATA_FILE,
        encoding=ENCODING,
    )


@lru_cache(maxsize=1)
def load_constructor_standings_data():
    return pd.read_csv(
        Path(DATA_DIRECTORY) / CONSTRUCTOR_STANDINGS_DATA_FILE,
        encoding=ENCODING,
    )


@lru_cache(maxsize=1)
def load_sprint_results_data():
    return pd.read_csv(
        Path(DATA_DIRECTORY) / SPRINT_RESULTS_DATA_FILE,
        encoding=ENCODING,
    )


@lru_cache(maxsize=1)
def load_lap_times():
    return pd.read_csv(Path(DATA_DIRECTORY) / LAP_TIMES_FILE, encoding=ENCODING)
