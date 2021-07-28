import re
from sqlalchemy.orm import session
from app.common.models import User
from flask.blueprints import Blueprint
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from app import app
from sqlalchemy.orm import sessionmaker

from app import db

from flask import render_template
from . import bp

@bp.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('test.html', error=error)

@bp.route('/regiter/', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        user = User(request.form['username'], request.form['password'], request.form['email'], 0,0,0)
        print(user.email)
        db.session.add(user)
        db.session.commit()
        return render_template('test_reg.html', error=error)
    else:
        return render_template('test_reg.html', error=error)
    return render_template('test_reg.html', error=error)
