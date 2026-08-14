from models.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name= db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    username = db.Column(db.String(100), unique=True, nullable=False)
    profile_picture = db.Column(db.String(255), default='img/user/user.png')
    active = db.Column(db.Boolean, default=True)
    video_visto = db.Column(db.Boolean, default=False, nullable=False)
   
   

    def __init__(self, name, last_name, email, password, username, profile_picture):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.username = username
        self.profile_picture = profile_picture

    def serialize(self):
        return {
            'id_user': self.id_user,
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email,
            'username': self.username,
            'profile_picture': self.profile_picture
        }
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)