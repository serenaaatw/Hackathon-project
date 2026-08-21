from models.db import db
from models.progress import Progress
from models.category import Category


class ProgressService:

    @staticmethod
    def obtener_o_crear(id_user, id_word):
        progreso = Progress.query.filter_by(id_user=id_user, id_word=id_word).first()
        if progreso is None:
            progreso = Progress(id_user=id_user, id_word=id_word)
            db.session.add(progreso)
            db.session.commit()
        return progreso

    @staticmethod
    def registrar_resultado(id_user, id_word, correcto):
        #Llamado desde el juego cada vez que el niño/a responde algo
        progreso = ProgressService.obtener_o_crear(id_user, id_word)
        progreso.registrar_intento(correcto)
        db.session.commit()
        return progreso

    @staticmethod
    def categoria_dominada(id_user, categoria):
        #Una categoría está dominada cuando TODAS sus palabras lo están
        if not categoria.words:
            return False

        for palabra in categoria.words:
            progreso = Progress.query.filter_by(
                id_user=id_user, id_word=palabra.id_word
            ).first()
            if progreso is None or not progreso.esta_dominada():
                return False

        return True

    @staticmethod
    def siguiente_categoria(id_user):
        
        #Decide qué categoría le toca al niño/a ahora.

        categorias = Category.query.order_by(Category.id_category).all()

        for categoria in categorias:
            if not ProgressService.categoria_dominada(id_user, categoria):
                return categoria

        # Si domina todas las categorías existentes, por ahora la
        # repetimos como refuerzo (no hay "categoría siguiente" real
        # todavía). Cuando haya más categorías esto deja de pasar.
        return categorias[-1] if categorias else None

    @staticmethod
    def progreso_de_categoria(id_user, categoria):
        """Para el módulo de progreso del tutor: % de dominio de la categoría."""
        palabras = categoria.words
        if not palabras:
            return 0

        total_dominio = 0
        for palabra in palabras:
            progreso = Progress.query.filter_by(
                id_user=id_user, id_word=palabra.id_word
            ).first()
            total_dominio += progreso.dominio if progreso else 0

        return round(total_dominio / len(palabras))