import pandas as pd
from typing import Optional

import plotly.graph_objects as go

from analysis.data_loading import load_lap_times, load_races_data, load_drivers_data
from .enums import RaceName, PlottingVariable
from constants import DRIVER_ID_STR, RACE_ID_STR


def _calculate_gap_to_first_for_lap(data_for_lap: pd.DataFrame):
    """
    For a given lap, calculates the gap (in seconds) between each driver and the first
    driver in the race

    Parameters
    ----------
    data_for_lap
        The data for the lap

    Returns
    -------

    """
    gaps_to_first = []
    time_of_first_driver = data_for_lap[data_for_lap['position'] == 1]['cumulative_time'].values[0]
    for idx, row in data_for_lap.iterrows():
        if row['position'] == 1:
            gaps_to_first.append(0)
        else:
            diff = (row['cumulative_time'] - time_of_first_driver) / 1000
            gaps_to_first.append(diff)

    return pd.Series(gaps_to_first)


def calculate_gaps_to_first(lap_times_data: pd.DataFrame) -> pd.DataFrame:
    """
    For each lap in the race, calculate the time each driver is behind the first in the
    race

    Parameters
    ----------
    lap_times_data
        A dataframe containing the lap times for each lap and driver for a particular
        race in a given season

    Returns
    -------
    pd.DataFrame
        The lap times data with the gaps to first (in seconds) added
    """
    sorted_data = lap_times_data.sort_values(by=['lap', 'position'], axis=0, ascending=[True, True]).reset_index(drop=True)
    sorted_data['cumulative_time'] = sorted_data.groupby('driver_name')['milliseconds'].cumsum()
    gaps_to_first = sorted_data.groupby('lap').apply(_calculate_gap_to_first_for_lap).reset_index(drop=True)
    gaps_to_first.name = 'gap_to_first'
    merged_data = pd.merge(sorted_data, gaps_to_first, left_index=True, right_index=True)
    return merged_data


def load_reference_lap_times(race: RaceName, season: int) -> pd.DataFrame:
    """
    Load the reference lap times to use for the simulation

    Parameters
    ----------
    race
        The race for which to load the lap times
    season
        The season for which to load the lap times

    Returns
    -------
    pd.DataFrame
        The reference lap times
    """
    lap_times = load_lap_times()
    races_data = load_races_data()
    drivers_data = load_drivers_data()

    lap_times_with_races_data = pd.merge(
        lap_times,
        races_data[[RACE_ID_STR, 'year', 'name', 'date']],
        left_on=RACE_ID_STR,
        right_on=RACE_ID_STR,
    ).rename(columns={'name': 'race_name'})

    merged_data = pd.merge(
        lap_times_with_races_data,
        drivers_data[[DRIVER_ID_STR, 'forename', 'surname']],
        left_on=DRIVER_ID_STR,
        right_on=DRIVER_ID_STR,
    ).drop(DRIVER_ID_STR, axis=1)

    merged_data['driver_name'] = merged_data['forename'] + ' ' + merged_data['surname']
    merged_data = merged_data.drop(['forename', 'surname'], axis=1)

    reference_data = merged_data[merged_data['year'] == season]
    reference_data = reference_data[reference_data['race_name'] == race.value]
    return reference_data


def plot_simulation(
    lap_times_data: pd.DataFrame,
    variable_to_plot: PlottingVariable,
    number_of_drivers: Optional[int] = None,
):
    """
    Plot the results of the simulation. We also add an animation so we can show the
    evolution of the variable_to_plot over time

    Parameters
    ----------
    lap_times_data
        A dataframe containing the lap times for each lap and driver for a particular
        race in a given season
    number_of_drivers
        The numbers of drivers to include in the plot
    variable_to_plot
        The variable to plot
    """
    max_laps = lap_times_data['lap'].max()
    laps = list(range(1, max_laps))
    data_per_driver = []

    if number_of_drivers:
        sorted_data = lap_times_data.sort_values(by=['lap', 'position'], axis=0, ascending=[False, True])
        driver_names = sorted_data['driver_name'][:number_of_drivers].values
    else:
        driver_names = lap_times_data['driver_name'].unique()

    lap_times_data = calculate_gaps_to_first(lap_times_data)
    lap_times_data = lap_times_data[lap_times_data['driver_name'].isin(driver_names)]

    for driver in driver_names:
        data_for_driver = list(lap_times_data[lap_times_data['driver_name'] == driver][variable_to_plot.name].values)
        data_per_driver.append(data_for_driver)

    data = pd.DataFrame(
        list(zip(laps, *data_per_driver)),
        columns=['date', *driver_names]
    )

    data = data.set_index('date')
    max_value = lap_times_data[variable_to_plot.name].to_numpy().max()
    min_value = lap_times_data[variable_to_plot.name].to_numpy().min()
    data = data.reset_index()

    # Base plot
    fig = go.Figure(
        layout=go.Layout(
            updatemenus=[dict(type="buttons", direction="right", x=0.9, y=1.16), ],
            xaxis=dict(
                range=[1, max_laps],
                autorange=False, tickwidth=2,
                title_text="Time"),
            yaxis=dict(
                range=[min_value, max_value],
                autorange=False,
                title_text=variable_to_plot.value),
            title=variable_to_plot.value,
        )
    )

    for driver in data.columns[1:]:
        fig.add_trace(
            go.Scatter(
                x=data['date'],
                y=data.loc[:, driver],
                name=driver,
                visible=True,
            )
        )

    # Animation
    fig.update(frames=[
        go.Frame(
            data=[
                go.Scatter(x=data['date'][:k].values, y =data.loc[:, driver][:k].values)
                for driver in data.columns[1:]
            ]
        )
        for k in range(0, len(data))])

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        label="Play",
                        method="animate",
                        args=[None, {"frame": {"duration": 300}}]),
                ])
            )
        ]
    )

    fig.show()


def run_simulation(race: RaceName, reference_season: int):
    """
    Runs a simulation of a Formula 1 race

    Parameters
    ----------
    race
        The race to simulate
    reference_season
        The season to use as a reference for lap times, etc...
    """

    reference_lap_times = load_reference_lap_times(race=race, season=reference_season)
    calculate_gaps_to_first(lap_times_data=reference_lap_times)
    plot_simulation(reference_lap_times, number_of_drivers=5, variable_to_plot=PlottingVariable.gap_to_first)
