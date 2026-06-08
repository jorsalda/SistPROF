from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions import db
from app.models.docente import Docente
from app.models.permiso import Permiso
from app.models.estudiante import Estudiante

docente_bp = Blueprint("docente", __name__, url_prefix="/docentes")


# ==========================================================
# DASHBOARD DEL DOCENTE (NUEVO - PARA DOCENTE LOGUEADO)
# ==========================================================

@docente_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.rol != 'docente':
        abort(403)

    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    if not docente:
        flash("No se encontró información del docente", "danger")
        return redirect(url_for("auth.logout"))

    hoy = datetime.now().date()

    total_estudiantes = Estudiante.query.filter_by(
        docente_id=docente.id,
        activo=True
    ).count()

    total_permisos = Permiso.query.filter_by(
        docente_id=docente.id
    ).count()

    permisos_activos = Permiso.query.filter(
        Permiso.docente_id == docente.id,
        Permiso.fecha_inicio <= hoy,
        Permiso.fecha_fin >= hoy
    ).count()

    # ✅ NUEVO: Obtener últimos 5 permisos
    ultimos_permisos = Permiso.query.filter_by(
        docente_id=docente.id
    ).order_by(Permiso.fecha_inicio.desc()).limit(5).all()

    return render_template(
        "docentes/dashboard.html",
        docente=docente,
        total_estudiantes=total_estudiantes,
        total_permisos=total_permisos,
        permisos_activos=permisos_activos,
        ultimos_permisos=ultimos_permisos,  # ← NUEVO
        hoy=hoy
    )


@docente_bp.route("/mis-estudiantes")
@login_required
def mis_estudiantes():
    if current_user.rol != 'docente':
        abort(403)

    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    if not docente:
        flash("No se encontró información del docente", "danger")
        return redirect(url_for("auth.logout"))

    estudiantes_lista = Estudiante.query.filter_by(
        docente_id=docente.id,
        activo=True
    ).order_by(Estudiante.nombre).all()

    return render_template(
        "docente/estudiantes.html",
        estudiantes=estudiantes_lista,
        docente=docente
    )


@docente_bp.route("/mis-permisos")
@login_required
def mis_permisos():
    if current_user.rol != 'docente':
        abort(403)

    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    if not docente:
        flash("No se encontró información del docente", "danger")
        return redirect(url_for("auth.logout"))

    permisos_lista = Permiso.query.filter_by(
        docente_id=docente.id
    ).order_by(Permiso.fecha_inicio.desc()).all()

    hoy = datetime.now().date()

    return render_template(
        "docente/permisos.html",
        permisos=permisos_lista,
        docente=docente,
        hoy=hoy
    )


@docente_bp.route("/mis-permisos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_permiso_docente():
    if current_user.rol != 'docente':
        abort(403)

    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    if not docente:
        flash("No se encontró información del docente", "danger")
        return redirect(url_for("auth.logout"))

    if request.method == "POST":
        try:
            fecha_inicio = request.form.get("fecha_inicio")
            fecha_fin = request.form.get("fecha_fin")
            tipo = request.form.get("tipo")
            observacion = request.form.get("observacion", "").strip()

            if not fecha_inicio or not fecha_fin or not tipo:
                flash("Todos los campos son obligatorios", "danger")
                return redirect(url_for("docente.nuevo_permiso_docente"))

            permiso = Permiso(
                docente_id=docente.id,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                tipo=tipo,
                observacion=observacion if observacion else None,
                colegio_id=docente.colegio_id
            )
            db.session.add(permiso)
            db.session.commit()

            flash("Permiso solicitado correctamente", "success")
            return redirect(url_for("docente.mis_permisos"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")

    return render_template("docente/nuevo_permiso.html", docente=docente)


@docente_bp.route("/mi-perfil", methods=["GET", "POST"])
@login_required
def mi_perfil():
    if current_user.rol != 'docente':
        abort(403)

    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    if not docente:
        flash("No se encontró información del docente", "danger")
        return redirect(url_for("auth.logout"))

    if request.method == "POST":
        try:
            telefono = request.form.get("telefono", "").strip()
            email = request.form.get("email", "").strip()

            from app.models.usuario import Usuario
            email_existente = Usuario.query.filter(
                Usuario.email == email,
                Usuario.id != current_user.id
            ).first()

            if email_existente:
                flash("El correo electrónico ya está registrado", "danger")
                return redirect(url_for("docente.mi_perfil"))

            docente.telefono = telefono if telefono else None
            docente.email = email if email else None
            current_user.email = email
            current_user.nombre = docente.nombre

            db.session.commit()
            flash("Perfil actualizado correctamente", "success")

        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")

        return redirect(url_for("docente.mi_perfil"))

    return render_template("docente/perfil.html", docente=docente)


@docente_bp.route("/cambiar-password", methods=["GET", "POST"])
@login_required
def cambiar_password_docente():
    if current_user.rol != 'docente':
        abort(403)

    if request.method == "POST":
        from werkzeug.security import generate_password_hash
        nueva_password = request.form.get("password", "").strip()

        if not nueva_password or len(nueva_password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres", "danger")
            return redirect(url_for("docente.cambiar_password_docente"))

        try:
            current_user.password_hash = generate_password_hash(nueva_password)
            db.session.commit()
            flash("Contraseña actualizada correctamente", "success")
            return redirect(url_for("docente.dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")

    return render_template("docente/cambiar_password.html")

# ==========================================================
# MÓDULOS FUTUROS DEL DOCENTE
# ==========================================================

@docente_bp.route("/observador")
@login_required
def observador():
    if current_user.rol != 'docente':
        abort(403)

    return render_template("docentes/observador.html")


@docente_bp.route("/citaciones")
@login_required
def citaciones():
    if current_user.rol != 'docente':
        abort(403)

    return render_template("docentes/citaciones.html")


@docente_bp.route("/seguimiento")
@login_required
def seguimiento():
    if current_user.rol != 'docente':
        abort(403)

    return render_template("docentes/seguimiento.html")
# ==========================================================
# CRUD DE DOCENTES (PARA EL COLEGIO) - YA EXISTENTE
# ==========================================================

# ========== LISTAR DOCENTES ==========
@docente_bp.route("/")
@login_required
def listar():
    docentes = Docente.query.filter_by(
        colegio_id=current_user.colegio_id
    ).order_by(Docente.nombre).all()

    return render_template("docentes/listado.html", docentes=docentes)


# ========== NUEVO DOCENTE ==========
@docente_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        documento = request.form.get("documento", "").strip()
        telefono = request.form.get("telefono", "").strip()
        email = request.form.get("email", "").strip()

        if not nombre:
            flash("El nombre del docente es requerido", "danger")
            return redirect(url_for("docente.nuevo"))

        # Verificar si ya existe
        existe = Docente.query.filter_by(
            nombre=nombre,
            colegio_id=current_user.colegio_id
        ).first()

        if existe:
            flash("Este docente ya está registrado", "warning")
            return redirect(url_for("docente.nuevo"))

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
        return redirect(url_for("docente.listar"))

    return render_template("docentes/formulario.html", docente=None, titulo="Nuevo Docente")


# ========== EDITAR DOCENTE ==========
@docente_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
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
            return redirect(url_for("docente.editar", id=id))

        # Verificar si el nombre ya existe (excluyendo este docente)
        existe = Docente.query.filter(
            Docente.nombre == nombre,
            Docente.colegio_id == current_user.colegio_id,
            Docente.id != id
        ).first()

        if existe:
            flash("Ya existe otro docente con ese nombre", "warning")
            return redirect(url_for("docente.editar", id=id))

        # Actualizar
        docente.nombre = nombre
        docente.documento = documento if documento else None
        docente.telefono = telefono if telefono else None
        docente.email = email if email else None
        docente.activo = activo

        db.session.commit()

        flash(f"Docente '{nombre}' actualizado correctamente", "success")
        return redirect(url_for("docente.listar"))

    return render_template("docentes/formulario.html", docente=docente, titulo="Editar Docente")


# ========== ELIMINAR DOCENTE ==========
@docente_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
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

    return redirect(url_for("docente.listar"))


# ========== VER DETALLE ==========
@docente_bp.route("/ver/<int:id>")
@login_required
def ver(id):
    docente = Docente.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    # Obtener permisos del docente
    permisos = Permiso.query.filter_by(
        docente_id=id
    ).order_by(Permiso.fecha_inicio.desc()).all()

    return render_template("docentes/detalle.html", docente=docente, permisos=permisos)


# ========== API: CAMBIAR ESTADO ==========
@docente_bp.route("/cambiar-estado/<int:id>", methods=["POST"])
@login_required
def cambiar_estado(id):
    docente = Docente.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    docente.activo = not docente.activo
    db.session.commit()

    estado = "activado" if docente.activo else "desactivado"
    return jsonify({
        "success": True,
        "message": f"Docente {estado} correctamente",
        "activo": docente.activo
    })