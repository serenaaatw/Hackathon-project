from flask import Blueprint, render_template, abort

from services.exercise_service import ExerciseService
from flask import Blueprint, render_template, abort, session

learning_bp = Blueprint(
    "learning",
    __name__,
    url_prefix="/aprender"
)


@learning_bp.route("/")
def aprender():
    id_user = session.get("usuario_id")

    categoria, palabras = (
        ExerciseService.obtener_siguiente_aprendizaje(id_user)
    )


    if categoria is None:

        abort(404)


    return render_template(

        "child/reconocer.html",

        categoria_slug=categoria.slug,

        categoria_nombre=categoria.name,

        palabras=palabras

    )