from models.db import db
from models.progress import Progress
from models.category import Category
from models.word import Word


class ProgressService:

    INTENTOS_MINIMOS = 5
    UMBRAL_DOMINIO = 70
    MAX_PALABRAS_EJERCICIO = 8
    PALABRAS_NUEVAS_POR_APRENDIZAJE = 3

    @staticmethod
    def obtener_o_crear(
        id_user,
        id_word,
        ronda
    ):

        progreso = Progress.query.filter_by(
            id_user=id_user,
            id_word=id_word,
            ronda=ronda
        ).first()

        if progreso is None:

            progreso = Progress(
                id_user=id_user,
                id_word=id_word,
                ronda=ronda
            )

            db.session.add(progreso)
            db.session.commit()

        return progreso

    @staticmethod
    def registrar_resultado(
        id_user,
        id_word,
        correcto,
        ronda
    ):

        progreso = (
            ProgressService.obtener_o_crear(
                id_user,
                id_word,
                ronda
            )
        )

        progreso.registrar_intento(
            correcto
        )

        db.session.commit()

        return progreso

    @staticmethod
    def obtener_dificultad_palabras(
        id_user,
        palabras
    ):

        if not palabras:
            return 1

        dominios = []

        for palabra in palabras:

            progreso = Progress.query.filter_by(
                id_user=id_user,
                id_word=palabra.id_word
            ).order_by(
                Progress.updated_at.desc()
            ).first()

            if progreso is None:
                dominio = 0
            else:
                dominio = progreso.dominio

            dominios.append(dominio)

        promedio = (
            sum(dominios) /
            len(dominios)
        )

        if promedio < 50:
            return 1

        if promedio < 70:
            return 2

        return 3

    @staticmethod
    def obtener_progreso_palabra(
        id_user,
        id_word
    ):

        progreso = (
            Progress.query
            .filter_by(
                id_user=id_user,
                id_word=id_word
            )
            .order_by(
                Progress.updated_at.desc()
            )
            .first()
        )

        if progreso is None:

            return {
                "id_word": id_word,
                "aciertos": 0,
                "intentos": 0,
                "dominio": 0,
                "dominada": False,
                "necesita_refuerzo": True,
                "nueva": True,
                "ronda": None
            }

        return progreso.serialize()

    @staticmethod
    def esta_dominada(progreso):

        if progreso is None:
            return False

        return (
            progreso.intentos >=
            ProgressService.INTENTOS_MINIMOS
            and
            progreso.dominio >=
            ProgressService.UMBRAL_DOMINIO
        )

    @staticmethod
    def necesita_refuerzo(progreso):

        if progreso is None:
            return True

        return (
            progreso.intentos == 0
            or
            progreso.dominio <
            ProgressService.UMBRAL_DOMINIO
        )

    @staticmethod
    def obtener_palabras_nuevas_categoria(
        id_user,
        categoria_slug,
        limite=3
    ):

        categoria = (
            Category.query
            .filter_by(
                slug=categoria_slug
            )
            .first()
        )

        if categoria is None:
            return []

        resultado = []

        for palabra in categoria.words:

            progreso = (
                Progress.query
                .filter_by(
                    id_user=id_user,
                    id_word=palabra.id_word
                )
                .first()
            )

            if progreso is None:

                resultado.append(palabra)

            elif progreso.intentos == 0:

                resultado.append(palabra)

            if len(resultado) >= limite:
                break

        return resultado

    @staticmethod
    def obtener_palabras_nuevas(
        id_user,
        limite=3
    ):

        categorias = (
            Category.query
            .order_by(
                Category.id_category
            )
            .all()
        )

        resultado = []

        for categoria in categorias:

            nuevas = (
                ProgressService
                .obtener_palabras_nuevas_categoria(
                    id_user,
                    categoria.slug,
                    limite
                )
            )

            for palabra in nuevas:

                if palabra not in resultado:

                    resultado.append(
                        palabra
                    )

                if len(resultado) >= limite:
                    return resultado

        return resultado

    @staticmethod
    def obtener_palabras_en_refuerzo(
        id_user
    ):

        progresos = (
            Progress.query
            .filter_by(
                id_user=id_user
            )
            .order_by(
                Progress.dominio.asc(),
                Progress.updated_at.asc()
            )
            .all()
        )

        resultado = []

        for progreso in progresos:

            if progreso.necesita_refuerzo():

                palabra = Word.query.get(
                    progreso.id_word
                )

                if palabra is not None:
                    resultado.append(
                        palabra
                    )

        return resultado

    @staticmethod
    def obtener_palabras_prioritarias(
        id_user
    ):

        nuevas = (
            ProgressService.obtener_palabras_nuevas(
                id_user,
                ProgressService.PALABRAS_NUEVAS_POR_APRENDIZAJE
            )
        )

        refuerzo = (
            ProgressService.obtener_palabras_en_refuerzo(
                id_user
            )
        )

        resultado = []
        ids = set()

        for palabra in refuerzo:

            if palabra.id_word not in ids:

                resultado.append(
                    palabra
                )

                ids.add(
                    palabra.id_word
                )

        for palabra in nuevas:

            if palabra.id_word not in ids:

                resultado.append(
                    palabra
                )

                ids.add(
                    palabra.id_word
                )

        return resultado[
            :ProgressService.MAX_PALABRAS_EJERCICIO
        ]

    @staticmethod
    def obtener_palabras_para_ejercicio(
        id_user
    ):

        palabras = (
            ProgressService
            .obtener_palabras_prioritarias(
                id_user
            )
        )

        if palabras:

            return [
                palabra.serialize()
                for palabra in palabras
            ]

        dominadas = (
            Progress.query
            .filter_by(
                id_user=id_user
            )
            .order_by(
                Progress.updated_at.desc()
            )
            .limit(
                ProgressService.MAX_PALABRAS_EJERCICIO
            )
            .all()
        )

        resultado = []

        for progreso in dominadas:

            palabra = Word.query.get(
                progreso.id_word
            )

            if palabra is not None:

                resultado.append(
                    palabra.serialize()
                )

        return resultado

    @staticmethod
    def obtener_palabras_aprendidas(
        id_user
    ):

        progresos = (
            Progress.query
            .filter_by(
                id_user=id_user
            )
            .all()
        )

        resultado = []

        for progreso in progresos:

            if ProgressService.esta_dominada(
                progreso
            ):

                palabra = Word.query.get(
                    progreso.id_word
                )

                if palabra is not None:

                    resultado.append(
                        palabra
                    )

        return resultado

    @staticmethod
    def puede_aprender_nuevas(
        id_user
    ):

        palabras = (
            ProgressService
            .obtener_palabras_en_refuerzo(
                id_user
            )
        )

        return not bool(palabras)

    @staticmethod
    def obtener_siguiente_aprendizaje(
        id_user,
        categoria_slug=None
    ):

        if categoria_slug:

            palabras = (
                ProgressService
                .obtener_palabras_nuevas_categoria(
                    id_user,
                    categoria_slug,
                    ProgressService
                    .PALABRAS_NUEVAS_POR_APRENDIZAJE
                )
            )

        else:

            palabras = (
                ProgressService.obtener_palabras_nuevas(
                    id_user,
                    ProgressService
                    .PALABRAS_NUEVAS_POR_APRENDIZAJE
                )
            )

        return [
            palabra.serialize()
            for palabra in palabras
        ]

    @staticmethod
    def ronda_dominada(
        id_user,
        palabras
    ):

        if not palabras:
            return False

        for palabra in palabras:

            progreso = (
                Progress.query
                .filter_by(
                    id_user=id_user,
                    id_word=palabra.id_word
                )
                .order_by(
                    Progress.updated_at.desc()
                )
                .first()
            )

            if not ProgressService.esta_dominada(
                progreso
            ):
                return False

        return True

    @staticmethod
    def ronda_necesita_repeticion(
        id_user,
        palabras
    ):

        return not (
            ProgressService.ronda_dominada(
                id_user,
                palabras
            )
        )

    @staticmethod
    def obtener_progreso_usuario(
        id_user
    ):

        categorias = (
            Category.query
            .order_by(
                Category.id_category
            )
            .all()
        )

        resultado = []

        for categoria in categorias:

            palabras = []

            for palabra in categoria.words:

                progreso = (
                    Progress.query
                    .filter_by(
                        id_user=id_user,
                        id_word=palabra.id_word
                    )
                    .order_by(
                        Progress.updated_at.desc()
                    )
                    .first()
                )

                if progreso is None:

                    dominio = 0
                    intentos = 0
                    aciertos = 0
                    dominada = False

                else:

                    dominio = progreso.dominio
                    intentos = progreso.intentos
                    aciertos = progreso.aciertos

                    dominada = (
                        ProgressService.esta_dominada(
                            progreso
                        )
                    )

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
                    ) /
                    len(palabras)
                )

            else:

                progreso_categoria = 0

            resultado.append({
                "id_category":
                    categoria.id_category,
                "slug":
                    categoria.slug,
                "name":
                    categoria.name,
                "dominio":
                    progreso_categoria,
                "palabras":
                    palabras
            })

        return resultado
