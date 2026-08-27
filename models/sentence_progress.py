from models.db import db


class SentenceProgress(db.Model):
    __tablename__ = "sentence_progress"

    id_sentence_progress = db.Column(
        db.Integer,
        primary_key=True
    )

    id_user = db.Column(
        db.Integer,
        db.ForeignKey("users.id_user"),
        nullable=False
    )

    id_sentence = db.Column(
        db.Integer,
        db.ForeignKey("sentences.id_sentence"),
        nullable=False
    )

    aciertos = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    intentos = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    dominio = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    ronda = db.Column(
        db.Integer,
        nullable=True
    )

    user = db.relationship(
        "User",
        backref="progresos_oraciones"
    )

    sentence = db.relationship(
        "Sentence",
        backref="progresos"
    )

    UMBRAL_DOMINIO = 70

    def __init__(
        self,
        id_user,
        id_sentence,
        ronda=None
    ):
        self.id_user = id_user
        self.id_sentence = id_sentence
        self.aciertos = 0
        self.intentos = 0
        self.dominio = 0
        self.ronda = ronda

    def registrar_intento(self, correcto):
        self.intentos += 1

        if correcto:
            self.aciertos += 1

        self.dominio = round(
            (self.aciertos / self.intentos) * 100
        )

    def reiniciar(self):
        self.aciertos = 0
        self.intentos = 0
        self.dominio = 0

    def esta_dominada(self):
        return (
            self.intentos > 0
            and self.dominio >= self.UMBRAL_DOMINIO
        )

    def necesita_refuerzo(self):
        return (
            self.intentos > 0
            and not self.esta_dominada()
        )

    def es_nueva(self):
        return self.intentos == 0

    def serialize(self):
        return {
            "id_sentence_progress":
                self.id_sentence_progress,
            "id_sentence":
                self.id_sentence,
            "aciertos":
                self.aciertos,
            "intentos":
                self.intentos,
            "dominio":
                self.dominio,
            "dominada":
                self.esta_dominada(),
            "necesita_refuerzo":
                self.necesita_refuerzo(),
            "nueva":
                self.es_nueva(),
            "ronda":
                self.ronda
        }