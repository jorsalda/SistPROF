# ==========================================================
# ESTUDIANTES ROUTES - SistPROF (CORREGIDO)
# ==========================================================
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from sqlalchemy import or_
import secrets
from app.utils.permisos import requiere_permiso
from datetime import datetime

from app.extensions import db
from app.models.usuario import Usuario
from app.models.estudiante import Estudiante
from app.models.docente import Docente
from app.models.sede import Sede
from app.models.jornada import Jornada
from app.models.grupo import Grupo
from app.models.acudiente import Acudiente
from app.models.clase import Clase
from app.models.clase_estudiante import ClaseEstudiante
from app.models.grupo_materia import GrupoMateria
from app.models.examen import Examen, ProgramacionExamen
from app.models.resultado_examen import ResultadoExamen
from app.models.respuestas_examen_detalle import RespuestaExamenDetalle
from app.models.evaluacion_estudiante import EvaluacionEstudiante
from app.models.indicador_logro import IndicadorLogro
from app.models.CompetenciaEstudiante import CompetenciaEstudiante
from app.models.materia import Materia
from app.models.periodo_academico import PeriodoAcademico
from app.models.diagnostico_estudiante import DiagnosticoEstudiante

# ✅ CORRECCIÓN CRÍTICA: EL BLUEPRINT DEBE DEFINIRSE ANTES DE CUALQUIER RUTA
estudiante_bp = Blueprint(
    "estudiante",
    __name__,
    url_prefix="/estudiantes"
)


# ==========================================================
# DASHBOARD ESTUDIANTE
# ==========================================================
@estudiante_bp.route('/dashboard')
@login_required
def dashboard_estudiante():
    if current_user.rol != 'estudiante':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante:
        flash('Perfil no encontrado', 'warning')
        return redirect(url_for('auth.logout'))

    from app.models.resultado_examen import ResultadoExamen
    from app.models.diagnostico_estudiante import DiagnosticoEstudiante
    from datetime import datetime

    ultimos_resultados = ResultadoExamen.query.filter_by(
        estudiante_id=estudiante.id
    ).order_by(ResultadoExamen.fecha_finalizacion.desc()).limit(5).all()

    total_examenes = ResultadoExamen.query.filter_by(estudiante_id=estudiante.id).count()

    notas_validas = [r.nota_numerica for r in ultimos_resultados if r.nota_numerica is not None]
    promedio_general = round(sum(notas_validas) / len(notas_validas), 2) if notas_validas else '-'
    mejor_nota = max(notas_validas) if notas_validas else '-'

    # 👇 CONTAMOS LOS DIAGNÓSTICOS PARA MOSTRAR UN RESUMEN EN EL DASHBOARD
    total_diagnosticos = DiagnosticoEstudiante.query.filter_by(estudiante_id=estudiante.id).count()

    hoy = datetime.now()

    return render_template(
        'estudiantes/dashboard.html',
        estudiante=estudiante,
        total_examenes=total_examenes,
        promedio_general=promedio_general,
        mejor_nota=mejor_nota,
        ultimos_resultados=ultimos_resultados,
        total_diagnosticos=total_diagnosticos, # 👈 ENVIAMOS EL CONTEO
        hoy=hoy
    )

# ==========================================================
# VER DETALLE DEL ESTUDIANTE (Solo para el estudiante logueado)
# ==========================================================
@estudiante_bp.route('/mi-detalle')
@login_required
def mi_detalle():
    """Vista de detalle exclusiva para el estudiante (ve su propia información)."""
    if current_user.rol != 'estudiante':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante:
        flash('Perfil no encontrado', 'warning')
        return redirect(url_for('auth.logout'))

    asistencias_recientes = estudiante.asistencias[-10:] if hasattr(estudiante, "asistencias") and estudiante.asistencias else []
    novedades_recientes = estudiante.novedades[-10:] if hasattr(estudiante, "novedades") and estudiante.novedades else []
    tiene_piar = estudiante.tiene_piar_activo()

    return render_template(
        "estudiantes/detalle.html",  # 👈 ESTO ES LO QUE DEBE APUNTAR A LA IMAGEN 2
        estudiante=estudiante,
        asistencias=asistencias_recientes,
        novedades=novedades_recientes,
        tiene_piar=tiene_piar
    )


@estudiante_bp.route('/mi-perfil')
@login_required
def mi_perfil():
    """Vista unificada del perfil del estudiante (datos, QR, asistencias, novedades)."""
    if current_user.rol != 'estudiante':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante:
        flash('Perfil no encontrado', 'warning')
        return redirect(url_for('auth.logout'))

    from app.models.diagnostico_estudiante import DiagnosticoEstudiante
    diagnosticos = DiagnosticoEstudiante.query.filter_by(estudiante_id=estudiante.id).all()

    # 👇 LÍNEAS DE DIAGNÓSTICO
    print(f"🔍 DIAGNÓSTICOS ENCONTRADOS: {len(diagnosticos)}")
    for d in diagnosticos:
        print(f"🔍 - {d.descripcion}")

    # Traemos asistencias y novedades para la vista unificada
    asistencias = estudiante.asistencias[-10:] if hasattr(estudiante, "asistencias") and estudiante.asistencias else []
    novedades = estudiante.novedades[-10:] if hasattr(estudiante, "novedades") and estudiante.novedades else []

    return render_template(
        'estudiantes/mi_perfil.html',
        estudiante=estudiante,
        diagnosticos=diagnosticos,
        asistencias=asistencias,
        novedades=novedades
    )

# ==========================================================
# MIS CALIFICACIONES POR COMPETENCIA E INDICADOR
# ==========================================================
@estudiante_bp.route('/mis-calificaciones')
@login_required
def mis_calificaciones():
    """Vista de calificaciones del estudiante con tooltips coherentes."""
    if current_user.rol != 'estudiante':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante:
        flash('Perfil no encontrado', 'warning')
        return redirect(url_for('auth.logout'))

    # Obtener solo el periodo activo del colegio
    periodo_activo = PeriodoAcademico.query.filter_by(
        colegio_id=estudiante.colegio_id,
        activo=True
    ).first()

    if not periodo_activo:
        flash('No hay un periodo académico activo.', 'warning')
        return render_template(
            'estudiantes/mis_calificaciones.html',
            estudiante=estudiante,
            calificaciones={}
        )

    # Consulta JOIN filtrada por periodo activo
    evaluaciones = db.session.query(
        EvaluacionEstudiante, IndicadorLogro, CompetenciaEstudiante, Materia, PeriodoAcademico
    ).join(
        IndicadorLogro, EvaluacionEstudiante.indicador_id == IndicadorLogro.id
    ).join(
        CompetenciaEstudiante, IndicadorLogro.competencia_materia_id == CompetenciaEstudiante.id
    ).join(
        Materia, CompetenciaEstudiante.materia_id == Materia.id
    ).join(
        PeriodoAcademico, EvaluacionEstudiante.periodo_id == PeriodoAcademico.id
    ).filter(
        EvaluacionEstudiante.estudiante_id == estudiante.id,
        EvaluacionEstudiante.periodo_id == periodo_activo.id
    ).order_by(
        Materia.nombre,
        CompetenciaEstudiante.codigo,
        IndicadorLogro.orden
    ).all()

    # ESTRUCTURA LIMPIA
    calificaciones_por_periodo = {}

    for ev, ind, comp, mat, per in evaluaciones:
        pn = per.nombre
        mn = mat.nombre
        cc = comp.codigo
        cn = comp.nombre

        if pn not in calificaciones_por_periodo:
            calificaciones_por_periodo[pn] = {}

        if mn not in calificaciones_por_periodo[pn]:
            calificaciones_por_periodo[pn][mn] = type('MateriaObj', (), {
                'materia_id': mat.id,
                'competencias': {},
                'definitiva': 0.0
            })()

        if cc not in calificaciones_por_periodo[pn][mn].competencias:
            calificaciones_por_periodo[pn][mn].competencias[cc] = type('CompObj', (), {
                'nombre': cn,
                'indicadores': [],
                'promedio': None,
                'nivel': '',
                'enunciado_nivel': ''
            })()

        nota = float(ev.calificacion) if ev.calificacion is not None else None

        # ✅ FIX: Asegurar que la nota se asocie al indicador exacto
        calificaciones_por_periodo[pn][mn].competencias[cc].indicadores.append({
            'codigo': ind.codigo,
            'descripcion': ind.descripcion[:80] + '...' if len(ind.descripcion) > 80 else ind.descripcion,
            'nota': nota,
            'nivel_desempeño': getattr(ev, 'nivel_desempeño', None),
            'observacion': ev.observacion
        })

    # Calcular promedios y enunciados EXACTOS
    for periodo in calificaciones_por_periodo.values():
        for materia in periodo.values():
            def_suma = 0.0
            def_cuenta = 0

            for comp in materia.competencias.values():
                notas_validas = [i['nota'] for i in comp.indicadores if i['nota'] is not None]

                if notas_validas:
                    # ✅ FIX: Tomar la nota más alta de los indicadores (la que puso el docente)
                    # en lugar de promediar indicadores vacíos con ceros.
                    comp.promedio = max(notas_validas)
                    p = comp.promedio

                    # Asignar nivel cualitativo
                    if p >= 4.5:
                        comp.nivel = 'Superior'
                    elif p >= 3.0:
                        comp.nivel = 'Alto'
                    elif p >= 2.0:
                        comp.nivel = 'Básico'
                    else:
                        comp.nivel = 'Bajo'

                    # ✅ LÓGICA ESTRICTA: Buscar SOLO el indicador con nivel_desempeño exacto
                    enunciado_encontrado = ''
                    for ind_data in comp.indicadores:
                        # Comparación exacta de strings (case-sensitive)
                        if ind_data.get('nivel_desempeño') == comp.nivel and ind_data.get('descripcion'):
                            enunciado_encontrado = ind_data['descripcion']
                            break  # Salir al encontrar el primero

                    # Si no hay coincidencia exacta, dejar vacío (no mezclar)
                    comp.enunciado_nivel = enunciado_encontrado

                    def_suma += p
                    def_cuenta += 1
                else:
                    comp.promedio = None
                    comp.nivel = ''
                    comp.enunciado_nivel = ''

            materia.definitiva = round(def_suma / def_cuenta, 2) if def_cuenta > 0 else 0.0

    return render_template(
        'estudiantes/mis_calificaciones.html',
        estudiante=estudiante,
        calificaciones=calificaciones_por_periodo
    )

# ==========================================================
# MI HORARIO
# ==========================================================
@estudiante_bp.route('/mi-horario')
@login_required
def mi_horario():
    """Vista del horario del grupo del estudiante."""
    if current_user.rol != 'estudiante':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante:
        flash('Perfil no encontrado', 'warning')
        return redirect(url_for('auth.logout'))

    # Si no tiene grupo, no hay horario que mostrar
    if not estudiante.grupo_id:
        flash('No tienes un grupo académico asignado.', 'warning')
        return redirect(url_for('estudiante.dashboard_estudiante'))

    # Consultar clases del grupo del estudiante
    clases = db.session.query(Clase).join(
        GrupoMateria, Clase.grupo_materia_id == GrupoMateria.id
    ).filter(
        GrupoMateria.grupo_id == estudiante.grupo_id,
        Clase.colegio_id == estudiante.colegio_id,
        Clase.activo == True
    ).order_by(
        Clase.dia,
        Clase.hora_inicio
    ).all()

    # Agrupar por día
    dias_orden = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes']
    horario = {dia: [] for dia in dias_orden}

    for clase in clases:
        # clase.dia es un enum DiaSemana (ej. DiaSemana.LUNES)
        dia_valor = clase.dia.value if hasattr(clase.dia, 'value') else str(clase.dia)

        horario[dia_valor].append({
            'hora_inicio': clase.hora_inicio.strftime('%H:%M'),
            'hora_fin': clase.hora_fin.strftime('%H:%M'),
            'materia': clase.nombre_materia,
            'docente': clase.docente.nombre_completo if clase.docente else 'Sin asignar',
            'grupo': clase.nombre_grupo,
        })

    return render_template(
        'estudiantes/mi_horario.html',
        estudiante=estudiante,
        horario=horario
    )
# ==========================================================
# MI ASISTENCIA
# ==========================================================
@estudiante_bp.route('/mi-asistencia')
@login_required
def mi_asistencia():
    """Vista de asistencia del estudiante con consolidado y detalle."""
    if current_user.rol != 'estudiante':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante:
        flash('Perfil no encontrado', 'warning')
        return redirect(url_for('auth.logout'))

    from app.models.asistencia import Asistencia

    # Traer todas las asistencias del estudiante
    asistencias = Asistencia.query.filter_by(
        estudiante_id=estudiante.id
    ).order_by(Asistencia.fecha.desc()).all()

    # Consolidado
    total = len(asistencias)
    presentes = sum(1 for a in asistencias if a.estado == 'presente')
    tardes = sum(1 for a in asistencias if a.estado == 'tarde')
    ausentes = sum(1 for a in asistencias if a.estado == 'ausente')
    porcentaje = round((presentes / total) * 100, 1) if total > 0 else 0.0

    # Detalle: últimos 50
    detalle = asistencias[:50]

    return render_template(
        'estudiantes/mi_asistencia.html',
        estudiante=estudiante,
        total=total,
        presentes=presentes,
        tardes=tardes,
        ausentes=ausentes,
        porcentaje=porcentaje,
        detalle=detalle
    )

# ==========================================================
# MI OBSERVADOR
# ==========================================================
@estudiante_bp.route('/mi-observador')
@login_required
def mi_observador():
    """Vista del observador del estudiante: novedades + respuestas."""
    if current_user.rol != 'estudiante':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante:
        flash('Perfil no encontrado', 'warning')
        return redirect(url_for('auth.logout'))

    from app.models.novedad import Novedad

    novedades = Novedad.query.filter_by(
        estudiante_id=estudiante.id
    ).order_by(Novedad.fecha.desc(), Novedad.hora.desc()).all()

    return render_template(
        'estudiantes/mi_observador.html',
        estudiante=estudiante,
        novedades=novedades
    )


# ==========================================================
# MIS CITACIONES
# ==========================================================
@estudiante_bp.route('/mis-citaciones')
@login_required
def mis_citaciones():
    """Vista de citaciones del estudiante (solo lectura)."""
    if current_user.rol != 'estudiante':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante:
        flash('Perfil no encontrado', 'warning')
        return redirect(url_for('auth.logout'))

    from app.models.citacion_acudiente import CitacionAcudiente

    citaciones = CitacionAcudiente.query.filter_by(
        estudiante_id=estudiante.id
    ).order_by(CitacionAcudiente.fecha_citacion.desc()).all()

    return render_template(
        'estudiantes/mis_citaciones.html',
        estudiante=estudiante,
        citaciones=citaciones
    )

# ==========================================================
# MI PIAR
# ==========================================================
@estudiante_bp.route('/mi-piar')
@login_required
def mi_piar():
    """Vista del PIAR activo del estudiante."""
    if current_user.rol != 'estudiante':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante:
        flash('Perfil no encontrado', 'warning')
        return redirect(url_for('auth.logout'))

    from app.models.piar import PIAR
    from app.extensions import db

    # 👇 USAMOS SQL DIRECTO PARA ASEGURAR QUE EL DATO LLEGUE
    piar_activo = db.session.execute(
        db.text("SELECT id FROM piar WHERE estudiante_id = :est_id AND activo = true LIMIT 1"),
        {"est_id": estudiante.id}
    ).scalar()

    piar_obj = None
    if piar_activo:
        piar_obj = PIAR.query.get(piar_activo)

    # 👇 PRINT DE DIAGNÓSTICO
    print(f"🔍 ESTUDIANTE: {estudiante.nombre} (ID: {estudiante.id})")
    print(f"🔍 PIAR OBJ: {piar_obj}")

    return render_template(
        'estudiantes/mi_piar.html',
        estudiante=estudiante,
        piar=piar_obj
    )




# =========================================================
# LISTAR ESTUDIANTES
# =========================================================
@estudiante_bp.route("/")
@login_required
@requiere_permiso('secretaria.ver_estudiantes')
def listar():
    search = request.args.get('search', '').strip()
    sede_id = request.args.get('sede_id', type=int)
    grado = request.args.get('grado', '').strip()
    grupo_id = request.args.get('grupo_id', type=int)

    consulta = Estudiante.query.filter_by(colegio_id=current_user.colegio_id, activo=True)
    if search: consulta = consulta.filter(or_(Estudiante.nombre.ilike(f"%{search}%"), Estudiante.apellido.ilike(f"%{search}%")))
    if sede_id: consulta = consulta.filter_by(sede_id=sede_id)
    if grado: consulta = consulta.filter_by(grado=grado)
    if grupo_id: consulta = consulta.filter_by(grupo_id=grupo_id)

    estudiantes = consulta.order_by(Estudiante.nombre).all()

    # 👇 CREAMOS UN DICCIONARIO PARA SABER QUIÉN TIENE DIAGNÓSTICOS
    from app.models.diagnostico_estudiante import DiagnosticoEstudiante
    ids_estudiantes = [e.id for e in estudiantes]
    ids_con_diagnostico = set()
    if ids_estudiantes:
        diagnosticos_existentes = DiagnosticoEstudiante.query.filter(
            DiagnosticoEstudiante.estudiante_id.in_(ids_estudiantes)
        ).all()
        ids_con_diagnostico = {d.estudiante_id for d in diagnosticos_existentes}

    sedes = Sede.query.filter_by(colegio_id=current_user.colegio_id, activo=True).order_by(Sede.nombre).all()
    grupos = Grupo.query.filter_by(colegio_id=current_user.colegio_id, activo=True).order_by(Grupo.grado, Grupo.nombre).all()
    grados_unicos = db.session.query(Estudiante.grado).filter_by(colegio_id=current_user.colegio_id, activo=True).distinct().order_by(Estudiante.grado).all()
    grados_lista = [g[0] for g in grados_unicos if g[0]]

    layout = "secretaria/secretaria_base.html" if current_user.rol == 'secretaria' else "psicologo/psicologo_base.html" if current_user.rol == 'psicologo' else "coordinador/coordinador_base.html" if current_user.rol == 'coordinador' else "docentes/docente_base.html" if current_user.rol == 'docente' else "colegio/colegio_base.html"

    return render_template(
        "estudiantes/listado.html",
        estudiantes=estudiantes,
        sedes=sedes,
        grupos=grupos,
        grados_lista=grados_lista,
        current_sede_id=sede_id,
        current_grado=grado,
        current_grupo_id=grupo_id,
        layout=layout,
        ids_con_diagnostico=ids_con_diagnostico # 👈 ENVIAMOS LOS IDs
    )


# =========================================================
# API: OBTENER JORNADAS POR SEDE
# =========================================================
@estudiante_bp.route("/api/jornadas/<int:sede_id>")
@login_required
def api_jornadas_por_sede(sede_id):
    jornadas = Jornada.query.filter_by(
        sede_id=sede_id,
        colegio_id=current_user.colegio_id,
        activo=True
    ).order_by(Jornada.nombre).all()

    return jsonify([{"id": j.id, "nombre": j.nombre} for j in jornadas])


# =========================================================
# NUEVO ESTUDIANTE
# =========================================================
@estudiante_bp.route("/nuevo", methods=["GET", "POST"])
@requiere_permiso('secretaria.crear_estudiantes')
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
        acudiente_principal_id = request.form.get("acudiente_principal_id", type=int)

        campos_requeridos = {
            "nombre": nombre, "apellido": apellido, "tipo_documento": tipo_documento,
            "documento": documento, "email": email, "direccion": direccion,
            "telefono": telefono, "grupo_id": grupo_id, "acudiente_principal_id": acudiente_principal_id
        }

        for campo, valor in campos_requeridos.items():
            if not valor:
                flash(f"El campo '{campo.replace('_', ' ').title()}' es requerido", "danger")
                return redirect(url_for("estudiante.nuevo"))

        if Usuario.query.filter_by(email=email).first():
            flash("El correo electrónico ya está registrado", "danger")
            return redirect(url_for("estudiante.nuevo"))

        if Estudiante.query.filter_by(documento=documento, colegio_id=current_user.colegio_id).first():
            flash("Ya existe un estudiante con ese documento", "danger")
            return redirect(url_for("estudiante.nuevo"))

        grupo_obj = Grupo.query.filter_by(id=grupo_id, colegio_id=current_user.colegio_id).first()
        if not grupo_obj:
            flash("Grupo no válido", "danger")
            return redirect(url_for("estudiante.nuevo"))

        qr_token = f"EST-{current_user.colegio_id}-{secrets.token_hex(8).upper()}"

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
        db.session.flush()

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
            sede_id=(sede_id if sede_id else grupo_obj.sede_id),
            jornada_id=(jornada_id if jornada_id else grupo_obj.jornada_id),
            docente_id=docente_id,
            qr_token=qr_token,
            activo=True
        )
        db.session.add(estudiante)

        clases_del_grupo = db.session.query(Clase).join(
            GrupoMateria, Clase.grupo_materia_id == GrupoMateria.id
        ).filter(
            GrupoMateria.grupo_id == grupo_obj.id,
            Clase.activo == True,
            GrupoMateria.activo == True
        ).all()

        clases_matriculadas = 0
        for clase in clases_del_grupo:
            if not ClaseEstudiante.query.filter_by(clase_id=clase.id, estudiante_id=estudiante.id).first():
                db.session.add(ClaseEstudiante(clase_id=clase.id, estudiante_id=estudiante.id))
                clases_matriculadas += 1

        db.session.commit()

        flash(
            f"Estudiante '{nombre} {apellido}' registrado. Matriculado en {clases_matriculadas} clases. "
            f"Usuario: {email} | Clave: {documento}",
            "success"
        )
        return redirect(url_for("estudiante.listar"))

    sedes = Sede.query.filter_by(colegio_id=current_user.colegio_id, activo=True).all()
    jornadas = Jornada.query.filter_by(colegio_id=current_user.colegio_id, activo=True).all()
    docentes = Docente.query.filter_by(colegio_id=current_user.colegio_id, activo=True).all()
    grupos = Grupo.query.filter_by(colegio_id=current_user.colegio_id, activo=True).order_by(Grupo.grado,
                                                                                             Grupo.nombre).all()
    acudientes = Acudiente.query.filter_by(colegio_id=current_user.colegio_id).order_by(Acudiente.nombre).all()

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
@requiere_permiso('secretaria.editar_estudiantes')
@login_required
def editar(id):
    estudiante = Estudiante.query.filter_by(id=id, colegio_id=current_user.colegio_id).first_or_404()

    if request.method == "POST":
        print("🔥 DATOS RECIBIDOS:", request.form.to_dict())
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        grupo_id = request.form.get("grupo_id", type=int)
        sede_id = request.form.get("sede_id", type=int)
        jornada_id = request.form.get("jornada_id", type=int)
        docente_id = request.form.get("docente_id", type=int)
        direccion = request.form.get("direccion", "").strip()
        telefono = request.form.get("telefono", "").strip()
        acudiente_principal_id = request.form.get("acudiente_principal_id", type=int)

        tipo_documento = request.form.get("tipo_documento", "").strip()
        documento = request.form.get("documento", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        # 👇 CAPTURAR DIAGNÓSTICOS (texto multilínea del formulario)
        diagnosticos_texto = request.form.get("diagnosticos", "").strip()
        requiere_piar = request.form.get("requiere_piar") == "on"

        if not nombre or not apellido or not grupo_id:
            flash("Nombre, apellido y grupo son obligatorios", "danger")
            return redirect(url_for("estudiante.editar", id=id))

        grupo_obj = Grupo.query.filter_by(id=grupo_id, colegio_id=current_user.colegio_id).first()
        if not grupo_obj:
            flash("Grupo no válido", "danger")
            return redirect(url_for("estudiante.editar", id=id))

        # Actualizar datos básicos
        estudiante.nombre = nombre
        estudiante.apellido = apellido
        estudiante.direccion = direccion if direccion else estudiante.direccion
        estudiante.telefono = telefono if telefono else estudiante.telefono
        estudiante.acudiente_principal_id = acudiente_principal_id if acudiente_principal_id else estudiante.acudiente_principal_id
        estudiante.grupo_id = grupo_obj.id
        estudiante.sede_id = (sede_id if sede_id else grupo_obj.sede_id)
        estudiante.jornada_id = (jornada_id if jornada_id else grupo_obj.jornada_id)
        estudiante.docente_id = docente_id
        estudiante.tipo_documento = tipo_documento if tipo_documento else estudiante.tipo_documento
        estudiante.documento = documento if documento else estudiante.documento
        estudiante.requiere_piar = requiere_piar

        # Actualizar correo
        if email:
            estudiante.email = email
            if estudiante.usuario:
                estudiante.usuario.email = email

        # Actualizar contraseña
        if password and estudiante.usuario:
            from werkzeug.security import generate_password_hash
            estudiante.usuario.password_hash = generate_password_hash(password)

        if 'activo' in request.form:
            estudiante.activo = request.form.get("activo") == "on"

        try:
            db.session.commit()  # Guarda datos del estudiante

            # 👇 AGREGUE ESTAS LÍNEAS AQUÍ
            from app.models.diagnostico_estudiante import DiagnosticoEstudiante
            if diagnosticos_texto:
                for linea in diagnosticos_texto.split('\n'):
                    if linea.strip():
                        db.session.add(DiagnosticoEstudiante(estudiante_id=estudiante.id, descripcion=linea.strip()))
            # 👆 FIN DE LO QUE DEBE AGREGAR

            db.session.commit()  # Guarda los diagnósticos
            flash(f"Estudiante '{nombre} {apellido}' actualizado", "success")
            return redirect(url_for("estudiante.listar"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar: {str(e)}", "danger")
            return redirect(url_for("estudiante.editar", id=id))

    sedes = Sede.query.filter_by(colegio_id=current_user.colegio_id, activo=True).all()
    jornadas = Jornada.query.filter_by(colegio_id=current_user.colegio_id, activo=True).all()
    docentes = Docente.query.filter_by(colegio_id=current_user.colegio_id, activo=True).all()
    grupos = Grupo.query.filter_by(colegio_id=current_user.colegio_id, activo=True).order_by(Grupo.grado,
                                                                                             Grupo.nombre).all()
    acudientes = Acudiente.query.filter_by(colegio_id=current_user.colegio_id).order_by(Acudiente.nombre).all()

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
@requiere_permiso('secretaria.eliminar_estudiantes')
@login_required
def eliminar(id):
    estudiante = Estudiante.query.filter_by(id=id, colegio_id=current_user.colegio_id).first_or_404()
    nombre = estudiante.nombre

    tiene_historial = (
            (hasattr(estudiante, "asistencias") and len(estudiante.asistencias) > 0) or
            (hasattr(estudiante, "novedades") and len(estudiante.novedades) > 0) or
            (hasattr(estudiante, "evaluaciones") and len(estudiante.evaluaciones) > 0)
    )

    if tiene_historial:
        estudiante.activo = False
        db.session.commit()
        flash(f"Estudiante '{nombre}' desactivado (tiene historial)", "warning")
    else:
        db.session.delete(estudiante)
        db.session.commit()
        flash(f"Estudiante '{nombre}' eliminado", "success")

    return redirect(url_for("estudiante.listar"))


# =========================================================
# VER DETALLE
# =========================================================
@estudiante_bp.route("/ver/<int:id>")
@requiere_permiso('secretaria.ver_estudiantes')
@login_required
def ver(id):
    estudiante = Estudiante.query.filter_by(id=id, colegio_id=current_user.colegio_id).first_or_404()

    asistencias_recientes = estudiante.asistencias[-10:] if hasattr(estudiante,
                                                                    "asistencias") and estudiante.asistencias else []
    novedades_recientes = estudiante.novedades[-10:] if hasattr(estudiante,
                                                                "novedades") and estudiante.novedades else []
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
@requiere_permiso('secretaria.editar_estudiantes')
@login_required
def cambiar_estado(id):
    estudiante = Estudiante.query.filter_by(id=id, colegio_id=current_user.colegio_id).first_or_404()
    estudiante.activo = not estudiante.activo
    db.session.commit()

    estado = "activado" if estudiante.activo else "desactivado"
    return jsonify({"success": True, "message": f"Estudiante {estado}", "activo": estudiante.activo})


# =========================================================
# REGENERAR QR
# =========================================================
@estudiante_bp.route("/regenerar-qr/<int:id>", methods=["POST"])
@login_required
def regenerar_qr(id):
    estudiante = Estudiante.query.filter_by(id=id, colegio_id=current_user.colegio_id).first_or_404()
    nuevo_qr = estudiante.generar_qr_token()
    db.session.commit()
    return jsonify({"success": True, "qr_token": nuevo_qr, "message": "QR regenerado"})


# =========================================================
# BUSCAR POR QR
# =========================================================
@estudiante_bp.route("/buscar-qr/<token>")
@login_required
def buscar_por_qr(token):
    estudiante = Estudiante.query.filter_by(qr_token=token, colegio_id=current_user.colegio_id).first()
    if estudiante:
        return jsonify({
            "success": True,
            "estudiante": {
                "id": estudiante.id,
                "nombre": estudiante.nombre,
                "grupo": (estudiante.grupo.nombre if estudiante.grupo else "")
            }
        })
    return jsonify({"success": False, "message": "Estudiante no encontrado"}), 404


# =========================================================
# ASISTENCIA RÁPIDA
# =========================================================
@estudiante_bp.route("/asistencia-rapida", methods=["GET", "POST"])
@login_required
def asistencia_rapida():
    if request.method == "POST":
        qr_token = request.form.get("qr_token", "").strip()
        estado = request.form.get("estado", "presente")

        if not qr_token:
            flash("Token QR no válido", "danger")
            return redirect(url_for("estudiante.asistencia_rapida"))

        estudiante = Estudiante.query.filter_by(qr_token=qr_token, colegio_id=current_user.colegio_id).first()
        if not estudiante:
            flash("Estudiante no encontrado", "danger")
            return redirect(url_for("estudiante.asistencia_rapida"))

        try:
            from app.models.asistencia import Asistencia
            db.session.add(Asistencia(
                estudiante_id=estudiante.id,
                clase_id=None,
                fecha=datetime.now().date(),
                estado=estado,
                registrada_por=current_user.id
            ))
            db.session.commit()
            flash(f"Asistencia registrada: {estudiante.nombre}", "success")
        except ImportError:
            flash("Módulo de asistencias no configurado", "warning")

        return redirect(url_for("estudiante.asistencia_rapida"))

    return render_template("estudiantes/asistencia_rapida.html")


# =========================================================
# MOTOR INGENIOS
# =========================================================
@estudiante_bp.route("/ingenios")
@login_required
def ingenios():
    return render_template("estudiantes/ingenios.html")


# =========================================================
# MIS RESULTADOS
# =========================================================
@estudiante_bp.route('/mis-resultados')
@login_required
def mis_resultados():
    if current_user.rol != 'estudiante':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante:
        flash('Perfil no encontrado', 'warning')
        return redirect(url_for('auth.logout'))

    resultados = db.session.query(
        ResultadoExamen,
        Examen.nombre.label('examen_nombre')
    ).join(Examen, ResultadoExamen.examen_id == Examen.id).filter(
        ResultadoExamen.estudiante_id == estudiante.id
    ).order_by(ResultadoExamen.fecha_finalizacion.desc()).all()

    return render_template('estudiantes/mis_resultados.html', estudiante=estudiante, resultados=resultados)


# =========================================================
# GESTIÓN DE ESTUDIANTES (ADMIN)
# =========================================================
@estudiante_bp.route("/gestion")
@login_required
def gestion_estudiantes():
    from app.services.estudiante_service import EstudianteService

    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    grado = request.args.get('grado', '').strip()
    grupo_id = request.args.get('grupo_id', type=int)

    resultado = EstudianteService.get_all_by_colegio(
        colegio_id=current_user.colegio_id,
        page=page, per_page=15,
        search=search if search else None,
        grado=grado if grado else None,
        grupo_id=grupo_id if grupo_id else None
    )

    estadisticas = EstudianteService.get_estadisticas(current_user.colegio_id)
    grupos = Grupo.query.filter_by(colegio_id=current_user.colegio_id, activo=True).order_by(Grupo.grado,
                                                                                             Grupo.nombre).all()

    grados_unicos = db.session.query(Estudiante.grado).filter_by(
        colegio_id=current_user.colegio_id, activo=True
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
# APIs AUXILIARES
# =========================================================
@estudiante_bp.route("/api/grupos/<int:sede_id>")
@login_required
def api_grupos_por_sede(sede_id):
    jornada_id = request.args.get("jornada", type=int)
    consulta = Grupo.query.filter_by(sede_id=sede_id, colegio_id=current_user.colegio_id, activo=True)
    if jornada_id:
        consulta = consulta.filter_by(jornada_id=jornada_id)

    grupos = consulta.order_by(Grupo.grado, Grupo.nombre).all()
    return jsonify([{"id": g.id, "grado": g.grado, "nombre": g.nombre} for g in grupos])


@estudiante_bp.route("/api/acudientes")
@login_required
def api_acudientes():
    acudientes = Acudiente.query.filter_by(colegio_id=current_user.colegio_id).order_by(Acudiente.nombre).all()
    return jsonify([{
        'id': a.id, 'nombre': a.nombre, 'telefono': a.telefono,
        'email': a.email, 'parentesco': a.parentesco
    } for a in acudientes])


@estudiante_bp.route("/api/estadisticas")
@login_required
def api_estadisticas():
    from app.services.estudiante_service import EstudianteService
    return jsonify(EstudianteService.get_estadisticas(current_user.colegio_id))


@estudiante_bp.route('/api/mis-materias')
@login_required
def mis_materias():
    if current_user.rol != 'estudiante':
        return jsonify({'error': 'No autorizado'}), 403

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

    materias = []
    if estudiante.grupo_id:
        grupo_materias = GrupoMateria.query.filter_by(grupo_id=estudiante.grupo_id, activo=True).all()
        materias_ids = [gm.materia_id for gm in grupo_materias if gm.materia_id]
        if materias_ids:
            materias = Materia.query.filter(Materia.id.in_(materias_ids)).all()

    return jsonify([{'id': m.id, 'nombre': m.nombre} for m in materias])


# =========================================================
# REGISTRO PÚBLICO
# =========================================================
@estudiante_bp.route("/registro-publico", methods=["GET", "POST"])
def registro_publico():
    COLEGIO_INDEPENDIENTE_ID = 46

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        email = request.form.get("email", "").strip().lower()
        documento = request.form.get("documento", "").strip()
        telefono = request.form.get("telefono", "").strip()
        direccion = request.form.get("direccion", "").strip()

        if not all([nombre, apellido, email, documento]):
            flash("Los campos marcados con * son obligatorios", "danger")
            return redirect(url_for("estudiante.registro_publico"))

        if Usuario.query.filter_by(email=email).first():
            flash("El correo ya está registrado", "danger")
            return redirect(url_for("estudiante.registro_publico"))

        if Estudiante.query.filter_by(documento=documento, colegio_id=COLEGIO_INDEPENDIENTE_ID).first():
            flash("Ya existe un estudiante con ese documento", "danger")
            return redirect(url_for("estudiante.registro_publico"))

        password_inicial = documento
        try:
            usuario_estudiante = Usuario(
                nombre=f"{nombre} {apellido}",
                email=email,
                password_hash=generate_password_hash(password_inicial),
                rol='estudiante',
                colegio_id=COLEGIO_INDEPENDIENTE_ID,
                sede_id=None,
                is_active=True,
                is_approved=True
            )
            db.session.add(usuario_estudiante)
            db.session.flush()

            estudiante = Estudiante(
                nombre=nombre,
                apellido=apellido,
                documento=documento,
                email=email,
                usuario_id=usuario_estudiante.id,
                telefono=telefono,
                direccion=direccion,
                colegio_id=COLEGIO_INDEPENDIENTE_ID,
                sede_id=17,
                jornada_id=48,
                acudiente_principal_id=23,
                grupo_id=None,
                docente_id=None,
                qr_token=f"EST-IND-{secrets.token_hex(8).upper()}",
                activo=True
            )
            db.session.add(estudiante)
            db.session.commit()

            flash(
                f"¡Registro exitoso!<br>📧 Email: <strong>{email}</strong><br>"
                f"🔑 Contraseña: <strong>{password_inicial}</strong>",
                "success"
            )
            return redirect(url_for("auth.login"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar: {str(e)}", "danger")
            return redirect(url_for("estudiante.registro_publico"))

    return render_template("estudiantes/registro_publico.html")


# =========================================================
# PRESENTAR EXAMEN (PUENTE PARA CLSESTUDIANTE)
# =========================================================
@estudiante_bp.route('/presentar-examen/<int:id>')
@login_required
def presentar_examen(id):
    if current_user.rol != 'estudiante':
        abort(403)

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante:
        abort(403)

    examen = Examen.query.get_or_404(id)

    ya_respondio = ResultadoExamen.query.filter_by(
        examen_id=id, estudiante_id=estudiante.id
    ).first()

    if ya_respondio:
        flash("Ya has presentado este examen.", "warning")
        return redirect(url_for('estudiante.mis_resultados'))

    return render_template(
        'estudiantes/examen_estudiante.html',
        examen_id=id
    )


# =========================================================
# GUARDAR RESPUESTA (CALIFICACIÓN AUTOMÁTICA)
# =========================================================
@estudiante_bp.route('/guardar-respuesta/<int:id>', methods=["POST"])
@login_required
def guardar_respuesta(id):
    if current_user.rol != 'estudiante':
        abort(403)

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante:
        abort(403)

    examen = Examen.query.get_or_404(id)

    if ResultadoExamen.query.filter_by(examen_id=id, estudiante_id=estudiante.id).first():
        flash("Ya has presentado este examen.", "warning")
        return redirect(url_for('estudiante.mis_resultados'))

    preguntas = examen.contenido_json or []
    if not preguntas:
        flash("Este examen no tiene preguntas.", "danger")
        return redirect(url_for('estudiante.examenes_disponibles'))

    respuestas_correctas = 0
    detalles = []

    for pregunta in preguntas:
        num = pregunta["numero"]
        respuesta_estudiante = request.form.get(f"pregunta_{num}") or ""
        es_correcta = respuesta_estudiante == pregunta.get("respuesta_correcta")

        if es_correcta:
            respuestas_correctas += 1

        detalles.append({
            "numero_pregunta": num,
            "texto_pregunta": pregunta.get("texto", ""),
            "respuesta_seleccionada": respuesta_estudiante,
            "respuesta_correcta": pregunta.get("respuesta_correcta", ""),
            "es_correcta": es_correcta,
            "indicador_logro_id": pregunta.get("indicador_logro_id")
        })

    total_preguntas = len(preguntas)
    porcentaje = (respuestas_correctas / total_preguntas) * 100
    nota_numerica = round((porcentaje / 100) * 5, 2)

    if porcentaje >= 90:
        literal = "S"
    elif porcentaje >= 80:
        literal = "A"
    elif porcentaje >= 70:
        literal = "B"
    elif porcentaje >= 60:
        literal = "b"
    else:
        literal = "I"

    resultado = ResultadoExamen(
        estudiante_id=estudiante.id,
        examen_id=id,
        materia_id=examen.materia_id,
        total_preguntas=total_preguntas,
        respuestas_correctas=respuestas_correctas,
        respuestas_incorrectas=(total_preguntas - respuestas_correctas),
        porcentaje=porcentaje,
        nota_numerica=nota_numerica,
        literal=literal,
        fecha_finalizacion=datetime.utcnow()
    )
    db.session.add(resultado)
    db.session.flush()

    for det in detalles:
        db.session.add(RespuestaExamenDetalle(resultado_examen_id=resultado.id, **det))

    # ==========================================================
    # EL PUENTE: Inyectar la nota en evaluaciones_estudiante
    # ==========================================================
    programacion = ProgramacionExamen.query.filter_by(
        examen_id=examen.id, grupo_id=estudiante.grupo_id, activo=True
    ).first()
    
    if programacion and programacion.competencia_materia_id:
        indicador = IndicadorLogro.query.filter_by(
            competencia_materia_id=programacion.competencia_materia_id
        ).order_by(IndicadorLogro.id).first()

        if indicador:
            from app.models.periodo_academico import PeriodoAcademico
            periodo_activo = PeriodoAcademico.query.filter_by(
                colegio_id=estudiante.colegio_id, activo=True
            ).first()
            
            periodo_id = periodo_activo.id if periodo_activo else None

            if periodo_id:
                ev = EvaluacionEstudiante.query.filter_by(
                    estudiante_id=estudiante.id,
                    indicador_id=indicador.id,
                    periodo_id=periodo_id
                ).first()

                if ev:
                    ev.calificacion = nota_numerica
                else:
                    db.session.add(EvaluacionEstudiante(
                        estudiante_id=estudiante.id,
                        indicador_id=indicador.id,
                        periodo_id=periodo_id,
                        calificacion=nota_numerica
                    ))

    db.session.commit()
    flash("Examen enviado, calificado y registrado en la planilla correctamente.", "success")
    return redirect(url_for('estudiante.mis_resultados'))


@estudiante_bp.route("/examenes-disponibles")
@login_required
def examenes_disponibles():
    if current_user.rol != 'estudiante':
        abort(403)

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante or not estudiante.grupo_id:
        flash("No tienes un grupo académico asignado.", "warning")
        return redirect(url_for('estudiante.dashboard'))

    ahora = datetime.now()

    examenes = Examen.query.join(ProgramacionExamen).filter(
        ProgramacionExamen.grupo_id == estudiante.grupo_id,
        ProgramacionExamen.activo == True,
        ProgramacionExamen.fecha_apertura <= ahora,
        ProgramacionExamen.fecha_cierre >= ahora,
        Examen.eliminado == False,
        Examen.contenido_json.isnot(None),
        Examen.activo == True
    ).order_by(ProgramacionExamen.fecha_apertura.desc()).all()

    resultados_previos = ResultadoExamen.query.filter_by(estudiante_id=estudiante.id).all()
    examenes_respondidos_ids = {r.examen_id for r in resultados_previos}

    return render_template(
        "estudiantes/examenes_disponibles.html",
        examenes=examenes,
        examenes_respondidos=examenes_respondidos_ids,
        resultados=resultados_previos
    )