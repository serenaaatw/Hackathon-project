from flask import (
Blueprint,
render_template)

help_bp = Blueprint(
"help",
__name__,
url_prefix="/ayuda"
)

@help_bp.route("/")
def ayuda():
    return render_template("help.html")

