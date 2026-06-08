from flask import Blueprint, request, jsonify, session

from app.services.acudiente_service import AcudienteService
from functools import wraps

api_acudiente_bp = Blueprint('api_acudiente', __name__, url_prefix='/api/acudiente')


def login_required_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'No autorizado'}), 401
        if session.get('rol') != 'acudiente':
            return jsonify({'error': 'Acceso denegado'}), 403
        return f(*args, **kwargs)

    return decorated_function


@api_acudiente_bp.route('/estudiante/<int:estudiante_id>/rendimiento')
@login_required_api
def get_rendimiento(estudiante_id):
    """Obtener rendimiento académico por materias"""
    service = AcudienteService()
    user_id = session['user_id']

    if not service.verificar_pertenencia(user_id, estudiante_id):
        return jsonify({'error': 'No autorizado'}), 403

    data = service.get_rendimiento_grafico(estudiante_id)
    return jsonify(data)


@api_acudiente_bp.route('/estudiante/<int:estudiante_id>/calificaciones')
@login_required_api
def get_calificaciones(estudiante_id):
    """Obtener calificaciones por período"""
    service = AcudienteService()
    user_id = session['user_id']
    periodo_id = request.args.get('periodo', type=int)

    if not service.verificar_pertenencia(user_id, estudiante_id):
        return jsonify({'error': 'No autorizado'}), 403

    data = service.get_calificaciones_json(estudiante_id, periodo_id)
    return jsonify(data)


@api_acudiente_bp.route('/novedades/reportar', methods=['POST'])
@login_required_api
def reportar_novedad():
    """Reportar una novedad por parte del acudiente"""
    data = request.get_json()

    if not data.get('estudiante_id'):
        return jsonify({'error': 'estudiante_id es requerido'}), 400
    if not data.get('informe'):
        return jsonify({'error': 'informe es requerido'}), 400

    service = AcudienteService()
    user_id = session['user_id']

    # Verificar pertenencia
    if not service.verificar_pertenencia(user_id, data['estudiante_id']):
        return jsonify({'error': 'No autorizado'}), 403

    result = service.reportar_novedad(
        estudiante_id=data['estudiante_id'],
        tipo_novedad=data.get('tipo_novedad', 'DISCIPLINA'),
        informe=data['informe'],
        usuario_id=user_id
    )

    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400


@api_acudiente_bp.route('/novedades/<int:novedad_id>/responder', methods=['POST'])
@login_required_api
def responder_novedad(novedad_id):
    """Responder a una novedad"""
    data = request.get_json()

    if not data.get('respuesta'):
        return jsonify({'error': 'respuesta es requerida'}), 400

    service = AcudienteService()
    user_id = session['user_id']

    result = service.responder_novedad(novedad_id, data['respuesta'], user_id)

    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400


@api_acudiente_bp.route('/citaciones/<int:citacion_id>/confirmar', methods=['PUT'])
@login_required_api
def confirmar_citacion(citacion_id):
    """Confirmar asistencia a una citación"""
    service = AcudienteService()
    user_id = session['user_id']

    result = service.confirmar_citacion(citacion_id, user_id)

    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400


@api_acudiente_bp.route('/mensajes/enviar', methods=['POST'])
@login_required_api
def enviar_mensaje():
    """Enviar mensaje al colegio/docente"""
    data = request.get_json()

    if not data.get('estudiante_id'):
        return jsonify({'error': 'estudiante_id es requerido'}), 400
    if not data.get('mensaje'):
        return jsonify({'error': 'mensaje es requerido'}), 400

    service = AcudienteService()
    user_id = session['user_id']

    if not service.verificar_pertenencia(user_id, data['estudiante_id']):
        return jsonify({'error': 'No autorizado'}), 403

    result = service.enviar_mensaje(
        estudiante_id=data['estudiante_id'],
        mensaje=data['mensaje'],
        acudiente_id=user_id
    )

    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400


@api_acudiente_bp.route('/reuniones/solicitar', methods=['POST'])
@login_required_api
def solicitar_reunion():
    """Solicitar reunión con el colegio"""
    data = request.get_json()

    if not data.get('estudiante_id'):
        return jsonify({'error': 'estudiante_id es requerido'}), 400
    if not data.get('fecha'):
        return jsonify({'error': 'fecha es requerida'}), 400

    service = AcudienteService()
    user_id = session['user_id']

    if not service.verificar_pertenencia(user_id, data['estudiante_id']):
        return jsonify({'error': 'No autorizado'}), 403

    result = service.solicitar_reunion(
        estudiante_id=data['estudiante_id'],
        fecha=data['fecha'],
        motivo=data.get('motivo', 'general'),
        mensaje=data.get('mensaje', ''),
        acudiente_id=user_id
    )

    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400


@api_acudiente_bp.route('/notificaciones/pendientes')
@login_required_api
def get_notificaciones():
    """Obtener número de notificaciones pendientes"""
    service = AcudienteService()
    user_id = session['user_id']

    count = service.get_notificaciones_count(user_id)
    return jsonify({'count': count})