from flask import Flask
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
from .api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

from .home import bp as home_bp
app.register_blueprint(home_bp, url_prefix='/')

from .test import bp as test_bp
app.register_blueprint(test_bp, url_prefix='/test')

@app.route('/')
def index():
    return redirect(url_for('home.index'))
