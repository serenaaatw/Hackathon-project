from flask import Blueprint, render_template, abort

from services.exercise_service import ExerciseService


learning_bp = Blueprint(
    "learning",
    __name__,
    url_prefix="/aprender"
)


@learning_bp.route("/")
def aprender():

    categoria, palabras = (
        ExerciseService.obtener_siguiente_aprendizaje()
    )


    if categoria is None:

        abort(404)


    return render_template(

        "child/reconocer.html",

        categoria_slug=categoria.slug,

        categoria_nombre=categoria.name,

        palabras=palabras

    )