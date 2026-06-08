from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from app.extensions import db

from app.models.estudiante import Estudiante
from app.models.colegio import Colegio
from app.models.docente import Docente
from app.models.sede import Sede
from app.models.jornada import Jornada
from app.models.grupo import Grupo

import secrets
from datetime import datetime

estudiante_bp = Blueprint(
    "estudiante",
    __name__,
    url_prefix="/estudiantes"
)


# =========================================================
# LISTAR ESTUDIANTES
# =========================================================
@estudiante_bp.route("/")
@login_required
def listar():
    """Lista todos los estudiantes activos"""

    estudiantes = Estudiante.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).order_by(Estudiante.nombre).all()

    return render_template(
        "estudiantes/listado.html",
        estudiantes=estudiantes
    )


# =========================================================
# NUEVO ESTUDIANTE
# =========================================================
@estudiante_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()

        grupo_id = request.form.get("grupo_id", type=int)

        sede_id = request.form.get("sede_id", type=int)
        jornada_id = request.form.get("jornada_id", type=int)
        docente_id = request.form.get("docente_id", type=int)

        # =================================================
        # VALIDACIONES
        # =================================================

        if not nombre:
            flash("El nombre del estudiante es requerido", "danger")
            return redirect(url_for("estudiante.nuevo"))

        if not grupo_id:
            flash("Debe seleccionar un grupo", "danger")
            return redirect(url_for("estudiante.nuevo"))

        grupo_obj = Grupo.query.filter_by(
            id=grupo_id,
            colegio_id=current_user.colegio_id
        ).first()

        if not grupo_obj:
            flash("Grupo no válido", "danger")
            return redirect(url_for("estudiante.nuevo"))

        # =================================================
        # EVITAR DUPLICADOS
        # =================================================

        existe = Estudiante.query.filter_by(
            nombre=nombre,
            grupo_id=grupo_id,
            colegio_id=current_user.colegio_id
        ).first()

        if existe:
            flash("Ese estudiante ya existe en el grupo seleccionado", "warning")
            return redirect(url_for("estudiante.nuevo"))

        # =================================================
        # GENERAR TOKEN QR
        # =================================================

        qr_token = f"EST-{current_user.colegio_id}-{secrets.token_hex(8).upper()}"

        # =================================================
        # CREAR ESTUDIANTE
        # =================================================

        estudiante = Estudiante(
            nombre=nombre,

            # Compatibilidad temporal
            grado=grupo_obj.grado,
            grupo=grupo_obj.nombre,

            grupo_id=grupo_obj.id,

            colegio_id=current_user.colegio_id,

            sede_id=sede_id if sede_id else grupo_obj.sede_id,

            jornada_id=jornada_id if jornada_id else grupo_obj.jornada_id,

            docente_id=docente_id if docente_id else None,

            institucion_id=current_user.colegio_id,

            qr_token=qr_token,

            activo=True
        )

        db.session.add(estudiante)
        db.session.commit()

        flash(
            f"Estudiante '{nombre}' registrado correctamente",
            "success"
        )

        return redirect(url_for("estudiante.listar"))

    # =====================================================
    # GET
    # =====================================================

    sedes = Sede.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).all()

    jornadas = Jornada.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).all()

    docentes = Docente.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).all()

    grupos = Grupo.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).order_by(
        Grupo.grado,
        Grupo.nombre
    ).all()

    return render_template(
        "estudiantes/formulario.html",
        estudiante=None,
        titulo="Nuevo Estudiante",
        sedes=sedes,
        jornadas=jornadas,
        docentes=docentes,
        grupos=grupos
    )


# =========================================================
# EDITAR ESTUDIANTE
# =========================================================
@estudiante_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):

    estudiante = Estudiante.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()

        grupo_id = request.form.get("grupo_id", type=int)

        sede_id = request.form.get("sede_id", type=int)
        jornada_id = request.form.get("jornada_id", type=int)
        docente_id = request.form.get("docente_id", type=int)

        activo = request.form.get("activo") == "on"

        # =================================================
        # VALIDACIONES
        # =================================================

        if not nombre:
            flash("El nombre es obligatorio", "danger")
            return redirect(url_for("estudiante.editar", id=id))

        if not grupo_id:
            flash("Debe seleccionar un grupo", "danger")
            return redirect(url_for("estudiante.editar", id=id))

        grupo_obj = Grupo.query.filter_by(
            id=grupo_id,
            colegio_id=current_user.colegio_id
        ).first()

        if not grupo_obj:
            flash("Grupo no válido", "danger")
            return redirect(url_for("estudiante.editar", id=id))

        # =================================================
        # VALIDAR DUPLICADOS
        # =================================================

        existe = Estudiante.query.filter(
            Estudiante.nombre == nombre,
            Estudiante.grupo_id == grupo_id,
            Estudiante.colegio_id == current_user.colegio_id,
            Estudiante.id != id
        ).first()

        if existe:
            flash("Ya existe otro estudiante igual en ese grupo", "warning")
            return redirect(url_for("estudiante.editar", id=id))

        # =================================================
        # ACTUALIZAR
        # =================================================

        estudiante.nombre = nombre

        estudiante.grupo_id = grupo_obj.id

        # Compatibilidad temporal
        estudiante.grado = grupo_obj.grado
        estudiante.grupo = grupo_obj.nombre

        estudiante.sede_id = sede_id if sede_id else grupo_obj.sede_id

        estudiante.jornada_id = (
            jornada_id if jornada_id else grupo_obj.jornada_id
        )

        estudiante.docente_id = (
            docente_id if docente_id else None
        )

        estudiante.activo = activo

        db.session.commit()

        flash(
            f"Estudiante '{nombre}' actualizado correctamente",
            "success"
        )

        return redirect(url_for("estudiante.listar"))

    # =====================================================
    # GET
    # =====================================================

    sedes = Sede.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).all()

    jornadas = Jornada.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).all()

    docentes = Docente.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).all()

    grupos = Grupo.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).order_by(
        Grupo.grado,
        Grupo.nombre
    ).all()

    return render_template(
        "estudiantes/formulario.html",
        estudiante=estudiante,
        titulo="Editar Estudiante",
        sedes=sedes,
        jornadas=jornadas,
        docentes=docentes,
        grupos=grupos
    )


# =========================================================
# ELIMINAR ESTUDIANTE
# =========================================================
@estudiante_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):

    estudiante = Estudiante.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    nombre = estudiante.nombre

    tiene_asistencias = len(estudiante.asistencias) > 0
    tiene_novedades = len(estudiante.novedades) > 0
    tiene_evaluaciones = len(estudiante.evaluaciones) > 0

    if tiene_asistencias or tiene_novedades or tiene_evaluaciones:

        estudiante.activo = False
        db.session.commit()

        flash(
            f"Estudiante '{nombre}' desactivado",
            "warning"
        )

    else:

        db.session.delete(estudiante)
        db.session.commit()

        flash(
            f"Estudiante '{nombre}' eliminado",
            "success"
        )

    return redirect(url_for("estudiante.listar"))


# =========================================================
# VER DETALLE
# =========================================================
@estudiante_bp.route("/ver/<int:id>")
@login_required
def ver(id):

    estudiante = Estudiante.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    asistencias_recientes = (
        estudiante.asistencias[-10:]
        if estudiante.asistencias else []
    )

    novedades_recientes = (
        estudiante.novedades[-10:]
        if estudiante.novedades else []
    )

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


# =========================================================
# CAMBIAR ESTADO
# =========================================================
@estudiante_bp.route("/cambiar-estado/<int:id>", methods=["POST"])
@login_required
def cambiar_estado(id):

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


# =========================================================
# REGENERAR QR
# =========================================================
@estudiante_bp.route("/regenerar-qr/<int:id>", methods=["POST"])
@login_required
def regenerar_qr(id):

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


# =========================================================
# BUSCAR POR QR
# =========================================================
@estudiante_bp.route("/buscar-qr/<token>")
@login_required
def buscar_por_qr(token):

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

    return jsonify({
        "success": False,
        "message": "Estudiante no encontrado"
    }), 404


# =========================================================
# ASISTENCIA RÁPIDA
# =========================================================
@estudiante_bp.route("/asistencia-rapida", methods=["GET", "POST"])
@login_required
def asistencia_rapida():

    if request.method == "POST":

        qr_token = request.form.get("qr_token", "").strip()

        estado = request.form.get(
            "estado",
            "presente"
        )

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

        try:

            from app.models.asistencia import Asistencia

            asistencia = Asistencia(
                estudiante_id=estudiante.id,
                clase_id=None,
                fecha=datetime.now().date(),
                estado=estado,
                registrada_por=current_user.id
            )

            db.session.add(asistencia)
            db.session.commit()

            flash(
                f"Asistencia registrada: {estudiante.nombre}",
                "success"
            )

        except ImportError:

            flash(
                "Módulo de asistencias no configurado aún",
                "warning"
            )

        return redirect(url_for("estudiante.asistencia_rapida"))

    return render_template(
        "estudiantes/asistencia_rapida.html"
    )


# =========================================================
# MOTOR INGENIOS
# =========================================================
@estudiante_bp.route("/ingenios")
@login_required
def ingenios():

    return render_template(
        "estudiantes/ingenios.html"
    )