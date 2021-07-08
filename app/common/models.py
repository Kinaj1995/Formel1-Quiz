from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy import Table
from sqlalchemy.sql.schema import Column

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Passwort@localhost/F1-Quiz"
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    points = db.Column(db.Integer())
    number_of_question = db.Column(db.Integer())
    false_answers = db.Column(db.Integer())


    def __init__(self, username, password, email, points, number_of_questions, false_answers):
        self.username = username
        self.password = password
        self.email = email
        self.points = points
        self.number_of_question = number_of_questions
        self.false_answers = false_answers

    def __repr__(self):
        return '<id {}>'.format(self.id)

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
    answers = db.Column(JSON, nullable=False)

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
        return '<id {}>'.format(self.id)


question_answer = Table('question_answer', db.Model.metadata,
Column('question_id', Integer, ForeignKey('questions.id')),
Column('answer_id', Integer, ForeignKey('answers.id')))


with app.app_context():
    db.create_all()
