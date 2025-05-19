from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Games Table
class Game(db.Model):
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    platform = db.Column(db.String(50), nullable=False)

    stats = db.relationship('Stat', back_populates='game', cascade='all, delete-orphan')

# User Stats Table
class Stat(db.Model):
    __tablename__ = 'user_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    playtime = db.Column(db.Integer, default=0, nullable=False)
    remarks = db.Column(db.String(255))

    user = db.relationship('User', back_populates='stats')
    game = db.relationship('Game', back_populates='stats')

# Only ONE User class definition here:
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    Age = db.Column(db.Integer)
    Quote = db.Column(db.Text)
    profile_picture = db.Column(db.String(300), default='default.png')

    stats = db.relationship('Stat', back_populates='user', cascade='all, delete-orphan')
