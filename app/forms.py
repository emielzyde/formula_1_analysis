from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

from simulation.enums import RaceName


class ModeSelectionForm(FlaskForm):
    modes = ['Simulation', 'Historical Analysis']
    mode_choices = [tuple([mode, mode]) for mode in modes]
    mode = SelectField('Mode', choices=modes)
    submit = SubmitField('Submit selection!')


class SimulationSelectionForm(FlaskForm):
    races = [race.value for race in RaceName]
    race_choices = [tuple([race, race]) for race in races]
    race = SelectField('Race', choices=race_choices)

    years = list(range(1994, 2023))
    year_choices = [tuple([year, year]) for year in years]
    year = SelectField('Year', choices=year_choices)

    submit = SubmitField('Submit selection!')
