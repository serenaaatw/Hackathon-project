from flask import Flask
from config.config import DATABASE_CONNECTION_URI, DATABASE_ENGINE_OPTIONS
from dotenv import load_dotenv

from models.db import db
from flask_login import LoginManager

from routes.auth_routes import auth_bp
from routes.informative_routes import informative_bp
from routes.learning_routes import learning_bp
from routes.game_routes import game_bp
from routes.menuPrincipal_routes import menu_principal
from routes.progress_routes import progress_routes
from routes.profile_routes import profile
from routes.contact_routes import contact_bp
from routes.sentence_routes import sentence_bp
from routes.inicio_routes import inicio_bp
from routes.vision_routes import vision_bp

import os
from routes.help_routes import help_bp

import os

load_dotenv()

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_routes.login_route"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.secret_key = os.getenv("SECRET_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = DATABASE_ENGINE_OPTIONS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(auth_bp)
app.register_blueprint(informative_bp)
app.register_blueprint(learning_bp)
app.register_blueprint(game_bp)
app.register_blueprint(menu_principal)
app.register_blueprint(progress_routes)
app.register_blueprint(profile)
app.register_blueprint(contact_bp)
app.register_blueprint(sentence_bp)
app.register_blueprint(inicio_bp)
app.register_blueprint(vision_bp)

app.register_blueprint(help_bp)

db.init_app(app)

with app.app_context():

    from models.user import User
    from models.category import Category
    from models.word import Word
    from models.progress import Progress

    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)