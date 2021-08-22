from flask import Flask
from flask.helpers import url_for
from flask_login import LoginManager
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.secret_key = '1212121212121221'
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Passwort@localhost/F1-Quiz'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

engine = create_engine('postgresql://postgres:Passwort@localhost/F1-Quiz')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

from .api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

from .home import bp as home_bp
app.register_blueprint(home_bp, url_prefix='/')

from .test import bp as test_bp
app.register_blueprint(test_bp, url_prefix='/test')

from .quiz import bp as quiz_bp
app.register_blueprint(quiz_bp, url_prefix='/quiz')

from .leaderboard import bp as leaderboard_bp
app.register_blueprint(leaderboard_bp, url_prefix='/leaderboard') 

@app.route('/')
def index():
    return redirect(url_for('home.index'))
