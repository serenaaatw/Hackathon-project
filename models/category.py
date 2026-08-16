from models.db import db

class Category(db.Model):
    __tablename__ = 'categories'

    id_category = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)   # "animales" (para la URL)
    name = db.Column(db.String(100), nullable=False)               # "Animales" (para mostrar)

    words = db.relationship('Word', backref='category', lazy=True)

    def __init__(self, slug, name):
        self.slug = slug
        self.name = name

    def serialize(self):
        return {
            'id_category': self.id_category,
            'slug': self.slug,
            'name': self.name,
        }