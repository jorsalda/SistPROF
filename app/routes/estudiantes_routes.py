from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.estudiante import Estudiante
from app.models.colegio import Colegio
from app.models.docente import Docente
from app.models.sede import Sede
from app.models.jornada import Jornada
import secrets
import string
from datetime import datetime

estudiante_bp = Blueprint("estudiante", __name__, url_prefix="/estudiantes")


# ========== LISTAR ESTUDIANTES ==========
@estudiante_bp.route("/")
@login_required
def listar():
    """Lista todos los estudiantes del colegio del usuario actual"""
    estudiantes = Estudiante.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).order_by(Estudiante.nombre).all()

    return render_template("estudiantes/listado.html", estudiantes=estudiantes)


# ========== NUEVO ESTUDIANTE ==========
@estudiante_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    """Registro de nuevo estudiante"""
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        grado = request.form.get("grado", "").strip()
        grupo = request.form.get("grupo", "").strip()
        sede_id = request.form.get("sede_id", type=int)
        jornada_id = request.form.get("jornada_id", type=int)
        docente_id = request.form.get("docente_id", type=int)

        # Validaciones
        if not nombre:
            flash("El nombre del estudiante es requerido", "danger")
            return redirect(url_for("estudiante.nuevo"))

        if not grado:
            flash("El grado es requerido", "danger")
            return redirect(url_for("estudiante.nuevo"))

        # Verificar si ya existe
        existe = Estudiante.query.filter_by(
            nombre=nombre,
            grado=grado,
            grupo=grupo,
            colegio_id=current_user.colegio_id
        ).first()

        if existe:
            flash("Este estudiante ya está registrado en ese grado/grupo", "warning")
            return redirect(url_for("estudiante.nuevo"))

        # Generar QR token único
        qr_token = f"EST-{current_user.colegio_id}-{secrets.token_hex(8).upper()}"

        # Crear estudiante
        estudiante = Estudiante(
            nombre=nombre,
            grado=grado,
            grupo=grupo if grupo else None,
            colegio_id=current_user.colegio_id,
            sede_id=sede_id if sede_id else None,
            jornada_id=jornada_id if jornada_id else None,
            docente_id=docente_id if docente_id else None,
            institucion_id=current_user.colegio_id,
            qr_token=qr_token,
            activo=True
        )

        db.session.add(estudiante)
        db.session.commit()

        flash(f"Estudiante '{nombre}' registrado correctamente. QR: {qr_token}", "success")
        return redirect(url_for("estudiante.listar"))

    # GET: Cargar datos para el formulario
    sedes = Sede.query.filter_by(colegio_id=current_user.colegio_id, activo=True).all()
    jornadas = Jornada.query.filter_by(colegio_id=current_user.colegio_id, activo=True).all()
    docentes = Docente.query.filter_by(colegio_id=current_user.colegio_id, activo=True).all()

    return render_template(
        "estudiantes/formulario.html",
        estudiante=None,
        titulo="Nuevo Estudiante",
        sedes=sedes,
        jornadas=jornadas,
        docentes=docentes
    )


# ========== EDITAR ESTUDIANTE ==========
@estudiante_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    """Editar estudiante existente"""
    estudiante = Estudiante.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        grado = request.form.get("grado", "").strip()
        grupo = request.form.get("grupo", "").strip()
        sede_id = request.form.get("sede_id", type=int)
        jornada_id = request.form.get("jornada_id", type=int)
        docente_id = request.form.get("docente_id", type=int)
        activo = request.form.get("activo") == "on"

        if not nombre:
            flash("El nombre del estudiante es requerido", "danger")
            return redirect(url_for("estudiante.editar", id=id))

        # Verificar duplicados (excluyendo este estudiante)
        existe = Estudiante.query.filter(
            Estudiante.nombre == nombre,
            Estudiante.grado == grado,
            Estudiante.grupo == grupo,
            Estudiante.colegio_id == current_user.colegio_id,
            Estudiante.id != id
        ).first()

        if existe:
            flash("Ya existe otro estudiante con esos datos", "warning")
            return redirect(url_for("estudiante.editar", id=id))

        # Actualizar
        estudiante.nombre = nombre
        estudiante.grado = grado
        estudiante.grupo = grupo if grupo else None
        estudiante.sede_id = sede_id if sede_id else None
        estudiante.jornada_id = jornada_id if jornada_id else None
        estudiante.docente_id = docente_id if docente_id else None
        estudiante.activo = activo

        db.session.commit()

        flash(f"Estudiante '{nombre}' actualizado correctamente", "success")
        return redirect(url_for("estudiante.listar"))

    # GET: Cargar datos
    sedes = Sede.query.filter_by(colegio_id=current_user.colegio_id, activo=True).all()
    jornadas = Jornada.query.filter_by(colegio_id=current_user.colegio_id, activo=True).all()
    docentes = Docente.query.filter_by(colegio_id=current_user.colegio_id, activo=True).all()

    return render_template(
        "estudiantes/formulario.html",
        estudiante=estudiante,
        titulo="Editar Estudiante",
        sedes=sedes,
        jornadas=jornadas,
        docentes=docentes
    )


# ========== ELIMINAR ESTUDIANTE ==========
@estudiante_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    """Eliminar o desactivar estudiante"""
    estudiante = Estudiante.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    nombre = estudiante.nombre

    # Verificar si tiene registros relacionados (Asistencias, Novedades, Evaluaciones)
    tiene_asistencias = len(estudiante.asistencias) > 0
    tiene_novedades = len(estudiante.novedades) > 0
    tiene_evaluaciones = len(estudiante.evaluaciones) > 0

    if tiene_asistencias or tiene_novedades or tiene_evaluaciones:
        # No eliminar, solo desactivar para mantener integridad referencial
        estudiante.activo = False
        db.session.commit()
        flash(f"Estudiante '{nombre}' desactivado (tiene registros asociados)", "warning")
    else:
        # Eliminar permanentemente si no tiene historial
        db.session.delete(estudiante)
        db.session.commit()
        flash(f"Estudiante '{nombre}' eliminado permanentemente", "success")

    return redirect(url_for("estudiante.listar"))


# ========== VER DETALLE ==========
@estudiante_bp.route("/ver/<int:id>")
@login_required
def ver(id):
    """Ver detalle completo del estudiante"""
    estudiante = Estudiante.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    # Obtener datos relacionados
    asistencias_recientes = estudiante.asistencias[-10:] if estudiante.asistencias else []
    novedades_recientes = estudiante.novedades[-10:] if estudiante.novedades else []
    acudientes = estudiante.get_acudientes()
    tiene_piar = estudiante.tiene_piar_activo()

    return render_template(
        "estudiantes/detalle.html",
        estudiante=estudiante,
        asistencias=asistencias_recientes,
        novedades=novedades_recientes,
        acudientes=acudientes,
        tiene_piar=tiene_piar
    )


# ========== API: CAMBIAR ESTADO ==========
@estudiante_bp.route("/cambiar-estado/<int:id>", methods=["POST"])
@login_required
def cambiar_estado(id):
    """Activar/desactivar estudiante vía AJAX"""
    estudiante = Estudiante.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    estudiante.activo = not estudiante.activo
    db.session.commit()

    estado = "activado" if estudiante.activo else "desactivado"
    return jsonify({
        "success": True,
        "message": f"Estudiante {estado} correctamente",
        "activo": estudiante.activo
    })


# ========== API: REGENERAR QR ==========
@estudiante_bp.route("/regenerar-qr/<int:id>", methods=["POST"])
@login_required
def regenerar_qr(id):
    """Generar nuevo token QR para el estudiante"""
    estudiante = Estudiante.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    nuevo_qr = estudiante.generar_qr_token()
    db.session.commit()

    return jsonify({
        "success": True,
        "qr_token": nuevo_qr,
        "message": "QR regenerado correctamente"
    })


# ========== API: BUSCAR ESTUDIANTE POR QR ==========
@estudiante_bp.route("/buscar-qr/<token>")
@login_required
def buscar_por_qr(token):
    """Buscar estudiante por token QR"""
    estudiante = Estudiante.query.filter_by(
        qr_token=token,
        colegio_id=current_user.colegio_id
    ).first()

    if estudiante:
        return jsonify({
            "success": True,
            "estudiante": {
                "id": estudiante.id,
                "nombre": estudiante.nombre,
                "grado": estudiante.grado,
                "grupo": estudiante.grupo
            }
        })
    else:
        return jsonify({
            "success": False,
            "message": "Estudiante no encontrado"
        }), 404


# ========== REGISTRAR ASISTENCIA RÁPIDA ==========
@estudiante_bp.route("/asistencia-rapida", methods=["GET", "POST"])
@login_required
def asistencia_rapida():
    """Registro rápido de asistencia por QR"""
    if request.method == "POST":
        qr_token = request.form.get("qr_token", "").strip()
        estado = request.form.get("estado", "presente")  # presente, tarde, ausente

        if not qr_token:
            flash("Token QR no válido", "danger")
            return redirect(url_for("estudiante.asistencia_rapida"))

        estudiante = Estudiante.query.filter_by(
            qr_token=qr_token,
            colegio_id=current_user.colegio_id
        ).first()

        if not estudiante:
            flash("Estudiante no encontrado", "danger")
            return redirect(url_for("estudiante.asistencia_rapida"))

        # Registrar asistencia
        # Nota: Asegúrate de tener el modelo Asistencia importado o creado
        try:
            from app.models.asistencia import Asistencia
            asistencia = Asistencia(
                estudiante_id=estudiante.id,
                clase_id=None,  # Asistencia general
                fecha=datetime.now().date(),
                estado=estado,
                registrada_por=current_user.id
            )
            db.session.add(asistencia)
            db.session.commit()
            flash(f"Asistencia registrada: {estudiante.nombre} - {estado}", "success")
        except ImportError:
            flash("Módulo de asistencias no configurado aún", "warning")

        return redirect(url_for("estudiante.asistencia_rapida"))

    return render_template("estudiantes/asistencia_rapida.html")