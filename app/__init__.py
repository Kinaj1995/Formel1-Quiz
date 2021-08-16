from flask import Flask
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
db = SQLAlchemy()

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

@app.route('/')
def index():
    return redirect(url_for('home.index'))
