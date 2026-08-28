from flask import (
    Blueprint,
    render_template,
    abort,
    url_for,
    session,
    jsonify,
    request
)

from services.sentence_service import SentenceService
from services.learning_service import LearningService

from models.db import db


sentence_bp = Blueprint(
    "sentence",
    __name__,
    url_prefix="/oraciones"
)

def serializar_oraciones(oraciones):

    resultado = []

    for oracion in oraciones:

        data = oracion.serialize()

        if oracion.image_file:

            data["image_url"] = url_for(
                "static",
                filename=(
                    "img/sentences/"
                    + oracion.image_file
                )
            )

        else:

            data["image_url"] = None

        if oracion.lsa_video_file:

            data["lsa_video_url"] = url_for(
                "static",
                filename=(
                    "videos/lsa/sentences/"
                    + oracion.lsa_video_file
                )
            )

        else:

            data["lsa_video_url"] = None

        if oracion.sentence_video_file:

            data["video_url"] = url_for(
                "static",
                filename=(
                    "videos/sentences/"
                    + oracion.sentence_video_file
                )
            )

        else:

            data["video_url"] = None

        if oracion.audio_file:
        
            data["audio_url"] = url_for(
                 "static",
                filename=(
                 "audio/sentences/"
                            + oracion.audio_file
                        )
                    )
        else:
        
            data["audio_url"] = None

        resultado.append(data)

    return resultado


@sentence_bp.route("/fin")
def fin_oraciones():

    id_user = session.get(
        "usuario_id"
    )

    if id_user is None:
        abort(401)

    palabras_dominadas = (
        LearningService.obtener_palabras_dominadas(
            id_user
        )
    )

    return render_template(
        "child/fin.html",
        palabras=[
            palabra.serialize()
            for palabra in palabras_dominadas
        ]
    )



@sentence_bp.route("/reconocer")
def reconocer_oraciones():

    id_user = session.get(
        "usuario_id"
    )

    if id_user is None:
        abort(401)

    ids_refuerzo = session.get(
        "oraciones_refuerzo"
    )

    if ids_refuerzo:

        oraciones = (
            SentenceService
            .obtener_bloque_por_ids(
                ids_refuerzo
            )
        )

    else:

        oraciones = (
            SentenceService
            .obtener_oraciones_de_palabras_aprendidas(
                id_user
            )
        )

    if not oraciones:
        abort(404)

    return render_template(
        "child/reconocer_oracion.html",
        oraciones=serializar_oraciones(
            oraciones
        )
    )

@sentence_bp.route("/juego/1")
def juego_oraciones_1():

    id_user = session.get(
        "usuario_id"
    )

    if id_user is None:
        abort(401)


    ids_refuerzo = session.get(
        "oraciones_refuerzo"
    )

    if ids_refuerzo:

        oraciones = (
            SentenceService
            .obtener_bloque_por_ids(
                ids_refuerzo
            )
        )

        numero_bloque = session.get(
            "oraciones_bloque",
            1
        )

    else:


        ids_oraciones = session.get(
            "oraciones_totales"
        )

        if not ids_oraciones:

            oraciones_totales = (
                SentenceService
                .obtener_oraciones_de_palabras_aprendidas(
                    id_user
                )
            )

            if not oraciones_totales:
                abort(404)

            ids_oraciones = [
                oracion.id_sentence
                for oracion in oraciones_totales
            ]

            session["oraciones_totales"] = (
                ids_oraciones
            )

        numero_bloque = session.get(
            "oraciones_bloque",
            1
        )

        inicio = (
            (numero_bloque - 1) * 3
        )

        ids_bloque = ids_oraciones[
            inicio:inicio + 3
        ]

        oraciones = (
            SentenceService
            .obtener_bloque_por_ids(
                ids_bloque
            )
        )

    if not oraciones:
        abort(404)


    session["oraciones_actuales"] = [
        oracion.id_sentence
        for oracion in oraciones
    ]

    session["oraciones_juego_actual"] = 1

    return render_template(
        "games/juego_oraciones1.html",
        oraciones=serializar_oraciones(
            oraciones
        ),
        numero_bloque=numero_bloque
    )



@sentence_bp.route("/juego/2")
def juego_oraciones_2():

    ids_actuales = session.get(
        "oraciones_actuales"
    )

    if not ids_actuales:

        return (
            jsonify({
                "ok": False,
                "mensaje": "No hay oraciones activas."
            }),
            400
        )

    oraciones = (
        SentenceService
        .obtener_bloque_por_ids(
            ids_actuales
        )
    )

    if not oraciones:
        abort(404)

    session["oraciones_juego_actual"] = 2

    return render_template(
        "games/juego_oraciones2.html",
        oraciones=serializar_oraciones(
            oraciones
        )
    )



@sentence_bp.route(
    "/registrar-resultado",
    methods=["POST"]
)
def registrar_resultado():

    datos = request.get_json(
        silent=True
    ) or {}

    id_sentence = datos.get(
        "id_sentence"
    )

    correcto = datos.get(
        "correcto"
    )

    juego = datos.get(
        "juego"
    )

    if (
        id_sentence is None
        or correcto is None
        or juego not in [1, 2]
    ):

        return (
            jsonify({
                "ok": False,
                "mensaje": "Datos inválidos."
            }),
            400
        )

    id_user = session.get(
        "usuario_id"
    )

    if not id_user:

        return (
            jsonify({
                "ok": False,
                "mensaje": "Usuario no autenticado."
            }),
            401
        )

    oracion = (
        SentenceService
        .obtener_oracion(
            id_sentence
        )
    )

    if not oracion:

        return (
            jsonify({
                "ok": False,
                "mensaje": "La oración no existe."
            }),
            404
        )

    progreso = (
        SentenceService
        .obtener_o_crear_progreso(
            id_user=id_user,
            id_sentence=id_sentence
        )
    )

    progreso.registrar_intento(
        bool(correcto)
    )

    print(
        "GUARDANDO:",
        id_user,
        id_sentence,
        correcto,
        progreso.aciertos,
        progreso.intentos,
        progreso.dominio
    )

    db.session.add(
        progreso
    )

    db.session.commit()

    print(
        "GUARDADO:",
        progreso.id_sentence_progress
    )

    return jsonify({
        "ok": True,
        "progreso": progreso.serialize()
    })


@sentence_bp.route(
    "/finalizar-juego-1",
    methods=["POST"]
)
def finalizar_juego_1():

    ids_actuales = session.get(
        "oraciones_actuales"
    )

    if not ids_actuales:

        return (
            jsonify({
                "ok": False,
                "mensaje": "No hay bloque activo."
            }),
            400
        )

    session["oraciones_juego_actual"] = 2

    return jsonify({
        "ok": True,
        "siguiente": "/oraciones/juego/2"
    })



@sentence_bp.route(
    "/finalizar-juego-2",
    methods=["POST"]
)

def finalizar_juego_2():

    ids_actuales = session.get(
        "oraciones_actuales"
    )

    numero_bloque = session.get(
        "oraciones_bloque",
        1
    )

    if not ids_actuales:

        return (
            jsonify({
                "ok": False,
                "mensaje": "No hay bloque activo."
            }),
            400
        )

    id_user = session.get(
        "usuario_id"
    )

    if not id_user:

        return (
            jsonify({
                "ok": False,
                "mensaje": "Usuario no autenticado."
            }),
            401
        )

    dominado = (
        SentenceService
        .bloque_dominado(
            id_user,
            ids_actuales
        )
    )

    if dominado:

        session.pop(
            "oraciones_refuerzo",
            None
        )

        if numero_bloque >= 3:

            session.pop(
                "oraciones_bloque",
                None
            )

            session.pop(
                "oraciones_actuales",
                None
            )

            session.pop(
                "oraciones_juego_actual",
                None
            )

            session.pop(
                "oraciones_totales",
                None
            )

            return jsonify({
                "ok": True,
                "completo": True,
                "siguiente": "/oraciones/fin"
            })

        siguiente_bloque = (
            numero_bloque + 1
        )

        session["oraciones_bloque"] = (
            siguiente_bloque
        )

        session.pop(
            "oraciones_actuales",
            None
        )

        return jsonify({
            "ok": True,
            "completo": False,
            "refuerzo": False,
            "siguiente": "/oraciones/juego/1"
        })


    refuerzo = (
        SentenceService
        .obtener_refuerzo(
            id_user,
            ids_actuales
        )
    )


    if refuerzo:

        ids_refuerzo = [
            oracion.id_sentence
            for oracion in refuerzo
        ]


        if numero_bloque >= 3:

            session.pop(
                "oraciones_refuerzo",
                None
            )

            session.pop(
                "oraciones_bloque",
                None
            )

            session.pop(
                "oraciones_actuales",
                None
            )

            session.pop(
                "oraciones_juego_actual",
                None
            )

            session.pop(
                "oraciones_totales",
                None
            )

            return jsonify({
                "ok": True,
                "completo": True,
                "refuerzo": True,
                "siguiente": "/oraciones/fin"
            })


        session["oraciones_refuerzo"] = (
            ids_refuerzo
        )

        session["oraciones_actuales"] = (
            ids_refuerzo
        )

        return jsonify({
            "ok": True,
            "completo": False,
            "refuerzo": True,
            "siguiente": "/oraciones/juego/1"
        })


    if numero_bloque >= 3:

        session.pop(
            "oraciones_bloque",
            None
        )

        session.pop(
            "oraciones_actuales",
            None
        )

        session.pop(
            "oraciones_juego_actual",
            None
        )

        session.pop(
            "oraciones_totales",
            None
        )

        return jsonify({
            "ok": True,
            "completo": True,
            "siguiente": "/oraciones/fin"
        })


    return jsonify({
        "ok": True,
        "completo": False,
        "refuerzo": False,
        "siguiente": "/oraciones/juego/1"
    })