from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.user import User
from models.category import Category
from models.progress import Progress
from services.progress_service import ProgressService
from flask_login import login_required

profile = Blueprint("profile", __name__)


@profile.route("/perfil")
@login_required
def perfil():
    # Aceptamos 'usuario_id' que es como lo guardas en AuthService.login()
    user_id = session.get("usuario_id") or session.get("user_id") or session.get("id_user")
    
    if not user_id:
        flash("Debes iniciar sesión para acceder.", "warning")
        return redirect(url_for("auth_routes.login_route"))

    user = User.query.get_or_404(user_id)
    if user.is_tutor():
        return redirect(url_for("profile.perfil_tutor"))
    return render_template("child/profile.html", child=user)



@profile.route("/perfil/tutor")
@login_required
def perfil_tutor():
    # Aceptamos 'usuario_id' aquí también
    user_id = session.get("usuario_id") or session.get("user_id") or session.get("id_user")
    
    if not user_id:
        flash("Debes iniciar sesión para acceder.", "warning")
        return redirect(url_for("auth_routes.login_route"))

    tutor = User.query.get_or_404(user_id)

    if not tutor.is_tutor():
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for("profile.perfil"))

    # 1. Obtener niños asignados y todas las categorías/juegos
    children = tutor.children.all()
    categories = Category.query.all()

    # 2. Estructurar estadísticas por niño
    children_stats = []
    
    for child in children:
        cat_stats = []
        total_porcentajes = 0

        for cat in categories:
            porcentaje = ProgressService.progreso_de_categoria(child.id_user, cat)
            total_porcentajes += porcentaje

            cat_stats.append({
                "category_name": cat.name,
                "percentage": porcentaje
            })

        promedio_general = round(total_porcentajes / len(categories)) if categories else 0
        
        progresos_nino = Progress.query.filter_by(id_user=child.id_user).all()
        words_mastered_count = sum(1 for p in progresos_nino if p.esta_dominada())

        children_stats.append({
            "child": child,
            "promedio_general": promedio_general,
            "words_mastered": words_mastered_count,
            "categories": cat_stats
        })

    return render_template(
        "tutor/profile.html", 
        tutor=tutor, 
        children_stats=children_stats
    )
    