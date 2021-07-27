
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
from app.common.models import User
from . import bp


@bp.route('/auth/login', methods=('POST',))
def api_login():
    user = User.find(request.json.get('username', ''))
    if not user or not user.active or not user.check_password(request.json.get('password', '')):
        return jsonify(success=False), 401
    login_user(user, remember=request.json.get('remember', False))
    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
    return jsonify({
        'id': current_user.id,
        'username': current_user.name,
        'name': current_user.display_name,
        'email': current_user.email,
        'local': current_user.local,
        'active': current_user.active,
        'roles': [role.name for role in current_user.roles]
    })


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