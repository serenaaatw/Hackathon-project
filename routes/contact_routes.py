from flask import Blueprint, render_template, request

contact = Blueprint("contact", __name__)


@contact.route("/contactanos", methods=["GET", "POST"])
def contactanos():

    if request.method == "POST":

        motivo = request.form.get("motivo")
        correo = request.form.get("correo")
        mensaje = request.form.get("mensaje")

        
        print("MOTIVO:", motivo)
        print("CORREO:", correo)
        print("MENSAJE:", mensaje)

        return render_template("contacto_exitoso.html")

    return render_template("contactanos.html")