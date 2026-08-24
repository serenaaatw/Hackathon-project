from models.db import db


class LearningRound(db.Model):
    __tablename__ = "learning_rounds"

    id_round = db.Column(
        db.Integer,
        primary_key=True
    )

    id_user = db.Column(
        db.Integer,
        db.ForeignKey("users.id_user"),
        nullable=False
    )

    id_category = db.Column(
        db.Integer,
        db.ForeignKey("categories.id_category"),
        nullable=False
    )

    fase = db.Column(
        db.String(30),
        nullable=False,
        default="aprendizaje"
    )

    juego_actual = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    completada = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )

    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    user = db.relationship(
        "User",
        backref="rondas_aprendizaje"
    )

    category = db.relationship(
        "Category",
        backref="rondas_aprendizaje"
    )

    palabras = db.relationship(
        "LearningRoundWord",
        back_populates="ronda",
        cascade="all, delete-orphan",
        order_by="LearningRoundWord.orden"
    )

    def avanzar_juego(self):

        if self.juego_actual < 5:
            self.juego_actual += 1

        self.fase = "ejercicios"

    def reiniciar_juegos(self):

        self.juego_actual = 1
        self.fase = "ejercicios"
        self.completada = False

    def completar(self):

        self.juego_actual = 5
        self.fase = "completada"
        self.completada = True

    def serialize(self):

        return {
            "id_round": self.id_round,
            "id_user": self.id_user,
            "id_category": self.id_category,
            "fase": self.fase,
            "juego_actual": self.juego_actual,
            "completada": self.completada,
            "palabras": [
                palabra.serialize()
                for palabra in self.palabras
            ]
        }