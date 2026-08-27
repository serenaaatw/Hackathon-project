from models.db import db


class ExerciseProgress(db.Model):
    __tablename__ = "exercise_progress"

    id_exercise_progress = db.Column(
        db.Integer,
        primary_key=True
    )

    id_round = db.Column(
        db.Integer,
        db.ForeignKey("learning_round.id_round"),
        nullable=False
    )

    numero_juego = db.Column(
        db.Integer,
        nullable=False
    )

    completado = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    round = db.relationship(
        "LearningRound",
        backref="ejercicios"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "id_round",
            "numero_juego",
            name="uq_round_juego"
        ),
    )

    def __init__(
        self,
        id_round,
        numero_juego
    ):
        self.id_round = id_round
        self.numero_juego = numero_juego
        self.completado = False

    def marcar_completado(self):
        self.completado = True

    def serialize(self):
        return {
            "id_exercise_progress":
                self.id_exercise_progress,
            "id_round":
                self.id_round,
            "numero_juego":
                self.numero_juego,
            "completado":
                self.completado
        }
