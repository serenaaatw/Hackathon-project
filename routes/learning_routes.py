from flask import Blueprint

learning = Blueprint("learning", __name__)

@learning.route("/aprendizaje")
def aprendizaje():
    return "Aprendizaje en desarrollo"