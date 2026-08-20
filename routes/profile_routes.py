from flask import Blueprint,render_template,session,redirect,url_for,flash
from models.user import User

profile = Blueprint("profile", __name__)

@profile.route("/perfil")
def perfil():
    user_id=session.get("user_id")#obtener los usuarios
    if not user_id:
        flash("Debe iniciar sesión para ver tu perfil.", "peligro")
        return redirect(url_for("auth.login"))
#buscar los datos del perfil del niño
    child=User.query.get_or_404(user_id)
    return render_template("child/profile.html", child=child)