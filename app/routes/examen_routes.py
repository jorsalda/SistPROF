# app/routes/examen_routes.py

import json
import random
from datetime import datetime
from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from sqlalchemy import text, or_

from app.extensions import db
from app.models.periodo_academico import PeriodoAcademico
from app.models.tipo_examen import TipoExamen
from app.models.materia import Materia
from app.models.examen import Examen, ProgramacionExamen
from app.models.pregunta import Pregunta
from app.models.resultado_examen import ResultadoExamen
from app.models.respuestas_examen_detalle import RespuestaExamenDetalle
from app.models.estudiante import Estudiante
from app.models.examen_contenido import ExamenContenido
from app.models.evaluacion_estudiante import EvaluacionEstudiante
from app.models.CompetenciaEstudiante import CompetenciaEstudiante
from app.models.indicador_logro import IndicadorLogro
from app.services.document_service import extraer_texto_de_archivo
from app.services.ia_service import generar_preguntas_json

examen_bp = Blueprint('examen', __name__, url_prefix='/api/examen')


# ==========================================================
# CREAR EXAMEN UNIFICADO (BANCO Y MANUAL)
# ==========================================================
@examen_bp.route("/crear", methods=["GET", "POST"], endpoint="crear_examen")
@examen_bp.route("/crear-desde-banco", methods=["GET", "POST"], endpoint="crear_desde_banco")
@login_required
def crear_examen():
    if current_user.rol not in ['docente', 'coordinador', 'admin_colegio']:
        abort(403)

    # 1. Cargar materias del colegio o globales
    materias = Materia.query.filter_by(colegio_id=current_user.colegio_id).all()
    if not materias:
        materias = Materia.query.all()

    # 2. Obtener la lista completa de preguntas de la base de datos
    preguntas_db = Pregunta.query.all()

    # 3. Formatear las preguntas a una lista de diccionarios compatible con el modal JS
    preguntas_banco_list = []
    for p in preguntas_db:
        # Extraer el texto de forma segura sin importar si el atributo es 'texto' o 'enunciado'
        contenido_texto = getattr(p, 'texto', None) or getattr(p, 'enunciado', '')

        # Obtener el nombre de la materia asociada
        materia_obj = next((m for m in materias if m.id == p.materia_id), None)
        nombre_materia = materia_obj.nombre if materia_obj else "Matemáticas"

        preguntas_banco_list.append({
            'id': p.id,
            'texto': contenido_texto,
            'enunciado': contenido_texto,  # Mapeo clave para la columna del modal
            'materia_id': p.materia_id,
            'materia_nombre': nombre_materia,
            'dificultad': getattr(p, 'dificultad', 'media'),
            'tipo': getattr(p, 'tipo', 'Múltiple Opción')
        })

    # 4. Construir la estructura de competencias e indicadores para la vista
    estructura_evaluacion = {}
    for m in materias:
        competencias = CompetenciaEstudiante.query.filter_by(materia_id=m.id).all()
        comps_data = []
        for c in competencias:
            inds = IndicadorLogro.query.filter_by(competencia_id=c.id).all()
            comps_data.append({
                'id': c.id,
                'codigo': c.codigo,
                'nombre': c.nombre,
                'indicadores': [{'id': i.id, 'codigo': i.codigo, 'desc': i.descripcion} for i in inds]
            })
        estructura_evaluacion[m.id] = comps_data

    # 5. Guardar la evaluación enviada desde el formulario (POST)
    if request.method == "POST":
        try:
            titulo = request.form.get("titulo", "").strip() or request.form.get("titulo_examen", "").strip()
            materia_id = request.form.get("materia_id")
            preguntas_ids = request.form.getlist("preguntas_seleccionadas")

            if not titulo or not materia_id:
                flash("El título y la materia son obligatorios.", "danger")
                return redirect(url_for("examen.crear_examen"))

            # Consultar los registros seleccionados
            ids_limpios = [int(pid) for pid in preguntas_ids if pid.isdigit()]
            preguntas_objs = Pregunta.query.filter(Pregunta.id.in_(ids_limpios)).all() if ids_limpios else []

            contenido_json = []
            for idx, p in enumerate(preguntas_objs, start=1):
                contenido_texto_p = getattr(p, 'texto', None) or getattr(p, 'enunciado', '')
                contenido_json.append({
                    "numero": idx,
                    "texto": contenido_texto_p,
                    "opciones": p.opciones if isinstance(p.opciones, dict) else {},
                    "respuesta_correcta": getattr(p, 'respuesta_correcta', ''),
                    "dificultad": getattr(p, 'dificultad', 'media'),
                    "puntos_maximos": getattr(p, 'puntos', 1)
                })

            nuevo_examen = Examen(
                titulo=titulo,
                nombre=titulo,
                descripcion="Evaluación creada desde el banco de preguntas",
                materia_id=int(materia_id),
                colegio_id=current_user.colegio_id,
                contenido_json=contenido_json,
                tiempo_limite_minutos=30,
                fecha_creacion=datetime.now(),
                activo=True,
                eliminado=False
            )
            db.session.add(nuevo_examen)
            db.session.commit()

            flash("✅ Examen guardado exitosamente.", "success")
            return redirect(url_for("examen.listar_examenes"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al guardar el examen: {str(e)}", "danger")

    return render_template(
        "examenes/crear_examen.html",
        materias=materias,
        preguntas_banco=preguntas_banco_list,  # <-- CAMBIAR AQUÍ (estaba como preguntas_db)
        preguntas_banco_json=json.dumps(preguntas_banco_list),
        estructura_evaluacion=json.dumps(estructura_evaluacion)
    )

# ==========================================================
# VISTA: FORMULARIO GENERADOR DE EXÁMENES CON IA
# ==========================================================
@examen_bp.route("/crear-ia", methods=["GET"])
@login_required
def crear_examen_ia():
    if current_user.rol not in ['docente', 'coordinador', 'admin_colegio']:
        abort(403)
    materias = Materia.query.filter_by(colegio_id=current_user.colegio_id).all()
    return render_template("examenes/crear_examen_ia.html", materias=materias)

# ==========================================================
# GUARDAR EXAMEN GENERADO POR IA (DESDE PREVIEW)
# ==========================================================
@examen_bp.route("/guardar-examen-ia", methods=["POST"])
@login_required
def guardar_examen_ia():
    if current_user.rol not in ['docente', 'coordinador', 'admin_colegio']:
        abort(403)
    try:
        titulo = request.form.get("titulo_examen", "").strip()
        materia_id = request.form.get("materia_id")
        grado = request.form.get("grado")

        if not titulo or not materia_id:
            flash("El título y la materia son obligatorios.", "danger")
            return redirect(url_for("examen.crear_examen_ia"))

        preguntas_data = []
        idx = 0
        while True:
            texto = request.form.get(f"preguntas[{idx}][texto]")
            if not texto:
                break

            tipo_ctx = request.form.get(f"preguntas[{idx}][tipo_contexto]", "")
            url_ctx = request.form.get(f"preguntas[{idx}][url_contexto]", "")
            indicador_id = request.form.get(f"preguntas[{idx}][indicador_logro_id]")

            pregunta = {
                "numero": idx + 1,
                "texto": texto.strip(),
                "opciones": {
                    "A": request.form.get(f"preguntas[{idx}][opcion_a]", "").strip(),
                    "B": request.form.get(f"preguntas[{idx}][opcion_b]", "").strip(),
                    "C": request.form.get(f"preguntas[{idx}][opcion_c]", "").strip(),
                    "D": request.form.get(f"preguntas[{idx}][opcion_d]", "").strip()
                },
                "respuesta_correcta": request.form.get(f"preguntas[{idx}][respuesta_correcta]"),
                "dificultad": request.form.get(f"preguntas[{idx}][dificultad]", "media"),
                "puntos_maximos": int(request.form.get(f"preguntas[{idx}][puntos]", 1)),
                "explicacion": request.form.get(f"preguntas[{idx}][explicacion]", "").strip(),
                "indicador_logro_id": int(indicador_id) if indicador_id and indicador_id.isdigit() else None,
                "url_contexto": url_ctx if url_ctx else None,
                "tipo_contexto": tipo_ctx if tipo_ctx else None
            }
            preguntas_data.append(pregunta)
            idx += 1

        if not preguntas_data:
            flash("No se encontraron preguntas válidas para guardar.", "danger")
            return redirect(url_for("examen.crear_examen_ia"))

        nuevo_examen = Examen(
            titulo=titulo,
            nombre=titulo,
            descripcion=f"Evaluación generada con IA para {grado}",
            materia_id=int(materia_id),
            colegio_id=current_user.colegio_id,
            contenido_json=preguntas_data,
            tiempo_limite_minutos=30,
            fecha_creacion=datetime.now(),
            activo=True,
            eliminado=False
        )
        db.session.add(nuevo_examen)
        db.session.commit()

        flash(f"✅ Examen '{titulo}' guardado exitosamente con {len(preguntas_data)} preguntas.", "success")
        return redirect(url_for("examen.listar_examenes"))

    except Exception as e:
        db.session.rollback()
        flash(f"Error al guardar el examen: {str(e)}", "danger")
        import traceback
        traceback.print_exc()
        return redirect(url_for("examen.crear_examen_ia"))

# ==========================================================
# ENDPOINT ÚNICO JSON: OBTENER EXAMEN PARA EL ESTUDIANTE (FRONTEND)
# ==========================================================
@examen_bp.route("/<int:examen_id>/json", methods=["GET"])
@login_required
def obtener_examen_json(examen_id):
    try:
        examen = Examen.query.filter_by(
            id=examen_id,
            colegio_id=current_user.colegio_id,
            eliminado=False
        ).first()

        preguntas_formateadas = []

        # OPCIÓN A: El examen existe y contiene preguntas en contenido_json
        if examen and examen.contenido_json:
            preguntas_raw = examen.contenido_json
            for idx, p in enumerate(preguntas_raw, start=1):
                opciones_dict = p.get("opciones", {})
                if isinstance(opciones_dict, dict):
                    opciones_lista = [
                        opciones_dict.get('A', ''),
                        opciones_dict.get('B', ''),
                        opciones_dict.get('C', ''),
                        opciones_dict.get('D', '')
                    ]
                elif isinstance(opciones_dict, list):
                    opciones_lista = opciones_dict
                else:
                    opciones_lista = []

                preguntas_formateadas.append({
                    "id": p.get("numero", idx),
                    "numero": p.get("numero", idx),
                    "pregunta": p.get("texto", ""),
                    "texto": p.get("texto", ""),
                    "opciones": opciones_lista,
                    "respuesta": p.get("respuesta_correcta", ""),
                    "respuesta_correcta": p.get("respuesta_correcta", ""),
                    "explicacion": p.get("explicacion", ""),
                    "contexto": p.get("contexto"),
                    "dificultad": p.get("dificultad", "media"),
                    "puntos": p.get("puntos_maximos", 1),
                    "indicador_logro_id": p.get("indicador_logro_id"),
                    "url_contexto": p.get("url_contexto"),
                    "tipo_contexto": p.get("tipo_contexto")
                })

        # OPCIÓN B: Consultar directamente de la tabla Pregunta (PostgreSQL)
        else:
            cantidad = request.args.get('cantidad', default=10, type=int)
            preguntas_db = Pregunta.query.filter(
                or_(
                    Pregunta.materia_id == (examen.materia_id if examen else 1),
                    Pregunta.docente_id == current_user.id
                )
            ).limit(cantidad).all()

            for idx, p in enumerate(preguntas_db, start=1):
                opciones_raw = p.opciones
                if isinstance(opciones_raw, dict):
                    opciones_lista = [
                        opciones_raw.get('A', ''),
                        opciones_raw.get('B', ''),
                        opciones_raw.get('C', ''),
                        opciones_raw.get('D', '')
                    ]
                elif isinstance(opciones_raw, list):
                    opciones_lista = opciones_raw
                else:
                    opciones_lista = []

                preguntas_formateadas.append({
                    "id": p.id,
                    "numero": idx,
                    "pregunta": getattr(p, 'texto', None) or getattr(p, 'enunciado', ''),
                    "texto": getattr(p, 'texto', None) or getattr(p, 'enunciado', ''),
                    "opciones": opciones_lista,
                    "respuesta": getattr(p, 'respuesta_correcta', None) or getattr(p, 'correcta', ''),
                    "respuesta_correcta": getattr(p, 'respuesta_correcta', None) or getattr(p, 'correcta', ''),
                    "explicacion": getattr(p, 'explicacion', ''),
                    "contexto": getattr(p, 'contexto', None),
                    "dificultad": getattr(p, 'dificultad', 'media'),
                    "puntos": getattr(p, 'puntos', 1),
                    "indicador_logro_id": getattr(p, 'indicador_logro_id', None)
                })

        return jsonify({
            "success": True,
            "examen": {
                "id": examen.id if examen else examen_id,
                "titulo": (examen.titulo or examen.nombre) if examen else "Examen de Evaluación",
                "descripcion": examen.descripcion if examen else "",
                "tiempo_limite": (examen.tiempo_limite_minutos if examen else 30) or 30,
                "total_preguntas": len(preguntas_formateadas),
                "preguntas": preguntas_formateadas
            },
            "preguntas": preguntas_formateadas
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error al cargar examen: {str(e)}"}), 500

# ==========================================================
# RENDERIZAR VISTA DE EXAMEN PARA ESTUDIANTE
# ==========================================================
@examen_bp.route('/estudiante', methods=['GET'])
@login_required
def render_examen_estudiante():
    exam_id = request.args.get('id', type=int)
    examen_obj = Examen.query.get(exam_id) if exam_id else Examen.query.filter_by(activo=True).first()
    examen_data = {
        'id': examen_obj.id if examen_obj else 1,
        'materia_id': examen_obj.materia_id if examen_obj else 1
    }
    return render_template('estudiantes/examen_estudiante.html', examen=examen_data)

# ==========================================================
# GUARDAR RESULTADOS DEL EXAMEN
# ==========================================================
@examen_bp.route('/guardar', methods=['POST'])
@login_required
def guardar_resultado_examen():
    try:
        data = request.get_json()
        if 'examen_id' not in data or 'respuestas' not in data:
            return jsonify({'error': 'Faltan campos requeridos: examen_id o respuestas'}), 400

        estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
        if not estudiante:
            return jsonify({'error': 'Usuario no es un estudiante válido'}), 400

        periodo_activo = PeriodoAcademico.query.filter_by(
            activo=True,
            colegio_id=current_user.colegio_id
        ).order_by(PeriodoAcademico.anio.desc(), PeriodoAcademico.orden.desc()).first()

        if not periodo_activo:
            return jsonify({'error': 'No hay periodo académico activo'}), 400

        periodo_id = periodo_activo.id

        config_result = db.session.execute(
            text("SELECT permite_editar_notas FROM configuracion_periodo WHERE periodo_id = :pid"),
            {"pid": periodo_id}
        )
        permite = config_result.scalar()
        if not permite:
            return jsonify({
                'error': 'Periodo cerrado para edición de notas. Contacte al coordinador.'
            }), 403

        materia_id = data.get('materia_id')
        if not materia_id or materia_id == 0:
            examen_obj = Examen.query.get(data['examen_id'])
            if examen_obj:
                materia_id = examen_obj.materia_id
            else:
                return jsonify({'error': 'Examen no encontrado'}), 404

        respuestas = data['respuestas']
        total_preguntas = len(respuestas)
        correctas = sum(1 for r in respuestas if r.get('es_correcta', False))
        incorrectas = total_preguntas - correctas
        porcentaje = (correctas / total_preguntas * 100) if total_preguntas > 0 else 0

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
            materia_id=materia_id,
            respuestas_correctas=correctas,
            respuestas_incorrectas=incorrectas,
            porcentaje=porcentaje,
            literal=literal,
            nota_numerica=nota_decimal,
            fecha_finalizacion=datetime.utcnow()
        )
        db.session.add(resultado)
        db.session.flush()

        prog = ProgramacionExamen.query.filter_by(
            examen_id=data['examen_id'],
            grupo_id=estudiante.grupo_id,
            activo=True
        ).first()

        if prog and prog.competencia_materia_id:
            indicadores_comp = IndicadorLogro.query.filter_by(
                competencia_materia_id=prog.competencia_materia_id
            ).all()

            for ind in indicadores_comp:
                eval_existente = EvaluacionEstudiante.query.filter_by(
                    estudiante_id=estudiante.id,
                    indicador_id=ind.id,
                    periodo_id=periodo_id
                ).first()

                if eval_existente:
                    nueva_nota = round((eval_existente.calificacion + nota_decimal) / 2, 2)
                    eval_existente.calificacion = nueva_nota
                    eval_existente.observacion = f"Actualizado por examen {data['examen_id']}"
                else:
                    nueva_eval = EvaluacionEstudiante(
                        estudiante_id=estudiante.id,
                        indicador_id=ind.id,
                        periodo_id=periodo_id,
                        calificacion=nota_decimal,
                        observacion=f"Evaluado en examen {data['examen_id']}"
                    )
                    db.session.add(nueva_eval)
        else:
            acumulado_indicadores = {}
            for resp in respuestas:
                ind_id = resp.get('indicador_logro_id')
                if ind_id:
                    if ind_id not in acumulado_indicadores:
                        acumulado_indicadores[ind_id] = {'correctas': 0, 'total': 0}
                    acumulado_indicadores[ind_id]['total'] += 1
                    if resp.get('es_correcta', False):
                        acumulado_indicadores[ind_id]['correctas'] += 1

            for ind_id, stats in acumulado_indicadores.items():
                nota_ind = round((stats['correctas'] / stats['total']) * 5, 2) if stats['total'] > 0 else 0
                eval_existente = EvaluacionEstudiante.query.filter_by(
                    estudiante_id=estudiante.id,
                    indicador_id=ind_id,
                    periodo_id=periodo_id
                ).first()

                if eval_existente:
                    nueva_nota = round((eval_existente.calificacion + nota_ind) / 2, 2)
                    eval_existente.calificacion = nueva_nota
                    eval_existente.observacion = f"Actualizado por examen {data['examen_id']}"
                else:
                    nueva_eval = EvaluacionEstudiante(
                        estudiante_id=estudiante.id,
                        indicador_id=ind_id,
                        periodo_id=periodo_id,
                        calificacion=nota_ind,
                        observacion=f"Evaluado en examen {data['examen_id']}"
                    )
                    db.session.add(nueva_eval)

        for idx, resp in enumerate(respuestas):
            detalle = RespuestaExamenDetalle(
                resultado_examen_id=resultado.id,
                numero_pregunta=idx,
                texto_pregunta=resp.get('texto_pregunta', ''),
                respuesta_seleccionada=resp.get('respuesta_seleccionada', ''),
                respuesta_correcta=resp.get('respuesta_correcta', ''),
                es_correcta=resp.get('es_correcta', False),
                tiempo_respuesta_seg=resp.get('tiempo_respuesta_seg'),
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
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# ==========================================================
# LISTADO DE EXÁMENES (VISTA ESTUDIANTE)
# ==========================================================
@examen_bp.route('/listado')
@login_required
def listado_examenes():
    if current_user.rol != 'estudiante':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('estudiantes/listado_examenes.html')

# ==========================================================
# LISTAR MIS EXÁMENES (VISTA DOCENTE)
# ==========================================================
@examen_bp.route("/mis-examenes")
@login_required
def listar_examenes():
    examenes = Examen.query.options(
        joinedload(Examen.programaciones)
    ).filter_by(
        colegio_id=current_user.colegio_id,
        activo=True,
        eliminado=False
    ).order_by(Examen.fecha_creacion.desc()).all()

    examenes_con_contteo = []
    for e in examenes:
        total = 0
        if e.contenido_json and isinstance(e.contenido_json, list):
            total += len(e.contenido_json)
        contenidos = ExamenContenido.query.filter_by(examen_id=e.id, activo=True).all()
        for c in contenidos:
            if c.contenido_json and isinstance(c.contenido_json, list):
                total += len(c.contenido_json)
        examenes_con_contteo.append({'examen': e, 'total_preguntas': total})

    return render_template("examenes/listar_examenes.html", examenes=examenes_con_contteo)

# ==========================================================
# VER DETALLE DE EXAMEN
# ==========================================================
@examen_bp.route("/ver/<int:id>")
@login_required
def ver_examen(id):
    examen = Examen.query.get_or_404(id)
    if examen.colegio_id != current_user.colegio_id:
        abort(403)
    return render_template("examenes/ver_examen.html", examen=examen)

# ==========================================================
# ELIMINAR EXAMEN (BORRADO LÓGICO)
# ==========================================================
@examen_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_examen(id):
    examen = Examen.query.get_or_404(id)
    if examen.colegio_id != current_user.colegio_id:
        abort(403)
    try:
        examen.eliminado = True
        db.session.commit()
        flash("Examen eliminado correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar: {str(e)}", "danger")
    return redirect("/api/examen/mis-examenes")

# ==========================================================
# EDITAR EXAMEN (CON EDICIÓN DE PREGUNTAS)
# ==========================================================
@examen_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_examen(id):
    examen = Examen.query.get_or_404(id)
    if examen.colegio_id != current_user.colegio_id:
        abort(403)

    if not examen.contenido_json or len(examen.contenido_json) == 0:
        flash("No se puede editar un examen sin preguntas. Por favor, cree uno nuevo.", "warning")
        return redirect(url_for('examen.ver_examen', id=examen.id))

    if request.method == "POST":
        try:
            examen.titulo = request.form.get("titulo", "").strip()
            examen.nombre = examen.titulo
            examen.descripcion = request.form.get("descripcion", "").strip()
            tiempo = request.form.get("tiempo_limite_minutos")

            if tiempo and tiempo.isdigit():
                examen.tiempo_limite_minutos = int(tiempo)
            else:
                flash("El tiempo límite debe ser un número válido", "danger")
                return redirect(url_for('examen.editar_examen', id=id))

            preguntas_data = []
            idx = 0
            while True:
                texto = request.form.get(f"preguntas[{idx}][texto]")
                if not texto:
                    break

                opcion_a = request.form.get(f"preguntas[{idx}][opcion_a]", "").strip()
                opcion_b = request.form.get(f"preguntas[{idx}][opcion_b]", "").strip()
                respuesta_correcta = request.form.get(f"preguntas[{idx}][respuesta_correcta]")

                if not opcion_a or not opcion_b:
                    flash(f"La pregunta {idx + 1} debe tener al menos las opciones A y B", "danger")
                    return redirect(url_for('examen.editar_examen', id=id))

                if not respuesta_correcta:
                    flash(f"Debe seleccionar la respuesta correcta para la pregunta {idx + 1}", "danger")
                    return redirect(url_for('examen.editar_examen', id=id))

                pregunta = {
                    "numero": idx + 1,
                    "texto": texto.strip(),
                    "opciones": {
                        "A": opcion_a,
                        "B": opcion_b,
                        "C": request.form.get(f"preguntas[{idx}][opcion_c]", "").strip(),
                        "D": request.form.get(f"preguntas[{idx}][opcion_d]", "").strip()
                    },
                    "respuesta_correcta": respuesta_correcta,
                    "dificultad": request.form.get(f"preguntas[{idx}][dificultad]", "media"),
                    "puntos_maximos": int(request.form.get(f"preguntas[{idx}][puntos]", 1)),
                    "explicacion": request.form.get(f"preguntas[{idx}][explicacion]", "").strip()
                }
                preguntas_data.append(pregunta)
                idx += 1

            if not preguntas_data:
                flash("Un examen debe tener al menos una pregunta", "danger")
                return redirect(url_for('examen.editar_examen', id=id))

            examen.contenido_json = preguntas_data
            db.session.commit()
            flash("Examen actualizado correctamente", "success")
            return redirect(url_for('examen.ver_examen', id=examen.id))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar: {str(e)}", "danger")
            return redirect(url_for('examen.editar_examen', id=id))

    return render_template("examenes/editar_examen.html", examen=examen)

# ==========================================================
# FUNCIÓN AUXILIAR: GUARDAR SELECCIÓN DE PREGUNTAS
# ==========================================================
def guardar_seleccion_preguntas(examen_id, preguntas_seleccionadas):
    try:
        contenido_existente = ExamenContenido.query.filter_by(examen_id=examen_id, version=1).first()
        if contenido_existente:
            contenido_existente.contenido_json = preguntas_seleccionadas
            flash("Selección de preguntas actualizada exitosamente", "success")
        else:
            nuevo_contenido = ExamenContenido(
                examen_id=examen_id,
                contenido_json=preguntas_seleccionadas,
                version=1,
                activo=True
            )
            db.session.add(nuevo_contenido)
            flash("Preguntas vinculadas al examen exitosamente", "success")

        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        flash(f"Error al guardar selección: {str(e)}", "danger")
        return False

# ==========================================================
# SEGUIMIENTO DE RESULTADOS Y ESTADÍSTICAS
# ==========================================================
@examen_bp.route("/resultados/<int:id>")
@login_required
def ver_resultados_examen(id):
    examen = Examen.query.get_or_404(id)
    if examen.colegio_id != current_user.colegio_id:
        abort(403)

    prog = ProgramacionExamen.query.filter_by(
        examen_id=examen.id,
        activo=True
    ).first()

    if not prog:
        flash("Este examen no está asignado a ningún grupo.", "warning")
        return redirect(url_for('examen.ver_examen', id=examen.id))

    estudiantes = Estudiante.query.filter_by(
        grupo_id=prog.grupo_id,
        activo=True
    ).order_by(Estudiante.apellido, Estudiante.nombre).all()

    resultados_map = {}
    for r in ResultadoExamen.query.filter_by(examen_id=examen.id).all():
        resultados_map[r.estudiante_id] = r

    total_estudiantes = len(estudiantes)
    presentados = sum(1 for e in estudiantes if e.id in resultados_map)
    pendientes = total_estudiantes - presentados
    notas_validas = [r.nota_numerica for r in resultados_map.values() if r.nota_numerica is not None]
    promedio_grupo = round(sum(notas_validas) / len(notas_validas), 2) if notas_validas else 0

    stats = {
        'total': total_estudiantes,
        'presentados': presentados,
        'pendientes': pendientes,
        'promedio': promedio_grupo,
        'aprobados': sum(1 for n in notas_validas if n >= 3.0),
        'reprobados': sum(1 for n in notas_validas if n < 3.0)
    }

    return render_template(
        "examenes/resultados_examen.html",
        examen=examen,
        grupo=prog.grupo,
        estudiantes=estudiantes,
        resultados_map=resultados_map,
        stats=stats
    )

# ==========================================================
# API: COMPETENCIAS POR GRUPO Y MATERIA
# ==========================================================
@examen_bp.route("/api/competencias-por-grupo-materia", methods=["GET"])
@login_required
def api_competencias_por_grupo_materia():
    try:
        grupo_id = request.args.get('grupo_id', type=int)
        materia_id = request.args.get('materia_id', type=int)

        if not materia_id and not grupo_id:
            return jsonify({"error": "Faltan parámetros"}), 400

        query = CompetenciaEstudiante.query.filter(
            or_(
                CompetenciaEstudiante.materia_id == materia_id,
                CompetenciaEstudiante.grupo_id == grupo_id
            )
        ).order_by(CompetenciaEstudiante.codigo)

        competencias = query.all()
        resultado = []
        for comp in competencias:
            resultado.append({
                "id": comp.id,
                "codigo": comp.codigo or f"C{comp.id}",
                "nombre": comp.nombre[:60] + "..." if len(comp.nombre) > 60 else comp.nombre,
                "porcentaje": float(comp.porcentaje) if comp.porcentaje else 0
            })

        return jsonify(resultado), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ==========================================================
# ASIGNAR EXAMEN A GRUPO (CON COMPETENCIA)
# ==========================================================
@examen_bp.route("/<int:examen_id>/asignar", methods=["GET", "POST"])
@login_required
def asignar_examen(examen_id):
    if current_user.rol not in ['docente', 'coordinador']:
        abort(403)

    examen = Examen.query.get_or_404(examen_id)
    if examen.colegio_id != current_user.colegio_id:
        abort(403)

    from app.models.grupo import Grupo
    from app.models.grupo_materia import GrupoMateria
    from app.models.docente import Docente

    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    if docente:
        ids_grupos_docente = db.session.query(GrupoMateria.grupo_id).filter_by(
            docente_id=docente.id,
            activo=True
        ).distinct().all()
        ids_grupos_docente = [g[0] for g in ids_grupos_docente]

        grupos_todos = Grupo.query.filter(
            Grupo.id.in_(ids_grupos_docente),
            Grupo.activo == True
        ).order_by(Grupo.grado, Grupo.nombre).all() if ids_grupos_docente else []

        grupos_ya_asignados = db.session.query(ProgramacionExamen.grupo_id).filter_by(
            examen_id=examen_id,
            activo=True
        ).all()
        grupos_ya_asignados_ids = [g[0] for g in grupos_ya_asignados]

        grupos = [g for g in grupos_todos if g.id not in grupos_ya_asignados_ids]
    else:
        grupos = []

    materias = Materia.query.order_by(Materia.nombre).all()

    if request.method == "POST":
        try:
            grupo_id = request.form.get("grupo_id", type=int)
            competencia_id = request.form.get("competencia_materia_id", type=int)
            fecha_apertura = request.form.get("fecha_apertura")
            fecha_cierre = request.form.get("fecha_cierre")

            if not all([grupo_id, competencia_id, fecha_apertura, fecha_cierre]):
                flash("Grupo, competencia, fecha de apertura y fecha de cierre son obligatorios.", "danger")
                return redirect(url_for("examen.asignar_examen", examen_id=examen_id))

            competencia = CompetenciaEstudiante.query.get(competencia_id)
            if not competencia:
                flash("La competencia seleccionada no existe.", "danger")
                return redirect(url_for("examen.asignar_examen", examen_id=examen_id))

            prog_existente = ProgramacionExamen.query.filter_by(
                examen_id=examen_id,
                grupo_id=grupo_id,
                activo=True
            ).first()

            fecha_apertura_dt = datetime.strptime(fecha_apertura, "%Y-%m-%dT%H:%M")
            fecha_cierre_dt = datetime.strptime(fecha_cierre, "%Y-%m-%dT%H:%M")

            if fecha_cierre_dt <= fecha_apertura_dt:
                flash("La fecha de cierre debe ser posterior a la fecha de apertura.", "danger")
                return redirect(url_for("examen.asignar_examen", examen_id=examen_id))

            if prog_existente:
                prog_existente.competencia_materia_id = competencia_id
                prog_existente.fecha_apertura = fecha_apertura_dt
                prog_existente.fecha_cierre = fecha_cierre_dt
                flash("✅ Programación actualizada exitosamente.", "success")
            else:
                nueva_prog = ProgramacionExamen(
                    examen_id=examen_id,
                    grupo_id=grupo_id,
                    competencia_materia_id=competencia_id,
                    fecha_apertura=fecha_apertura_dt,
                    fecha_cierre=fecha_cierre_dt,
                    activo=True
                )
                db.session.add(nueva_prog)
                flash("✅ Examen asignado exitosamente.", "success")

            db.session.commit()
            return redirect(url_for("examen.ver_examen", id=examen_id))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al asignar: {str(e)}", "danger")
            import traceback
            traceback.print_exc()

    return render_template(
        "examenes/asignar_examen.html",
        examen=examen,
        grupos=grupos,
        materias=materias
    )

# ==========================================================
# API: EXÁMENES DISPONIBLES PARA ESTUDIANTE (JSON)
# ==========================================================
@examen_bp.route('/disponibles')
@login_required
def api_examenes_disponibles():
    if current_user.rol != 'estudiante':
        return jsonify({'error': 'No autorizado'}), 403

    estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
    if not estudiante or not estudiante.grupo_id:
        return jsonify([])

    ahora = datetime.now()
    examenes = Examen.query.join(ProgramacionExamen).filter(
        ProgramacionExamen.grupo_id == estudiante.grupo_id,
        ProgramacionExamen.activo == True,
        ProgramacionExamen.fecha_apertura <= ahora,
        ProgramacionExamen.fecha_cierre >= ahora,
        Examen.eliminado == False,
        Examen.activo == True
    ).order_by(ProgramacionExamen.fecha_apertura.desc()).all()

    resultado = []
    for ex in examenes:
        resultado.append({
            'id': ex.id,
            'nombre': ex.titulo,
            'descripcion': ex.descripcion or '',
            'tiempo_limite_minutos': ex.tiempo_limite_minutos or 30,
            'materia_id': ex.materia_id
        })

    return jsonify(resultado)