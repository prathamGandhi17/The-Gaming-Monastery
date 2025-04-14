from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import enum

class Rating(enum.Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

class Genres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True)

class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True) #changed the title to be unique so that no duplicate entries
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    description = db.Column(db.String(100))
    developer = db.Column(db.String(20))
    publisher = db.Column(db.String(20))
    image_url = db.Column(db.String(200))
    release_date = db.Column(db.Date)

class UserGames(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    status = db.Column(db.Enum('To Play', 'Playing', 'Played'))
    start_date = db.Column(db.Date)
    finish_date = db.Column(db.Date)
    rating = db.Column(db.Enum(Rating))
    review = db.Column(db.String(400))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(150))

   