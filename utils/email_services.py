import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import random
import os

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")

def send_verification_code(adressee):
    code = random.randint(100000, 999999)

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    sender = {
        "name": "EduSeñas",
        "email": MAIL_USERNAME
    }

    email = sib_api_v3_sdk.SendSmtpEmail(
        sender=sender,
        to=[{"email": adressee}],
        subject="Código de verificación",
        text_content=f"""
Hola {adressee}!

Gracias por registrarte en EduSeñas.

Tu código de verificación es:

====================
{code}
====================

Ingresá este código en la página de verificación.

No compartas este código con nadie.

Si no solicitaste este código, ignorá este correo.

Saludos,
EduSeñas Team
"""
    )

    try:
        api_instance.send_transac_email(email)
        return code

    except ApiException as e:
        raise Exception(
            f"Error al enviar el correo: {e}"
        )


def send_contact_message(
    user_email,
    motivo,
    mensaje
):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    sender = {
        "name": "EduSeñas",
        "email": MAIL_USERNAME
    }

    email = sib_api_v3_sdk.SendSmtpEmail(
        sender=sender,
        to=[{"email": MAIL_USERNAME}],
        reply_to={"email": user_email},
        subject=motivo.upper(),
        text_content=f"""
Nuevo mensaje recibido desde EduSeñas.

MOTIVO:
{motivo}

MAIL DEL USUARIO:
{user_email}

MENSAJE:
{mensaje}
"""
    )

    try:
        api_instance.send_transac_email(email)

    except ApiException as e:
        raise Exception(
            f"Error al enviar el correo: {e}"
        )


def verify_code(
    input_code,
    actual_code
):
    return (
        str(input_code) ==
        str(actual_code)
    )
