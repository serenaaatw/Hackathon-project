from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from services.auth_services import AuthService
from utils.email_services import verify_code

auth_bp = Blueprint("auth_routes", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register_route():
    return AuthService.register()

@auth_bp.route("/login", methods=["GET", "POST"])
def login_route():
    return AuthService.login()

@auth_bp.route("/logout")
def logout_route():
    return AuthService.logout()

@auth_bp.route("/verify_email", methods=["GET", "POST"])
def verify_email_route():
    if request.method == "GET":
        return render_template("verify_email.html")

    input_code = request.form.get("verification_code")
    actual_code = session.get("verification_code")

    if actual_code is None:
        return render_template(
            "verify_email.html",
            error="La sesión expiró. Volvé a registrarte."
        )

    if verify_code(input_code, actual_code):
        if session.get("verification_purpose") == "register":
            return AuthService.create_user()
        elif session.get("verification_purpose") == "recover_password":
            return redirect(url_for("auth_routes.reset_password_route"))

    return render_template(
        "verify_email.html",
        error="El código de verificación es incorrecto."
    )

@auth_bp.route("/recover_password", methods=["GET", "POST"])
def recover_password_route():
    return AuthService.recover_password()

@auth_bp.route("/reset_password", methods=["GET", "POST"])
def reset_password_route():
    return AuthService.reset_password()