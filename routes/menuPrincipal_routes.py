from flask import Blueprint, render_template
from flask_login import login_required

menu_principal = Blueprint('menu_principal', __name__)


@menu_principal.route('/menu')
@login_required
def mostrar_menu():
    return render_template('menu_principal.html')