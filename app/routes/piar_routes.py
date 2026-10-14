# ==========================================================
# PIAR ROUTES - SistPROF
# ==========================================================
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

piar_bp = Blueprint("piar", __name__, url_prefix="/piar")


# ════════════════════════════════════════════════════════════════
# DASHBOARD
# ════════════════════════════════════════════════════════════════

@piar_bp.route("/dashboard")
@login_required
def dashboard():
    """Panel principal del Profesional PIAR."""
    if current_user.rol != 'profesional_piar':
        abort(403)

    return render_template("piar/dashboard.html")