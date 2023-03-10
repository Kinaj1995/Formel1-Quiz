from flask.blueprints import Blueprint
from app import db

from flask import render_template
from . import bp

from flask import request, jsonify, current_app as app


from flask import redirect, render_template, request,  url_for, jsonify
from flask_login import current_user

from app.common.models import Difficulty, User, Questions, answers
from  sqlalchemy.sql.expression import func


@bp.route('/')
def quiz():
    return render_template("quiz.html")

@bp.route('/question/<diff_id>')
def quiz_api_question(diff_id):
    if current_user.is_authenticated:
        Questions.query.get(1)
        question = Questions.query.filter(Questions.difficultyid == diff_id).order_by(func.random()).first()
        anwser = answers.query.filter(answers.id == question.id).first()
        import base64
        img_bi = question.picture
        encoded_img = base64.b64encode(img_bi)
        a = encoded_img.decode()

        return render_template("inner_quiz.html",question=question, anwser=anwser, correct=anwser.correct, picture=a, diff=diff_id)  
    else:
        return render_template('exception.html')

@bp.route('/question/next/', methods=('GET', 'POST'))
def quiz_next():
    if current_user.is_authenticated:
        res = request.json

        user = User.query.filter(User.id == current_user.id).first()
        user.number_of_question += 1
        if res["Correct"]:
            diff_id = res['Diff_id']
            print("b")
            diff = Difficulty.query.filter(Difficulty.id == diff_id).first()
            user.points += diff.points
            db.session.commit()   
        else: 
            diff_id = res['Diff_id']
            print("a")
            user.false_answers += 1
            db.session.commit()
        
        return redirect(url_for('quiz.quiz_api_question', diff_id=diff_id))
    else:
        return render_template('exception.html')
