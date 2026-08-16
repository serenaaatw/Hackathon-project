from services.learning_service import LearningService

class ExerciseService:

    @staticmethod
    def palabras_para_categoria(categoria):
        """Serializa las palabras de una categoría para mandarlas al template/JS."""
        return [w.serialize() for w in categoria.words]

    @staticmethod
    def obtener_categoria_con_palabras(slug):
        """Atajo: busca la categoría y devuelve (categoria, palabras) o (None, None)."""
        categoria = LearningService.obtener_categoria(slug)
        if categoria is None:
            return None, None
        return categoria, ExerciseService.palabras_para_categoria(categoria)