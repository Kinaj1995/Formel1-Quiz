from flask.blueprints import Blueprint
from app import app

from flask import render_template
from . import bp

@bp.route('/home')
def index():
    return render_template("home.html")

@bp.route('/quiz')
def quiz():
    return render_template("quiz.html")

@bp.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html")