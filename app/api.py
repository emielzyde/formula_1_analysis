import os

import flask
import plotly.offline as pyo
from flask import Markup
from flask_socketio import SocketIO
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

from analysis.preliminary_analysis import construct_driver_standings_data
from simulation.enums import RaceName
from simulation.run import run_simulation
from .forms import ChatBotForm, ModeSelectionForm, SimulationSelectionForm

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
        if form.mode.data == 'Chatbot':
            return flask.redirect('/chatbot')
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


@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    """
    The starting page for the chatbot part of the app
    """
    form = ChatBotForm()
    if form.validate_on_submit():
        if form.api_key and form.query:
            os.environ["OPENAI_API_KEY"] = form.api_key.data
            standings_data = construct_driver_standings_data()
            chatbot_agent = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            agent = create_pandas_dataframe_agent(
                chatbot_agent,
                standings_data,
                verbose=True,
            )
            query_output = agent.run(form.query.data)

            return flask.render_template(
                'chat_bot_home_page.html',
                form=form,
                query_output=f'The answer is: {query_output}'
            )

    return flask.render_template(
        'chat_bot_home_page.html',
        form=form,
    )
