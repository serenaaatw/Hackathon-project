from services.learning_service import LearningService
from services.learning_round_service import LearningRoundService
from models.progress import Progress
from models.sentence import Sentence


class ExerciseService:

    UMBRAL_REPETICION = 50

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
    def obtener_progreso_ronda(
        id_user,
        palabras
    ):

        total_intentos = 0
        total_aciertos = 0

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
                continue

            total_intentos += progreso.intentos
            total_aciertos += progreso.aciertos

        if total_intentos == 0:
            return 0

        return round(
            (
                total_aciertos /
                total_intentos
            ) * 100
        )

    @staticmethod
    def puede_formar_oracion(
        id_user,
        palabras=None
    ):

        progresos = (
            Progress.query
            .filter(
                Progress.id_user == id_user,
                Progress.intentos > 0,
                Progress.dominio >=
                ExerciseService.UMBRAL_REPETICION
            )
            .all()
        )

        ids_dominados = {
            progreso.id_word
            for progreso in progresos
        }

        if palabras:

            ids_ronda = {
                palabra.id_word
                for palabra in palabras
            }

            ids_dominados = (
                ids_dominados |
                ids_ronda
            )

        if not ids_dominados:
            return False

        oracion = (
            Sentence.query
            .filter(
                Sentence.id_subject.in_(
                    ids_dominados
                ),
                Sentence.id_action.in_(
                    ids_dominados
                )
            )
            .first()
        )

        return oracion is not None

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
                "ronda": ronda,
                "juego_actual": None
            }

        progreso_ronda = (
            ExerciseService.obtener_progreso_ronda(
                id_user,
                palabras
            )
        )

        if progreso_ronda < ExerciseService.UMBRAL_REPETICION:

            ronda = (
                LearningRoundService.reiniciar_ronda(
                    id_user
                )
            )

            return {
                "decision": "repetir",
                "ronda": ronda,
                "juego_actual": 1
            }

        puede_formar = (
            ExerciseService.puede_formar_oracion(
                id_user,
                palabras
            )
        )

        if puede_formar:

            LearningRoundService.completar_ronda(
                id_user
            )

            return {
                "decision": "oracion",
                "ronda": None,
                "juego_actual": None
            }

        nueva_ronda = (
            LearningRoundService.crear_siguiente_ronda(
                id_user
            )
        )

        if nueva_ronda is not None:

            return {
                "decision": "aprender",
                "ronda": nueva_ronda,
                "juego_actual": 0
            }

        LearningRoundService.completar_ronda(
            id_user
        )

        return {
            "decision": "oracion",
            "ronda": None,
            "juego_actual": None
        }