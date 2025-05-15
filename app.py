from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from models import db, User
from routes import bp as main_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy
db.init_app(app)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Use 'main.login' matching your blueprint
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprint with no prefix
app.register_blueprint(main_bp, url_prefix='')

if __name__ == '__main__':
    app.run(debug=True)
