from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    abort,
    url_for
)

from flask_login import login_required
from services.exercise_service import ExerciseService
from services.progress_service import ProgressService


game_bp = Blueprint(
    "game",
    __name__,
    url_prefix="/juego"
)


def obtener_palabras_usuario():

    id_user = session.get("usuario_id")

    if id_user is None:
        return None

    return (
        ExerciseService
        .obtener_palabras_para_ejercicio(id_user)
    )


def obtener_contexto_juego():

    palabras = obtener_palabras_usuario()

    if palabras is None:
        abort(401)

    if not palabras:
        abort(404)

    return palabras


def serializar_palabras(palabras):

    resultado = []

    for palabra in palabras:

        data = palabra.serialize()

        data["image_url"] = url_for(
            "static",
            filename=(
                "img/"
                + palabra.category.slug
                + "/"
                + palabra.image_file
            )
        )

        if palabra.lsa_video_file:

            data["lsa_video_url"] = url_for(
                "static",
                filename=(
                    "videos/lsa/"
                    + palabra.category.slug
                    + "/"
                    + palabra.lsa_video_file
                )
            )

        else:

            data["lsa_video_url"] = None

        resultado.append(data)

    return resultado


@game_bp.route("/1")
@login_required
def juego1():

    palabras = obtener_contexto_juego()

    return render_template(
        "games/juego1.html",
        palabras=serializar_palabras(palabras)
    )

@game_bp.route("/unir")
@login_required
def juego_unir():

    palabras = obtener_contexto_juego()

    return render_template(
        "games/juego_unir.html",
        palabras=serializar_palabras(palabras),
        categoria_slug=palabras[0].category.slug,
        categoria_nombre=palabras[0].category.name
    )


@game_bp.route("/3")
@login_required
def juego3():

    palabras = obtener_contexto_juego()

    return render_template(
        "games/juego3.html",
        palabras=serializar_palabras(palabras),
        categoria_slug=palabras[0].category.slug,
        categoria_nombre=palabras[0].category.name
    )


@game_bp.route("/4")
@login_required
def juego4():

    id_user = session.get("usuario_id")

    if id_user is None:
        abort(401)

    palabras = obtener_contexto_juego()

    dificultad = (
        ProgressService.obtener_dificultad_palabras(
            id_user,
            palabras
        )
    )

    return render_template(
        "games/juego4.html",
        palabras=serializar_palabras(palabras),
        categoria_slug=palabras[0].category.slug,
        categoria_nombre=palabras[0].category.name,
        dificultad=dificultad
    )


@game_bp.route(
    "/completar",
    methods=["POST"]
)
@login_required
def completar_juego():

    id_user = session.get("usuario_id")

    if id_user is None:

        return jsonify({
            "ok": False,
            "error": "No hay sesión activa"
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    numero_juego = data.get(
        "numero_juego"
    )

    if numero_juego is None:

        return jsonify({
            "ok": False,
            "error": "Falta numero_juego"
        }), 400

    try:

        numero_juego = int(
            numero_juego
        )

    except (
        TypeError,
        ValueError
    ):

        return jsonify({
            "ok": False,
            "error": "Juego inválido"
        }), 400

    if numero_juego < 1 or numero_juego > 4:

        return jsonify({
            "ok": False,
            "error": "Juego inválido"
        }), 400

    ronda = (
        ExerciseService.completar_juego(
            id_user,
            numero_juego
        )
    )

    if ronda is None:

        return jsonify({
            "ok": False,
            "error": "No hay una ronda activa"
        }), 404

    if numero_juego < 4:

        estado = (
            ExerciseService.obtener_estado_ronda(
                id_user
            )
        )

        return jsonify({
            "ok": True,
            "decision": None,
            "juego_actual": (
                estado["juego_actual"]
                if estado is not None
                else None
            ),
            "ronda_completada": False
        })

    resultado = (
        ExerciseService.resolver_decision(
            id_user
        )
    )

    if resultado is None:

        return jsonify({
            "ok": False,
            "error": "No se pudo resolver la decisión"
        }), 404

    ronda_resultado = resultado.get(
        "ronda"
    )

    decision = resultado.get("decision")

    session["decision_aprendizaje"] = decision

    return jsonify({
        "ok": True,
        "decision": decision,
        "juego_actual": resultado.get(
            "juego_actual"
        ),
        "ronda_completada": (
            decision == "oracion"
        ),
        "hay_ronda": (
            ronda_resultado is not None
        )
    })


@game_bp.route(
    "/decidir",
    methods=["POST"]
)
@login_required
def decidir_siguiente_paso():

    id_user = session.get("usuario_id")

    if id_user is None:

        return jsonify({
            "ok": False,
            "error": "No hay sesión activa"
        }), 401

    resultado = (
        ExerciseService.resolver_decision(
            id_user
        )
    )

    if resultado is None:

        return jsonify({
            "ok": False,
            "error": "No hay una ronda activa"
        }), 404

    ronda = resultado.get(
        "ronda"
    )

    return jsonify({
        "ok": True,
        "decision": resultado.get(
            "decision"
        ),
        "juego_actual": resultado.get(
            "juego_actual"
        ),
        "hay_ronda": ronda is not None
    })


@game_bp.route(
    "/registrar-resultado",
    methods=["POST"]
)
@login_required
def registrar_resultado():

    id_user = session.get("usuario_id")

    if id_user is None:

        return jsonify({
            "ok": False,
            "error": "No hay sesión activa"
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    id_word = data.get(
        "id_word"
    )

    correcto = data.get(
        "correcto"
    )

    if (
        id_word is None
        or correcto is None
    ):

        return jsonify({
            "ok": False,
            "error": "Faltan datos"
        }), 400

    ronda = (
        ExerciseService.obtener_ronda_activa(
            id_user
        )
    )

    if ronda is None:

        return jsonify({
            "ok": False,
            "error": "No hay una ronda activa"
        }), 404

    progreso = (
        ProgressService.registrar_resultado(
            id_user,
            id_word,
            bool(correcto),
            ronda.id_round
        )
    )

    return jsonify({
        "ok": True,
        "progreso": progreso.serialize()
    })