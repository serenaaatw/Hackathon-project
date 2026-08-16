from flask import Blueprint, render_template, abort
from services.exercise_service import ExerciseService

game_bp = Blueprint("game", __name__, url_prefix="/juego")


@game_bp.route("/1/<categoria_slug>")
def juego1(categoria_slug):
    #Juego 1 (Emparejar): imagen, palabra
    categoria, palabras = ExerciseService.obtener_categoria_con_palabras(categoria_slug)
    if categoria is None:
        abort(404)

    return render_template(
        "games/juego1.html",
        categoria_slug=categoria_slug,
        categoria_nombre=categoria.name,
        palabras=palabras,
    )