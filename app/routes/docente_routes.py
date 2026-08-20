from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash
import json
import re

# Imports de Modelos Existentes
from app.models.pregunta import Pregunta
from app.models.materia import Materia
from app.models.docente import Docente
from app.models.permiso import Permiso
from app.models.estudiante import Estudiante
from app.models.grupo import Grupo
from app.models.usuario import Usuario
from app.models.sede import Sede
from app.models.examen import Examen
from app.models.examen_contenido import ExamenContenido
from app.extensions import db

# ✅ NUEVOS IMPORTS PARA LA PLANILLA Y SEGUIMIENTO
from app.models.grupo_materia import GrupoMateria
from app.models.CompetenciaEstudiante import CompetenciaEstudiante
from app.models.indicador_logro import IndicadorLogro
from app.models.evaluacion_estudiante import EvaluacionEstudiante
from app.models.periodo_academico import PeriodoAcademico
from app.models.configuracion_periodo import ConfiguracionPeriodo
from services.ia_service import generar_analisis_pedagogico, logger

docente_bp = Blueprint("docente", __name__, url_prefix="/docentes")


# ==========================================================
# DASHBOARD DEL DOCENTE
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

    # 1. GRUPOS QUE DIRIGE
    grupos_dirigidos = Grupo.query.filter_by(director_docente_id=docente.id, activo=True).all()
    ids_grupos_dirigidos = [g.id for g in grupos_dirigidos]

    # 2. GRUPOS DONDE ENSEÑA MATERIAS
    asignaciones_materias = GrupoMateria.query.filter_by(docente_id=docente.id, activo=True).all()
    ids_grupos_materias = list(set([gm.grupo_id for gm in asignaciones_materias]))

    todos_ids_grupos = list(set(ids_grupos_dirigidos + ids_grupos_materias))

    if todos_ids_grupos:
        total_estudiantes = Estudiante.query.filter(
            Estudiante.grupo_id.in_(todos_ids_grupos),
            Estudiante.activo == True
        ).count()
    else:
        total_estudiantes = 0

    # 3. CARGA ACADÉMICA DETALLADA
    carga_academica = {}
    for asignacion in asignaciones_materias:
        materia_nombre = asignacion.materia.nombre if asignacion.materia else "Sin materia"
        grupo = asignacion.grupo
        if not grupo or not grupo.activo:
            continue

        grupo_key = f"{grupo.grado}{grupo.nombre}"
        if materia_nombre not in carga_academica:
            carga_academica[materia_nombre] = []

        grupo_info = {
            'id': grupo.id,
            'nombre': grupo_key,
            'sede': grupo.sede.nombre if grupo.sede else "N/A",
            'horas': asignacion.horas_semanales or 0
        }
        if grupo_info not in carga_academica[materia_nombre]:
            carga_academica[materia_nombre].append(grupo_info)

    # 4. PERMISOS
    total_permisos = Permiso.query.filter_by(docente_id=docente.id).count()
    permisos_activos = Permiso.query.filter(
        Permiso.docente_id == docente.id,
        Permiso.fecha_inicio <= hoy,
        Permiso.fecha_fin >= hoy
    ).count()
    ultimos_permisos = Permiso.query.filter_by(docente_id=docente.id).order_by(Permiso.fecha_inicio.desc()).limit(
        5).all()

    return render_template(
        "docentes/dashboard.html",
        docente=docente,
        total_estudiantes=total_estudiantes,
        total_permisos=total_permisos,
        permisos_activos=permisos_activos,
        ultimos_permisos=ultimos_permisos,
        hoy=hoy,
        carga_academica=carga_academica,
        total_materias=len(carga_academica),
        total_grupos=len(todos_ids_grupos)
    )


# ==========================================================
# MIS ESTUDIANTES
# ==========================================================
@docente_bp.route("/mis-estudiantes")
@login_required
def mis_estudiantes():
    if current_user.rol != 'docente':
        abort(403)

    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    if not docente:
        flash("No se encontró información del docente", "danger")
        return redirect(url_for("auth.logout"))

    search = request.args.get('search', '').strip()
    sede_id = request.args.get('sede_id', type=int)
    grupo_id = request.args.get('grupo_id', type=int)

    grupos_dirigidos = Grupo.query.filter_by(director_docente_id=docente.id, activo=True).all()
    ids_grupos_dirigidos = [g.id for g in grupos_dirigidos]

    asignaciones_materias = GrupoMateria.query.filter_by(docente_id=docente.id, activo=True).all()
    ids_grupos_materias = list(set([gm.grupo_id for gm in asignaciones_materias]))

    todos_ids_grupos = list(set(ids_grupos_dirigidos + ids_grupos_materias))

    grupos_disponibles = Grupo.query.filter(
        Grupo.id.in_(todos_ids_grupos), Grupo.activo == True
    ).order_by(Grupo.grado, Grupo.nombre).all() if todos_ids_grupos else []

    if todos_ids_grupos:
        consulta = Estudiante.query.filter(Estudiante.grupo_id.in_(todos_ids_grupos), Estudiante.activo == True)
        if search:
            consulta = consulta.filter(
                re.or_(Estudiante.nombre.ilike(f"%{search}%"), Estudiante.apellido.ilike(f"%{search}%")))
        if sede_id:
            consulta = consulta.filter_by(sede_id=sede_id)
        if grupo_id:
            consulta = consulta.filter_by(grupo_id=grupo_id)
        estudiantes_lista = consulta.order_by(Estudiante.nombre).all()
    else:
        estudiantes_lista = []

    sedes = Sede.query.filter_by(colegio_id=docente.colegio_id, activo=True).order_by(Sede.nombre).all()

    return render_template(
        "docentes/estudiantes.html",
        estudiantes=estudiantes_lista,
        docente=docente,
        sedes=sedes,
        grupos_disponibles=grupos_disponibles,
        search=search,
        current_sede_id=sede_id,
        current_grupo_id=grupo_id,
        total_estudiantes=len(estudiantes_lista),
        activos=sum(1 for e in estudiantes_lista if e.activo)
    )


# ==========================================================
# SEGUIMIENTO ACADÉMICO (REDIRIGE A PLANILLA)
# ==========================================================
@docente_bp.route("/seguimiento")
@login_required
def seguimiento():
    try:
        docente = Docente.query.filter_by(usuario_id=current_user.id).first()
        if not docente:
            flash("Perfil de docente no encontrado.", "danger")
            return redirect(url_for('docente.dashboard'))

        asignacion = GrupoMateria.query.filter_by(docente_id=docente.id, activo=True).first()

        if asignacion:
            return redirect(url_for('docente.ver_planilla',
                                    grupo_id=asignacion.grupo_id,
                                    materia_id=asignacion.materia_id))
        else:
            flash("No tienes grupos o materias asignadas para ver seguimiento.", "warning")
            return redirect(url_for('docente.dashboard'))
    except Exception as e:
        print(f"Error en seguimiento: {e}")
        flash("Error al cargar el seguimiento.", "danger")
        return redirect(url_for('docente.dashboard'))



# ==========================================================
# RESTO DE RUTAS EXISTENTES (Permisos, Perfil, CRUD Docentes, etc.)
# ==========================================================

@docente_bp.route("/mis-permisos")
@login_required
def mis_permisos():
    if current_user.rol != 'docente':
        abort(403)
    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    if not docente:
        flash("No se encontró información del docente", "danger")
        return redirect(url_for("auth.logout"))
    permisos_lista = Permiso.query.filter_by(docente_id=docente.id).order_by(Permiso.fecha_inicio.desc()).all()
    return render_template("docentes/permisos.html", permisos=permisos_lista, docente=docente,
                           hoy=datetime.now().date())


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
                docente_id=docente.id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin,
                tipo=tipo, observacion=observacion if observacion else None, colegio_id=docente.colegio_id
            )
            db.session.add(permiso)
            db.session.commit()
            flash("Permiso solicitado correctamente", "success")
            return redirect(url_for("docente.mis_permisos"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")
    return render_template("docentes/nuevo_permiso.html", docente=docente)


@docente_bp.route("/mis-permisos/eliminar/<int:permiso_id>", methods=["POST"])
@login_required
def eliminar_permiso_docente(permiso_id):
    if current_user.rol != 'docente':
        abort(403)
    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    if not docente:
        flash("No se encontró información del docente", "danger")
        return redirect(url_for("auth.logout"))
    permiso = Permiso.query.filter_by(id=permiso_id, docente_id=docente.id).first_or_404()
    try:
        db.session.delete(permiso)
        db.session.commit()
        flash("Permiso eliminado correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar: {str(e)}", "danger")
    return redirect(url_for("docente.mis_permisos"))


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
            email_existente = Usuario.query.filter(Usuario.email == email, Usuario.id != current_user.id).first()
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
    return render_template("docentes/perfil.html", docente=docente)


@docente_bp.route("/cambiar-password", methods=["GET", "POST"])
@login_required
def cambiar_password_docente():
    if current_user.rol != 'docente':
        abort(403)
    if request.method == "POST":
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
    return render_template("docentes/cambiar_password.html")


@docente_bp.route("/observador")
@login_required
def observador():
    if current_user.rol != 'docente': abort(403)
    return render_template("docentes/observador.html")


@docente_bp.route("/citaciones")
@login_required
def citaciones():
    if current_user.rol != 'docente': abort(403)
    return render_template("docentes/citaciones.html")


@docente_bp.route("/")
@login_required
def listar():
    docentes = Docente.query.filter_by(colegio_id=current_user.colegio_id).order_by(Docente.nombre).all()
    return render_template("docentes/listado.html", docentes=docentes)


@docente_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    sedes = Sede.query.filter_by(colegio_id=current_user.colegio_id, activo=True).order_by(Sede.nombre).all()
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        documento = request.form.get("documento", "").strip()
        email = request.form.get("email", "").strip().lower()
        telefono = request.form.get("telefono", "").strip()
        sede_id = request.form.get("sede_id", "").strip()

        if not nombre or not apellido or not documento or not email or not sede_id:
            flash("Todos los campos obligatorios deben ser completados", "danger")
            return redirect(url_for("docente.nuevo"))
        if len(documento) < 6:
            flash("El documento debe tener al menos 6 caracteres", "danger")
            return redirect(url_for("docente.nuevo"))
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            flash("El correo electrónico no tiene un formato válido", "danger")
            return redirect(url_for("docente.nuevo"))
        if Docente.query.filter_by(documento=documento, colegio_id=current_user.colegio_id).first():
            flash("Ya existe un docente con ese documento", "danger")
            return redirect(url_for("docente.nuevo"))
        if Usuario.query.filter_by(email=email).first():
            flash("El correo electrónico ya está registrado", "danger")
            return redirect(url_for("docente.nuevo"))

        try:
            usuario = Usuario(
                email=email, password_hash=generate_password_hash(documento), nombre=nombre, apellido=apellido,
                rol='docente', colegio_id=current_user.colegio_id, sede_id=int(sede_id),
                is_active=True, is_approved=True, fecha_aprobacion=datetime.now(), failed_attempts=0
            )
            db.session.add(usuario)
            db.session.flush()
            docente = Docente(
                nombre=nombre, apellido=apellido, documento=documento, telefono=telefono if telefono else None,
                email=email, colegio_id=current_user.colegio_id, usuario_id=usuario.id, sede_id=int(sede_id),
                activo=True
            )
            db.session.add(docente)
            db.session.commit()
            flash(f"✅ Docente '{nombre} {apellido}' registrado. Contraseña inicial: {documento}", "success")
            return redirect(url_for("docente.listar"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar: {str(e)}", "danger")
    return render_template("docentes/formulario.html", docente=None, titulo="Nuevo Docente", sedes=sedes)


@docente_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    docente = Docente.query.filter_by(id=id, colegio_id=current_user.colegio_id).first_or_404()
    sedes = Sede.query.filter_by(colegio_id=current_user.colegio_id, activo=True).order_by(Sede.nombre).all()
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        documento = request.form.get("documento", "").strip()
        email = request.form.get("email", "").strip().lower()
        telefono = request.form.get("telefono", "").strip()
        sede_id = request.form.get("sede_id", "").strip()
        activo = request.form.get("activo") == "on"

        if not nombre or not apellido or not email:
            flash("Nombre, apellido y email son requeridos", "danger")
            return redirect(url_for("docente.editar", id=id))
        if Usuario.query.filter(Usuario.email == email, Usuario.id != docente.usuario_id).first():
            flash("El correo ya está registrado por otro usuario", "danger")
            return redirect(url_for("docente.editar", id=id))
        if documento and Docente.query.filter(Docente.documento == documento,
                                              Docente.colegio_id == current_user.colegio_id,
                                              Docente.id != id).first():
            flash("Ya existe otro docente con ese documento", "danger")
            return redirect(url_for("docente.editar", id=id))

        try:
            docente.nombre = nombre
            docente.apellido = apellido
            docente.documento = documento if documento else None
            docente.telefono = telefono if telefono else None
            docente.email = email
            docente.sede_id = int(sede_id) if sede_id else None
            docente.activo = activo
            if docente.usuario:
                docente.usuario.nombre = nombre
                docente.usuario.apellido = apellido
                docente.usuario.email = email
                docente.usuario.sede_id = int(sede_id) if sede_id else None
            db.session.commit()
            flash(f"✅ Docente '{nombre} {apellido}' actualizado", "success")
            return redirect(url_for("docente.listar"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar: {str(e)}", "danger")
    return render_template("docentes/formulario.html", docente=docente, titulo="Editar Docente", sedes=sedes)


@docente_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    docente = Docente.query.filter_by(id=id, colegio_id=current_user.colegio_id).first_or_404()
    nombre = docente.nombre
    if Permiso.query.filter_by(docente_id=id).first():
        docente.activo = False
        db.session.commit()
        flash(f"Docente '{nombre}' desactivado (tiene permisos asociados)", "warning")
    else:
        db.session.delete(docente)
        db.session.commit()
        flash(f"Docente '{nombre}' eliminado permanentemente", "success")
    return redirect(url_for("docente.listar"))


@docente_bp.route("/ver/<int:id>")
@login_required
def ver(id):
    docente = Docente.query.filter_by(id=id, colegio_id=current_user.colegio_id).first_or_404()
    permisos = Permiso.query.filter_by(docente_id=id).order_by(Permiso.fecha_inicio.desc()).all()
    return render_template("docentes/detalle.html", docente=docente, permisos=permisos)


@docente_bp.route("/cambiar-estado/<int:id>", methods=["POST"])
@login_required
def cambiar_estado(id):
    docente = Docente.query.filter_by(id=id, colegio_id=current_user.colegio_id).first_or_404()
    docente.activo = not docente.activo
    db.session.commit()
    estado = "activado" if docente.activo else "desactivado"
    return jsonify({"success": True, "message": f"Docente {estado} correctamente", "activo": docente.activo})


@docente_bp.route("/banco-preguntas")
@login_required
def banco_preguntas():
    preguntas_banco = Pregunta.query.filter_by(docente_id=current_user.id).order_by(
        Pregunta.fecha_creacion.desc()).all()
    materias = Materia.query.all()
    return render_template("docentes/banco_preguntas.html", preguntas=preguntas_banco, materias=materias)


@docente_bp.route("/crear-desde-banco", methods=["GET", "POST"])
@login_required
def crear_desde_banco():
    if current_user.rol not in ['docente', 'coordinador', 'admin_colegio']:
        abort(403)
    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    materias = Materia.query.all()
    preguntas_banco = Pregunta.query.filter_by(docente_id=current_user.id).all()

    if request.method == "POST":
        try:
            titulo = request.form.get("titulo_examen", "").strip()
            materia_id = request.form.get("materia_id")
            grado = request.form.get("grado")
            if not titulo or not materia_id:
                flash("Título y materia son obligatorios.", "danger")
                return redirect(url_for("docente.crear_desde_banco"))

            ids_seleccionados_json = request.form.get("ids_preguntas_banco")
            if not ids_seleccionados_json:
                flash("Debes seleccionar al menos una pregunta del banco.", "warning")
                return redirect(url_for("docente.crear_desde_banco"))

            ids_seleccionados = json.loads(ids_seleccionados_json)
            preguntas_validas = Pregunta.query.filter(Pregunta.id.in_(ids_seleccionados)).all()
            if len(preguntas_validas) != len(ids_seleccionados):
                flash("Algunas preguntas seleccionadas no son válidas.", "danger")
                return redirect(url_for("docente.crear_desde_banco"))

            nuevo_examen = Examen(
                titulo=titulo, nombre=titulo, descripcion=f"Examen creado desde banco para {grado}",
                materia_id=materia_id, colegio_id=current_user.colegio_id, tiempo_limite_minutos=30,
                fecha_creacion=datetime.now(), activo=True
            )
            db.session.add(nuevo_examen)
            db.session.flush()

            contenido_para_guardar = [{"pregunta_id": p.id, "orden": idx + 1} for idx, p in
                                      enumerate(preguntas_validas)]
            nuevo_contenido = ExamenContenido(examen_id=nuevo_examen.id, contenido_json=contenido_para_guardar,
                                              version=1, activo=True)
            db.session.add(nuevo_contenido)
            db.session.commit()

            flash(f"✅ Examen '{titulo}' creado con {len(preguntas_validas)} preguntas.", "success")
            return redirect(url_for("examen.listar_examenes"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear examen: {str(e)}", "danger")
            import traceback
            traceback.print_exc()
    return render_template("examenes/crear_examen.html", docente=docente, materias=materias,
                           preguntas_banco=preguntas_banco)


@docente_bp.route("/examen/<int:id>/asignar", methods=["GET", "POST"])
@login_required
def asignar_examen(id):
    if current_user.rol != 'docente':
        abort(403)
    from app.models.examen import ProgramacionExamen

    examen = Examen.query.get_or_404(id)
    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    if not docente:
        flash("Error: No se encontró perfil de docente.", "danger")
        return redirect(url_for("docente.mis_examenes"))

    ids_grupos_docente = db.session.query(GrupoMateria.grupo_id).filter_by(docente_id=docente.id, activo=True).all()
    ids_grupos_docente = [g[0] for g in ids_grupos_docente]
    grupos_disponibles = Grupo.query.filter(Grupo.id.in_(ids_grupos_docente), Grupo.activo == True).order_by(
        Grupo.grado, Grupo.nombre).all() if ids_grupos_docente else []

    if request.method == "POST":
        grupo_id = request.form.get("grupo_id")
        fecha_apertura = request.form.get("fecha_apertura")
        fecha_cierre = request.form.get("fecha_cierre")
        if not grupo_id or not fecha_apertura or not fecha_cierre:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for("docente.asignar_examen", id=id))

        existe = ProgramacionExamen.query.filter_by(examen_id=id, grupo_id=int(grupo_id)).first()
        try:
            if existe:
                existe.fecha_apertura = fecha_apertura
                existe.fecha_cierre = fecha_cierre
                existe.activo = True
                flash("Programación actualizada correctamente", "success")
            else:
                nueva_prog = ProgramacionExamen(examen_id=id, grupo_id=int(grupo_id), fecha_apertura=fecha_apertura,
                                                fecha_cierre=fecha_cierre, activo=True)
                db.session.add(nueva_prog)
                flash("Examen asignado al grupo exitosamente", "success")
            db.session.commit()
            return redirect("/api/examen/mis-examenes")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al guardar: {str(e)}", "danger")
    return render_template("docentes/asignar_examen.html", examen=examen, grupos=grupos_disponibles)


# ============================================================
# GENERADOR DE CÓDIGOS DE COMPETENCIA
# ============================================================

def generar_codigo_competencia(materia_id, nivel_educativo):
    """
    Genera un código único incremental basado en el nivel educativo.
    Rangos diferenciados por caso:
      - Bajo:     b200-b299  (minúscula)
      - Básico:   B300-B399  (mayúscula)
      - Alto:     A400-A499  (mayúscula)
      - Superior: S500-S599  (mayúscula)
    """
    config_codigos = {
        'Bajo': {'prefijo': 'b2', 'base': 200},
        'Básico': {'prefijo': 'B3', 'base': 300},
        'Alto': {'prefijo': 'A4', 'base': 400},
        'Superior': {'prefijo': 'S5', 'base': 500}
    }

    if nivel_educativo not in config_codigos:
        raise ValueError(f"Nivel educativo '{nivel_educativo}' no válido.")

    config = config_codigos[nivel_educativo]
    prefijo = config['prefijo']
    base = config['base']

    ultimo_codigo = CompetenciaEstudiante.query.filter(
        CompetenciaEstudiante.materia_id == materia_id,
        CompetenciaEstudiante.codigo.like(f"{prefijo}%")
    ).order_by(CompetenciaEstudiante.codigo.desc()).first()

    if ultimo_codigo:
        try:
            num_actual = int(''.join(filter(str.isdigit, ultimo_codigo.codigo)))
            nuevo_num = num_actual + 1
            limite_superior = base + 99
            if nuevo_num > limite_superior:
                raise ValueError(f"Límite alcanzado para nivel {nivel_educativo}.")
        except (ValueError, IndexError):
            nuevo_num = base
    else:
        nuevo_num = base

    return f"{prefijo}{nuevo_num}"

# ============================================================
# GENERAR COMPETENCIAS MADRE
# ============================================================
@docente_bp.route("/api/competencias-madre", methods=["POST"])
@login_required
def crear_competencia_madre():
    print("🔥 [DEBUG] Entrando a crear_competencia_madre")  # LOG 1

    if current_user.rol != 'docente':
        abort(403)

    try:
        data = request.get_json()
        print(f"🔥 [DEBUG] Datos recibidos: {data}")  # LOG 2

        materia_id = data.get('materia_id')
        descripcion_madre = data.get('descripcion_madre', '').strip()
        indicadores = data.get('indicadores', {})

        if not all([materia_id, descripcion_madre]):
            return jsonify({"error": "Materia y descripción son obligatorios"}), 400

        # Validar niveles
        niveles_requeridos = ['bajo', 'basico', 'alto', 'superior']
        for nivel in niveles_requeridos:
            if nivel not in indicadores or not indicadores[nivel].strip():
                return jsonify({"error": f"Falta descripción para nivel: {nivel}"}), 400

        # ✅ NUEVO: Obtener el GRUPO_ID correspondiente a esta materia y docente
        # Esto evita que las nuevas competencias queden sin grupo (NULL)
        grupo_materia = GrupoMateria.query.filter_by(
            docente_id=current_user.id,
            materia_id=materia_id,
            activo=True
        ).first()

        grupo_id_para_guardar = grupo_materia.grupo_id if grupo_materia else None
        print(f" [DEBUG] Grupo detectado para guardar: {grupo_id_para_guardar}")

        # 1. GENERAR CÓDIGO SECUENCIAL (C1, C2...)
        # Filtramos también por grupo para que la secuencia sea correcta por grado
        ultima_comp = CompetenciaEstudiante.query.filter_by(
            materia_id=materia_id,
            grupo_id=grupo_id_para_guardar
        ).order_by(CompetenciaEstudiante.id.desc()).first()

        nuevo_numero = 1
        if ultima_comp and ultima_comp.codigo:
            try:
                num_actual = int(''.join(filter(str.isdigit, ultima_comp.codigo)))
                nuevo_numero = num_actual + 1
            except (ValueError, TypeError):
                pass

        codigo_madre = f"C{nuevo_numero}"
        print(f"🔥 [DEBUG] Código generado: {codigo_madre}")  # LOG 3

        # 2. Crear Competencia Madre CON GRUPO_ID
        nueva_competencia = CompetenciaEstudiante(
            materia_id=materia_id,
            nombre=descripcion_madre[:150],
            descripcion=descripcion_madre,
            nivel_educativo='Integral',
            codigo=codigo_madre,
            porcentaje=20,
            grupo_id=grupo_id_para_guardar  # ✅ ASIGNAR EL GRUPO AQUÍ
        )
        db.session.add(nueva_competencia)
        db.session.flush()

        # 3. Crear Indicadores
        config_indicadores = {
            'bajo': {'codigo': 'b200', 'nombre': 'Bajo', 'orden': 1},
            'basico': {'codigo': 'B300', 'nombre': 'Basico', 'orden': 2},
            'alto': {'codigo': 'A400', 'nombre': 'Alto', 'orden': 3},
            'superior': {'codigo': 'S500', 'nombre': 'Superior', 'orden': 4}
        }

        for key, config in config_indicadores.items():
            ind = IndicadorLogro(
                competencia_materia_id=nueva_competencia.id,
                descripcion=indicadores[key].strip(),
                codigo=config['codigo'],
                nivel=config['nombre'],
                orden=config['orden']
            )
            db.session.add(ind)

        db.session.commit()
        print(f"✅ [DEBUG] Guardado exitoso ID: {nueva_competencia.id}")  # LOG 4

        return jsonify({
            "success": True,
            "message": f"Competencia {codigo_madre} creada exitosamente"
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"❌ [DEBUG] ERROR CRÍTICO: {e}")  # LOG 5
        import traceback;
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500



# ============================================================
# GESTIÓN DE COMPETENCIAS (VISTA INLINE)
# ============================================================
@docente_bp.route("/competencias")
@login_required
def gestionar_competencias():
    # 1. OBTENER DATOS BÁSICOS DEL DOCENTE Y PERIODO
    docente = Docente.query.filter_by(usuario_id=current_user.id).first()

    periodo_actual = PeriodoAcademico.query.filter_by(colegio_id=docente.colegio_id, activo=True).first()
    periodo_abierto = True
    if periodo_actual:
        config_periodo = ConfiguracionPeriodo.query.filter_by(periodo_id=periodo_actual.id).first()
        if config_periodo and not config_periodo.permite_editar_competencias:
            periodo_abierto = False

    # 2. CONSULTA DE MATERIAS (JOIN CON GRUPOS)
    materias_raw = db.session.query(GrupoMateria, Materia, Grupo).join(
        Materia, GrupoMateria.materia_id == Materia.id
    ).join(
        Grupo, GrupoMateria.grupo_id == Grupo.id
    ).filter(
        GrupoMateria.docente_id == docente.id,
        GrupoMateria.activo == True
    ).order_by(Grupo.grado, Grupo.nombre, Materia.nombre).all()

    opciones_materias = []
    for gm, mat, grp in materias_raw:
        grado_info = f"{grp.grado}° {grp.nombre}" if grp else "Sin Grado"
        label = f"{mat.nombre} ({grado_info})"

        opciones_materias.append({
            'id': gm.materia_id,
            'grupo_id': grp.id,
            'label': label
        })

    # 3. PARSEAR SELECCIÓN COMPUESTA (VALOR: "MATERIA_ID-GRUPO_ID")
    seleccion_raw = request.args.get('seleccion', '')
    materia_id_seleccionada = None
    grupo_id_seleccionado = None

    if '-' in str(seleccion_raw):
        parts = str(seleccion_raw).split('-')
        try:
            materia_id_seleccionada = int(parts[0])
            grupo_id_seleccionado = int(parts[1])
        except ValueError:
            pass

    # Fallback: Si no hay selección válida, usar la primera opción disponible
    if not materia_id_seleccionada and opciones_materias:
        primera_op = opciones_materias[0]
        materia_id_seleccionada = primera_op['id']
        grupo_id_seleccionado = primera_op['grupo_id']

    print(f" [DEBUG] Selección Cruda: {seleccion_raw}")
    print(f" [DEBUG] Filtrando por Materia={materia_id_seleccionada}, Grupo={grupo_id_seleccionado}")

    # 4. OBTENER COMPETENCIAS (FILTRO ESTRICTO POR MATERIA + GRUPO)
    competencias_madres = []
    indicadores_hijos = []

    if materia_id_seleccionada and grupo_id_seleccionado:
        competencias_madres = CompetenciaEstudiante.query.filter_by(
            materia_id=materia_id_seleccionada,
            grupo_id=grupo_id_seleccionado
        ).order_by(CompetenciaEstudiante.codigo).all()

        print(f" [DEBUG] Competencias encontradas: {len(competencias_madres)}")

        ids_madres = [c.id for c in competencias_madres]
        if ids_madres:
            indicadores_hijos = IndicadorLogro.query.filter(
                IndicadorLogro.competencia_materia_id.in_(ids_madres)
            ).order_by(IndicadorLogro.orden).all()
    else:
        print(" [WARN] No hay selección válida de materia/grupo.")

    # 5. AGRUPAR EN ESTRUCTURA JERÁRQUICA PARA EL ACORDEÓN
    competencias_agrupadas = {}

    for comp in competencias_madres:
        competencias_agrupadas[comp.id] = {
            'madre': comp,
            'hijos': []
        }

    for ind in indicadores_hijos:
        if ind.competencia_materia_id in competencias_agrupadas:
            competencias_agrupadas[ind.competencia_materia_id]['hijos'].append(ind)

    lista_para_template = list(competencias_agrupadas.values())

    # 6. RENDERIZAR TEMPLATE
    return render_template(
        "docentes/gestion_competencias.html",
        periodo_abierto=periodo_abierto,
        opciones_materias=opciones_materias,
        competencias=lista_para_template,
        periodo_actual=periodo_actual,
        materia_seleccionada_id=materia_id_seleccionada,
        grupo_seleccionado_id=grupo_id_seleccionado
    )





# ============================================================
# ENDPOINT IA PARA ANÁLISIS PEDAGÓGICO
# ============================================================
@docente_bp.route("/api/ia/analizar-estudiante", methods=["POST"])
@login_required
def analizar_estudiante_ia():
    """Genera fortalezas, debilidades y plan de apoyo usando IA."""

    data = request.get_json()
    est_id = data.get('estudiante_id')
    mat_id = data.get('materia_id')
    per_id = data.get('periodo_id')

    if not all([est_id, mat_id, per_id]):
        return jsonify({"error": "Faltan parámetros requeridos"}), 400

    try:
        # Obtener notas con contexto completo
        evaluaciones = EvaluacionEstudiante.query.filter_by(
            estudiante_id=est_id,
            periodo_id=per_id
        ).join(IndicadorLogro).join(CompetenciaEstudiante).all()

        if not evaluaciones:
            return jsonify({
                "fortalezas": ["No hay datos suficientes para analizar"],
                "debilidades": [],
                "plan_apoyo": "Registre calificaciones para obtener un análisis pedagógico."
            }), 200

        # Preparar contexto para IA
        contexto_notas = []
        for ev in evaluaciones:
            contexto_notas.append({
                "competencia": ev.competencia_materia.nombre,
                "codigo": ev.competencia_materia.codigo,
                "indicador": ev.indicador_logro.codigo,
                "nota": float(ev.calificacion) if ev.calificacion else 0.0
            })

        # Llamar a servicio IA
        resultado_ia = generar_analisis_pedagogico(contexto_notas)

        return jsonify({
            "fortalezas": resultado_ia.get('fortalezas', []),
            "debilidades": resultado_ia.get('debilidades', []),
            "plan_apoyo": resultado_ia.get('plan_apoyo', '')
        })

    except Exception as e:
        logger.error(f"Error en análisis IA para estudiante {est_id}: {str(e)}")
        return jsonify({
            "error": "No se pudo completar el análisis.",
            "detalle": str(e)
        }), 500

# =============================================================================
# PLAN-001 | Paso 1.1 | Endpoint GET: Planilla de Calificaciones
# =============================================================================

from flask import abort
from sqlalchemy import text
from app.models import (
    Docente, Estudiante, Grupo, GrupoMateria, Materia,
    PeriodoAcademico, CompetenciaEstudiante, IndicadorLogro,
    EvaluacionEstudiante, NotaComponenteEstudiante
)


# ==========================================================
# SELECTOR DE PLANILLA DE CALIFICACIONES
# ==========================================================
@docente_bp.route("/planilla-selector")
@login_required
def ver_planilla_selector():
    """Vista intermedia para que el docente elija Grupo y Materia antes de ir a la planilla."""
    if current_user.rol != 'docente':
        abort(403)

    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    if not docente:
        flash("Perfil de docente no encontrado.", "danger")
        return redirect(url_for('docente.dashboard'))

    # Obtener asignaciones activas del docente
    asignaciones = GrupoMateria.query.filter_by(docente_id=docente.id, activo=True).all()

    # Agrupar por materia para facilitar la selección
    materias_con_grupos = {}
    for asig in asignaciones:
        mat_nombre = asig.materia.nombre if asig.materia else "Sin Nombre"
        if mat_nombre not in materias_con_grupos:
            materias_con_grupos[mat_nombre] = {
                'id': asig.materia_id,
                'grupos': []
            }

        grupo = asig.grupo
        if grupo and grupo.activo:
            materias_con_grupos[mat_nombre]['grupos'].append({
                'id': grupo.id,
                'nombre': f"{grupo.grado} {grupo.nombre}"
            })

    return render_template(
        "docentes/selector_planilla.html",
        materias=materias_con_grupos
    )


@docente_bp.route("/planilla/<int:grupo_id>/<int:materia_id>", methods=["GET", "POST"])
@login_required
def ver_planilla(grupo_id, materia_id):
    """
    GET: Muestra la planilla de calificaciones (1 columna por competencia).
    POST: Guarda las notas y niveles de desempeño.
    """
    if current_user.rol not in ['docente', 'coordinador']:
        abort(403)

    # -------------------------------------------------------------------------
    # 1. Datos comunes (GET y POST)
    # -------------------------------------------------------------------------
    docente = Docente.query.filter_by(usuario_id=current_user.id).first_or_404()

    asignacion = GrupoMateria.query.filter_by(
        grupo_id=grupo_id,
        materia_id=materia_id,
        docente_id=docente.id,
        activo=True
    ).first_or_404()

    grupo = asignacion.grupo
    materia = asignacion.materia

    periodo = PeriodoAcademico.query.filter_by(
        colegio_id=docente.colegio_id,
        activo=True
    ).order_by(PeriodoAcademico.anio.desc()).first()

    if not periodo:
        flash("No hay un periodo académico activo.", "warning")
        return redirect(url_for("docente.dashboard"))

    periodo_id = periodo.id

    # ✅ NUEVO: Leer configuración institucional de evaluación
    config_eval = db.session.execute(text("""
        SELECT tipo_captura FROM configuracion_evaluacion 
        WHERE colegio_id = :cid
    """), {"cid": docente.colegio_id}).fetchone()

    tipo_captura = config_eval.tipo_captura if config_eval else 'NUMERICA'

    # ========================================================================
    # POST: GUARDAR NOTAS Y NIVELES
    # ========================================================================
    if request.method == "POST":
        try:
            # Auditoría: quién modifica
            db.session.execute(
                text("SET LOCAL app.current_user_id = :uid"),
                {"uid": current_user.id}
            )

            # Detectar JSON o form tradicional
            if request.is_json:
                data = request.get_json()
                notas = data.get('notas', {})
                componentes = data.get('componentes', {})
                ponderaciones = data.get('ponderaciones', {})
                niveles = data.get('niveles', {})
            else:
                notas = {}
                componentes = {}
                ponderaciones = {}
                niveles = {}
                for key, val in request.form.items():
                    if key.startswith('nota_'):
                        parts = key.split('_')
                        if len(parts) == 3:
                            est_id, comp_id = parts[1], parts[2]
                            if est_id not in notas:
                                notas[est_id] = {}
                            notas[est_id][comp_id] = val
                    elif key.startswith('autoeval_'):
                        est_id = key.split('_')[1]
                        if est_id not in componentes:
                            componentes[est_id] = {}
                        componentes[est_id]['autoevaluacion'] = val
                    elif key.startswith('examen_'):
                        est_id = key.split('_')[1]
                        if est_id not in componentes:
                            componentes[est_id] = {}
                        componentes[est_id]['examen_final'] = val
                    elif key.startswith('nivel_'):
                        parts = key.split('_')
                        if len(parts) == 3:
                            est_id, comp_id = parts[1], parts[2]
                            if est_id not in niveles:
                                niveles[est_id] = {}
                            niveles[est_id][comp_id] = val

            # -----------------------------------------------------------------
            # Guardar notas por competencia (usando el primer indicador)
            # -----------------------------------------------------------------
            for est_id, competencias in notas.items():
                for comp_id, valor in competencias.items():
                    if valor is None or str(valor).strip() == '':
                        continue

                    nota_val = float(valor)
                    if nota_val < 0 or nota_val > 5:
                        msg = f"Nota fuera de rango (0-5): {nota_val}"
                        if request.is_json:
                            return jsonify({"success": False, "error": msg}), 400
                        flash(msg, "danger")
                        return redirect(url_for('docente.ver_planilla', grupo_id=grupo_id, materia_id=materia_id))

                    indicador = IndicadorLogro.query.filter_by(
                        competencia_materia_id=int(comp_id)
                    ).order_by(IndicadorLogro.id).first()

                    if not indicador:
                        indicador = IndicadorLogro(
                            competencia_materia_id=int(comp_id),
                            descripcion=f"Indicador general - Competencia {comp_id}",
                            codigo="GENERAL"
                        )
                        db.session.add(indicador)
                        db.session.flush()

                    ev = EvaluacionEstudiante.query.filter_by(
                        estudiante_id=int(est_id),
                        indicador_id=indicador.id,
                        periodo_id=periodo_id
                    ).first()

                    if ev:
                        ev.calificacion = nota_val
                    else:
                        db.session.add(EvaluacionEstudiante(
                            estudiante_id=int(est_id),
                            indicador_id=indicador.id,
                            periodo_id=periodo_id,
                            calificacion=nota_val
                        ))

            # -----------------------------------------------------------------
            # Guardar niveles de desempeño por competencia
            # -----------------------------------------------------------------
            for est_id, comps in niveles.items():
                for comp_id, nivel in comps.items():
                    if not nivel or str(nivel).strip() == '':
                        continue

                    indicador = IndicadorLogro.query.filter_by(
                        competencia_materia_id=int(comp_id)
                    ).order_by(IndicadorLogro.id).first()

                    if not indicador:
                        continue

                    ev = EvaluacionEstudiante.query.filter_by(
                        estudiante_id=int(est_id),
                        indicador_id=indicador.id,
                        periodo_id=periodo_id
                    ).first()

                    if ev:
                        ev.nivel_desempeño = nivel
                    else:
                        db.session.add(EvaluacionEstudiante(
                            estudiante_id=int(est_id),
                            indicador_id=indicador.id,
                            periodo_id=periodo_id,
                            nivel_desempeño=nivel
                        ))

            # -----------------------------------------------------------------
            # Guardar componentes (autoeval, examen)
            # -----------------------------------------------------------------
            for est_id, comps in componentes.items():
                for tipo, valor in comps.items():
                    if valor is None or str(valor).strip() == '':
                        continue

                    nota_val = float(valor)
                    if nota_val < 0 or nota_val > 5:
                        msg = f"Componente fuera de rango (0-5): {nota_val}"
                        if request.is_json:
                            return jsonify({"success": False, "error": msg}), 400
                        flash(msg, "danger")
                        return redirect(url_for('docente.ver_planilla', grupo_id=grupo_id, materia_id=materia_id))

                    nc = NotaComponenteEstudiante.query.filter_by(
                        estudiante_id=int(est_id),
                        grupo_materia_id=asignacion.id,
                        periodo_academico_id=periodo_id,
                        tipo_componente=tipo
                    ).first()

                    if nc:
                        nc.calificacion = nota_val
                        nc.registrada_por = current_user.id
                    else:
                        db.session.add(NotaComponenteEstudiante(
                            estudiante_id=int(est_id),
                            grupo_materia_id=asignacion.id,
                            periodo_academico_id=periodo_id,
                            tipo_componente=tipo,
                            calificacion=nota_val,
                            registrada_por=current_user.id
                        ))

            # -----------------------------------------------------------------
            # Actualizar ponderaciones si vienen
            # -----------------------------------------------------------------
            if ponderaciones:
                for comp_id, nuevo_pct in ponderaciones.items():
                    comp = CompetenciaEstudiante.query.filter_by(
                        id=int(comp_id), materia_id=materia_id
                    ).first()
                    if comp:
                        comp.porcentaje = float(nuevo_pct)

            db.session.commit()

            if request.is_json:
                return jsonify({"success": True, "message": "Notas guardadas correctamente"})

            flash("✅ Notas guardadas correctamente", "success")
            return redirect(url_for('docente.ver_planilla', grupo_id=grupo_id, materia_id=materia_id))

        except Exception as e:
            db.session.rollback()
            import traceback;
            traceback.print_exc()
            error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)

            if request.is_json:
                return jsonify({"success": False, "error": error_msg}), 500

            flash(f"Error al guardar: {error_msg}", "danger")
            return redirect(url_for('docente.ver_planilla', grupo_id=grupo_id, materia_id=materia_id))

    # ========================================================================
    # GET: RENDERIZAR PLANILLA
    # ========================================================================
    puede_editar = True
    try:
        result = db.session.execute(text("""
            SELECT permite_editar_notas 
            FROM configuracion_periodo 
            WHERE colegio_id = :colegio_id AND periodo_id = :periodo_id
        """), {
            "colegio_id": docente.colegio_id,
            "periodo_id": periodo_id
        }).fetchone()
        if result and result.permite_editar_notas is False:
            puede_editar = False
    except Exception:
        pass

    # ✅ CORREGIDO: Filtrar competencias por Materia Y Grupo específico
    # Esto evita que se mezclen competencias de 10° y 11° en la misma planilla
    competencias_raw = CompetenciaEstudiante.query.filter_by(
        materia_id=materia_id,
        grupo_id=grupo_id  # <--- FILTRO CLAVE AGREGADO
    ).order_by(CompetenciaEstudiante.codigo).all()

    comp_ids = [c.id for c in competencias_raw]
    primer_indicador_por_comp = {}
    if comp_ids:
        todos_indicadores = IndicadorLogro.query.filter(
            IndicadorLogro.competencia_materia_id.in_(comp_ids)
        ).order_by(IndicadorLogro.competencia_materia_id, IndicadorLogro.id).all()
        for ind in todos_indicadores:
            if ind.competencia_materia_id not in primer_indicador_por_comp:
                primer_indicador_por_comp[ind.competencia_materia_id] = ind.id

    estructura = []
    for comp in competencias_raw:
        estructura.append({
            "id": comp.id,
            "nombre": comp.nombre,
            "codigo": comp.codigo or f"C{comp.id}",
            "porcentaje": float(comp.porcentaje) if comp.porcentaje else 0,
            "primer_indicador_id": primer_indicador_por_comp.get(comp.id)
        })

    # Estudiantes
    estudiantes_raw = Estudiante.query.filter_by(
        grupo_id=grupo_id, activo=True
    ).order_by(Estudiante.apellido, Estudiante.nombre).all()

    estudiantes_ids = [e.id for e in estudiantes_raw]

    # Notas y niveles por indicador
    evaluaciones = EvaluacionEstudiante.query.filter(
        EvaluacionEstudiante.estudiante_id.in_(estudiantes_ids),
        EvaluacionEstudiante.periodo_id == periodo_id
    ).all()

    # Indexar por estudiante -> indicador
    evals_por_indicador = {}
    for ev in evaluaciones:
        if ev.estudiante_id not in evals_por_indicador:
            evals_por_indicador[ev.estudiante_id] = {}
        evals_por_indicador[ev.estudiante_id][ev.indicador_id] = {
            "calificacion": float(ev.calificacion) if ev.calificacion else None,
            "nivel_desempeño": ev.nivel_desempeño
        }

    # Indexar por estudiante -> competencia (usando el primer indicador)
    indicador_a_competencia = {v: k for k, v in primer_indicador_por_comp.items()}
    evaluaciones_por_competencia = {}
    for est_id in estudiantes_ids:
        evaluaciones_por_competencia[est_id] = {}
        for comp in competencias_raw:
            primer_ind_id = primer_indicador_por_comp.get(comp.id)
            if primer_ind_id and primer_ind_id in evals_por_indicador.get(est_id, {}):
                evaluaciones_por_competencia[est_id][comp.id] = evals_por_indicador[est_id][primer_ind_id]
            else:
                evaluaciones_por_competencia[est_id][comp.id] = {
                    "calificacion": None,
                    "nivel_desempeño": None
                }

    # Componentes (autoeval, examen)
    componentes = NotaComponenteEstudiante.query.filter(
        NotaComponenteEstudiante.estudiante_id.in_(estudiantes_ids),
        NotaComponenteEstudiante.grupo_materia_id == asignacion.id,
        NotaComponenteEstudiante.periodo_academico_id == periodo_id
    ).all()

    componentes_por_estudiante = {}
    for comp in componentes:
        if comp.estudiante_id not in componentes_por_estudiante:
            componentes_por_estudiante[comp.estudiante_id] = {}
        componentes_por_estudiante[comp.estudiante_id][comp.tipo_componente] = float(
            comp.calificacion) if comp.calificacion else None

    # Preparar lista final
    estudiantes = []
    for est in estudiantes_raw:
        piar_activo = False
        if hasattr(est, 'piar') and est.piar:
            piar_activo = getattr(est.piar, 'activo', False)

        estudiantes.append({
            "id": est.id,
            "nombre": est.nombre or "",
            "apellido": est.apellido or "",
            "piar_activo": piar_activo,
            "evaluaciones": evaluaciones_por_competencia.get(est.id, {}),
            "autoeval": componentes_por_estudiante.get(est.id, {}).get("autoevaluacion", ""),
            "examen": componentes_por_estudiante.get(est.id, {}).get("examen_final", "")
        })

    pct_autoeval = 5
    pct_examen = 20
    total_pct = sum(c["porcentaje"] for c in estructura) + pct_autoeval + pct_examen

    return render_template(
        "docentes/planilla.html",
        grupo=grupo,
        materia=materia,
        periodo=periodo,
        estructura=estructura,
        estudiantes=estudiantes,
        pct_autoeval=pct_autoeval,
        pct_examen=pct_examen,
        total_pct=total_pct,
        puede_editar=puede_editar,
        tipo_captura=tipo_captura
    )