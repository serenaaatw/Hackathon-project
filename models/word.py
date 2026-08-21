from models.db import db

class Word(db.Model):
    __tablename__ = 'words'

    id_word = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)              # "PERRO"
    articulo = db.Column(db.String(10), nullable=True)            # "EL" / "LA" (None para palabras sin artículo, como verbos)
    image_file = db.Column(db.String(255), nullable=False)        # "perro.png"
    lsa_video_file = db.Column(db.String(255), nullable=True)     # null hasta grabar con la intérprete (si se puede jaja)
    id_category = db.Column(db.Integer, db.ForeignKey('categories.id_category'), nullable=False)

    def __init__(self, word, image_file, id_category, articulo=None, lsa_video_file=None):
        self.word = word
        self.articulo = articulo
        self.image_file = image_file
        self.id_category = id_category
        self.lsa_video_file = lsa_video_file

    def serialize(self):
        return {
            'id_word': self.id_word,
            'word': self.word,
            'articulo': self.articulo,
            'image_file': self.image_file,
            'lsa_video_file': self.lsa_video_file,
        }