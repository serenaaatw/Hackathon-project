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


    image_file = db.Column(
        db.String(255),
        nullable=True
    )

    lsa_video_file = db.Column(
        db.String(255),
        nullable=True
    )

    sentence_video_file = db.Column(
        db.String(255),
        nullable=True
    )

    audio_file = db.Column(
        db.String(255),
        nullable=True
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
        id_action,
        image_file=None,
        lsa_video_file=None,
        sentence_video_file=None,
        audio_file=None
    ):
        self.text = text
        self.id_subject = id_subject
        self.id_action = id_action
        self.image_file = image_file
        self.lsa_video_file = lsa_video_file
        self.sentence_video_file = sentence_video_file
        self.audio_file = audio_file


    def serialize(self):

        return {
            "id_sentence": self.id_sentence,

            "text": self.text,

            "id_subject": self.id_subject,

            "id_action": self.id_action,

            "image_file": self.image_file,

            "lsa_video_file": self.lsa_video_file,

            "sentence_video_file": self.sentence_video_file,

            "audio_file": self.audio_file,

            "words": [
                sentence_word.word.serialize()
                for sentence_word in self.sentence_words
            ]
        }