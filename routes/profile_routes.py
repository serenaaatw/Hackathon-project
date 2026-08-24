from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.user import User

profile = Blueprint("profile", __name__)

@profile.route("/perfil")
def perfil():
    user_id = session.get("user_id")
    if not user_id:
        flash("Debes iniciar sesión para acceder.", "warning")
        return redirect(url_for("auth_routes.login_route"))

    user = User.query.get_or_404(user_id)
    if user.is_tutor():
        return redirect(url_for("profile.perfil_tutor"))
    return render_template("child/profile.html", child=user)

@profile.route("/perfil/tutor")
def perfil_tutor():
    user_id = session.get("user_id")
    if not user_id:
        flash("Debes iniciar sesión para acceder.", "warning")
        return redirect(url_for("auth_routes.login_route"))

    tutor = User.query.get_or_404(user_id)

    # Control de acceso: Si un niño intenta acceder, lo enviamos a su perfil
    if not tutor.is_tutor():
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for("profile.perfil"))

    # Obtenemos la lista de niños asignados usando la relación del modelo
    children = tutor.children.all()

    return render_template("tutor/profile.html", tutor=tutor, children=children)