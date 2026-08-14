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
# PLANILLA DE CALIFICACIONES POR COMPETENCIAS
# ==========================================================
@docente_bp.route("/planilla/<int:grupo_id>/<int:materia_id>")
@login_required
def ver_planilla(grupo_id, materia_id):
    if current_user.rol not in ['docente', 'coordinador']:
        abort(403)

    try:
        # 1. Datos Básicos
        grupo = Grupo.query.get_or_404(grupo_id)
        materia = Materia.query.get_or_404(materia_id)

        estudiantes = Estudiante.query.filter_by(
            grupo_id=grupo_id, activo=True
        ).order_by(Estudiante.apellido, Estudiante.nombre).all()

        periodo_actual = PeriodoAcademico.query.filter_by(
            colegio_id=current_user.colegio_id, activo=True
        ).first()
        periodo_id = periodo_actual.id if periodo_actual else None

        # 2. ✅ CONSTRUCCIÓN CORRECTA DE ESTRUCTURA (Competencias + Indicadores)
        competencias = CompetenciaEstudiante.query.filter_by(
            materia_id=materia_id
        ).order_by(CompetenciaEstudiante.codigo).all()

        estructura = []
        for comp in competencias:
            # Buscar indicadores hijos para ESTA competencia específica
            inds = IndicadorLogro.query.filter_by(competencia_id=comp.id).all()
            estructura.append({
                'id': comp.id,
                'codigo': comp.codigo,
                'nombre': comp.nombre,
                'indicadores': inds  # Lista de objetos IndicadorLogro
            })

        # 3. Configuración de Columnas (Porcentajes)
        columnas_evaluacion = [
            {'tipo': 'fija', 'nombre': 'Autoeval', 'porcentaje': 5.0, 'clave': 'autoeval', 'es_fija': True},
            {'tipo': 'fija', 'nombre': 'Coeval', 'porcentaje': 20.0, 'clave': 'coeval', 'es_fija': True}
        ]

        num_competencias = len(competencias)
        porc_restante = 75.0
        porc_por_comp = round(porc_restante / num_competencias, 2) if num_competencias > 0 else 0

        for comp in competencias:
            columnas_evaluacion.append({
                'tipo': 'competencia',
                'nombre': comp.nombre[:20],
                'codigo': comp.codigo,
                'porcentaje': porc_por_comp,
                'id': comp.id,
                'clave': f'comp_{comp.id}',
                'es_fija': False
            })

        suma_total = sum(c['porcentaje'] for c in columnas_evaluacion)
        alerta_porcentaje = None
        if suma_total > 100:
            alerta_porcentaje = f"⚠️ Suma excede 100% ({suma_total}%)"
        elif suma_total < 100:
            alerta_porcentaje = f"ℹ️ Falta distribuir {round(100 - suma_total, 2)}%"

        # 4. Cargar Notas Existentes (EVAL_MAP)
        eval_map = {}
        if estudiantes and periodo_id:
            all_ind_ids = []
            for s in estructura:
                all_ind_ids.extend([i.id for i in s['indicadores']])

            if all_ind_ids:
                evaluaciones = EvaluacionEstudiante.query.filter(
                    EvaluacionEstudiante.estudiante_id.in_([e.id for e in estudiantes]),
                    EvaluacionEstudiante.indicador_id.in_(all_ind_ids),
                    EvaluacionEstudiante.periodo_id == periodo_id
                ).all()

                for ev in evaluaciones:
                    if ev.estudiante_id not in eval_map:
                        eval_map[ev.estudiante_id] = {}
                    val = getattr(ev, 'calificacion', None)
                    try:
                        eval_map[ev.estudiante_id][ev.indicador_id] = float(val) if val else 0
                    except:
                        pass

        # 5. Renderizar
        return render_template(
            "docentes/planilla.html",
            grupo=grupo,
            materia=materia,
            estudiantes=estudiantes,
            estructura=estructura,  # ✅ VARIABLE CLAVE
            columnas_evaluacion=columnas_evaluacion,
            eval_map=eval_map,
            periodo=periodo_actual,
            suma_porcentajes=round(suma_total, 2),
            alerta_porcentaje=alerta_porcentaje
        )

    except Exception as e:
        print(f"Error en ver_planilla: {e}")
        import traceback;
        traceback.print_exc()
        flash(f"Error al cargar la planilla: {str(e)}", "danger")
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
# GESTIÓN DE COMPETENCIAS (VISTA INLINE)
# ============================================================
@docente_bp.route("/competencias", methods=["GET", "POST"])
@login_required
def gestionar_competencias():
    """Vista principal del docente para ver y crear competencias (Formulario Inline)."""

    # 1. Importaciones necesarias
    from app.models.periodo_academico import PeriodoAcademico
    from app.models.configuracion_periodo import ConfiguracionPeriodo
    from app.models.grupo_materia import GrupoMateria
    from app.models.materia import Materia
    from app.models.docente import Docente
    from app.models.grupo import Grupo
    from app.models.CompetenciaEstudiante import CompetenciaEstudiante
    from datetime import datetime

    # 2. Obtener Periodo Activo y Validar Estado
    periodo_actual = PeriodoAcademico.query.filter_by(
        colegio_id=current_user.colegio_id, activo=True
    ).first()

    if not periodo_actual:
        flash("No hay un periodo académico activo configurado.", "warning")
        return redirect(url_for('docente.dashboard'))

    config_periodo = ConfiguracionPeriodo.query.filter_by(
        colegio_id=current_user.colegio_id, periodo_id=periodo_actual.id
    ).first()

    # Verificar si está abierto para competencias
    periodo_abierto = (
        config_periodo and
        config_periodo.estado == 'ABIERTO' and
        config_periodo.permite_editar_competencias
    )

    # Validar fechas de cierre (Doble seguridad)
    if periodo_abierto and config_periodo.fecha_cierre:
        if datetime.now() > config_periodo.fecha_cierre:
            periodo_abierto = False
            flash("La fecha límite para editar competencias ha vencido.", "danger")

    # 3. Obtener Docente y Materias Asignadas
    docente_actual = Docente.query.filter_by(usuario_id=current_user.id).first()
    if not docente_actual:
        flash("No se encontró perfil de docente asociado.", "danger")
        return redirect(url_for('docente.dashboard'))

    asignaciones = db.session.query(
        GrupoMateria.materia_id, Grupo.grado, Materia.nombre.label('materia_nombre')
    ).join(Grupo, GrupoMateria.grupo_id == Grupo.id) \
        .join(Materia, GrupoMateria.materia_id == Materia.id) \
        .filter(GrupoMateria.docente_id == docente_actual.id, GrupoMateria.activo == True) \
        .distinct().order_by(Grupo.grado, Materia.nombre).all()

    materias_para_select = []
    seen = set()
    for row in asignaciones:
        key = (row.materia_id, row.grado)
        if key not in seen:
            seen.add(key)
            materias_para_select.append({
                'id': row.materia_id,
                'label': f"{row.materia_nombre} ({row.grado})"
            })

    materias_ids = [m['id'] for m in materias_para_select]

    # 4. Manejo del POST (Creación Inline)
    if request.method == "POST":
        if not periodo_abierto:
            flash("El periodo está cerrado para edición de competencias.", "warning")
            return redirect(url_for('docente.gestionar_competencias'))

        materia_id = request.form.get("materia_id", type=int)
        descripcion_completa = request.form.get("descripcion", "").strip()
        nivel_educativo = request.form.get("nivel_educativo", "").strip()

        # ✅ CORRECCIÓN: Truncar nombre a 145 chars + "..." si excede 150
        nombre_corto = descripcion_completa[:145] + "..." if len(descripcion_completa) > 150 else descripcion_completa

        # Validación exacta
        if not all([materia_id, nombre_corto, nivel_educativo]):
            flash("Materia, nombre y nivel educativo son obligatorios.", "danger")
            return redirect(url_for('docente.gestionar_competencias'))

        try:
            # Generar Código usando tu función existente
            nuevo_codigo = generar_codigo_competencia(materia_id, nivel_educativo)

            # ✅ CREAR COMPETENCIA SIN periodo_id Y CON NOMBRE TRUNCADO
            nueva_competencia = CompetenciaEstudiante(
                materia_id=materia_id,
                nombre=nombre_corto,              # Texto seguro (<150 chars)
                codigo=nuevo_codigo,
                nivel_educativo=nivel_educativo,
                descripcion=descripcion_completa, # Texto completo en campo TEXT
                porcentaje=0.0
            )
            db.session.add(nueva_competencia)
            db.session.commit()
            flash(f"✅ Competencia creada exitosamente con código: {nuevo_codigo}", "success")

        except ValueError as e:
            flash(str(e), "danger")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al guardar: {str(e)}", "danger")
            print(f"ERROR DB: {e}")

        return redirect(url_for('docente.gestionar_competencias'))

    # 5. GET: Listar competencias
    competencias = CompetenciaEstudiante.query.filter(
        CompetenciaEstudiante.materia_id.in_(materias_ids)
    ).order_by(CompetenciaEstudiante.codigo).all() if materias_ids else []

    return render_template(
        "docentes/gestion_competencias.html",
        periodo_actual=periodo_actual,
        periodo_abierto=periodo_abierto,
        materias_para_select=materias_para_select,
        competencias=competencias
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