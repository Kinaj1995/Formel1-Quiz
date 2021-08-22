from flask.blueprints import Blueprint
from app import app

from flask import render_template
from . import bp

@bp.route('/home')
def index():
    return render_template("home.html")
