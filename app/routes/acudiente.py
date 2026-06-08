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
    user_id = current_user.id  # ← CAMBIADO

    # Obtener estudiantes asociados
    estudiantes = service.get_estudiantes_by_acudiente(user_id)

    # Obtener novedades recientes
    novedades_recientes = service.get_novedades_recientes(estudiantes_ids=[e['id'] for e in estudiantes])

    # Obtener citaciones pendientes
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
    user_id = current_user.id  # ← CAMBIADO
    estudiantes = service.get_estudiantes_by_acudiente(user_id)

    return render_template('acudiente/mis_estudiantes.html', estudiantes=estudiantes)


@acudiente_bp.route('/estudiante/<int:estudiante_id>')
@login_required_acudiente
def estudiante_detalle(estudiante_id):
    """Detalle completo de un estudiante"""
    service = AcudienteService()
    user_id = current_user.id  # ← CAMBIADO

    # Verificar que el estudiante pertenezca al acudiente
    if not service.verificar_pertenencia(user_id, estudiante_id):
        flash('No tienes acceso a este estudiante', 'danger')
        return redirect(url_for('acudiente.mis_estudiantes'))

    estudiante = service.get_estudiante_info(estudiante_id)
    periodos = service.get_periodos_activos()
    calificaciones = service.get_calificaciones(estudiante_id)
    promedio_general = service.get_promedio_general(estudiante_id)
    asistencia_stats = service.get_asistencia_stats(estudiante_id)
    asistencias = service.get_asistencias_recientes(estudiante_id)
    examenes = service.get_examenes_estudiante(estudiante_id)
    novedades = service.get_novedades_estudiante(estudiante_id)
    citaciones = service.get_citaciones_estudiante(estudiante_id)

    return render_template('acudientes/estudiante_detalle.html',
                           estudiante=estudiante,
                           periodos=periodos,
                           calificaciones=calificaciones,
                           promedio_general=promedio_general,
                           asistencia_stats=asistencia_stats,
                           asistencias=asistencias,
                           examenes=examenes,
                           novedades=novedades,
                           citaciones=citaciones)


@acudiente_bp.route('/calificaciones')
@login_required_acudiente
def calificaciones():
    """Vista de calificaciones de todos los estudiantes"""
    return render_template('acudientes/calificaciones.html')


@acudiente_bp.route('/asistencia')
@login_required_acudiente
def asistencia():
    """Vista de asistencia de todos los estudiantes"""
    return render_template('acudientes/asistencia.html')


@acudiente_bp.route('/examenes')
@login_required_acudiente
def examenes():
    """Vista de exámenes de los estudiantes"""
    return render_template('acudientes/examenes.html')


@acudiente_bp.route('/novedades')
@login_required_acudiente
def novedades():
    """Vista de todas las novedades"""
    return render_template('acudientes/novedades.html')


@acudiente_bp.route('/citaciones')
@login_required_acudiente
def citaciones():
    """Vista de todas las citaciones"""
    return render_template('acudientes/citaciones.html')


@acudiente_bp.route('/perfil')
@login_required_acudiente
def perfil():
    """Perfil del acudiente"""
    return render_template('acudientes/perfil.html')