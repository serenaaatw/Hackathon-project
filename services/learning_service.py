from models.category import Category

class LearningService:

    @staticmethod
    def obtener_categoria(slug):
        """Busca una categoría por su slug (ej: 'animales'). Devuelve None si no existe."""
        return Category.query.filter_by(slug=slug).first()