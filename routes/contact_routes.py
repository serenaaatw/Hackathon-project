from flask import (
Blueprint,
render_template,
jsonify,
request,
session
)

from utils.email_services import send_contact_message

contact_bp = Blueprint(
"contact",
__name__,
url_prefix="/contacto"
)

@contact_bp.route("/")
def contacto():


    return render_template(
        "child/contacto.html"
    )


@contact_bp.route(
"/enviar",
methods=["POST"]
)
def enviar_contacto():


    data = (
        request.get_json(
            silent=True
        )
        or {}
    )


    motivo = (
        data.get("motivo")
        or ""
    ).strip()

    email = (
        data.get("email")
        or ""
    ).strip()

    mensaje = (
        data.get("mensaje")
        or ""
    ).strip()


    if not motivo:

        return jsonify({
            "ok": False,
            "mensaje":
                "SELECCIONÁ UN MOTIVO."
        }), 400


    if not email:

        return jsonify({
            "ok": False,
            "mensaje":
                "INGRESÁ TU MAIL."
        }), 400


    if not mensaje:

        return jsonify({
            "ok": False,
            "mensaje":
                "ESCRIBÍ UN MENSAJE."
        }), 400


    if len(mensaje) > 2000:

        return jsonify({
            "ok": False,
            "mensaje":
                "EL MENSAJE ES DEMASIADO LARGO."
        }), 400


    try:

        send_contact_message(
            user_email=email,
            motivo=motivo,
            mensaje=mensaje
        )

    except Exception as e:

        print(
            "ERROR CONTACTO:",
            e
        )

        return jsonify({
            "ok": False,
            "mensaje":
                "NO SE PUDO ENVIAR EL MENSAJE. INTENTÁ NUEVAMENTE."
        }), 500


    return jsonify({
        "ok": True,
        "mensaje":
            "MENSAJE ENVIADO CORRECTAMENTE."
    })

