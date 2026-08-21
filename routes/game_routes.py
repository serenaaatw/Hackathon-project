from flask import Blueprint, render_template, abort, request
from services.exercise_service import ExerciseService
from flask import request, jsonify, session
from services.progress_service import ProgressService

game_bp = Blueprint("game", __name__, url_prefix="/juego")


@game_bp.route("/1/<categoria_slug>")
def juego1(categoria_slug):
    categoria, palabras = ExerciseService.obtener_categoria_con_palabras(
        categoria_slug
    )

    if categoria is None:
        abort(404)

    return render_template(
        "games/juego1.html",
        categoria_slug=categoria_slug,
        categoria_nombre=categoria.name,
        palabras=palabras,
    )

@game_bp.route("/registrar-resultado", methods=["POST"])
def registrar_resultado():
    id_user = session.get("usuario_id")
    if id_user is None:
        return jsonify({"ok": False, "error": "No hay sesión activa"}), 401

    data = request.get_json(silent=True) or {}
    id_word = data.get("id_word")
    correcto = data.get("correcto")

    if id_word is None or correcto is None:
        return jsonify({"ok": False, "error": "Faltan datos"}), 400

    progreso = ProgressService.registrar_resultado(id_user, id_word, bool(correcto))
    return jsonify({"ok": True, "progreso": progreso.serialize()})

@game_bp.route("/3/<categoria_slug>")
def juego3(categoria_slug):
    categoria, palabras = ExerciseService.obtener_categoria_con_palabras(
        categoria_slug
    )

    if categoria is None:
        abort(404)

    return render_template(
        "games/juego3.html",
        categoria_slug=categoria_slug,
        categoria_nombre=categoria.name,
        palabras=palabras,
    )

@game_bp.route("/4/<categoria_slug>")
def juego4(categoria_slug):

    categoria, palabras = (
        ExerciseService.obtener_categoria_con_palabras(
            categoria_slug
        )
    )

    if categoria is None:
        abort(404)


    try:
        dificultad = int(
            request.args.get("dificultad", 1)
        )
    except (TypeError, ValueError):
        dificultad = 1

    dificultad = max(
        1,
        min(dificultad, 3)
    )

    return render_template(
        "games/juego4.html",
        categoria_slug=categoria_slug,
        categoria_nombre=categoria.name,
        palabras=palabras,
        dificultad=dificultad,
    )
