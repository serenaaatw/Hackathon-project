from flask import Blueprint

progress = Blueprint("progress", __name__)

@progress.route("/progreso")
def progreso():
    return "Progreso en desarrollo"