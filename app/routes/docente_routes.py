from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.docente import Docente
from app.models.permiso import Permiso

docente_bp = Blueprint("docente", __name__, url_prefix="/docentes")


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