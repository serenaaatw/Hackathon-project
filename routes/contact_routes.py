from flask import Blueprint

contact = Blueprint("contact", __name__)

@contact.route("/contactanos")
def contactanos():
    return "Contáctanos en desarrollo"