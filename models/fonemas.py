from models.db import db

class Fonema(db.Model):
    __tablename__ = 'fonemas'

    id_fonema = db.Column(db.Integer, primary_key=True)
    fonema = db.Column(db.String(10), nullable=False)
    imagen = db.Column(db.String(255), nullable=False)
    sonido = db.Column(db.String(255), nullable=False)

    def __init__(self, fonema, imagen, sonido):
        self.fonema = fonema
        self.imagen = imagen
        self.sonido = sonido

    def serialize(self):
        return {
            'id_fonema': self.id_fonema,
            'fonema': self.fonema,
            'imagen': self.imagen,
            'sonido': self.sonido,
        }
