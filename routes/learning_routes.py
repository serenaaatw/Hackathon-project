from flask import (
Blueprint,
render_template,
jsonify,
session,
abort,
redirect,
url_for,
request
)

from services.learning_service import LearningService
from services.learning_round_service import LearningRoundService
from services.sentence_service import SentenceService

learning_bp = Blueprint(
"learning",
__name__,
url_prefix="/aprender"
)

@learning_bp.route("/")
def aprender():

    id_user = session.get("usuario_id")

    if id_user is None:
        abort(401)

    decision = session.pop(
        "decision_aprendizaje",
        None
    )

    ronda = (
        LearningRoundService.obtener_ronda_activa(
            id_user
        )
    )

    if ronda is not None:

        if ronda.fase == "ejercicios":

            if ronda.juego_actual == 1:
                return redirect(
                    url_for("game.juego1")
                )

            if ronda.juego_actual == 2:
                return redirect(
                    url_for("game.juego_unir")
                )

            if ronda.juego_actual == 3:
                return redirect(
                    url_for("game.juego3")
                )

            if ronda.juego_actual == 4:
                return redirect(
                    url_for("game.juego4")
                )

        palabras = (
            LearningRoundService.obtener_palabras_ronda(
                ronda
            )
        )

        if not palabras:
            abort(404)

        categoria = palabras[0].category

        return render_template(
            "child/reconocer.html",
            categoria_slug=categoria.slug,
            categoria_nombre=categoria.name,
            palabras=[
                palabra.serialize()
                for palabra in palabras
            ],
            decision=decision
        )

    palabras_nuevas = (
        LearningService.obtener_palabras_para_aprender(
            id_user
        )
    )

    if not palabras_nuevas:
        abort(404)

    categoria = palabras_nuevas[0].category

    ronda = (
        LearningRoundService.crear_ronda(
            id_user,
            palabras_nuevas
        )
    )

    if ronda is None:
        abort(404)

    return render_template(
        "child/reconocer.html",
        categoria_slug=categoria.slug,
        categoria_nombre=categoria.name,
        palabras=[
            palabra.serialize()
            for palabra in palabras_nuevas
        ],
        decision=decision
    )

@learning_bp.route(
"/iniciar-ejercicios",
methods=["POST"]
)
def iniciar_ejercicios():


    id_user = session.get("usuario_id")

    if id_user is None:

        return jsonify({
            "ok": False,
            "error": "No hay sesión activa"
        }), 401

    ronda = (
        LearningRoundService.iniciar_ejercicios(
            id_user
        )
    )

    if ronda is None:

        return jsonify({
            "ok": False,
            "error": "No hay una ronda activa"
        }), 404

    return jsonify({
        "ok": True,
        "juego_actual": ronda.juego_actual
    })
