from flask import request, render_template, redirect, session, url_for
from models.user import User
from models.db import db
from email_validator import validate_email, EmailNotValidError
from utils.email_services import send_verification_code, verify_code
from flask_login import login_user, logout_user


class AuthService:

    @staticmethod
    def register():

        if request.method == "GET":

            session.pop("verification_code", None)
            session.pop("pending_user", None)
            session.pop("email", None)
            session.pop("verification_purpose", None)

            return render_template("register.html")

        try:

            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]
            username = request.form["username"]
            last_name = request.form["last_name"]
            rol = request.form["rol"]

            try:

                validate_email(email)

            except EmailNotValidError:

                raise ValueError(
                    "El correo ingresado no es válido"
                )

            existing_user = User.query.filter_by(
                email=email
            ).first()

            existing_username = User.query.filter_by(
                username=username
            ).first()

            if existing_username:

                raise ValueError(
                    "Nombre de usuario ya registrado"
                )

            if existing_user:

                raise ValueError(
                    "Usuario ya registrado"
                )

            if len(password) < 8:

                raise ValueError(
                    "La contraseña debe tener al menos 8 caracteres"
                )

            code = send_verification_code(email)

            session["verification_code"] = str(code)
            session["email"] = email
            session["verification_purpose"] = "register"

            session["pending_user"] = {
                "name": name,
                "last_name": last_name,
                "email": email,
                "username": username,
                "password": password,
                "rol": rol
            }

            return redirect(
                url_for(
                    "auth_routes.verify_email_route"
                )
            )

        except Exception as error:

            return render_template(
                "register.html",
                error=str(error)
            )


    @staticmethod
    def create_user():

        data = session["pending_user"]

        new_user = User(
            name=data["name"],
            last_name=data["last_name"],
            email=data["email"],
            username=data["username"],
            password="",
            profile_picture="img/user/user.png",
            rol=data["rol"]
        )

        new_user.set_password(
            data["password"]
        )

        db.session.add(new_user)
        db.session.commit()

        session.pop(
            "pending_user",
            None
        )

        session.pop(
            "verification_code",
            None
        )

        return redirect(
            url_for(
                "auth_routes.login_route"
            )
        )


    @staticmethod
    def login():

        if request.method == "GET":

            session.pop(
                "usuario_id",
                None
            )

            session.pop(
                "email",
                None
            )

            return render_template(
                "login.html"
            )

        try:

            email_or_username = request.form[
                "username or email"
            ]

            password = request.form[
                "password"
            ]

            user = User.query.filter_by(
                email=email_or_username
            ).first()

            if not user:

                user = User.query.filter_by(
                    username=email_or_username
                ).first()

            if not user:

                raise ValueError(
                    "Usuario no existente"
                )

            if not user.check_password(
                password
            ):

                raise ValueError(
                    "Contraseña incorrecta"
                )

            login_user(user)

            session["usuario_id"] = user.id_user

            if not user.video_visto:

                return redirect(
                    url_for(
                        "informative_routes.video_informativo"
                    )
                )

            return redirect(
                url_for(
                    "menu_principal.mostrar_menu"
                )
            )

        except Exception as error:

            return render_template(
                "login.html",
                error=str(error)
            )


    @staticmethod
    def logout():

        logout_user()

        session.clear()

        return redirect(
            url_for(
                "auth_routes.login_route"
            )
        )


    @staticmethod
    def recover_password():

        if request.method == "GET":

            session.pop(
                "verification_purpose",
                None
            )

            return render_template(
                "recover_password.html"
            )

        try:

            if not session.get("email"):

                email = request.form.get(
                    "email"
                )

                try:

                    validate_email(email)

                except EmailNotValidError:

                    raise ValueError(
                        "El correo ingresado no es válido"
                    )

                if not User.query.filter_by(
                    email=email
                ).first():

                    raise ValueError(
                        "El correo electrónico no está registrado."
                    )

                session["email"] = email

            else:

                email = session.get(
                    "email"
                )

            session[
                "verification_purpose"
            ] = "recover_password"

            if not email:

                raise ValueError(
                    "La sesión expiró. Volvé a iniciar el proceso de recuperación de contraseña."
                )

            code = send_verification_code(
                email
            )

            session[
                "verification_code"
            ] = str(code)

            return redirect(
                url_for(
                    "auth_routes.verify_email_route"
                )
            )

        except Exception as error:

            return render_template(
                "recover_password.html",
                error=str(error)
            )


    @staticmethod
    def reset_password():

        if request.method == "GET":

            return render_template(
                "reset_password.html"
            )

        try:

            new_password = request.form[
                "new_password"
            ]

            confirm_password = request.form[
                "confirm_password"
            ]

            if new_password != confirm_password:

                raise ValueError(
                    "Las contraseñas no coinciden"
                )

            if len(new_password) < 8:

                raise ValueError(
                    "La contraseña debe tener al menos 8 caracteres"
                )

            email = session.get(
                "email"
            )

            user = User.query.filter_by(
                email=email
            ).first()

            if not user:

                raise ValueError(
                    "Usuario no existente"
                )

            user.set_password(
                new_password
            )

            db.session.commit()

            session.pop(
                "email",
                None
            )

            session.pop(
                "verification_code",
                None
            )

            return redirect(
                url_for(
                    "auth_routes.login_route"
                )
            )

        except Exception as error:

            return render_template(
                "reset_password.html",
                error=str(error)
            )


    @staticmethod
    def editar_perfil():

        from flask_login import current_user

        if not current_user.is_authenticated:

            return redirect(
                url_for(
                    "auth_routes.login_route"
                )
            )

        if request.method == "GET":

            return render_template(
                "editar_perfil.html",
                child=current_user
            )

        try:

            foto = request.files.get(
                "profile_picture"
            )

            if not foto or not foto.filename:

                raise ValueError(
                    "Seleccioná una imagen."
                )

            allowed_extensions = {
                "jpg",
                "jpeg",
                "png",
                "gif",
                "webp"
            }

            extension = (
                foto.filename
                .rsplit(".", 1)[-1]
                .lower()
            )

            if extension not in allowed_extensions:

                raise ValueError(
                    "El formato de imagen no es válido."
                )

            import os
            import uuid

            filename = (
                str(uuid.uuid4())
                + "."
                + extension
            )

            upload_folder = os.path.join(
                "static",
                "img",
                "user"
            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            filepath = os.path.join(
                upload_folder,
                filename
            )

            foto.save(filepath)

            current_user.profile_picture = (
                "img/user/" + filename
            )

            db.session.commit()

            return redirect(
                url_for(
                    "profile.perfil"
                )
            )

        except Exception as error:

            return render_template(
                "editar_perfil.html",
                child=current_user,
                error=str(error)
            )