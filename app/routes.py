from app import app

from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/pages/homo')
def homo():
    return render_template("homo.html")