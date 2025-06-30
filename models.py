from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Movie(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100))
    release_year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    poster_url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False) # Link Movie to User

