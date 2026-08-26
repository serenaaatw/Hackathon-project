from flask import (
    Blueprint,
    render_template,
    abort,
    url_for
)

from services.sentence_service import SentenceService


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
                filename="img/oraciones/" + oracion.image_file
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
                filename="videos/oraciones/" + oracion.sentence_video_file
            )
        else:
            data["video_url"] = None

        if oracion.audio_file:
            data["audio_url"] = url_for(
                "static",
                filename="audio/oraciones/" + oracion.audio_file
            )
        else:
            data["audio_url"] = None

        resultado.append(data)

    return resultado


@sentence_bp.route("/reconocer")
def reconocer_oraciones():

    oraciones = SentenceService.obtener_oraciones_para_reconocer()

    if not oraciones:
        abort(404)

    return render_template(
        "child/reconocer_oracion.html",
        oraciones=serializar_oraciones(oraciones)
    )