# routes/api_examen_bp.py
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.examen import Examen
from app.models.tipo_examen import TipoExamen
from app.models.resultado_examen import ResultadoExamen
from app.models.estudiante import Estudiante
from app.extensions import db
from datetime import datetime
import os
import json

api_examen_bp = Blueprint('api_examen', __name__, url_prefix='/api/examen')


@api_examen_bp.route('/<int:examen_id>/json')
@login_required
def obtener_json_examen(examen_id):
    examen = Examen.query.get_or_404(examen_id)

    if examen.colegio_id != current_user.colegio_id:
        return jsonify({'error': 'No tiene acceso a este examen'}), 403

    if examen.contenido_json:
        return jsonify(examen.contenido_json)

    if not examen.archivo_json:
        return jsonify({'error': 'Este examen no tiene contenido'}), 404

    ruta_json = os.path.join('static', 'examenes', examen.archivo_json)

    if not os.path.exists(ruta_json):
        return jsonify({'error': f'Archivo {examen.archivo_json} no encontrado'}), 404

    with open(ruta_json, 'r', encoding='utf-8') as f:
        contenido = json.load(f)

    return jsonify(contenido)





@api_examen_bp.route('/guardar-resultado', methods=['POST'])
@login_required
def guardar_resultado():
    data = request.get_json()

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

    existe = ResultadoExamen.query.filter_by(
        estudiante_id=estudiante.id,
        examen_id=data['examen_id']
    ).first()

    if existe:
        return jsonify({'error': 'Ya presentó este examen'}), 400

    resultado = ResultadoExamen(
        estudiante_id=estudiante.id,
        examen_id=data['examen_id'],
        materia_id=1,
        total_preguntas=data['respuestas_correctas'] + data['respuestas_incorrectas'],
        respuestas_correctas=data['respuestas_correctas'],
        respuestas_incorrectas=data['respuestas_incorrectas'],
        porcentaje=data['porcentaje'],
        nota_numerica=data['nota_numerica'],
        literal=data['literal'],
        fecha_finalizacion=datetime.utcnow()
    )

    db.session.add(resultado)
    db.session.commit()

    return jsonify({'success': True, 'resultado_id': resultado.id})