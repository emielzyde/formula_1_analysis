from app.api import app

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

app.run(
    host='0.0.0.0',
    port=5001,
)
