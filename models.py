from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Users Table
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # Relationship to Stats
    stats = db.relationship('Stat', back_populates='user', cascade='all, delete-orphan')

# Games Table
class Game(db.Model):
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # Added platform directly to Game (PC, Console, Mobile)

    # Relationship to Stats
    stats = db.relationship('Stat', back_populates='game', cascade='all, delete-orphan')

# User Stats Table (core interaction table)
class Stat(db.Model):
    __tablename__ = 'user_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    playtime = db.Column(db.Integer, default=0, nullable=False)
    remarks = db.Column(db.String(255))  # Optional remarks

    # Relationships
    user = db.relationship('User', back_populates='stats')
    game = db.relationship('Game', back_populates='stats')
