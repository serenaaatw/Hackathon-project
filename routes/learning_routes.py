from flask import Blueprint, render_template, abort
from services.exercise_service import ExerciseService

learning_bp = Blueprint("learning", __name__, url_prefix="/aprender")


@learning_bp.route("/<categoria_slug>")
def reconocer(categoria_slug):
    #Fase de reconocimiento: foto + seña + palabra, obligatoria antes de los juegos
    categoria, palabras = ExerciseService.obtener_categoria_con_palabras(categoria_slug)
    if categoria is None:
        abort(404)

    return render_template(
        "child/reconocer.html",
        categoria_slug=categoria_slug,
        categoria_nombre=categoria.name,
        palabras=palabras,
    )