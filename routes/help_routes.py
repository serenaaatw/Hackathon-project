from flask import (
Blueprint,
render_template)

from flask_login import login_required

help_bp = Blueprint(
"help",
__name__,
url_prefix="/ayuda"
)


@help_bp.route("/")
@login_required
def ayuda():
    return render_template("help.html")

