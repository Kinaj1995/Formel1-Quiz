from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy import Table
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import Column
from flask_login import UserMixin
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Passwort@localhost/F1-Quiz"
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    points = db.Column(db.Integer())
    number_of_question = db.Column(db.Integer())
    false_answers = db.Column(db.Integer())


    def __init__(self, username, password, email, points, noq, fa):
        self.username = username
        self.password = password
        self.email = email
        self.points = points
        self.number_of_question = noq
        self.false_answers = fa

    def __repr__(self):
        return '<id {}>'.format(self.id)
        
    @classmethod
    def find(cls, user_name):
        user = User.query.filter_by(username=user_name).first()

        if not user:
            return null
        
        return user

class Difficulty(db.Model):
    __tablename__ = 'difficulty'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    points = db.Column(db.Integer(), nullable=False)

    def __init__(self, name, points):
        self.name = name
        self.points = points

    def __repr__(self):
        return '<id {}>'.format(self.id)

class answers(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer(), primary_key=True)
    option1 = db.Column(db.String(), nullable=False)
    option2 = db.Column(db.String(), nullable=False)
    option3 = db.Column(db.String(), nullable=False)
    option4 = db.Column(db.String(), nullable=False)
    correct = db.Column(db.Integer(), nullable=False)

    def __init__(self, answers):
        self.answers = answers
        

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Questions(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer(), primary_key=True)
    difficultyid = db.Column(db.Integer(), ForeignKey(Difficulty.id))
    question = db.Column(db.String(), nullable=False)
    picture = db.Column(db.LargeBinary())

    def __init__(self, difficultyid, question, picture):
        self.difficultyid = difficultyid
        self.question = question
        self.picture = picture

    def __repr__(self):
        return '<id {}, question {}, picture {}>'.format(self.id, self.question, self.picture)


question_answer = Table('question_answer', db.Model.metadata,
Column('question_id', Integer, ForeignKey('questions.id')),
Column('answer_id', Integer, ForeignKey('answers.id')))


with app.app_context():
    db.create_all()
