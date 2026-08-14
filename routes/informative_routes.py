from flask import Blueprint, render_template, redirect, url_for, session
from models.user import User
from models.db import db

informative_bp = Blueprint("informative_routes", __name__)


@informative_bp.route("/video-informativo")
def video_informativo():

    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return redirect(url_for("auth_routes.login_route"))

    user = User.query.get(usuario_id)

    if not user:
        session.clear()
        return redirect(url_for("auth_routes.login_route"))

    if user.video_visto:
        return redirect(url_for("home.home_route"))

    return render_template("video_informativo.html")


@informative_bp.route("/video-informativo/completar", methods=["POST"])
def completar_video():

    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return redirect(url_for("auth_routes.login_route"))

    user = User.query.get(usuario_id)

    if not user:
        session.clear()
        return redirect(url_for("auth_routes.login_route"))

    user.video_visto = True
    db.session.commit()

    return redirect(url_for("home.home_route"))