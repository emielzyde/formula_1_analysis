from typing import NoReturn

import pandas as pd
import plotly.graph_objs as go

from .data_loading import (
    load_constructors_data,
    load_constructor_standings_data,
    load_drivers_data,
    load_driver_standings_data,
    load_races_data,
    load_results_data,
    load_sprint_results_data,
)
from .enums import StandingsDataType
from constants import DRIVER_ID_STR, RACE_ID_STR

EMPTY_SYMBOL = '\\N'
EMPTY_SYMBOL_THRESHOLD = 0.05
CONSTRUCTOR_ID_STR = 'constructorId'


def drop_empty_columns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Drops empty columns. Some of the datasets have columns where all or most of the
    values are \\N. These should be dropped if we have more than a given threshold of
    these values

    Parameters
    ----------
    data
        The dataframe from which empty columns should be dropped

    Returns
    -------
    pd.DataFrame
        The data with the empty columns dropped
    """
    return (
        data
        .replace(EMPTY_SYMBOL, pd.NA)
        .dropna(axis=1, thresh=int(EMPTY_SYMBOL_THRESHOLD*data.shape[0]))
    )


def _merge_races_constructors_and_standings_data(
    standings_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Merges the standings, races and constructors data

    Parameters
    ----------
    standings_data
        The standings data. This could be, for example, driver standings or constructor
        standings

    Returns
    -------
    pd.DataFrame
        The merged data
    """
    standings_data = drop_empty_columns(standings_data)

    constructors_data = load_constructors_data()
    races_data = drop_empty_columns(load_races_data())

    if CONSTRUCTOR_ID_STR in standings_data.columns:
        standings_data = pd.merge(
            standings_data,
            constructors_data[[CONSTRUCTOR_ID_STR, 'name']],
            left_on=CONSTRUCTOR_ID_STR,
            right_on=CONSTRUCTOR_ID_STR,
        ).drop(CONSTRUCTOR_ID_STR, axis=1).rename(columns={'name': 'constructor_name'})

    return pd.merge(
        standings_data,
        races_data[[RACE_ID_STR, 'year', 'name', 'date']],
        left_on=RACE_ID_STR,
        right_on=RACE_ID_STR,
    ).rename(columns={'name': 'race_name'})


def construct_constructor_standings_data() -> pd.DataFrame:
    """
    Constructs the constructor standings data. First merges the standings data with the
    races data and the constructors data so that the dataset has all the information.

    In the process of doing this, some spot checks on the quality of the data were done,
    and it was determined that the data is accurate

    Returns
    -------
    pd.DataFrame
        The constructor standings data
    """
    standings_data = load_constructor_standings_data()
    merged_data = _merge_races_constructors_and_standings_data(
        standings_data=standings_data,
    )
    return merged_data


def construct_driver_standings_data() -> pd.DataFrame:
    """
    Constructs the driver standings data. First merges the standings data with the races
    data, the drivers data and the constructors data so that the dataset has all the
    information.

    In the process of doing this, some spot checks on the quality of the data were done,
    and it was determined that the data is accurate.

    Returns
    -------
    pd.DataFrame
        The driver standings data
    """
    standings_data = load_driver_standings_data()
    standings_data = drop_empty_columns(standings_data)
    drivers_data = drop_empty_columns(load_drivers_data())

    merged_data = _merge_races_constructors_and_standings_data(
        standings_data=standings_data,
    )
    merged_data = pd.merge(
        merged_data,
        drivers_data[[DRIVER_ID_STR, 'forename', 'surname']],
        left_on=DRIVER_ID_STR,
        right_on=DRIVER_ID_STR,
    ).drop(DRIVER_ID_STR, axis=1)

    merged_data['driver_name'] = merged_data['forename'] + ' ' + merged_data['surname']
    merged_data = merged_data.drop(['forename', 'surname'], axis=1)
    merged_data['date'] = pd.to_datetime(merged_data['date'])
    merged_data = merged_data.sort_values(by='date', ascending=False)
    return merged_data


def plot_standings_data_over_time(
    standings_data: pd.DataFrame,
    year: int,
    standings_data_type: StandingsDataType,
) -> NoReturn:
    """
    Plots standings data (e.g. constructor standings, driver standings) over the course
    of any given season

    Parameters
    ----------
    standings_data
        The standings data that should be plotted over a given season
    year
        The season for which to plot the data
    standings_data_type
        The type of standings data that should be plotted
    """
    standings_data['date'] = pd.to_datetime(standings_data['date'])
    standings_data = standings_data.sort_values(by='date')
    standings_for_year_data = standings_data[standings_data['year'] == year]

    fig = go.Figure()
    for name in standings_for_year_data[standings_data_type.value].unique():
        data = standings_for_year_data[
            standings_for_year_data[standings_data_type.value] == name
        ]
        fig.add_traces(
            go.Scatter(
                x=data['date'],
                y=data['points'],
                mode='lines',
                name=name
            ),
        )
    fig.show()


def calculate_race_at_which_season_is_decided(
    standings_data: pd.DataFrame,
    year: int,
) -> str:
    """
    Calculates the earliest race at which a season is decided. A season is decided if
    nobody can overtake the leader in the standings, even on the assumption that the
    leader scores 0 points going forward and the closest challenger scores all available
    points

    Note, as of a few seasons ago, we need to take account of the points available in
    the sprint races. We also need to account for the fastest lap points, which were
    (re-)introduced in 2019.

    Parameters
    ----------
    standings_data
        The standings data. This can be the driver standings or the constructor
        standings
    year
        The year for which we find the earliest date at which it was decided

    Returns
    -------
    str
        The race at which the season was decided
    """
    race_name = ''
    sprint_results_data = drop_empty_columns(load_sprint_results_data())
    results_data = drop_empty_columns(load_results_data())
    races_data = drop_empty_columns(load_races_data())

    sprints_and_races_data = pd.merge(
        sprint_results_data,
        races_data[[RACE_ID_STR, 'year', 'name', 'date']],
        left_on=RACE_ID_STR,
        right_on=RACE_ID_STR,
    ).rename(columns={'name': 'race_name'})

    results_and_races_data = pd.merge(
        results_data,
        races_data[[RACE_ID_STR, 'year', 'name', 'date']],
        left_on=RACE_ID_STR,
        right_on=RACE_ID_STR,
    ).rename(columns={'name': 'race_name'})

    standings_data_for_year = standings_data[standings_data['year'] == year]
    sprints_data_for_year = sprints_and_races_data[
        sprints_and_races_data['year'] == year
    ]
    results_data_for_year = results_and_races_data[
        results_and_races_data['year'] == year
    ]

    max_points_per_sprint = (
        sprints_data_for_year
        .groupby('raceId')['points']
        .max()
        .reset_index()
        .rename(columns={'points': 'sprint_points'})
    )
    max_points_per_race = (
        results_data_for_year
        .groupby('raceId')['points']
        .max()
        .reset_index()
        .rename(columns={'points': 'race_points'})
    )

    # Account for the sprint points for each race
    if year >= 2019:
        sorted_max_points_per_race = sorted(
            max_points_per_race['race_points'].unique())[::-1]
        second_highest_points = sorted_max_points_per_race[1]
        if sorted_max_points_per_race[0] == sorted_max_points_per_race[1] + 1:
            max_points_per_race['race_points'] = (
                max_points_per_race['race_points']
                .apply(lambda x: x + 1 if x == second_highest_points else x)
            )

    unique_races_in_year = sorted(standings_data_for_year['raceId'].unique())
    for race in unique_races_in_year:
        standings_data_after_race = standings_data_for_year[
            standings_data_for_year['raceId'] == race
        ]
        max_sprint_points_after_race =max_points_per_sprint[max_points_per_sprint['raceId'] > race]['sprint_points'].sum()
        max_points_after_race = max_points_per_race[max_points_per_race['raceId'] > race]['race_points'].sum()
        max_total_points_after_race = (
            max_sprint_points_after_race + max_points_after_race
        )

        highest_standings_after_race = standings_data_after_race['points'].max()
        second_highest_standings_after_race = (
            standings_data_after_race['points']
            .sort_values(ascending=False)
            .iloc[1]
        )

        is_season_decided = (
            highest_standings_after_race
            > second_highest_standings_after_race + max_total_points_after_race
        )
        if is_season_decided:
            race_name = races_data[races_data['raceId'] == race]['name']
            print(
                f'The world championship in {year} was decided at the '
                f'{race_name.iloc[0]}'
            )
            break

    return race_name
