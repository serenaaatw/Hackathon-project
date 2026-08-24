from models.db import db
from models.sentence_word import SentenceWord


class Sentence(db.Model):
    __tablename__ = "sentences"

    id_sentence = db.Column(
        db.Integer,
        primary_key=True
    )

    text = db.Column(
        db.String(255),
        nullable=False
    )

    id_subject = db.Column(
        db.Integer,
        db.ForeignKey("words.id_word"),
        nullable=False
    )

    id_action = db.Column(
        db.Integer,
        db.ForeignKey("words.id_word"),
        nullable=False
    )

    subject = db.relationship(
        "Word",
        foreign_keys=[id_subject]
    )

    action = db.relationship(
        "Word",
        foreign_keys=[id_action]
    )

    sentence_words = db.relationship(
        "SentenceWord",
        back_populates="sentence",
        order_by=SentenceWord.orden,
        cascade="all, delete-orphan"
    )

    def __init__(
        self,
        text,
        id_subject,
        id_action
    ):
        self.text = text
        self.id_subject = id_subject
        self.id_action = id_action

    def serialize(self):
        return {
            "id_sentence": self.id_sentence,
            "text": self.text,
            "id_subject": self.id_subject,
            "id_action": self.id_action,
            "words": [
                sentence_word.word.serialize()
                for sentence_word in self.sentence_words
            ]
        }
