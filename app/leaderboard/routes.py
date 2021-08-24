from flask.blueprints import Blueprint
from app import app
from app.common.models import User
from sqlalchemy import desc
from flask import render_template
from . import bp

@bp.route('/')
def quiz():
    users = User.query.order_by(desc(User.points)).all()
    return render_template("leaderboard.html", users=users)
