from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.docente import Docente
from app.models.permiso import Permiso
from app.extensions import db
from datetime import datetime

colegio_bp = Blueprint("colegio", __name__, url_prefix="/dashboard")


@colegio_bp.route("/")
@login_required
def dashboard():
    """Dashboard específico para el colegio del usuario actual"""

    # Verificar si es superadmin (redirigir al dashboard global)
    if current_user.is_superadmin:
        return redirect(url_for('admin.dashboard'))

    # Estadísticas específicas del colegio
    total_docentes = Docente.query.filter_by(
        colegio_id=current_user.colegio_id
    ).count()

    total_permisos = Permiso.query.filter_by(
        colegio_id=current_user.colegio_id
    ).count()

    # Permisos activos (hoy está entre fecha_inicio y fecha_fin)
    hoy = datetime.utcnow().date()
    permisos_activos = Permiso.query.filter(
        Permiso.colegio_id == current_user.colegio_id,
        Permiso.fecha_inicio <= hoy,
        Permiso.fecha_fin >= hoy
    ).count()

    # Permisos pendientes (fecha_inicio > hoy)
    permisos_pendientes = Permiso.query.filter(
        Permiso.colegio_id == current_user.colegio_id,
        Permiso.fecha_inicio > hoy
    ).count()

    # Docentes activos
    docentes_activos = Docente.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).count()

    # Últimos 5 permisos
    ultimos_permisos = Permiso.query.filter_by(
        colegio_id=current_user.colegio_id
    ).order_by(Permiso.fecha_inicio.desc()).limit(5).all()

    return render_template(
        "colegio/dashboard.html",
        total_docentes=total_docentes,
        total_permisos=total_permisos,
        permisos_activos=permisos_activos,
        permisos_pendientes=permisos_pendientes,
        docentes_activos=docentes_activos,
        ultimos_permisos=ultimos_permisos,
        hoy=hoy
    )


# ════════════════════════════════════════════════════════════════
# LISTADO DE DOCENTES DENTRO DEL DASHBOARD
# ════════════════════════════════════════════════════════════════

@colegio_bp.route("/docentes")
@login_required
def lista_docentes():
    """Lista de docentes del colegio actual (dentro del dashboard)"""
    docentes = Docente.query.filter_by(
        colegio_id=current_user.colegio_id
    ).order_by(Docente.nombre).all()

    return render_template("colegio/docentes.html", docentes=docentes)


# ════════════════════════════════════════════════════════════════
# NUEVO DOCENTE DENTRO DEL DASHBOARD
# ════════════════════════════════════════════════════════════════

@colegio_bp.route("/docentes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_docente():
    """Registrar nuevo docente (dentro del dashboard)"""
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        documento = request.form.get("documento", "").strip()
        telefono = request.form.get("telefono", "").strip()
        email = request.form.get("email", "").strip()

        if not nombre:
            flash("El nombre del docente es requerido", "danger")
            return redirect(url_for("colegio.nuevo_docente"))

        # Verificar si ya existe
        existe = Docente.query.filter_by(
            nombre=nombre,
            colegio_id=current_user.colegio_id
        ).first()

        if existe:
            flash("Este docente ya está registrado", "warning")
            return redirect(url_for("colegio.nuevo_docente"))

        # Crear docente
        docente = Docente(
            nombre=nombre,
            documento=documento if documento else None,
            telefono=telefono if telefono else None,
            email=email if email else None,
            colegio_id=current_user.colegio_id,
            activo=True
        )

        db.session.add(docente)
        db.session.commit()

        flash(f"Docente '{nombre}' registrado correctamente", "success")
        return redirect(url_for("colegio.lista_docentes"))

    return render_template("colegio/formulario_docente.html", docente=None, titulo="Nuevo Docente")


# ════════════════════════════════════════════════════════════════
# EDITAR DOCENTE DENTRO DEL DASHBOARD
# ════════════════════════════════════════════════════════════════

@colegio_bp.route("/docentes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_docente(id):
    """Editar docente (dentro del dashboard)"""
    docente = Docente.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        documento = request.form.get("documento", "").strip()
        telefono = request.form.get("telefono", "").strip()
        email = request.form.get("email", "").strip()
        activo = request.form.get("activo") == "on"

        if not nombre:
            flash("El nombre del docente es requerido", "danger")
            return redirect(url_for("colegio.editar_docente", id=id))

        # Verificar si el nombre ya existe (excluyendo este docente)
        existe = Docente.query.filter(
            Docente.nombre == nombre,
            Docente.colegio_id == current_user.colegio_id,
            Docente.id != id
        ).first()

        if existe:
            flash("Ya existe otro docente con ese nombre", "warning")
            return redirect(url_for("colegio.editar_docente", id=id))

        # Actualizar
        docente.nombre = nombre
        docente.documento = documento if documento else None
        docente.telefono = telefono if telefono else None
        docente.email = email if email else None
        docente.activo = activo

        db.session.commit()

        flash(f"Docente '{nombre}' actualizado correctamente", "success")
        return redirect(url_for("colegio.lista_docentes"))

    return render_template("colegio/formulario_docente.html", docente=docente, titulo="Editar Docente")


# ════════════════════════════════════════════════════════════════
# ELIMINAR DOCENTE DENTRO DEL DASHBOARD
# ════════════════════════════════════════════════════════════════

@colegio_bp.route("/docentes/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_docente(id):
    """Eliminar docente (dentro del dashboard)"""
    docente = Docente.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    nombre = docente.nombre

    # Verificar si tiene permisos asociados
    tiene_permisos = Permiso.query.filter_by(docente_id=id).first()

    if tiene_permisos:
        # No eliminar, marcar como inactivo
        docente.activo = False
        db.session.commit()
        flash(f"Docente '{nombre}' desactivado (tiene permisos asociados)", "warning")
    else:
        # Eliminar permanentemente
        db.session.delete(docente)
        db.session.commit()
        flash(f"Docente '{nombre}' eliminado permanentemente", "success")

    return redirect(url_for("colegio.lista_docentes"))


# ════════════════════════════════════════════════════════════════
# LISTADO DE PERMISOS DENTRO DEL DASHBOARD
# ════════════════════════════════════════════════════════════════

@colegio_bp.route("/permisos")
@login_required
def lista_permisos():
    """Lista de permisos del colegio actual (dentro del dashboard)"""
    permisos = Permiso.query.filter_by(
        colegio_id=current_user.colegio_id
    ).order_by(Permiso.fecha_inicio.desc()).all()

    hoy = datetime.utcnow().date()

    return render_template("colegio/permisos.html", permisos=permisos, hoy=hoy)

# ════════════════════════════════════════════════════════════════
# PERMISOS DE UN DOCENTE ESPECÍFICO
# ════════════════════════════════════════════════════════════════

@colegio_bp.route("/docentes/<int:docente_id>/permisos")
@login_required
def permisos_docente(docente_id):
    """Lista de permisos de un docente específico (dentro del dashboard)"""
    docente = Docente.query.filter_by(
        id=docente_id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    permisos = Permiso.query.filter_by(
        docente_id=docente_id,
        colegio_id=current_user.colegio_id
    ).order_by(Permiso.fecha_inicio.desc()).all()

    hoy = datetime.utcnow().date()

    return render_template(
        "colegio/permisos_docente.html",
        docente=docente,
        permisos=permisos,
        hoy=hoy
    )
# ════════════════════════════════════════════════════════════════
# NUEVO PERMISO DENTRO DEL DASHBOARD
# ════════════════════════════════════════════════════════════════

@colegio_bp.route("/permisos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_permiso():
    """Registrar nuevo permiso (dentro del dashboard)"""
    docentes = Docente.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).all()

    # Obtener todos los permisos del colegio para mostrar historial
    # Convertir a formato serializable para JSON
    permisos_query = Permiso.query.filter_by(
        colegio_id=current_user.colegio_id
    ).order_by(Permiso.fecha_inicio.desc()).all()

    # Serializar permisos manualmente
    todos_permisos = []
    for permiso in permisos_query:
        todos_permisos.append({
            'id': permiso.id,
            'docente_id': permiso.docente_id,
            'tipo': permiso.tipo,
            'fecha_inicio': permiso.fecha_inicio.isoformat() if permiso.fecha_inicio else None,
            'fecha_fin': permiso.fecha_fin.isoformat() if permiso.fecha_fin else None,
            'observacion': permiso.observacion
        })

    hoy = datetime.utcnow().date()

    if request.method == "POST":
        permiso = Permiso(
            docente_id=request.form.get("docente_id"),
            fecha_inicio=request.form.get("fecha_inicio"),
            fecha_fin=request.form.get("fecha_fin"),
            tipo=request.form.get("tipo"),
            observacion=request.form.get("observacion"),
            colegio_id=current_user.colegio_id
        )

        db.session.add(permiso)
        db.session.commit()

        flash("Permiso registrado correctamente", "success")
        return redirect(url_for("colegio.lista_permisos"))

    return render_template(
        "colegio/formulario_permiso.html",
        docentes=docentes,
        todos_permisos=todos_permisos,
        hoy=hoy
    )

# ════════════════════════════════════════════════════════════════
# ELIMINAR PERMISO DENTRO DEL DASHBOARD
# ════════════════════════════════════════════════════════════════

@colegio_bp.route("/permisos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_permiso(id):
    """Eliminar permiso (dentro del dashboard)"""
    permiso = Permiso.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    docente_nombre = permiso.docente.nombre
    db.session.delete(permiso)
    db.session.commit()

    flash(f"Permiso de {docente_nombre} eliminado correctamente", "success")
    return redirect(url_for("colegio.lista_permisos"))