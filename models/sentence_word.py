from models.db import db


class SentenceWord(db.Model):
    __tablename__ = "sentence_words"

    id_sentence_word = db.Column(
        db.Integer,
        primary_key=True
    )

    id_sentence = db.Column(
        db.Integer,
        db.ForeignKey("sentences.id_sentence"),
        nullable=False
    )

    id_word = db.Column(
        db.Integer,
        db.ForeignKey("words.id_word"),
        nullable=False
    )

    orden = db.Column(
        db.Integer,
        nullable=False
    )

    word = db.relationship(
        "Word",
        backref="sentence_words"
    )

    sentence = db.relationship(
        "Sentence",
        back_populates="sentence_words"
    )

    def __init__(
        self,
        id_sentence,
        id_word,
        orden
    ):
        self.id_sentence = id_sentence
        self.id_word = id_word
        self.orden = orden

    def serialize(self):
        return {
            "id_sentence_word": self.id_sentence_word,
            "id_sentence": self.id_sentence,
            "id_word": self.id_word,
            "orden": self.orden
        }