from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from datetime import datetime

from app.extensions import db
from app.models.colegio import Colegio
from app.models.docente import Docente
from app.models.permiso import Permiso
from app.models.sede import Sede
from app.models.estudiante import Estudiante
from app.models.jornada import Jornada


colegio_bp = Blueprint(
    "colegio",
    __name__,
    url_prefix="/dashboard"
)


# ==========================================================
# DASHBOARD PRINCIPAL
# ==========================================================

@colegio_bp.route("/")
@login_required
def dashboard():

    if current_user.is_superadmin:
        return redirect(url_for("admin.dashboard"))

    colegio = Colegio.query.get_or_404(
        current_user.colegio_id
    )

    hoy = datetime.utcnow().date()

    total_sedes = Sede.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).count()

    total_jornadas = Jornada.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).count()

    total_docentes = Docente.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).count()

    total_estudiantes = Estudiante.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).count()

    total_permisos = Permiso.query.filter_by(
        colegio_id=current_user.colegio_id
    ).count()

    permisos_activos = Permiso.query.filter(
        Permiso.colegio_id == current_user.colegio_id,
        Permiso.fecha_inicio <= hoy,
        Permiso.fecha_fin >= hoy
    ).count()

    permisos_pendientes = Permiso.query.filter(
        Permiso.colegio_id == current_user.colegio_id,
        Permiso.fecha_inicio > hoy
    ).count()

    ultimos_permisos = Permiso.query.filter_by(
        colegio_id=current_user.colegio_id
    ).order_by(
        Permiso.fecha_inicio.desc()
    ).limit(5).all()

    return render_template(
        "colegio/dashboard.html",
        colegio=colegio,
        total_sedes=total_sedes,
        total_jornadas=total_jornadas,
        total_docentes=total_docentes,
        total_estudiantes=total_estudiantes,
        total_permisos=total_permisos,
        permisos_activos=permisos_activos,
        permisos_pendientes=permisos_pendientes,
        ultimos_permisos=ultimos_permisos,
        hoy=hoy
    )


# ==========================================================
# SEDES
# ==========================================================

@colegio_bp.route("/sedes")
@login_required
def sedes():

    colegio = Colegio.query.get_or_404(
        current_user.colegio_id
    )

    sedes = colegio.sedes

    return render_template(
        "colegio/sedes.html",
        colegio=colegio,
        sedes=sedes
    )


@colegio_bp.route("/sedes/nueva", methods=["GET", "POST"])
@login_required
def nueva_sede():

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()
        direccion = request.form.get("direccion", "").strip()
        telefono = request.form.get("telefono", "").strip()
        activo = request.form.get("activo") == "on"

        if not nombre:
            flash(
                "El nombre de la sede es obligatorio",
                "danger"
            )
            return redirect(url_for("colegio.nueva_sede"))

        existe = Sede.query.filter_by(
            nombre=nombre,
            colegio_id=current_user.colegio_id
        ).first()

        if existe:
            flash(
                "Ya existe una sede con ese nombre",
                "warning"
            )
            return redirect(url_for("colegio.nueva_sede"))

        sede = Sede(
            nombre=nombre,
            direccion=direccion if direccion else None,
            telefono=telefono if telefono else None,
            activo=activo,
            colegio_id=current_user.colegio_id
        )

        db.session.add(sede)
        db.session.commit()

        flash(
            "Sede registrada correctamente",
            "success"
        )

        return redirect(url_for("colegio.sedes"))

    return render_template(
        "colegio/formulario_sede.html"
    )


@colegio_bp.route("/sedes/<int:sede_id>")
@login_required
def detalle_sede(sede_id):

    sede = Sede.query.filter_by(
        id=sede_id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    return render_template(
        "colegio/detalle_sede.html",
        sede=sede
    )


@colegio_bp.route("/sedes/<int:sede_id>/editar", methods=["GET", "POST"])
@login_required
def editar_sede(sede_id):

    sede = Sede.query.filter_by(
        id=sede_id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    if request.method == "POST":

        sede.nombre = request.form.get("nombre")
        sede.direccion = request.form.get("direccion")
        sede.telefono = request.form.get("telefono")
        sede.activo = request.form.get("activo") == "on"

        db.session.commit()

        flash(
            "Sede actualizada correctamente",
            "success"
        )

        return redirect(
            url_for(
                "colegio.detalle_sede",
                sede_id=sede.id
            )
        )

    return render_template(
        "colegio/formulario_sede.html",
        sede=sede
    )


# ==========================================================
# JORNADAS
# ==========================================================

@colegio_bp.route("/sedes/<int:sede_id>/jornadas")
@login_required
def jornadas_sede(sede_id):

    sede = Sede.query.filter_by(
        id=sede_id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    jornadas = sede.jornadas

    return render_template(
        "colegio/jornadas_sede.html",
        sede=sede,
        jornadas=jornadas
    )


@colegio_bp.route(
    "/sedes/<int:sede_id>/jornadas/nueva",
    methods=["GET", "POST"]
)
@login_required
def nueva_jornada(sede_id):

    sede = Sede.query.filter_by(
        id=sede_id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    if request.method == "POST":

        nombre = request.form.get("nombre")
        hora_inicio = request.form.get("hora_inicio")
        hora_fin = request.form.get("hora_fin")
        tolerancia_minutos = request.form.get(
            "tolerancia_minutos",
            0
        )

        jornada = Jornada(
            nombre=nombre,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            tolerancia_minutos=tolerancia_minutos,
            sede_id=sede.id,
            colegio_id=current_user.colegio_id,
            activo=True
        )

        db.session.add(jornada)
        db.session.commit()

        flash(
            "Jornada registrada correctamente",
            "success"
        )

        return redirect(
            url_for(
                "colegio.jornadas_sede",
                sede_id=sede.id
            )
        )

    return render_template(
        "colegio/formulario_jornada.html",
        sede=sede
    )


# ==========================================================
# DOCENTES
# ==========================================================

@colegio_bp.route("/docentes")
@login_required
def lista_docentes():

    docentes = Docente.query.filter_by(
        colegio_id=current_user.colegio_id
    ).order_by(
        Docente.nombre
    ).all()

    return render_template(
        "colegio/docentes.html",
        docentes=docentes
    )


@colegio_bp.route("/docentes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_docente():

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()
        documento = request.form.get("documento", "").strip()
        telefono = request.form.get("telefono", "").strip()
        email = request.form.get("email", "").strip()

        if not nombre:
            flash(
                "El nombre del docente es requerido",
                "danger"
            )
            return redirect(
                url_for("colegio.nuevo_docente")
            )

        existe = Docente.query.filter_by(
            nombre=nombre,
            colegio_id=current_user.colegio_id
        ).first()

        if existe:
            flash(
                "Este docente ya está registrado",
                "warning"
            )
            return redirect(
                url_for("colegio.nuevo_docente")
            )

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

        flash(
            f"Docente '{nombre}' registrado correctamente",
            "success"
        )

        return redirect(
            url_for("colegio.lista_docentes")
        )

    return render_template(
        "colegio/formulario_docente.html",
        docente=None,
        titulo="Nuevo Docente"
    )


@colegio_bp.route("/docentes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_docente(id):

    docente = Docente.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    if request.method == "POST":

        docente.nombre = request.form.get("nombre")
        docente.documento = request.form.get("documento")
        docente.telefono = request.form.get("telefono")
        docente.email = request.form.get("email")
        docente.activo = request.form.get("activo") == "on"

        db.session.commit()

        flash(
            "Docente actualizado correctamente",
            "success"
        )

        return redirect(
            url_for("colegio.lista_docentes")
        )

    return render_template(
        "colegio/formulario_docente.html",
        docente=docente,
        titulo="Editar Docente"
    )


@colegio_bp.route("/docentes/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_docente(id):

    docente = Docente.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    tiene_permisos = Permiso.query.filter_by(
        docente_id=id
    ).first()

    if tiene_permisos:
        docente.activo = False
        db.session.commit()

        flash(
            "Docente desactivado (tiene permisos asociados)",
            "warning"
        )
    else:
        db.session.delete(docente)
        db.session.commit()

        flash(
            "Docente eliminado correctamente",
            "success"
        )

    return redirect(
        url_for("colegio.lista_docentes")
    )


# ==========================================================
# PERMISOS
# ==========================================================

@colegio_bp.route("/permisos")
@login_required
def lista_permisos():

    permisos = Permiso.query.filter_by(
        colegio_id=current_user.colegio_id
    ).order_by(
        Permiso.fecha_inicio.desc()
    ).all()

    hoy = datetime.utcnow().date()

    return render_template(
        "colegio/permisos.html",
        permisos=permisos,
        hoy=hoy
    )


@colegio_bp.route("/docentes/<int:docente_id>/permisos")
@login_required
def permisos_docente(docente_id):

    docente = Docente.query.filter_by(
        id=docente_id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    permisos = Permiso.query.filter_by(
        docente_id=docente_id,
        colegio_id=current_user.colegio_id
    ).order_by(
        Permiso.fecha_inicio.desc()
    ).all()

    hoy = datetime.utcnow().date()

    return render_template(
        "colegio/permisos_docente.html",
        docente=docente,
        permisos=permisos,
        hoy=hoy
    )


@colegio_bp.route("/permisos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_permiso():

    docentes = Docente.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).all()

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

        flash(
            "Permiso registrado correctamente",
            "success"
        )

        return redirect(
            url_for("colegio.lista_permisos")
        )

    return render_template(
        "colegio/formulario_permiso.html",
        docentes=docentes
    )


@colegio_bp.route("/permisos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_permiso(id):

    permiso = Permiso.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    db.session.delete(permiso)
    db.session.commit()

    flash(
        "Permiso eliminado correctamente",
        "success"
    )

    return redirect(
        url_for("colegio.lista_permisos")
    )