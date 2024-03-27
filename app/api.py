import flask
from flask_socketio import SocketIO

from .forms import ModeSelectionForm

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
    return flask.render_template('simulation_home_page.html')
