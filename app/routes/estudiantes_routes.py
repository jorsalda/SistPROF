from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app.models.usuario import Usuario
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

from app.models.clase import Clase
from app.models.clase_estudiante import ClaseEstudiante
from app.models.grupo_materia import GrupoMateria

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
        tipo_documento = request.form.get("tipo_documento", "").strip()
        documento = request.form.get("documento", "").strip()
        email = request.form.get("email", "").strip().lower()
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
        # VALIDACIONES DE CAMPOS OBLIGATORIOS
        # =================================================

        if not nombre:
            flash("El nombre del estudiante es requerido", "danger")
            return redirect(url_for("estudiante.nuevo"))

        if not apellido:
            flash("El apellido del estudiante es requerido", "danger")
            return redirect(url_for("estudiante.nuevo"))

        if not tipo_documento:
            flash("El tipo de documento es requerido", "danger")
            return redirect(url_for("estudiante.nuevo"))

        if not documento:
            flash("El número de documento es requerido", "danger")
            return redirect(url_for("estudiante.nuevo"))

        if not email:
            flash("El correo electrónico es requerido", "danger")
            return redirect(url_for("estudiante.nuevo"))

        if not direccion:
            flash("La dirección es obligatoria", "danger")
            return redirect(url_for("estudiante.nuevo"))

        if not telefono:
            flash("El teléfono es obligatorio", "danger")
            return redirect(url_for("estudiante.nuevo"))

        if not grupo_id:
            flash("Debe seleccionar un grupo", "danger")
            return redirect(url_for("estudiante.nuevo"))

        if not acudiente_principal_id:
            flash("Debe seleccionar un acudiente principal", "danger")
            return redirect(url_for("estudiante.nuevo"))

        # =================================================
        # VALIDACIONES DE DUPLICADOS
        # =================================================

        if Usuario.query.filter_by(email=email).first():
            flash("El correo electrónico ya está registrado en el sistema", "danger")
            return redirect(url_for("estudiante.nuevo"))

        if Estudiante.query.filter_by(documento=documento, colegio_id=current_user.colegio_id).first():
            flash("Ya existe un estudiante con ese número de documento", "danger")
            return redirect(url_for("estudiante.nuevo"))

        if Estudiante.query.filter_by(
            nombre=nombre,
            apellido=apellido,
            grupo_id=grupo_id,
            colegio_id=current_user.colegio_id
        ).first():
            flash("Ese estudiante ya existe en el grupo seleccionado", "warning")
            return redirect(url_for("estudiante.nuevo"))

        # =================================================
        # VALIDACIONES DE EXISTENCIA
        # =================================================

        grupo_obj = Grupo.query.filter_by(
            id=grupo_id,
            colegio_id=current_user.colegio_id
        ).first()

        if not grupo_obj:
            flash("Grupo no válido", "danger")
            return redirect(url_for("estudiante.nuevo"))

        # =================================================
        # TOKEN QR
        # =================================================

        qr_token = (
            f"EST-{current_user.colegio_id}-"
            f"{secrets.token_hex(8).upper()}"
        )

        # =================================================
        # PASO 1: CREAR USUARIO PARA EL ESTUDIANTE
        # Usuario = email del formulario
        # Contraseña = número de documento
        # =================================================

        usuario_estudiante = Usuario(
            nombre=f"{nombre} {apellido}",
            email=email,
            password_hash=generate_password_hash(documento),
            rol='estudiante',
            colegio_id=current_user.colegio_id,
            sede_id=(sede_id if sede_id else grupo_obj.sede_id),
            is_active=True,
            is_approved=True
        )
        db.session.add(usuario_estudiante)
        db.session.flush()  # Para obtener el ID del usuario sin hacer commit

        # =================================================
        # PASO 2: CREAR ESTUDIANTE (vinculado al usuario)
        # =================================================

        estudiante = Estudiante(
            nombre=nombre,
            apellido=apellido,
            tipo_documento=tipo_documento,
            documento=documento,
            email=email,
            usuario_id=usuario_estudiante.id,
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

        # =================================================
        # PASO 3: MATRÍCULA AUTOMÁTICA EN LAS CLASES DEL GRUPO
        # =================================================

        clases_del_grupo = db.session.query(Clase).join(
            GrupoMateria, Clase.grupo_materia_id == GrupoMateria.id
        ).filter(
            GrupoMateria.grupo_id == grupo_obj.id,
            Clase.activo == True,
            GrupoMateria.activo == True
        ).all()

        clases_matriculadas = 0

        for clase in clases_del_grupo:
            ya_matriculado = ClaseEstudiante.query.filter_by(
                clase_id=clase.id,
                estudiante_id=estudiante.id
            ).first()

            if not ya_matriculado:
                matricula = ClaseEstudiante(
                    clase_id=clase.id,
                    estudiante_id=estudiante.id
                )
                db.session.add(matricula)
                clases_matriculadas += 1

        # Guardar todo en la base de datos
        db.session.commit()

        flash(
            f"Estudiante '{nombre} {apellido}' registrado correctamente. "
            f"Matriculado en {clases_matriculadas} clases automáticamente. "
            f"Usuario: {email} | Contraseña: {documento}",
            "success"
        )
        return redirect(url_for("estudiante.listar"))

    # =====================================================
    # GET - Mostrar formulario vacío
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


@estudiante_bp.route('/mis-resultados')
@login_required
def mis_resultados():
    if current_user.rol != 'estudiante':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    from app.models.estudiante import Estudiante
    from app.models.resultado_examen import ResultadoExamen
    from app.models.examen import Examen

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante:
        flash('Perfil de estudiante no encontrado', 'warning')
        return redirect(url_for('auth.logout'))

    # Obtener todos los resultados del estudiante
    resultados = db.session.query(
        ResultadoExamen,
        Examen.nombre.label('examen_nombre')
    ).join(
        Examen, ResultadoExamen.examen_id == Examen.id
    ).filter(
        ResultadoExamen.estudiante_id == estudiante.id
    ).order_by(
        ResultadoExamen.fecha.desc()
    ).all()

    return render_template(
        'estudiantes/mis_resultados.html',
        estudiante=estudiante,
        resultados=resultados
    )


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
# GESTIÓN DE ESTUDIANTES (PARA EL ADMIN)
# =========================================================

@estudiante_bp.route("/gestion")
@login_required
def gestion_estudiantes():
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


@estudiante_bp.route('/api/mis-materias')
@login_required
def mis_materias():
    if current_user.rol != 'estudiante':
        return jsonify({'error': 'No autorizado'}), 403

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

    # Obtener materias del grupo del estudiante a través de grupo_materias
    materias = []
    if estudiante.grupo_id:
        from app.models.materia import Materia

        grupo_materias = GrupoMateria.query.filter_by(
            grupo_id=estudiante.grupo_id,
            activo=True
        ).all()

        materias_ids = [gm.materia_id for gm in grupo_materias if gm.materia_id]

        if materias_ids:
            materias = Materia.query.filter(Materia.id.in_(materias_ids)).all()

    return jsonify([{'id': m.id, 'nombre': m.nombre} for m in materias])