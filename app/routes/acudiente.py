from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user

from app.services.acudiente_service import AcudienteService
from functools import wraps

acudiente_bp = Blueprint('acudiente', __name__, url_prefix='/acudiente')


def login_required_acudiente(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Por favor inicia sesión', 'warning')
            return redirect(url_for('auth.login'))

        if current_user.rol != 'acudiente':
            flash('No tienes acceso a esta sección', 'danger')
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)

    return decorated_function


@acudiente_bp.route('/')
@login_required_acudiente
def dashboard():
    """Dashboard principal del acudiente"""
    service = AcudienteService()
    user_id = current_user.id

    estudiantes = service.get_estudiantes_by_acudiente(user_id)
    novedades_recientes = service.get_novedades_recientes(estudiantes_ids=[e['id'] for e in estudiantes])
    citaciones_pendientes = service.get_citaciones_pendientes(estudiantes_ids=[e['id'] for e in estudiantes])

    return render_template('acudientes/dashboard_acudiente.html',
                           estudiantes=estudiantes,
                           novedades_recientes=novedades_recientes,
                           citaciones_pendientes=citaciones_pendientes)


@acudiente_bp.route('/mis-estudiantes')
@login_required_acudiente
def mis_estudiantes():
    """Lista de estudiantes a cargo"""
    service = AcudienteService()
    user_id = current_user.id
    estudiantes = service.get_estudiantes_by_acudiente(user_id)
    return render_template('acudientes/mis_estudiantes.html', estudiantes=estudiantes)


@acudiente_bp.route('/estudiante/<int:estudiante_id>')
@login_required_acudiente
def estudiante_detalle(estudiante_id):
    """Detalle completo de un estudiante (usa la vista simple para evitar errores)"""
    service = AcudienteService()
    user_id = current_user.id

    if not service.verificar_pertenencia(user_id, estudiante_id):
        flash('No tienes acceso a este estudiante', 'danger')
        return redirect(url_for('acudiente.mis_estudiantes'))

    estudiante = service.get_estudiante_info(estudiante_id)
    calificaciones = service.get_calificaciones(estudiante_id)
    promedio_general = service.get_promedio_general(estudiante_id)
    asistencia_stats = service.get_asistencia_stats(estudiante_id)

    return render_template('acudientes/detalle_estudiante.html',
                           estudiante=estudiante,
                           calificaciones=calificaciones,
                           promedio_general=promedio_general,
                           asistencia_stats=asistencia_stats)


@acudiente_bp.route('/calificaciones')
@login_required_acudiente
def calificaciones():
    """Vista de calificaciones de todos los estudiantes"""
    service = AcudienteService()
    user_id = current_user.id
    estudiantes = service.get_estudiantes_by_acudiente(user_id)

    for est in estudiantes:
        est['calificaciones'] = service.get_calificaciones(est['id'])

    return render_template('acudientes/calificaciones.html', estudiantes=estudiantes)


@acudiente_bp.route('/asistencia')
@login_required_acudiente
def asistencia():
    """Vista de asistencia de todos los estudiantes"""
    service = AcudienteService()
    user_id = current_user.id
    estudiantes = service.get_estudiantes_by_acudiente(user_id)

    for est in estudiantes:
        est['asistencia_stats'] = service.get_asistencia_stats(est['id'])
        est['asistencias'] = service.get_asistencias_recientes(est['id'])

    return render_template('acudientes/asistencia.html', estudiantes=estudiantes)


@acudiente_bp.route('/examenes')
@login_required_acudiente
def examenes():
    """Vista de exámenes de los estudiantes"""
    service = AcudienteService()
    user_id = current_user.id
    estudiantes = service.get_estudiantes_by_acudiente(user_id)

    for est in estudiantes:
        est['examenes'] = service.get_examenes_estudiante(est['id'])

    return render_template('acudientes/examenes.html', estudiantes=estudiantes)


@acudiente_bp.route('/novedades')
@login_required_acudiente
def novedades():
    """Vista de todas las novedades (AHORA SÍ ENVÍA LOS DATOS)"""
    service = AcudienteService()
    user_id = current_user.id
    estudiantes = service.get_estudiantes_by_acudiente(user_id)

    for est in estudiantes:
        est['novedades'] = service.get_novedades_estudiante(est['id'])

    return render_template('acudientes/novedades.html', estudiantes=estudiantes)


@acudiente_bp.route('/citaciones')
@login_required_acudiente
def citaciones():
    """Vista de todas las citaciones"""
    service = AcudienteService()
    user_id = current_user.id
    estudiantes = service.get_estudiantes_by_acudiente(user_id)

    for est in estudiantes:
        est['citaciones'] = service.get_citaciones_estudiante(est['id'])

    return render_template('acudientes/citaciones.html', estudiantes=estudiantes)


@acudiente_bp.route('/perfil')
@login_required_acudiente
def perfil():
    """Perfil del acudiente"""
    return render_template('acudientes/perfil.html')