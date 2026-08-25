from models.sentence import Sentence
from models.progress import Progress


class SentenceService:

    @staticmethod
    def obtener_palabras_dominadas(id_user):

        progresos = (
            Progress.query
            .filter(
                Progress.id_user == id_user
            )
            .all()
        )

        palabras = []

        for progreso in progresos:

            if progreso.esta_dominada():

                palabras.append(
                    progreso.word
                )

        return palabras


    @staticmethod
    def obtener_oraciones_posibles(id_user):

        palabras_dominadas = (
            SentenceService.obtener_palabras_dominadas(
                id_user
            )
        )

        ids_dominados = {
            palabra.id_word
            for palabra in palabras_dominadas
        }

        oraciones = (
            Sentence.query
            .all()
        )

        posibles = []

        for oracion in oraciones:

            if (
                oracion.id_subject
                not in ids_dominados
            ):
                continue

            if (
                oracion.id_action
                not in ids_dominados
            ):
                continue

            posibles.append(
                oracion
            )

        return posibles


    @staticmethod
    def obtener_oracion_para_usuario(id_user):

        oraciones = (
            SentenceService.obtener_oraciones_posibles(
                id_user
            )
        )

        if not oraciones:
            return None

        return oraciones[0]


    @staticmethod
    def obtener_estado(id_user):
        oracion = (
            SentenceService.obtener_oracion_para_usuario(
                id_user
            )
        )

        if oracion is None:

            return {
                "tipo": "sin_oraciones",
                "oracion": None
            }

        return {
            "tipo": "oracion",
            "oracion": oracion.serialize()
        }
