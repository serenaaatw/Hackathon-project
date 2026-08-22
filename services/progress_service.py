from models.db import db
from models.progress import Progress
from models.category import Category


class ProgressService:

    @staticmethod
    def obtener_o_crear(id_user, id_word):

        progreso = Progress.query.filter_by(
            id_user=id_user,
            id_word=id_word
        ).first()

        if progreso is None:

            progreso = Progress(
                id_user=id_user,
                id_word=id_word
            )

            db.session.add(progreso)
            db.session.commit()

        return progreso

    @staticmethod
    def registrar_resultado(
        id_user,
        id_word,
        correcto
    ):

        progreso = ProgressService.obtener_o_crear(
            id_user,
            id_word
        )

        progreso.registrar_intento(
            correcto
        )

        db.session.commit()

        return progreso

    @staticmethod
    def obtener_progreso_usuario(id_user):

        categorias = Category.query.order_by(
            Category.id_category
        ).all()

        resultado = []

        for categoria in categorias:

            palabras = []

            for palabra in categoria.words:

                progreso = Progress.query.filter_by(
                    id_user=id_user,
                    id_word=palabra.id_word
                ).first()

                if progreso is None:

                    dominio = 0
                    intentos = 0
                    aciertos = 0
                    dominada = False

                else:

                    dominio = progreso.dominio
                    intentos = progreso.intentos
                    aciertos = progreso.aciertos
                    dominada = progreso.esta_dominada()

                palabras.append({
                    "id_word": palabra.id_word,
                    "word": palabra.word,
                    "articulo": palabra.articulo,
                    "dominio": dominio,
                    "intentos": intentos,
                    "aciertos": aciertos,
                    "dominada": dominada
                })

            if palabras:

                progreso_categoria = round(
                    sum(
                        palabra["dominio"]
                        for palabra in palabras
                    ) / len(palabras)
                )

            else:

                progreso_categoria = 0

            resultado.append({
                "id_category": categoria.id_category,
                "slug": categoria.slug,
                "name": categoria.name,
                "dominio": progreso_categoria,
                "palabras": palabras
            })

        return resultado
