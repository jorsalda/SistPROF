from flask_login import login_required, current_user
from flask import Blueprint, render_template, abort, session, redirect, url_for, flash

from app.models.estudiante import Estudiante
from app.models.sede import Sede
from app.models.permiso import Permiso
from app.models.docente import Docente

coordinador_bp = Blueprint(
    "coordinador",
    __name__,
    url_prefix="/coordinador"
)


# 1. DASHBOARD (Solo bienvenida)
@coordinador_bp.route("/")
@login_required
def dashboard():
    if not current_user.es_coordinador:
        abort(403)

    # Por ahora enviamos datos estáticos. Luego conectaremos esto a la BD filtrando por session['sede_actual_id']
    return render_template(
        "coordinador/coordinador_dashboard.html",
        total_docentes=15,
        total_estudiantes=120,
        total_permisos=5,
        total_novedades=2,
        # Las 3 nuevas opciones que pediste:
        total_acudientes=0,
        total_citaciones=0,
        total_observador=0
    )


# 2. SEDES (Aquí van las tarjetas para elegir)
@coordinador_bp.route("/sedes")
@login_required
def sedes():
    sedes = Sede.query.filter_by(colegio_id=current_user.colegio_id).all()
    return render_template("coordinador/sedes.html", sedes=sedes)


# 3. SELECCIONAR SEDE (Guarda en memoria y lleva a Estudiantes)
@coordinador_bp.route("/seleccionar-sede/<int:sede_id>")
@login_required
def seleccionar_sede(sede_id):
    sede = Sede.query.filter_by(id=sede_id, colegio_id=current_user.colegio_id).first()
    if sede:
        session['sede_actual_id'] = sede_id
        flash(f"Has seleccionado la sede: {sede.nombre}", "success")
    # Lo enviamos directo a Estudiantes como usted pidió
    return redirect(url_for('coordinador.estudiantes'))


# 4. DOCENTES (Usa la sede guardada)
@coordinador_bp.route("/docentes")
@login_required
def lista_docentes():
    sede_id = session.get('sede_actual_id')
    if not sede_id:
        flash("Por favor, seleccione una sede primero en el menú 'Sedes'.", "warning")
        return redirect(url_for('coordinador.sedes'))
    docentes = Docente.query.filter_by(sede_id=sede_id).order_by(Docente.nombre).all()
    return render_template("coordinador/docentes.html", docentes=docentes)


# 5. PERMISOS
@coordinador_bp.route("/permisos")
@login_required
def permisos():
    permisos = Permiso.query.filter_by(colegio_id=current_user.colegio_id).order_by(Permiso.fecha_inicio.desc()).all()
    return render_template("coordinador/permisos.html", permisos=permisos)


# 6. ESTUDIANTES (Usa la sede guardada con protección)
@coordinador_bp.route("/estudiantes")
@login_required
def estudiantes():
    sede_id = session.get('sede_actual_id')
    # PROTECCIÓN: Si no hay sede seleccionada, lo regresa a Sedes
    if not sede_id:
        flash("⚠️ Debe seleccionar una sede primero para ver los estudiantes.", "warning")
        return redirect(url_for('coordinador.sedes'))

    estudiantes_lista = Estudiante.query.filter_by(sede_id=sede_id).order_by(Estudiante.nombre).all()

    # Usando la ruta exacta de su carpeta: "estuidantes/estudiantes.html"
    return render_template(
        "estudiantes/estudiante.html",
        estudiantes=estudiantes_lista
    )

# ==========================================================
# RUTAS FALTANTES PARA EL MENÚ DEL COORDINADOR
# ==========================================================

@coordinador_bp.route("/acudientes")
@login_required
def acudientes():
    flash("El módulo de Acudientes está en construcción.", "info")
    return redirect(url_for('coordinador.dashboard'))

@coordinador_bp.route("/observador")
@login_required
def observador():
    flash("El módulo del Observador está en construcción.", "info")
    return redirect(url_for('coordinador.dashboard'))

@coordinador_bp.route("/citaciones")
@login_required
def citaciones():
    flash("El módulo de Citaciones está en construcción.", "info")
    return redirect(url_for('coordinador.dashboard'))

@coordinador_bp.route("/convivencia")
@login_required
def convivencia():
    flash("El módulo de Convivencia está en construcción.", "info")
    return redirect(url_for('coordinador.dashboard'))

@coordinador_bp.route("/seguimiento")
@login_required
def seguimiento():
    flash("El módulo de Seguimiento Académico está en construcción.", "info")
    return redirect(url_for('coordinador.dashboard'))

@coordinador_bp.route("/piar")
@login_required
def piar():
    flash("El módulo de PIAR está en construcción.", "info")
    return redirect(url_for('coordinador.dashboard'))

