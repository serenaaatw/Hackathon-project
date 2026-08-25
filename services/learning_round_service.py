from models.db import db
from models.learning_round import LearningRound
from models.learning_round_word import LearningRoundWord
from models.word import Word
from models.category import Category
from models.progress import Progress


class LearningRoundService:

    CANTIDAD_PALABRAS = 3
    CANTIDAD_JUEGOS = 4

    @staticmethod
    def obtener_ronda_activa(id_user):

        return (
            LearningRound.query
            .filter(
                LearningRound.id_user == id_user,
                LearningRound.completada.is_(False)
            )
            .order_by(
                LearningRound.id_round.desc()
            )
            .first()
        )

    @staticmethod
    def obtener_palabras_ronda(ronda):

        if ronda is None:
            return []

        return [
            palabra_ronda.word
            for palabra_ronda in ronda.palabras
        ]

    @staticmethod
    def crear_ronda(
        id_user,
        palabras,
        id_category=None
    ):

        if not palabras:
            return None

        ronda_existente = (
            LearningRoundService.obtener_ronda_activa(
                id_user
            )
        )

        if ronda_existente is not None:
            return ronda_existente

        palabras = palabras[
            :LearningRoundService.CANTIDAD_PALABRAS
        ]

        if len(palabras) < LearningRoundService.CANTIDAD_PALABRAS:
            return None

        if id_category is None:
            id_category = palabras[0].id_category

        ronda = LearningRound(
            id_user=id_user,
            id_category=id_category,
            fase="aprendizaje",
            juego_actual=0,
            completada=False
        )

        db.session.add(ronda)
        db.session.flush()

        for indice, palabra in enumerate(palabras):

            palabra_ronda = LearningRoundWord(
                id_round=ronda.id_round,
                id_word=palabra.id_word,
                orden=indice
            )

            db.session.add(palabra_ronda)

        db.session.commit()

        return ronda

    @staticmethod
    def iniciar_ejercicios(id_user):

        ronda = (
            LearningRoundService.obtener_ronda_activa(
                id_user
            )
        )

        if ronda is None:
            return None

        ronda.iniciar_ejercicios()

        db.session.commit()

        return ronda

    @staticmethod
    def obtener_estado_ronda(id_user):

        ronda = (
            LearningRoundService.obtener_ronda_activa(
                id_user
            )
        )

        if ronda is None:
            return None

        return {
            "ronda": ronda,
            "juego_actual": ronda.juego_actual,
            "fase": ronda.fase,
            "id_category": ronda.id_category,
            "palabras": (
                LearningRoundService.obtener_palabras_ronda(
                    ronda
                )
            )
        }

    @staticmethod
    def obtener_palabras_para_juego(id_user):

        ronda = (
            LearningRoundService.obtener_ronda_activa(
                id_user
            )
        )

        if ronda is None:
            return []

        return (
            LearningRoundService.obtener_palabras_ronda(
                ronda
            )
        )

    @staticmethod
    def completar_juego(
        id_user,
        numero_juego
    ):

        ronda = (
            LearningRoundService.obtener_ronda_activa(
                id_user
            )
        )

        if ronda is None:
            return None

        if ronda.fase != "ejercicios":
            return ronda

        if numero_juego != ronda.juego_actual:
            return ronda

        if numero_juego < LearningRoundService.CANTIDAD_JUEGOS:
            ronda.avanzar_juego()

        else:
            ronda.juego_actual = LearningRoundService.CANTIDAD_JUEGOS
            ronda.fase = "ejercicios"

        db.session.commit()

        return ronda

    
    @staticmethod
    def reiniciar_ronda(id_user):

        ronda = (
            LearningRoundService.obtener_ronda_activa(
                id_user
            )
        )

        if ronda is None:
            return None

        palabras = (
            LearningRoundService.obtener_palabras_ronda(
                ronda
            )
        )

        for palabra in palabras:

            progreso = (
                Progress.query
                .filter_by(
                    id_user=id_user,
                    id_word=palabra.id_word
                )
                .first()
            )

            if progreso is not None:
                db.session.delete(progreso)

        ronda.juego_actual = 0
        ronda.fase = "aprendizaje"
        ronda.completada = False

        db.session.commit()

        return ronda

    @staticmethod
    def crear_siguiente_ronda(id_user):

        ronda_actual = (
            LearningRound.query
            .filter_by(
                id_user=id_user
            )
            .order_by(
                LearningRound.id_round.desc()
            )
            .first()
        )

        if ronda_actual is None:
            return None

        categoria_actual = Category.query.get(
            ronda_actual.id_category
        )

        if categoria_actual is None:
            return None

        categorias = (
            Category.query
            .order_by(
                Category.id_category
            )
            .all()
        )

        categoria_siguiente = None

        for categoria in categorias:

            if (
                categoria.id_category >
                categoria_actual.id_category
            ):

                categoria_siguiente = categoria
                break

        if categoria_siguiente is None:
            return None

        palabras = (
            Word.query
            .filter_by(
                id_category=categoria_siguiente.id_category
            )
            .order_by(
                Word.id_word
            )
            .all()
        )

        resultado = []

        for palabra in palabras:

            progreso = (
                Progress.query
                .filter_by(
                    id_user=id_user,
                    id_word=palabra.id_word
                )
                .first()
            )

            if progreso is None:
                resultado.append(palabra)

            elif progreso.intentos == 0:
                resultado.append(palabra)

            if (
                len(resultado) >=
                LearningRoundService.CANTIDAD_PALABRAS
            ):
                break

        if (
            len(resultado) <
            LearningRoundService.CANTIDAD_PALABRAS
        ):
            return None

        if not ronda_actual.completada:

            ronda_actual.completar()

            db.session.commit()

        return LearningRoundService.crear_ronda(
            id_user,
            resultado,
            categoria_siguiente.id_category
        )

    @staticmethod
    def completar_ronda(id_user):

        ronda = (
            LearningRoundService.obtener_ronda_activa(
                id_user
            )
        )

        if ronda is None:
            return None

        ronda.completar()

        db.session.commit()

        return ronda

    @staticmethod
    def ronda_completada(id_user):

        ronda = (
            LearningRoundService.obtener_ronda_activa(
                id_user
            )
        )

        return ronda is None