from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Game(db.Model):
    __tablename__ = 'Game'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True, nullable=False)
    cost = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.Text(), unique=True, nullable=False)
    size = db.Column(db.Integer, default=datetime.utcnow)
    age_limited = db.Column(db.Integer, unique=True, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)


class Buyer(db.Model):
    __tablename__ = "Buyer"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    age = db.Column(db.Integer, default=True, nullable=False)