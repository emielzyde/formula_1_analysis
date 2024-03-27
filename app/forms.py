from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class ModeSelectionForm(FlaskForm):
    modes = ['Simulation', 'Historical Analysis']
    mode_choices = [tuple([mode, mode]) for mode in modes]
    mode = SelectField('Mode', choices=modes)
    submit = SubmitField('Submit selection!')
