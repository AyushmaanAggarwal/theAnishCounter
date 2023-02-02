from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(150))
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    emailauth = db.Column(db.String()) # Used to verify email address using autogenerated number
    emailauthexp = db.Column(db.Integer()) # Used for checking expiration date for email verification
    emailauthattempts = db.Column(db.Integer())
    resetpassword = db.Column(db.String()) # Used to reset password using autogenerated number
    resetpasswordexp = db.Column(db.Integer()) # Used for checking expiration date for password reset
    password = db.Column(db.String(150))
    testlevel = db.Column(db.String(10))
    createdBooks = db.relationship('Book')

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
    title = db.Column(db.String(150))
    imdb_id = db.Column(db.String(150))
    year = db.Column(db.Integer)
    rating = db.Column(db.String(150))
    plot = db.Column(db.String(1000))
    runtime = db.Column(db.String(150))
    posterUrl = db.Column(db.String(1000))
    likes = db.Column(db.Integer)
    likedUsers = db.relationship('User', secondary=movies_likes, backref='movies')
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Lateness(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    lateTotal = db.Column(db.Integer)
    lastArrived = db.Column(db.DateTime)
    lastTime = db.Column(db.DateTime)


book_likes = db.Table('book_likes',
                        db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookTitle = db.Column(db.String(150))
    author = db.Column(db.String(150))
    publishYear = db.Column(db.Integer)
    isbn = db.Column(db.Integer)
    cover_id = db.Column(db.Integer)
    olid = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    likedUsers = db.relationship('User', secondary=book_likes, backref='books')
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
