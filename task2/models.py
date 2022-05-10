from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime
import json

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """ User model """

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    hashed_pswd = db.Column(db.String(), nullable=False)
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'username' : self.username,
       }

class Question(db.Model):
    """ Question model """
    __tablename__ = "question"

    question = db.Column(db.String(), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id'             : self.id,
           'question'       : self.question,
           'user'           : [i.serialize for i in User.query.filter_by(id=self.user_id).all()], 
       }


class Answer(db.Model):
    __tablename__ = "answer"

    answer = db.Column(db.String(), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question = db.relationship(Question)
    user = db.relationship(User)


    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id'             : self.id,
           'answer'         : self.answer,
           'question'       : [i.serialize for i in Question.query.filter_by(id=self.question_id).all()],
          
       }

