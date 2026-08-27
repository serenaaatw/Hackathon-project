from models.category import Category
from models.word import Word
from models.progress import Progress
from models.sentence import Sentence
from models.db import db


class LearningService:

    PALABRAS_POR_RONDA = 3
    UMBRAL_APRENDIZAJE = 70

    CATEGORIAS_APRENDIZAJE = [
        "animales",
        "acciones"
    ]

    @staticmethod
    def obtener_categoria(slug):

        return (
            Category.query
            .filter_by(slug=slug)
            .first()
        )

    @staticmethod
    def obtener_palabras_nuevas(id_user):

        palabras = (
            Word.query
            .outerjoin(
                Progress,
                (
                    Progress.id_word == Word.id_word
                ) &
                (
                    Progress.id_user == id_user
                )
            )
            .filter(
                db.or_(
                    Progress.id_progress.is_(None),
                    Progress.intentos == 0
                )
            )
            .all()
        )

        return palabras

    @staticmethod
    def obtener_palabras_nuevas_categoria(
        id_user,
        categoria
    ):

        palabras = (
            LearningService.obtener_palabras_nuevas(
                id_user
            )
        )

        return [
            palabra
            for palabra in palabras
            if palabra.category.slug == categoria.slug
        ]

    @staticmethod
    def obtener_categoria_actual(id_user):

        for slug in LearningService.CATEGORIAS_APRENDIZAJE:

            categoria = (
                LearningService.obtener_categoria(slug)
            )

            if categoria is None:
                continue

            palabras = (
                LearningService.obtener_palabras_nuevas_categoria(
                    id_user,
                    categoria
                )
            )

            # Antes exigía >= PALABRAS_POR_RONDA (3) para considerar
            # la categoría "actual". Se relaja a "alguna palabra
            # nueva" para no perder las últimas palabras sueltas de
            # una categoría (ej: pájaro y vaca en animales), que antes
            # nunca llegaban a juntar 3 propias y quedaban afuera.
            if palabras:
                return categoria

        return None

    @staticmethod
    def obtener_siguiente_categoria(
        categoria_slug
    ):

        if categoria_slug not in (
            LearningService.CATEGORIAS_APRENDIZAJE
        ):
            return None

        indice = (
            LearningService.CATEGORIAS_APRENDIZAJE.index(
                categoria_slug
            )
        )

        siguiente = indice + 1

        if (
            siguiente >=
            len(LearningService.CATEGORIAS_APRENDIZAJE)
        ):
            return None

        return LearningService.obtener_categoria(
            LearningService.CATEGORIAS_APRENDIZAJE[
                siguiente
            ]
        )

    @staticmethod
    def obtener_progreso_palabra(
        id_user,
        id_word
    ):

        return (
            Progress.query
            .filter_by(
                id_user=id_user,
                id_word=id_word
            )
            .first()
        )

    @staticmethod
    def palabras_dominadas(
        id_user,
        palabras
    ):

        if not palabras:
            return False

        for palabra in palabras:

            progreso = (
                LearningService.obtener_progreso_palabra(
                    id_user,
                    palabra.id_word
                )
            )

            if progreso is None:
                return False

            if not progreso.esta_dominada():
                return False

        return True

    @staticmethod
    def obtener_palabras_dominadas(id_user):

        progresos = (
            Progress.query
            .filter(
                Progress.id_user == id_user,
                Progress.intentos > 0,
                Progress.dominio >=
                LearningService.UMBRAL_APRENDIZAJE
            )
            .all()
        )

        return [
            progreso.word
            for progreso in progresos
        ]

    @staticmethod
    def puede_formar_oracion(id_user):

        palabras_dominadas = (
            LearningService.obtener_palabras_dominadas(
                id_user
            )
        )

        ids = {
            palabra.id_word
            for palabra in palabras_dominadas
        }

        if not ids:
            return False

        oracion = (
            Sentence.query
            .filter(
                Sentence.id_subject.in_(ids),
                Sentence.id_action.in_(ids)
            )
            .first()
        )

        return oracion is not None

    @staticmethod
    def obtener_decision(
        id_user,
        palabras_ronda,
        categoria_slug
    ):

        dominadas = (
            LearningService.palabras_dominadas(
                id_user,
                palabras_ronda
            )
        )

        if not dominadas:
            return {
                "decision": "repetir",
                "categoria": categoria_slug
            }

        if LearningService.puede_formar_oracion(id_user):
            return {
                "decision": "oraciones",
                "categoria": categoria_slug
            }

        siguiente = (
            LearningService.obtener_siguiente_categoria(
                categoria_slug
            )
        )

        if siguiente is None:
            return {
                "decision": "completado",
                "categoria": None
            }

        return {
            "decision": "nuevo_aprendizaje",
            "categoria": siguiente.slug
        }

    @staticmethod
    def obtener_palabras_para_aprender(
        id_user,
        categoria_slug=None
    ):

        if categoria_slug is None:

            categoria = (
                LearningService.obtener_categoria_actual(
                    id_user
                )
            )

        else:

            categoria = (
                LearningService.obtener_categoria(
                    categoria_slug
                )
            )

        if categoria is None:
            return []

        palabras = (
            LearningService.obtener_palabras_nuevas_categoria(
                id_user,
                categoria
            )
        )

        return palabras[
            :LearningService.PALABRAS_POR_RONDA
        ]

    @staticmethod
    def obtener_siguiente_aprendizaje(
        id_user,
        categoria_slug=None
    ):

        categoria = None

        if categoria_slug:

            categoria = (
                LearningService.obtener_categoria(
                    categoria_slug
                )
            )

        else:

            categoria = (
                LearningService.obtener_categoria_actual(
                    id_user
                )
            )

        if categoria is None:
            return None, []

        palabras = (
            LearningService.obtener_palabras_para_aprender(
                id_user,
                categoria.slug
            )
        )

        if len(palabras) < LearningService.PALABRAS_POR_RONDA:
            return None, []

        return categoria, palabras

    @staticmethod
    def hay_palabras_para_aprender(
        id_user,
        categoria_slug=None
    ):

        return bool(
            LearningService.obtener_palabras_para_aprender(
                id_user,
                categoria_slug
            )
        )