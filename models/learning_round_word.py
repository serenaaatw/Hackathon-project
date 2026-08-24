from models.db import db


class LearningRoundWord(db.Model):
    __tablename__ = "learning_round_words"

    id_round_word = db.Column(
        db.Integer,
        primary_key=True
    )

    id_round = db.Column(
        db.Integer,
        db.ForeignKey("learning_rounds.id_round"),
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

    ronda = db.relationship(
        "LearningRound",
        back_populates="palabras"
    )

    word = db.relationship(
        "Word",
        backref="rondas_aprendizaje"
    )

    def serialize(self):
        return self.word.serialize()