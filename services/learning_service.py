from models.category import Category

class LearningService:
    @staticmethod
    def obtener_categoria(slug):

        categoria = (
            Category.query
            .filter_by(slug=slug)
            .first()
        )
        return categoria


    @staticmethod
    def obtener_siguiente_aprendizaje():

        categoria = Category.query.first()


        if categoria is None:

            return None, []

        palabras = [
            palabra.serialize()
            for palabra in categoria.words
        ]

        return categoria, palabras