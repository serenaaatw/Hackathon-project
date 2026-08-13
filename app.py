from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from models.db import db
from routes.auth_routes import auth_bp
import os

app= Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.register_blueprint(auth_bp)

db.init_app(app)

with app.app_context():
    from models.user import User
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)