
from re import L
import re
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
from sqlalchemy.sql.functions import user
from sqlalchemy_utils import generic_relationship
from werkzeug.exceptions import Aborter, PreconditionRequired
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager
from app.common.models import User
from . import bp
import re



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/auth/login', methods=('POST', 'GET'))
def login():
    try:
        username = request.form['user']
        pw = request.form['password']
        user = User.find(username)

        if user.password == pw:
            login_user(user)

            return redirect(url_for('home.index'))
        else:
            return render_template('exception.html')
    except:
        return render_template('exception.html')
    


@bp.route('/auth/logout', methods=('POST',))
@login_required
def api_logout():
    logout_user()
   
    return redirect(url_for('home.index'))

@bp.route('/auth/whoami')
def api_whoami():
    if not current_user.is_anonymous:
        return jsonify({
            'id': current_user.id,
            'username': current_user.name,
            'name': current_user.display_name,
            'email': current_user.email,
            'local': current_user.local,
            'active': current_user.active,
            'roles': [role.name for role in current_user.roles]
        })
    return jsonify({}), 401


@bp.route("/auth/register", methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        uname = str(request.form['username'])
        regex_spec = re.compile('[@_!#$%^&*()<>?\|}{~:.,]')
        regex_let = re.compile('[a-zA-Z]')
        regex_num = re.compile('[0-9]')


        if User.query.filter_by(username=uname).first() is not None:
            return render_template("home.html", error="Username already taken")

        if len(str(request.form['password'])) < 8 or regex_spec.search(str(request.form['password'])) == None or regex_let.search(str(request.form['password'])) == None or regex_num.search(str(request.form['password'])) == None:
            return render_template("home.html", error="Password invalid")
        
        
        if str(request.form['password']) != str(request.form['password1']):
            return render_template("home.html", error="Password invalid")
        
        user = User(str(request.form['username']), str(request.form['password']), str(request.form['email']), 0, 0, 0)

        
        db.init_app(app)
        db.create_all()

        db.session.add(user)
        db.session.commit()
        return render_template('home.html', error="")
    else:
        return render_template('home.html', error="")
