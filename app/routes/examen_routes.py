from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.examen import Examen
from app.models.pregunta import Pregunta  # <-- NUEVO: Importamos el modelo Pregunta
from app.models.resultado_examen import ResultadoExamen
from app.models.respuestas_examen_detalle import RespuestaExamenDetalle
from app.models.estudiante import Estudiante
from app.models.tipo_examen import TipoExamen
from app.extensions import db
from datetime import datetime
import random  # <-- NUEVO: Para aleatorizar las preguntas

examen_bp = Blueprint('examen', __name__, url_prefix='/api/examen')


@examen_bp.route('/<int:examen_id>/json', methods=['GET'])
@login_required
def obtener_json_examen(examen_id):
    """
    Devuelve las preguntas aleatorias desde el banco de preguntas en la BD.
    Si no hay preguntas en la BD, hace fallback al JSON antiguo.
    """
    examen = Examen.query.get_or_404(examen_id)

    # Verificar que el estudiante pertenece al mismo colegio
    if examen.colegio_id != current_user.colegio_id:
        return jsonify({'error': 'No tiene acceso a este examen'}), 403

    # 1. Obtener la cantidad de preguntas que el estudiante quiere (por defecto 10)
    num_preguntas = request.args.get('cantidad', default=10, type=int)

    # 2. Consultar el banco de preguntas en la BD
    preguntas_db = Pregunta.query.filter_by(
        materia_id=examen.materia_id,
        tipo='icfes',
        activo=True
    ).all()

    # 3. Si NO hay preguntas en la BD, usamos el JSON antiguo (Fallback)
    if not preguntas_db:
        if examen.contenido_json:
            return jsonify(examen.contenido_json)
        return jsonify({'error': 'No hay preguntas disponibles en el banco para esta materia'}), 404

    # 4. Aleatorizar y limitar la cantidad
    random.shuffle(preguntas_db)
    preguntas_seleccionadas = preguntas_db[:num_preguntas]

    # 5. Formatear para que EstudianteJS lo entienda
    preguntas_formateadas = []
    for p in preguntas_seleccionadas:
        preguntas_formateadas.append({
            "pregunta": p.texto,
            "opciones": p.opciones,
            "respuesta": p.respuesta_correcta,
            "explicacion": p.explicacion,
            "tema": p.tema,
            "dificultad": p.dificultad
        })

    return jsonify({"preguntas": preguntas_formateadas})


@examen_bp.route('/disponibles', methods=['GET'])
@login_required
def examenes_disponibles():
    """
    Devuelve la lista de exámenes disponibles para el estudiante.
    Si se pasa materia_id, filtra por esa materia.
    """
    materia_id = request.args.get('materia_id', type=int)

    if current_user.rol == 'estudiante':
        query = Examen.query.join(TipoExamen).filter(
            Examen.activo == True,
            Examen.colegio_id == current_user.colegio_id,
            TipoExamen.disponible_individual == True
        )
        if materia_id:
            query = query.filter(Examen.materia_id == materia_id)
        examenes = query.all()
    else:
        query = Examen.query.filter_by(
            colegio_id=current_user.colegio_id,
            activo=True
        )
        if materia_id:
            query = query.filter(Examen.materia_id == materia_id)
        examenes = query.all()

    resultado = []
    for e in examenes:
        resultado.append({
            'id': e.id,
            'nombre': e.nombre,
            'descripcion': e.descripcion,
            'tipo_examen': e.tipo_examen.nombre if e.tipo_examen else None,
            'tiempo_limite_minutos': e.tiempo_limite_minutos,
            'materia_id': e.materia_id
        })

    return jsonify(resultado)


@examen_bp.route('/estudiante', methods=['GET'])
@login_required
def render_examen_estudiante():
    """
    Renderiza la plantilla del examen e inyecta los IDs necesarios.
    """
    exam_id = request.args.get('id', type=int)
    examen_obj = Examen.query.get(exam_id) if exam_id else Examen.query.filter_by(activo=True).first()

    examen_data = {
        'id': examen_obj.id if examen_obj else 1,
        'materia_id': examen_obj.materia_id if examen_obj else 1
    }

    return render_template('estudiantes/examen_estudiante.html', examen=examen_data)


@examen_bp.route('/guardar', methods=['POST'])
@login_required
def guardar_resultado_examen():
    """
    Recibe los resultados del examen desde el frontend y los guarda en PostgreSQL.
    """
    try:
        data = request.get_json()

        required_fields = ['examen_id', 'materia_id', 'respuestas']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400

        estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
        if not estudiante:
            return jsonify({'error': 'Usuario no es un estudiante válido'}), 400

        respuestas = data['respuestas']
        total_preguntas = len(respuestas)
        correctas = sum(1 for r in respuestas if r.get('es_correcta', False))
        incorrectas = total_preguntas - correctas
        porcentaje = (correctas / total_preguntas * 100) if total_preguntas > 0 else 0

        # Escala literal
        if porcentaje >= 100:
            literal = 'S'
        elif porcentaje >= 80:
            literal = 'A'
        elif porcentaje >= 60:
            literal = 'B'
        elif porcentaje >= 40:
            literal = 'b'
        else:
            literal = 'I'

        nota_decimal = round(porcentaje / 20, 2)

        resultado = ResultadoExamen(
            estudiante_id=estudiante.id,
            examen_id=data['examen_id'],
            materia_id=data['materia_id'],
            total_preguntas=total_preguntas,
            respuestas_correctas=correctas,
            respuestas_incorrectas=incorrectas,
            porcentaje=porcentaje,
            literal=literal,
            nota_numerica=nota_decimal,
            fecha_finalizacion=datetime.utcnow()
        )

        db.session.add(resultado)
        db.session.flush()

        for idx, resp in enumerate(respuestas):
            detalle = RespuestaExamenDetalle(
                resultado_examen_id=resultado.id,
                numero_pregunta=idx,
                texto_pregunta=resp.get('texto_pregunta', ''),
                respuesta_seleccionada=resp.get('respuesta_seleccionada', ''),
                respuesta_correcta=resp.get('respuesta_correcta', ''),
                es_correcta=resp.get('es_correcta', False),
                tiempo_respuesta_seg=resp.get('tiempo_respuesta_seg')
            )
            db.session.add(detalle)

        db.session.commit()

        return jsonify({
            'message': 'Examen guardado exitosamente',
            'resultado_id': resultado.id,
            'nota': nota_decimal,
            'literal': literal,
            'porcentaje': porcentaje
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@examen_bp.route('/listado')
@login_required
def listado_examenes():
    """
    Muestra la lista de exámenes disponibles para el estudiante.
    """
    if current_user.rol != 'estudiante':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('estudiantes/listado_examenes.html')