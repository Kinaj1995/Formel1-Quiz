from flask import request, jsonify, current_app as app
import enum
import os
import sys
import secrets
from datetime import datetime, timedelta
from functools import wraps
from urllib.parse import urlparse, urljoin

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, current_app, \
    jsonify, make_response
from flask_login import (AnonymousUserMixin, LoginManager, UserMixin,
                         current_user, login_required, login_user, logout_user)
from flask_principal import (AnonymousIdentity, Identity, Permission,
                             Principal, RoleNeed, UserNeed, identity_changed,
                             identity_loaded)
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy import Integer, String, UnicodeText, DateTime, Boolean, Unicode
from sqlalchemy import Table, Column, UniqueConstraint, or_
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy_utils import generic_relationship
from werkzeug.exceptions import Aborter
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.common.models import User, Questions, answers
from . import bp
from  sqlalchemy.sql.expression import func

@bp.route('/quiz/question/<diff_id>', methods=('GET',))
def quiz_api_question(diff_id):
    Questions.query.get(1)
    a = Questions.query.filter(Questions.difficultyid == diff_id).order_by(func.random()).first()
    anwser = answers.query.filter(answers.id == a.id).first()
    return render_template('test_reg.html', error=str(anwser.answers))
