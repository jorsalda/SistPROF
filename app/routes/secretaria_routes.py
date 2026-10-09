# ==========================================================
# SECRETARIA ROUTES - SistPROF
# ==========================================================
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

from app.models.docente import Docente
from app.models.estudiante import Estudiante
from app.models.acudiente import Acudiente
from app.models.coordinador import Coordinador

secretaria_bp = Blueprint("secretaria", __name__, url_prefix="/secretaria")


@secretaria_bp.route("/dashboard")
@login_required
def dashboard():
    """Panel principal de la secretaría."""
    if current_user.rol != 'secretaria':
        abort(403)

    colegio_id = current_user.colegio_id

    total_docentes = Docente.query.filter_by(
        colegio_id=colegio_id, activo=True
    ).count()

    total_estudiantes = Estudiante.query.filter_by(
        colegio_id=colegio_id, activo=True
    ).count()

    total_acudientes = Acudiente.query.filter_by(
        colegio_id=colegio_id
    ).count()

    total_coordinadores = Coordinador.query.filter_by(
        colegio_id=colegio_id
    ).count()

    return render_template(
        "secretaria/dashboard.html",
        total_docentes=total_docentes,
        total_estudiantes=total_estudiantes,
        total_acudientes=total_acudientes,
        total_coordinadores=total_coordinadores,
    )