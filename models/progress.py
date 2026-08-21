from models.db import db


class Progress(db.Model):
    __tablename__ = 'progress'

    id_progress = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    id_word = db.Column(db.Integer, db.ForeignKey('words.id_word'), nullable=False)

    aciertos = db.Column(db.Integer, default=0, nullable=False)
    intentos = db.Column(db.Integer, default=0, nullable=False)
    dominio = db.Column(db.Integer, default=0, nullable=False)  # porcentaje 0-100

    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    user = db.relationship('User', backref='progresos')
    word = db.relationship('Word', backref='progresos')

    # Umbral para considerar una palabra "dominada": necesita al menos
    # estos intentos Y este % de aciertos. Los dos juntos evitan que
    # una sola respuesta (acertada de casualidad) cuente como aprendida.
    INTENTOS_MINIMOS = 3
    UMBRAL_DOMINIO = 80

    def __init__(self, id_user, id_word):
        self.id_user = id_user
        self.id_word = id_word

    def registrar_intento(self, correcto):
        self.intentos += 1
        if correcto:
            self.aciertos += 1
        self.dominio = round((self.aciertos / self.intentos) * 100)

    def esta_dominada(self):
        return self.intentos >= self.INTENTOS_MINIMOS and self.dominio >= self.UMBRAL_DOMINIO

    def serialize(self):
        return {
            'id_word': self.id_word,
            'aciertos': self.aciertos,
            'intentos': self.intentos,
            'dominio': self.dominio,
            'dominada': self.esta_dominada(),
        }