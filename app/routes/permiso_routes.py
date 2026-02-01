from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from app.extensions import db
from app.models.permiso import Permiso
from app.models.docente import Docente
from datetime import datetime

permiso_bp = Blueprint("permiso", __name__, url_prefix="/permisos")

@permiso_bp.route("/")
@login_required
def listado():
    permisos = Permiso.query.filter_by(
        colegio_id=current_user.colegio_id
    ).order_by(Permiso.fecha_inicio.desc()).all()

    # Pasar la fecha actual para calcular permisos activos
    hoy = datetime.now().date()

    return render_template("permisos/listado.html",
                           permisos=permisos,
                           hoy=hoy)  # ← Agregar hoy


@permiso_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def formulario():
    docentes = Docente.query.filter_by(
        colegio_id=current_user.colegio_id
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

        flash("Permiso registrado correctamente", "success")
        return redirect(url_for("permiso.listado"))

    return render_template("permisos/formulario.html", docentes=docentes)


@permiso_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    permiso = Permiso.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    docente_nombre = permiso.docente.nombre
    db.session.delete(permiso)
    db.session.commit()

    flash(f"Permiso de {docente_nombre} eliminado correctamente", "success")
    return redirect(url_for("permiso.listado"))


# AGREGAR ESTA NUEVA RUTA
@permiso_bp.route("/api/permisos-docente/<int:docente_id>")
@login_required
def permisos_por_docente(docente_id):
    """API para obtener permisos de un docente específico"""
    # Verificar que el docente pertenece al colegio del usuario
    docente = Docente.query.filter_by(
        id=docente_id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    permisos = Permiso.query.filter_by(
        docente_id=docente_id,
        colegio_id=current_user.colegio_id
    ).order_by(Permiso.fecha_inicio.desc()).all()

    # Convertir a formato JSON
    permisos_json = []
    for permiso in permisos:
        permisos_json.append({
            'id': permiso.id,
            'tipo': permiso.tipo,
            'fecha_inicio': permiso.fecha_inicio.strftime('%d/%m/%Y'),
            'fecha_fin': permiso.fecha_fin.strftime('%d/%m/%Y'),
            'observacion': permiso.observacion or '',
            'dias': (permiso.fecha_fin - permiso.fecha_inicio).days + 1
        })

    return jsonify({
        'success': True,
        'docente': docente.nombre,
        'permisos': permisos_json,
        'total': len(permisos_json)
    })


