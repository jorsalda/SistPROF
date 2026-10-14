# ==========================================================
# PSICOLOGO ROUTES - SistPROF
# ==========================================================
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

psicologo_bp = Blueprint("psicologo", __name__, url_prefix="/psicologo")


# ════════════════════════════════════════════════════════════════
# DASHBOARD
# ════════════════════════════════════════════════════════════════

@psicologo_bp.route("/dashboard")
@login_required
def dashboard():
    """Panel principal del Psicólogo."""
    if current_user.rol != 'psicologo':
        abort(403)

    return render_template("psicologo/dashboard.html")