from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from app.extensions import db

from app.models.estudiante import Estudiante
from app.models.docente import Docente
from app.models.sede import Sede
from app.models.jornada import Jornada
from app.models.grupo import Grupo
from app.models.acudiente import Acudiente
from sqlalchemy import or_
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
    # Obtener filtros
    search = request.args.get('search', '').strip()
    sede_id = request.args.get('sede_id', type=int)
    grado = request.args.get('grado', '').strip()
    grupo_id = request.args.get('grupo_id', type=int)

    # Consulta base
    consulta = Estudiante.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    )

    # Aplicar filtros
    if search:
        consulta = consulta.filter(
            or_(
                Estudiante.nombre.ilike(f"%{search}%"),
                Estudiante.apellido.ilike(f"%{search}%")
            )
        )

    if sede_id:
        consulta = consulta.filter_by(sede_id=sede_id)

    if grado:
        consulta = consulta.filter_by(grado=grado)

    if grupo_id:
        consulta = consulta.filter_by(grupo_id=grupo_id)

    # Ordenar
    estudiantes = consulta.order_by(Estudiante.nombre).all()

    # Obtener datos para filtros
    sedes = Sede.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).order_by(Sede.nombre).all()

    grupos = Grupo.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).order_by(Grupo.grado, Grupo.nombre).all()

    # Obtener grados únicos
    grados_unicos = db.session.query(
        Estudiante.grado
    ).filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).distinct().order_by(Estudiante.grado).all()

    grados_lista = [g[0] for g in grados_unicos if g[0]]

    return render_template(
        "estudiantes/listado.html",
        estudiantes=estudiantes,
        sedes=sedes,
        grupos=grupos,
        grados_lista=grados_lista,
        current_sede_id=sede_id,
        current_grado=grado,
        current_grupo_id=grupo_id
    )


# =========================================================
# API: OBTENER JORNADAS POR SEDE (AJAX)
# =========================================================

@estudiante_bp.route("/api/jornadas/<int:sede_id>")
@login_required
def api_jornadas_por_sede(sede_id):
    """
    Endpoint AJAX para cargar jornadas filtradas por sede
    """
    jornadas = Jornada.query.filter_by(
        sede_id=sede_id,
        colegio_id=current_user.colegio_id,
        activo=True
    ).order_by(Jornada.nombre).all()

    return jsonify([
        {
            "id": j.id,
            "nombre": j.nombre
        }
        for j in jornadas
    ])



# =========================================================
# NUEVO ESTUDIANTE
# =========================================================
@estudiante_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        grupo_id = request.form.get("grupo_id", type=int)
        sede_id = request.form.get("sede_id", type=int)
        jornada_id = request.form.get("jornada_id", type=int)
        docente_id = request.form.get("docente_id", type=int)
        direccion = request.form.get("direccion", "").strip()
        telefono = request.form.get("telefono", "").strip()
        acudiente_principal_id = request.form.get(
            "acudiente_principal_id",
            type=int
        )

        # =================================================
        # VALIDACIONES
        # =================================================

        if not nombre:
            flash("El nombre del estudiante es requerido", "danger")
            return redirect(url_for("estudiante.nuevo"))

        if not apellido:
            flash("El apellido del estudiante es requerido", "danger")
            return redirect(url_for("estudiante.nuevo"))

        if not grupo_id:
            flash("Debe seleccionar un grupo", "danger")
            return redirect(url_for("estudiante.nuevo"))

        if not direccion:
            flash("La dirección es obligatoria", "danger")
            return redirect(url_for("estudiante.nuevo"))

        if not telefono:
            flash("El teléfono es obligatorio", "danger")
            return redirect(url_for("estudiante.nuevo"))

        if not acudiente_principal_id:
            flash("Debe seleccionar un acudiente principal", "danger")
            return redirect(url_for("estudiante.nuevo"))

        grupo_obj = Grupo.query.filter_by(
            id=grupo_id,
            colegio_id=current_user.colegio_id
        ).first()

        if not grupo_obj:
            flash("Grupo no válido", "danger")
            return redirect(url_for("estudiante.nuevo"))

        # =================================================
        # VALIDAR DUPLICADOS
        # =================================================

        existe = Estudiante.query.filter_by(
            nombre=nombre,
            apellido=apellido,
            grupo_id=grupo_id,
            colegio_id=current_user.colegio_id
        ).first()

        if existe:
            flash(
                "Ese estudiante ya existe en el grupo seleccionado",
                "warning"
            )
            return redirect(url_for("estudiante.nuevo"))

        # =================================================
        # TOKEN QR
        # =================================================

        qr_token = (
            f"EST-{current_user.colegio_id}-"
            f"{secrets.token_hex(8).upper()}"
        )

        # =================================================
        # CREAR ESTUDIANTE
        # =================================================

        estudiante = Estudiante(
            nombre=nombre,
            apellido=apellido,
            direccion=direccion,
            telefono=telefono,
            acudiente_principal_id=acudiente_principal_id,
            grupo_id=grupo_obj.id,
            colegio_id=current_user.colegio_id,
            sede_id=(
                sede_id
                if sede_id
                else grupo_obj.sede_id
            ),
            jornada_id=(
                jornada_id
                if jornada_id
                else grupo_obj.jornada_id
            ),
            docente_id=docente_id,
            qr_token=qr_token,
            activo=True
        )

        db.session.add(estudiante)
        db.session.commit()

        flash(
            f"Estudiante '{nombre} {apellido}' registrado correctamente",
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

    # 🔥 ACUDIENTES AGREGADOS
    acudientes = Acudiente.query.filter_by(
        colegio_id=current_user.colegio_id
    ).order_by(Acudiente.nombre).all()

    return render_template(
        "estudiantes/formulario.html",
        estudiante=None,
        titulo="Nuevo Estudiante",
        sedes=sedes,
        jornadas=jornadas,
        docentes=docentes,
        grupos=grupos,
        acudientes=acudientes
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
        apellido = request.form.get("apellido", "").strip()
        grupo_id = request.form.get("grupo_id", type=int)
        sede_id = request.form.get("sede_id", type=int)
        jornada_id = request.form.get("jornada_id", type=int)
        docente_id = request.form.get("docente_id", type=int)
        direccion = request.form.get("direccion", "").strip()
        telefono = request.form.get("telefono", "").strip()
        acudiente_principal_id = request.form.get(
            "acudiente_principal_id",
            type=int
        )

        # =================================================
        # VALIDACIONES
        # =================================================

        if not nombre:
            flash("El nombre es obligatorio", "danger")
            return redirect(url_for("estudiante.editar", id=id))

        if not apellido:
            flash("El apellido es obligatorio", "danger")
            return redirect(url_for("estudiante.editar", id=id))

        if not grupo_id:
            flash("Debe seleccionar un grupo", "danger")
            return redirect(url_for("estudiante.editar", id=id))

        if not direccion:
            flash("La dirección es obligatoria", "danger")
            return redirect(url_for("estudiante.editar", id=id))

        if not telefono:
            flash("El teléfono es obligatorio", "danger")
            return redirect(url_for("estudiante.editar", id=id))

        if not acudiente_principal_id:
            flash("Debe seleccionar un acudiente principal", "danger")
            return redirect(url_for("estudiante.editar", id=id))

        grupo_obj = Grupo.query.filter_by(
            id=grupo_id,
            colegio_id=current_user.colegio_id
        ).first()

        if not grupo_obj:
            flash("Grupo no válido", "danger")
            return redirect(url_for("estudiante.editar", id=id))

        # =================================================
        # DUPLICADOS
        # =================================================

        existe = Estudiante.query.filter(
            Estudiante.nombre == nombre,
            Estudiante.apellido == apellido,
            Estudiante.grupo_id == grupo_id,
            Estudiante.colegio_id == current_user.colegio_id,
            Estudiante.id != id
        ).first()

        if existe:
            flash(
                "Ya existe otro estudiante igual en ese grupo",
                "warning"
            )
            return redirect(url_for("estudiante.editar", id=id))

        # =================================================
        # ACTUALIZAR
        # =================================================

        estudiante.nombre = nombre
        estudiante.apellido = apellido
        estudiante.direccion = direccion
        estudiante.telefono = telefono
        estudiante.acudiente_principal_id = acudiente_principal_id
        estudiante.grupo_id = grupo_obj.id
        estudiante.sede_id = (
            sede_id
            if sede_id
            else grupo_obj.sede_id
        )
        estudiante.jornada_id = (
            jornada_id
            if jornada_id
            else grupo_obj.jornada_id
        )
        estudiante.docente_id = docente_id

        # ✅ CORRECCIÓN: No modificar activo si no viene en el formulario
        if 'activo' in request.form:
            estudiante.activo = request.form.get("activo") == "on"

        db.session.commit()

        flash(
            f"Estudiante '{nombre} {apellido}' actualizado correctamente",
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

    # 🔥 ACUDIENTES AGREGADOS (para edición también)
    acudientes = Acudiente.query.filter_by(
        colegio_id=current_user.colegio_id
    ).order_by(Acudiente.nombre).all()

    return render_template(
        "estudiantes/formulario.html",
        estudiante=estudiante,
        titulo="Editar Estudiante",
        sedes=sedes,
        jornadas=jornadas,
        docentes=docentes,
        grupos=grupos,
        acudientes=acudientes,
        edit_mode=True
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

    tiene_asistencias = hasattr(estudiante, "asistencias") and len(estudiante.asistencias) > 0
    tiene_novedades = hasattr(estudiante, "novedades") and len(estudiante.novedades) > 0
    tiene_evaluaciones = hasattr(estudiante, "evaluaciones") and len(estudiante.evaluaciones) > 0

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
        if hasattr(estudiante, "asistencias") and estudiante.asistencias
        else []
    )

    novedades_recientes = (
        estudiante.novedades[-10:]
        if hasattr(estudiante, "novedades") and estudiante.novedades
        else []
    )

    tiene_piar = estudiante.tiene_piar_activo()

    return render_template(
        "estudiantes/detalle.html",
        estudiante=estudiante,
        asistencias=asistencias_recientes,
        novedades=novedades_recientes,
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

    estado = (
        "activado"
        if estudiante.activo
        else "desactivado"
    )

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
                "grupo": (
                    estudiante.grupo.nombre
                    if estudiante.grupo
                    else ""
                )
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

        qr_token = request.form.get(
            "qr_token",
            ""
        ).strip()

        estado = request.form.get(
            "estado",
            "presente"
        )

        if not qr_token:

            flash(
                "Token QR no válido",
                "danger"
            )

            return redirect(
                url_for("estudiante.asistencia_rapida")
            )

        estudiante = Estudiante.query.filter_by(
            qr_token=qr_token,
            colegio_id=current_user.colegio_id
        ).first()

        if not estudiante:

            flash(
                "Estudiante no encontrado",
                "danger"
            )

            return redirect(
                url_for("estudiante.asistencia_rapida")
            )

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

        return redirect(
            url_for("estudiante.asistencia_rapida")
        )

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


@estudiante_bp.route('/examen')
@login_required
def examen():
    if current_user.rol != 'estudiante':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('dashboard.index'))
    return render_template('estudiantes/examen_estudiante.html')


@estudiante_bp.route('/dashboard')
@login_required
def dashboard_estudiante():
    if current_user.rol != 'estudiante':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('dashboard.index'))

    from app.models.estudiante import Estudiante
    from app.models.resultado_examen import ResultadoExamen
    from app.models.examen import Examen
    from datetime import datetime

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante:
        flash('Perfil de estudiante no encontrado', 'warning')
        return redirect(url_for('auth.logout'))

    # Estadísticas
    resultados = ResultadoExamen.query.filter_by(estudiante_id=estudiante.id).all()
    total_examenes = len(resultados)

    if total_examenes > 0:
        notas = [float(r.nota_numerica) for r in resultados if r.nota_numerica]
        promedio_general = round(sum(notas) / len(notas), 2) if notas else 0
        mejor_nota = max(notas) if notas else 0
    else:
        promedio_general = 0
        mejor_nota = 0

    # Últimos 5 resultados
    ultimos_resultados = db.session.query(
        ResultadoExamen,
        Examen.nombre.label('examen_nombre')
    ).join(
        Examen, ResultadoExamen.examen_id == Examen.id
    ).filter(
        ResultadoExamen.estudiante_id == estudiante.id
    ).order_by(
        ResultadoExamen.fecha.desc()
    ).limit(5).all()

    return render_template(
        'estudiantes/dashboard_estudiante.html',
        estudiante=estudiante,
        total_examenes=total_examenes,
        promedio_general=promedio_general,
        mejor_nota=mejor_nota,
        ultimos_resultados=ultimos_resultados,
        hoy=datetime.now()
    )


# =========================================================
# DASHBOARD ADMINISTRATIVO (NUEVO)
# =========================================================

@estudiante_bp.route("/dashboard")
@login_required
def dashboard_admin():
    """
    Dashboard administrativo con estadísticas, filtros y vista consolidada
    """
    from app.services.estudiante_service import EstudianteService

    # Parámetros de filtros
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    grado = request.args.get('grado', '').strip()
    grupo_id = request.args.get('grupo_id', type=int)

    # Obtener estudiantes con filtros
    resultado = EstudianteService.get_all_by_colegio(
        colegio_id=current_user.colegio_id,
        page=page,
        per_page=15,
        search=search if search else None,
        grado=grado if grado else None,
        grupo_id=grupo_id
    )

    # Obtener estadísticas
    estadisticas = EstudianteService.get_estadisticas(current_user.colegio_id)

    # Obtener datos para filtros
    grupos = Grupo.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).order_by(Grupo.grado, Grupo.nombre).all()

    # Obtener grados únicos
    grados_unicos = db.session.query(
        Estudiante.grado
    ).filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).distinct().order_by(Estudiante.grado).all()

    grados_lista = [g[0] for g in grados_unicos if g[0]]

    return render_template(
        "estudiantes/dashboard_admin.html",
        estudiantes=resultado['estudiantes'],
        pagination=resultado,
        estadisticas=estadisticas,
        grupos=grupos,
        grados_lista=grados_lista,
        search=search,
        current_grado=grado,
        current_grupo_id=grupo_id
    )


# =========================================================
# API: OBTENER GRUPOS POR SEDE (AJAX)
# =========================================================

@estudiante_bp.route("/api/grupos/<int:sede_id>")
@login_required
def api_grupos_por_sede(sede_id):

    jornada_id = request.args.get("jornada", type=int)

    consulta = Grupo.query.filter_by(
        sede_id=sede_id,
        colegio_id=current_user.colegio_id,
        activo=True
    )

    if jornada_id:
        consulta = consulta.filter_by(
            jornada_id=jornada_id
        )

    grupos = consulta.order_by(
        Grupo.grado,
        Grupo.nombre
    ).all()

    return jsonify([
        {
            "id": g.id,
            "grado": g.grado,
            "nombre": g.nombre
        }
        for g in grupos
    ])


# =========================================================
# API: OBTENER ACUDIENTES (AJAX)
# =========================================================

@estudiante_bp.route("/api/acudientes")
@login_required
def api_acudientes():
    """
    Endpoint AJAX para cargar acudientes del colegio
    """
    acudientes = Acudiente.query.filter_by(
        colegio_id=current_user.colegio_id
    ).order_by(Acudiente.nombre).all()

    return jsonify([{
        'id': a.id,
        'nombre': a.nombre,
        'telefono': a.telefono,
        'email': a.email,
        'parentesco': a.parentesco
    } for a in acudientes])


# =========================================================
# API: ESTADÍSTICAS RÁPIDAS (AJAX)
# =========================================================

@estudiante_bp.route("/api/estadisticas")
@login_required
def api_estadisticas():
    """
    Endpoint AJAX para obtener estadísticas actualizadas
    """
    from app.services.estudiante_service import EstudianteService

    estadisticas = EstudianteService.get_estadisticas(current_user.colegio_id)

    return jsonify(estadisticas)