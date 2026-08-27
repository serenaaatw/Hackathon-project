from models.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    username = db.Column(db.String(100), unique=True, nullable=False)
    profile_picture = db.Column(
        db.String(400),
        default='img/user/user.png'
    )
    active = db.Column(db.Boolean, default=True)
    video_visto = db.Column(db.Boolean, default=False, nullable=False)

    rol = db.Column(
        db.String(20),
        nullable=False
    )

    edad = db.Column(
        db.Integer,
        nullable=True
    )

    tutor_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id_user'),
        nullable=True
    )

    children = db.relationship(
        'User',
        backref=db.backref(
            'tutor',
            remote_side=[id_user]
        ),
        lazy='dynamic'
    )

    def __init__(
        self,
        name,
        last_name,
        email,
        password,
        username,
        profile_picture="img/user/user.png",
        rol='child',
        edad=None,
        tutor_id=None
    ):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.username = username
        self.profile_picture = profile_picture
        self.rol = rol
        self.edad = edad
        self.tutor_id = tutor_id

    def get_id(self):
        return str(self.id_user)

    def serialize(self):
        return {
            'id_user': self.id_user,
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email,
            'username': self.username,
            'profile_picture': self.profile_picture,
            'rol': self.rol,
            'edad': self.edad,
            'tutor_id': self.tutor_id
        }

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password,
            password
        )

    def is_child(self):
        return self.rol == 'child'

    def is_tutor(self):
        return self.rol == 'tutor'