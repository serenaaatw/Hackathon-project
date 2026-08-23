from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.user import User

profile = Blueprint("profile", __name__)

@profile.route("/perfil")
def perfil():
    user_id = session.get("user_id")
    if not user_id:
        flash("Debes iniciar sesión para ver tu perfil.", "warning")
        return redirect(url_for("auth_routes.login_route"))

    child = User.query.get_or_404(user_id)
    return render_template("child/profile.html", child=child)