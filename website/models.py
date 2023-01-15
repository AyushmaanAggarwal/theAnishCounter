from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(150))
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    counterName = db.Column(db.String(150))
    description = db.Column(db.String(1000))
    counts = db.Column(db.Integer)

movies_likes = db.Table('movie_likes',
                        db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movieName = db.Column(db.String(150))
    releaseYear = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    runtime = db.Column(db.String(150))
    likes = db.Column(db.Integer)
    likedUsers = db.relationship('User', secondary=movies_likes, backref='movies')

class Lateness(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    lateTotal = db.Column(db.Integer)
    arrived = db.Column(db.Boolean)
    lastTime = db.Column(db.DateTime)
