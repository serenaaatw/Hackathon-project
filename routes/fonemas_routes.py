from flask import (
Blueprint,
render_template)

from flask_login import login_required
from models.fonemas import Fonema

fonema_bp = Blueprint(
"fonemas",
__name__,
url_prefix="/fonemas"
)


@fonema_bp.route('/')
def fonemas():
    fonemas = Fonema.query.order_by(Fonema.id_fonema).all()

    return render_template(
        'child/fonemas.html',
        fonemas=fonemas
    )