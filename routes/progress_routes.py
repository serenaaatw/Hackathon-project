from flask import Blueprint, render_template, session, redirect, url_for

from services.progress_service import ProgressService

progress_routes = Blueprint(
    "progress",
    __name__,
    url_prefix="/progreso"
)


@progress_routes.route("/")
def progreso():

    id_user = session.get("usuario_id")

    if id_user is None:
        return redirect(url_for("auth.login"))

    datos = ProgressService.obtener_progreso_usuario(
        id_user
    )

    return render_template(
        "progreso.html",
        datos=datos
    )