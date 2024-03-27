from enum import Enum


class RaceName(Enum):
    """
    The possible races
    """
    australia = 'Australian Grand Prix'
    turkey = 'Turkish Grand Prix'


class PlottingVariable(Enum):
    """
    The possible variables to plot
    """
    position = 'Position'
    gap_to_first = 'Gap to First'
