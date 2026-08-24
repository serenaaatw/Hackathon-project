from services.learning_service import LearningService
from services.learning_round_service import LearningRoundService
from services.progress_service import ProgressService
from models.progress import Progress
from models.word import Word
from models.sentence import Sentence


class ExerciseService:

    @staticmethod
    def obtener_estado_aprendizaje(id_user):

        return LearningService.obtener_estado_aprendizaje(
            id_user
        )

    @staticmethod
    def obtener_palabras_para_ejercicio(id_user):

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
    def obtener_palabras_ronda_activa(id_user):

        return (
            ExerciseService.obtener_palabras_para_ejercicio(
                id_user
            )
        )

    @staticmethod
    def obtener_ronda_activa(id_user):

        return (
            LearningRoundService.obtener_ronda_activa(
                id_user
            )
        )

    @staticmethod
    def obtener_siguiente_aprendizaje(id_user):

        return (
            LearningService.obtener_siguiente_aprendizaje(
                id_user
            )
        )

    @staticmethod
    def obtener_estado_ronda(id_user):

        return (
            LearningRoundService.obtener_estado_ronda(
                id_user
            )
        )

    @staticmethod
    def obtener_juego_actual(id_user):

        estado = (
            LearningRoundService.obtener_estado_ronda(
                id_user
            )
        )

        if estado is None:
            return None

        return estado["juego_actual"]

    @staticmethod
    def completar_juego(
        id_user,
        numero_juego
    ):

        return (
            LearningRoundService.completar_juego(
                id_user,
                numero_juego
            )
        )

    @staticmethod
    def resolver_decision(id_user):

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

        if not palabras:
            return {
                "decision": "aprender",
                "ronda": ronda
            }

        necesita_repetir = False

        for palabra in palabras:

            progreso = (
                Progress.query
                .filter_by(
                    id_user=id_user,
                    id_word=palabra.id_word
                )
                .order_by(
                    Progress.updated_at.desc()
                )
                .first()
            )

            if progreso is None:
                necesita_repetir = True
                break

            if not ProgressService.esta_dominada(
                progreso
            ):
                necesita_repetir = True
                break

        if necesita_repetir:

            LearningRoundService.reiniciar_ronda(
                id_user
            )

            return {
                "decision": "repetir",
                "ronda": (
                    LearningRoundService
                    .obtener_ronda_activa(id_user)
                )
            }

        puede_formar_oracion = (
            ExerciseService.puede_formar_oracion(
                id_user,
                palabras
            )
        )

        if puede_formar_oracion:

            LearningRoundService.completar_ronda(
                id_user
            )

            return {
                "decision": "oracion",
                "ronda": None
            }

        nueva_ronda = (
            LearningRoundService.crear_siguiente_ronda(
                id_user
            )
        )

        if nueva_ronda is not None:

            return {
                "decision": "aprender",
                "ronda": nueva_ronda
            }

        LearningRoundService.completar_ronda(
            id_user
        )

        return {
            "decision": "oracion",
            "ronda": None
        }

    @staticmethod
    def puede_formar_oracion(
        id_user,
        palabras
    ):

        if not palabras:
            return False

        for palabra in palabras:

            sujeto = (
                Sentence.query
                .filter_by(
                    id_subject=palabra.id_word
                )
                .first()
            )

            if sujeto is not None:
                return True

        for palabra in palabras:

            accion = (
                Sentence.query
                .filter_by(
                    id_action=palabra.id_word
                )
                .first()
            )

            if accion is not None:
                return True

        return False