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