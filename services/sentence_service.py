from models.sentence import Sentence
from models.sentence_progress import SentenceProgress


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

        return progreso

    @staticmethod
    def obtener_progreso(
        id_user,
        id_sentence
    ):

        return (
            SentenceProgress.query
            .filter_by(
                id_user=id_user,
                id_sentence=id_sentence
            )
            .first()
        )

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