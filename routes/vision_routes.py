
from flask import Blueprint, render_template, send_from_directory, request, jsonify
import os

from vision.reconocimiento import (
    convertir_trazo_a_imagen,
    reconocer_letra,
    comparar_con_letra
)

vision_bp = Blueprint("vision", __name__)


@vision_bp.route("/reconocer_mano")
def reconocer():
    return render_template("child/reconocer_mano.html")


@vision_bp.route("/camara")
def camara():
    return render_template("child/camara.html")


@vision_bp.route("/hand_landmarker.task")
def hand_landmarker():

    ruta_vision = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(__file__)
            )
        ),
        "vision"
    )

    return send_from_directory(
        ruta_vision,
        "hand_landmarker.task"
    )


@vision_bp.route("/procesar_dibujo", methods=["POST"])
def procesar_dibujo():

    try:

        datos = request.get_json()

        puntos_dibujo = datos.get(
            "puntos_dibujo",
            []
        )

        letra_objetivo = datos.get(
            "letra_objetivo",
            "A"
        )

        if not puntos_dibujo:
            return jsonify({
                "error": "No se recibió ningún dibujo"
            }), 400

        # -------------------------------------------------
        # Convertir puntos de JavaScript a formato Python
        # -------------------------------------------------

        puntos_python = []

        for trazo in puntos_dibujo:

            nuevo_trazo = []

            for punto in trazo:

                x = float(punto["x"])
                y = float(punto["y"])

                nuevo_trazo.append(
                    (x, y)
                )

            if nuevo_trazo:
                puntos_python.append(
                    nuevo_trazo
                )

        if not puntos_python:
            return jsonify({
                "error": "El dibujo no contiene puntos válidos"
            }), 400

        print(
            "📥 Puntos recibidos:",
            len(puntos_python)
        )

        # -------------------------------------------------
        # Convertir dibujo a imagen
        # -------------------------------------------------

        imagen = convertir_trazo_a_imagen(
            puntos_python
        )

        if imagen is None:
            return jsonify({
                "error": "No se pudo convertir el dibujo"
            }), 400

        print("✅ Dibujo convertido a imagen")

        # -------------------------------------------------
        # Reconocimiento mediante IA
        # -------------------------------------------------

        letra_detectada, confianza = reconocer_letra(
            imagen
        )

        print(
            "🤖 IA:",
            letra_detectada,
            confianza
        )

        # -------------------------------------------------
        # Comparar contra la letra objetivo
        # -------------------------------------------------

        similitud = comparar_con_letra(
            imagen,
            letra_objetivo
        )

        print(
            "📊 Similitud:",
            similitud
        )

        # -------------------------------------------------
        # Calificación
        # -------------------------------------------------

        if similitud >= 70:

            calificacion = "BUENO"

        elif similitud >= 50:

            calificacion = "MEDIO"

        else:

            calificacion = "MALO"

        print(
            f"Letra: {letra_objetivo} | "
            f"Detectada: {letra_detectada} | "
            f"Confianza: {confianza:.2f}% | "
            f"Similitud: {similitud:.2f}% | "
            f"Resultado: {calificacion}"
        )

        return jsonify({

            "letra_objetivo": letra_objetivo,

            "letra_detectada": letra_detectada,

            "confianza": float(confianza),

            "similitud": float(similitud),

            "calificacion": calificacion

        })

    except Exception as error:

        print(
            "❌ Error procesando dibujo:",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500