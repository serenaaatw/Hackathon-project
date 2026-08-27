from flask import Blueprint, render_template
menu_principal = Blueprint('menu_principal', __name__)

@menu_principal.route('/menu')
def mostrar_menu():
    return render_template('menu_principal.html')