
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
from werkzeug.exceptions import Aborter
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager
from app.common.models import User
from . import bp




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/auth/login', methods=('POST', 'GET'))
def login():
    try:
        username = request.form['user']
        print(request.form)
        pw = request.form['password']
        user = User.find(username)

        if user.password == pw:
            login_user(user)

            return redirect(url_for('home'))
        else:
            return render_template('exception.html')
    except:
        return render_template('exception.html')
    


@bp.route('/auth/logout', methods=('POST',))
@login_required
def api_logout():
    logout_user()
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    resp = jsonify(success=True)
    resp.delete_cookie('product_id')
    return resp

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


@bp.route('/auth/token')
def api_token():
    from flask_wtf.csrf import generate_csrf
    return jsonify(token=generate_csrf())

@bp.route("/auth/find", methods=('GET',))
def auth_api_find():
    query = request.values.get('q')
    if not query:
        return jsonify([])
    ldap_result = User.query_ldap(query)
    results = [{'name': r[0], 'email': r[1], 'first_name': r[2], 'last_name': r[3]} for r in ldap_result]
    return jsonify(results)


@bp.route("/auth/permissions/", methods=('PUT', 'GET'))
def obj_permissions(obj, id):
    object = None
    obj_name = request.values.get('type', '')
    obj_id = request.values.get('id', '')
    try:
        from app.common import models
        obj_class = getattr(models, obj_name)
        if obj_class:
            object = obj_class.query.filter_by(id=int(obj_id)).one()
    except Exception as e:
        current_app.loggger.exception(e)
        return jsonify(success=False)

    if request.method == 'PUT':
        try:
            for item in request.json:
                user = User.query.filter_by(name=item['user']).one()

                ptype = 0
                for m in item['permissions']:
                    ptype |= ObjectPermissionType[m]

                perm = ObjectPermission.query.filter_by(object=object, user=user).one_or_none()
                if not perm:
                    perm = ObjectPermission(user=user, object=object, ptype=ptype)
                perm.ptype = ptype

                if ptype:
                    db.session.add(perm)
                else:
                    db.session.delete(perm)

            db.session.commit()
            success = True
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            success = False

    return "a"

@bp.route("/auth/register", methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        user = User(str(request.form['username']), str(request.form['password']), str(request.form['email']), 0, 0, 0)
        print(user.email)
        
        db.init_app(app)
        db.create_all()

        db.session.add(user)
        db.session.commit()
        return render_template('home.html', error=error)
    else:
        return render_template('home.html', error=error)
