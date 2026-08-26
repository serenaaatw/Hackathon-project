from models.sentence import Sentence


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