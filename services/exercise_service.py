from services.learning_service import LearningService


class ExerciseService:
    @staticmethod
    def palabras_para_categoria(categoria):
        return [
            palabra.serialize()
            for palabra in categoria.words
        ]


    @staticmethod
    def obtener_categoria_con_palabras(slug):

        categoria = (
            LearningService.obtener_categoria(slug)
        )


        if categoria is None:

            return None, None


        palabras = (
            ExerciseService
            .palabras_para_categoria(categoria)
        )


        return categoria, palabras


    @staticmethod
    def obtener_siguiente_aprendizaje():

        return (
            LearningService
            .obtener_siguiente_aprendizaje()
        )
