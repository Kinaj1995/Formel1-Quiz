from flask.blueprints import Blueprint
from app import app

from flask import render_template
from . import bp

@bp.route('/')
def quiz():
    return render_template("leaderboard.html")
