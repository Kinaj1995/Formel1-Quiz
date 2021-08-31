from flask.blueprints import Blueprint
from sqlalchemy.sql.functions import current_user
from app import app
from app.common.models import User
from sqlalchemy import desc
from flask import render_template
from flask_login import current_user
from . import bp

@bp.route('/')
def leaderboard():
    if current_user.is_authenticated:
        users = User.query.order_by(desc(User.points)).limit(10).all()
        return render_template('leaderboard.html', users=users)
    else:
        return render_template('exception.html')
