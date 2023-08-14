from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Pass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String)


# api google books
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check = db.Column(db.String, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    search = db.Column(db.String, unique=True, nullable=False)
    img = db.Column(db.String, unique=True, nullable=False)
    descr = db.Column(db.String, nullable=True)


# api imdb movies
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seen = db.Column(db.String, nullable=False)
    orig_title = name = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    search = db.Column(db.String, nullable=False)
    img = db.Column(db.String, nullable=True)
    appear_type = db.Column(db.String, nullable=False)
    job = db.Column(db.String, nullable=False)
    descr = db.Column(db.String, nullable=True)
    year = db.Column(db.Integer, nullable=True)
    runtime = db.Column(db.String, nullable=True)
