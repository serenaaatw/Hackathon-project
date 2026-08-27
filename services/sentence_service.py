from models.sentence import Sentence
from models.sentence_progress import SentenceProgress
from models.learning_round import LearningRound
from models.learning_round_word import LearningRoundWord
from models.db import db


class SentenceService:

    @staticmethod
    def obtener_oraciones_para_reconocer():

        return (
            Sentence.query
            .order_by(
                Sentence.id_sentence.asc()
            )
            .limit(3)
            .all()
        )

    @staticmethod
    def obtener_oracion(id_sentence):

        return (
            Sentence.query
            .filter_by(
                id_sentence=id_sentence
            )
            .first()
        )


    @staticmethod
    def obtener_oraciones_de_palabras_aprendidas(id_user):


        rondas = (
            LearningRound.query
            .filter(
                LearningRound.id_user == id_user,
                LearningRound.completada.is_(True)
            )
            .order_by(
                LearningRound.id_round.desc()
            )
            .limit(2)
            .all()
        )

        if len(rondas) < 2:
            return []


        palabras = []

        for ronda in rondas:

            palabras_ronda = (
                LearningRoundWord.query
                .filter_by(
                    id_round=ronda.id_round
                )
                .order_by(
                    LearningRoundWord.orden.asc()
                )
                .all()
            )

            for palabra_ronda in palabras_ronda:

                palabra = palabra_ronda.word

                if palabra is not None:
                    palabras.append(palabra)


        if len(palabras) < 6:
            return []


        animales = []
        acciones = []

        for palabra in palabras:

            categoria = palabra.category

            if categoria is None:
                continue

            slug = categoria.slug.lower()


            if slug in [
                "animales",
                "animal"
            ]:

                animales.append(palabra)

            elif slug in [
                "acciones",
                "accion"
            ]:

                acciones.append(palabra)


        animales = animales[:3]
        acciones = acciones[:3]

        if (
            len(animales) < 3
            or len(acciones) < 3
        ):
            return []

        ids_animales = {
            animal.id_word
            for animal in animales
        }

        ids_acciones = {
            accion.id_word
            for accion in acciones
        }

        oraciones = (
            Sentence.query
            .filter(
                Sentence.id_subject.in_(
                    ids_animales
                ),
                Sentence.id_action.in_(
                    ids_acciones
                )
            )
            .all()
        )


        combinaciones = {}

        for oracion in oraciones:

            clave = (
                oracion.id_subject,
                oracion.id_action
            )

            combinaciones[clave] = oracion

        resultado = []

        for animal in animales:

            for accion in acciones:

                clave = (
                    animal.id_word,
                    accion.id_word
                )

                oracion = combinaciones.get(
                    clave
                )

                if oracion is not None:

                    resultado.append(
                        oracion
                    )

        return resultado[:9]


    @staticmethod
    def obtener_bloque(numero_bloque):

        inicio = (
            (numero_bloque - 1) * 3
        )

        return (
            Sentence.query
            .order_by(
                Sentence.id_sentence.asc()
            )
            .offset(inicio)
            .limit(3)
            .all()
        )

    @staticmethod
    def obtener_bloque_por_ids(ids):

        if not ids:
            return []

        return (
            Sentence.query
            .filter(
                Sentence.id_sentence.in_(ids)
            )
            .order_by(
                Sentence.id_sentence.asc()
            )
            .all()
        )


    @staticmethod
    def obtener_o_crear_progreso(
        id_user,
        id_sentence
    ):

        progreso = (
            SentenceProgress.query
            .filter_by(
                id_user=id_user,
                id_sentence=id_sentence
            )
            .first()
        )

        if progreso is None:

            progreso = SentenceProgress(
                id_user=id_user,
                id_sentence=id_sentence
            )

            db.session.add(progreso)

        return progreso

    @staticmethod
    def bloque_dominado(
        id_user,
        ids_sentences
    ):

        if not ids_sentences:
            return False

        progresos = (
            SentenceProgress.query
            .filter(
                SentenceProgress.id_user == id_user,
                SentenceProgress.id_sentence.in_(
                    ids_sentences
                )
            )
            .all()
        )

        progresos_por_oracion = {
            progreso.id_sentence: progreso
            for progreso in progresos
        }

        for id_sentence in ids_sentences:

            progreso = (
                progresos_por_oracion.get(
                    id_sentence
                )
            )

            if not progreso:
                return False

            if not progreso.esta_dominada():
                return False

        return True


    @staticmethod
    def obtener_refuerzo(
        id_user,
        ids_sentences
    ):

        if not ids_sentences:
            return []

        progresos = (
            SentenceProgress.query
            .filter(
                SentenceProgress.id_user == id_user,
                SentenceProgress.id_sentence.in_(
                    ids_sentences
                )
            )
            .all()
        )

        progresos_por_oracion = {
            progreso.id_sentence: progreso
            for progreso in progresos
        }

        flojas = []

        for id_sentence in ids_sentences:

            progreso = (
                progresos_por_oracion.get(
                    id_sentence
                )
            )

            if (
                progreso
                and progreso.necesita_refuerzo()
            ):

                flojas.append(
                    id_sentence
                )

        if not flojas:
            return []

        ids_seleccionados = flojas[:3]

        if len(ids_seleccionados) < 3:

            for id_sentence in ids_sentences:

                if (
                    id_sentence
                    not in ids_seleccionados
                ):

                    ids_seleccionados.append(
                        id_sentence
                    )

                if len(ids_seleccionados) >= 3:
                    break

        return (
            Sentence.query
            .filter(
                Sentence.id_sentence.in_(
                    ids_seleccionados
                )
            )
            .order_by(
                Sentence.id_sentence.asc()
            )
            .all()
        )