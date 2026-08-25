from models.db import db


class Progress(db.Model):
    __tablename__ = "progress"

    id_progress = db.Column(
        db.Integer,
        primary_key=True
    )

    id_user = db.Column(
        db.Integer,
        db.ForeignKey("users.id_user"),
        nullable=False
    )

    id_word = db.Column(
        db.Integer,
        db.ForeignKey("words.id_word"),
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

    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    ronda = db.Column(
        db.Integer,
        nullable=True
    )

    user = db.relationship(
        "User",
        backref="progresos"
    )

    word = db.relationship(
        "Word",
        backref="progresos"
    )

    INTENTOS_MINIMOS = 1
    UMBRAL_DOMINIO = 70

    def __init__(
        self,
        id_user,
        id_word,
        ronda=None
    ):
        self.id_user = id_user
        self.id_word = id_word
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
            self.intentos >= self.INTENTOS_MINIMOS
            and
            self.dominio >= self.UMBRAL_DOMINIO
        )

    def necesita_refuerzo(self):

        if self.intentos == 0:
            return False

        return not self.esta_dominada()

    def es_nueva(self):

        return self.intentos == 0

    def serialize(self):

        return {
            "id_progress": self.id_progress,
            "id_word": self.id_word,
            "aciertos": self.aciertos,
            "intentos": self.intentos,
            "dominio": self.dominio,
            "dominada": self.esta_dominada(),
            "necesita_refuerzo": self.necesita_refuerzo(),
            "nueva": self.es_nueva(),
            "ronda": self.ronda
        }