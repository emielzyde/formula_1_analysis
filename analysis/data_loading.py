from functools import lru_cache
from pathlib import Path

import pandas as pd

from .constants import DATA_DIRECTORY

ENCODING = 'latin-1'
DRIVERS_DATA_FILE = 'drivers.csv'
DRIVER_STANDINGS_FILE = 'driver_standings.csv'
RESULTS_DATA_FILE = 'results.csv'
RACES_DATA_FILE = 'races.csv'
QUALIFYING_DATA_FILE = 'qualifying.csv'


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