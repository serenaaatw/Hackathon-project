import smtplib
from email.message import EmailMessage
import random
import os

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

def send_verification_code(adressee):
    code = random.randint(100000, 999999)

    msg = EmailMessage()

    msg["Subject"] = "Código de verificación"

    msg["From"] = MAIL_USERNAME

    msg["To"] = adressee

    msg.set_content(f"""

<<<<<<< HEAD
Gracias por registrarte en EduSeñas.
=======
>>>>>>> feature/Contacto

    Hola {adressee}!

    Gracias por registrarte en EduSeñas.

    Tu código de verificación es:

    ====================
    {code}
    ======

    Ingresá este código en la página de verificación.

    No compartas este código con nadie.

    Si no solicitaste este código, ignorá este correo.

    Saludos,
    EduSeñas Team
    """)


<<<<<<< HEAD
Saludos, Team EduSeñas
""")
    
    
=======
>>>>>>> feature/Contacto
    try:

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as server:

            server.login(
                MAIL_USERNAME,
                MAIL_PASSWORD
            )

            server.send_message(msg)

        return code

    except Exception as e:

        raise Exception(
            f"Error al enviar el correo: {e}"
        )


def send_contact_message(
user_email,
motivo,
mensaje
):

    msg = EmailMessage()

    msg["Subject"] = (
        f"{motivo.upper()}"
    )

    msg["From"] = MAIL_USERNAME

    msg["To"] = MAIL_USERNAME

    msg["Reply-To"] = user_email

    msg.set_content(f"""


    Nuevo mensaje recibido desde EduSeñas.

    MOTIVO:
    {motivo}

    MAIL DEL USUARIO:
    {user_email}

    MENSAJE:
    {mensaje}
    """)

    try:

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as server:

            server.login(
                MAIL_USERNAME,
                MAIL_PASSWORD
            )

            server.send_message(msg)

    except Exception as e:

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

