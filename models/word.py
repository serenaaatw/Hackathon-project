from models.db import db


class Word(db.Model):
    __tablename__ = 'words'

    id_word = db.Column(
        db.Integer,
        primary_key=True
    )

    word = db.Column(
        db.String(100),
        nullable=False
    )

    articulo = db.Column(
        db.String(10),
        nullable=True
    )

    image_file = db.Column(
        db.String(255),
        nullable=False
    )

    lsa_video_file = db.Column(
        db.String(255),
        nullable=True
    )

    id_category = db.Column(
        db.Integer,
        db.ForeignKey('categories.id_category'),
        nullable=False
    )

    def __init__(
        self,
        word,
        image_file,
        id_category,
        articulo=None,
        lsa_video_file=None
    ):
        self.word = word
        self.articulo = articulo
        self.image_file = image_file
        self.id_category = id_category
        self.lsa_video_file = lsa_video_file

    def serialize(self):
        categoria_slug = (
            self.category.slug
            if self.category
            else None
        )

        categoria_nombre = (
            self.category.name
            if self.category
            else None
        )

        image_url = None
        lsa_video_url = None

        if categoria_slug and self.image_file:
            image_url = (
                f"/static/img/{categoria_slug}/"
                f"{self.image_file}"
            )

        if categoria_slug and self.lsa_video_file:
            lsa_video_url = (
                f"/static/videos/lsa/{categoria_slug}/"
                f"{self.lsa_video_file}"
            )

        return {
            "id_word": self.id_word,
            "word": self.word,
            "articulo": self.articulo,
            "image_file": self.image_file,
            "lsa_video_file": self.lsa_video_file,
            "image_url": image_url,
            "lsa_video_url": lsa_video_url,
            "id_category": self.id_category,
            "categoria_slug": categoria_slug,
            "categoria_nombre": categoria_nombre
        }
