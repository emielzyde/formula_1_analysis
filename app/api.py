import flask
from flask_socketio import SocketIO
from flask import Markup
from simulation.run import run_simulation
from .forms import ModeSelectionForm, SimulationSelectionForm
from simulation.enums import RaceName
import plotly.offline as pyo
app = flask.Flask(__name__)
socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    The starting page for the app. This redirects to several other pages, depending
    on the selections made by the user.
    """
    form = ModeSelectionForm()
    if form.validate_on_submit():
        if form.mode.data == 'Simulation':
            return flask.redirect('/simulation')
    return flask.render_template('home_page.html', form=form)


@app.route('/simulation', methods=['GET', 'POST'])
def simulation():
    """
    The starting page for the simulation part of the app
    """
    form = SimulationSelectionForm()
    if form.validate_on_submit():
        if form.race.data and form.year.data:
            figure = run_simulation(
                race=RaceName(form.race.data),
                reference_season=int(form.year.data),
            )
            output = pyo.offline.plot(
                figure,
                include_plotlyjs=False,
                output_type='div',
                auto_play=False,
            )
            return flask.render_template(
                'simulation_home_page.html',
                form=form,
                fig=Markup(output),
            )

    return flask.render_template(
        'simulation_home_page.html',
        form=form,
        fig="",
    )
