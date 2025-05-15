import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '3871f0040c04d41f5f93a542ac63a1cc'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
