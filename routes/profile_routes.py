from flask import Blueprint

profile = Blueprint("profile", __name__)

@profile.route("/perfil")
def perfil():
    return "Perfil en desarrollo"