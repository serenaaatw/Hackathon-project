from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from models.db import db
from routes.auth_routes import auth_bp
from routes.informative_routes import informative_bp
from routes.learning_routes import learning_bp
from routes.game_routes import game_bp
from routes.menuPrincipal_routes import menu_principal
from routes.progress_routes import progress
from routes.profile_routes import profile
from routes.contact_routes import contact
import os

app= Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.register_blueprint(auth_bp)
app.register_blueprint(informative_bp)
app.register_blueprint(learning_bp)
app.register_blueprint(game_bp)
app.register_blueprint(menu_principal)
app.register_blueprint(progress)
app.register_blueprint(profile)
app.register_blueprint(contact)

db.init_app(app)

with app.app_context():
    from models.user import User
    from models.category import Category
    from models.word import Word
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
