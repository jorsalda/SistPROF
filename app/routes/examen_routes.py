from app.routes.estudiantes_routes import estudiante_bp
from app.models.tipo_examen import TipoExamen
from app.services.document_service import extraer_texto_de_archivo
from app.services.ia_service import generar_preguntas_json
from app.models.materia import Materia
from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app.models.examen import Examen, ProgramacionExamen
from app.models.pregunta import Pregunta
from app.models.resultado_examen import ResultadoExamen
from app.models.respuestas_examen_detalle import RespuestaExamenDetalle
from app.models.estudiante import Estudiante
from app.extensions import db
from datetime import datetime
import random
from app.models.examen_contenido import ExamenContenido
import json

examen_bp = Blueprint('examen', __name__, url_prefix='/api/examen')


# ==========================================================
# CREAR EXAMEN CON ASISTENCIA DE IA (FORMULARIO INICIAL)
# ==========================================================
@examen_bp.route("/crear-con-ia", methods=["GET", "POST"])
@login_required
def crear_examen_ia():
    if current_user.rol not in ['docente', 'coordinador', 'admin_colegio']:
        abort(403)

    if request.method == "POST":
        materia_id = request.form.get("materia_id")
        grado = request.form.get("grado")
        cantidad = int(request.form.get("cantidad", 5))
        archivo = request.files.get("archivo")

        if not archivo or archivo.filename == '':
            flash("Debes seleccionar un archivo para subir.", "danger")
            return redirect(request.url)

        ext = archivo.filename.rsplit('.', 1)[1].lower() if '.' in archivo.filename else ''
        if ext not in ['pdf', 'docx']:
            flash("Solo se permiten archivos en formato PDF o DOCX.", "danger")
            return redirect(request.url)

        try:
            texto_extraido = extraer_texto_de_archivo(archivo, ext)
            if not texto_extraido or len(texto_extraido.strip()) < 50:
                flash("No se pudo extraer suficiente texto del documento.", "warning")
                return redirect(request.url)

            materia = Materia.query.get(materia_id)
            nombre_materia = materia.nombre if materia else "la materia asignada"

            flash("🤖 La IA está analizando el documento...", "info")
            resultado_ia = generar_preguntas_json(texto_extraido, nombre_materia, grado, cantidad)

            return render_template(
                "examenes/preview_ia.html",
                preguntas=resultado_ia.get("preguntas", []),
                materia_id=materia_id,
                grado=grado,
                cantidad=cantidad,
                nombre_materia=nombre_materia
            )

        except Exception as e:
            flash(f"Error al procesar el documento con IA: {str(e)}", "danger")
            return redirect(request.url)

    materias = Materia.query.order_by(Materia.nombre).all()
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

            # ✅ CAPTURA DE CONTEXTO EN PREVIEW IA (Si el docente lo editó/agregó)
            tipo_ctx = request.form.get(f"preguntas[{idx}][tipo_contexto]", "")
            url_ctx = request.form.get(f"preguntas[{idx}][url_contexto]", "")

            pregunta = {
                "numero": idx + 1,
                "texto": texto,
                "opciones": {
                    "A": request.form.get(f"preguntas[{idx}][opcion_a]"),
                    "B": request.form.get(f"preguntas[{idx}][opcion_b]"),
                    "C": request.form.get(f"preguntas[{idx}][opcion_c]"),
                    "D": request.form.get(f"preguntas[{idx}][opcion_d]")
                },
                "respuesta_correcta": request.form.get(f"preguntas[{idx}][respuesta_correcta]"),
                "dificultad": request.form.get(f"preguntas[{idx}][dificultad]", "media"),
                "puntos_maximos": int(request.form.get(f"preguntas[{idx}][puntos]", 1)),
                "explicacion": request.form.get(f"preguntas[{idx}][explicacion]", ""),
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
            materia_id=materia_id,
            colegio_id=current_user.colegio_id,
            contenido_json=preguntas_data,
            tiempo_limite_minutos=30,
            fecha_creacion=datetime.now(),
            activo=True
        )
        db.session.add(nuevo_examen)
        db.session.flush()

        for p_data in preguntas_data:
            nueva_pregunta = Pregunta(
                texto=p_data["texto"],
                tipo="icfes",
                opciones=p_data["opciones"],
                respuesta_correcta=p_data["respuesta_correcta"],
                explicacion=p_data["explicacion"],
                dificultad=p_data["dificultad"],
                puntos_maximos=p_data["puntos_maximos"],
                materia_id=materia_id,
                fecha_creacion=datetime.now(),
                activo=True,
                docente_id=current_user.id,
                examen_id=None,
                # ✅ GUARDAR CONTEXTO EN EL BANCO
                url_contexto=p_data.get("url_contexto"),
                tipo_contexto=p_data.get("tipo_contexto")
            )
            db.session.add(nueva_pregunta)

        db.session.commit()

        flash(f"✅ Examen '{titulo}' guardado exitosamente con {len(preguntas_data)} preguntas.", "success")

        try:
            return redirect(url_for("examen.listar_examenes"))
        except:
            return redirect(url_for("docente.dashboard"))

    except Exception as e:
        db.session.rollback()
        flash(f"Error al guardar el examen: {str(e)}", "danger")
        return redirect(url_for("examen.crear_examen_ia"))


# ==========================================================
# OBTENER JSON DEL EXAMEN (PARA ESTUDIANTES)
# ==========================================================
@examen_bp.route('/<int:examen_id>/json', methods=['GET'])
@login_required
def obtener_json_examen(examen_id):
    examen = Examen.query.get_or_404(examen_id)

    if examen.colegio_id != current_user.colegio_id:
        return jsonify({'error': 'No tiene acceso a este examen'}), 403

    num_preguntas = request.args.get('cantidad', default=10, type=int)

    # Intentar cargar desde el Banco de Preguntas primero
    preguntas_db = Pregunta.query.filter_by(
        materia_id=examen.materia_id,
        tipo='icfes',
        activo=True
    ).all()

    preguntas_formateadas = []

    if preguntas_db:
        # --- CASO 1: Preguntas del Banco (BD) ---
        random.shuffle(preguntas_db)
        preguntas_seleccionadas = preguntas_db[:num_preguntas]

        for p in preguntas_seleccionadas:
            # Convertir opciones de Objeto {"A":"...", "B":"..."} a Lista ["...", "..."]
            lista_opciones = []
            if p.opciones and isinstance(p.opciones, dict):
                # Ordenamos por clave para mantener A, B, C, D
                for key in sorted(p.opciones.keys()):
                    lista_opciones.append(p.opciones[key])

            preguntas_formateadas.append({
                "pregunta": p.texto,
                "opciones": lista_opciones,  # <-- Aquí enviamos la lista
                "respuesta": p.respuesta_correcta,
                "explicacion": p.explicacion or "",
                "tema": p.tema or "",
                "dificultad": p.dificultad or "media",
                "url_contexto": p.url_contexto,
                "tipo_contexto": p.tipo_contexto
            })

    else:
        # --- CASO 2: Fallback a JSON antiguo (IA) ---
        if examen.contenido_json:
            contenido = examen.contenido_json if isinstance(examen.contenido_json, list) else examen.contenido_json.get(
                'preguntas', [])

            for p in contenido[:num_preguntas]:
                # También convertimos por si la IA guardó objeto
                ops_raw = p.get("opciones", {})
                lista_ops = list(ops_raw.values()) if isinstance(ops_raw, dict) else (
                    ops_raw if isinstance(ops_raw, list) else [])

                preguntas_formateadas.append({
                    "pregunta": p.get("texto", ""),
                    "opciones": lista_ops,
                    "respuesta": p.get("respuesta_correcta", ""),
                    "explicacion": p.get("explicacion", ""),
                    "tema": p.get("tema", ""),
                    "dificultad": p.get("dificultad", "media"),
                    "url_contexto": p.get("url_contexto"),
                    "tipo_contexto": p.get("tipo_contexto")
                })

    if not preguntas_formateadas:
        return jsonify({'error': 'No hay preguntas disponibles'}), 404

    return jsonify({"preguntas": preguntas_formateadas})

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
    examenes = Examen.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True,
        eliminado=False  # ✅ AGREGAR ESTA LÍNEA
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
@examen_bp.route("/eliminar/<int:id>", methods=["POST"])  # ✅ Cambiado a POST por seguridad
@login_required
def eliminar_examen(id):
    examen = Examen.query.get_or_404(id)

    # Validación de seguridad
    if examen.colegio_id != current_user.colegio_id:
        abort(403)

    try:
        # ✅ BORRADO LÓGICO: Usamos el nuevo campo 'eliminado'
        examen.eliminado = True
        db.session.commit()
        flash("Examen eliminado correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar: {str(e)}", "danger")

    # ✅ Redirección segura usando URL directa
    return redirect("/api/examen/mis-examenes")


# ==========================================================
# EDITAR EXAMEN (CON EDICIÓN DE PREGUNTAS)
# ==========================================================
@examen_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_examen(id):
    examen = Examen.query.get_or_404(id)

    # 1. Validación de seguridad (Nivel Colegio)
    if examen.colegio_id != current_user.colegio_id:
        abort(403)

    # 2. ✅ VALIDACIÓN TEMPRANA DE CONTENIDO (FUERA DEL IF ANTERIOR)
    # Si no hay preguntas, no tiene sentido mostrar el formulario de edición
    if not examen.contenido_json or len(examen.contenido_json) == 0:
        flash("No se puede editar un examen sin preguntas. Por favor, cree uno nuevo.", "warning")
        return redirect(url_for('examen.ver_examen', id=examen.id))

    # 3. Procesamiento del Formulario (POST)
    if request.method == "POST":
        try:
            # Actualizar metadatos básicos
            examen.titulo = request.form.get("titulo", "").strip()
            examen.nombre = examen.titulo
            examen.descripcion = request.form.get("descripcion", "").strip()

            tiempo = request.form.get("tiempo_limite_minutos")
            if tiempo and tiempo.isdigit():
                examen.tiempo_limite_minutos = int(tiempo)
            else:
                flash("El tiempo límite debe ser un número válido", "danger")
                return redirect(url_for('examen.editar_examen', id=id))

            # Procesar preguntas editadas
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

            # Guardar cambios en BD
            examen.contenido_json = preguntas_data
            db.session.commit()

            flash("Examen actualizado correctamente", "success")
            return redirect(url_for('examen.ver_examen', id=examen.id))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar: {str(e)}", "danger")
            return redirect(url_for('examen.editar_examen', id=id))

    # GET: Mostrar formulario (Solo llega aquí si pasó las validaciones anteriores)
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
    from app.models.examen import ProgramacionExamen

    examen = Examen.query.get_or_404(id)
    if examen.colegio_id != current_user.colegio_id:
        abort(403)

    # Obtener la programación activa para saber a qué grupo pertenece
    prog = ProgramacionExamen.query.filter_by(
        examen_id=examen.id,
        activo=True
    ).first()

    if not prog:
        flash("Este examen no está asignado a ningún grupo.", "warning")
        return redirect(url_for('examen.ver_examen', id=examen.id))

    # Obtener todos los estudiantes activos de ese grupo
    estudiantes = Estudiante.query.filter_by(
        grupo_id=prog.grupo_id,
        activo=True
    ).order_by(Estudiante.apellido, Estudiante.nombre).all()

    # Obtener resultados existentes para este examen
    resultados_map = {}
    for r in ResultadoExamen.query.filter_by(examen_id=examen.id).all():
        resultados_map[r.estudiante_id] = r

    # Calcular Estadísticas Básicas
    total_estudiantes = len(estudiantes)
    presentados = sum(1 for e in estudiantes if e.id in resultados_map)
    pendientes = total_estudiantes - presentados

    notas_validas = [r.nota_numerica for r in resultados_map.values() if r.nota_numerica is not None]
    promedio_grupo = round(sum(notas_validas) / len(notas_validas), 2) if notas_validas else 0

    # Pregunta con más errores (Estadística avanzada simple)
    # Nota: Esto requiere iterar sobre RespuestaExamenDetalle si quieres precisión total
    # Por ahora usaremos un placeholder o una consulta simple si tienes la tabla de detalles

    stats = {
        'total': total_estudiantes,
        'presentados': presentados,
        'pendientes': pendientes,
        'promedio': promedio_grupo,
        'aprobados': sum(1 for n in notas_validas if n >= 3.0),  # Asumiendo 3.0 como mínimo
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


# =========================================================
# API: OBTENER PREGUNTAS DE UN EXAMEN (PARA CLSESTUDIANTE)
# =========================================================
@examen_bp.route("/api/examen/<int:id>/json")
@login_required
def api_examen_json(id):
    """Devuelve las preguntas de un examen en formato JSON para el JS"""
    if current_user.rol != 'estudiante':
        return jsonify({"error": "No autorizado"}), 403

    examen = Examen.query.get_or_404(id)

    # Verificar seguridad básica
    if not examen.contenido_json or not isinstance(examen.contenido_json, list):
        return jsonify({"error": "Examen sin preguntas"}), 404

    preguntas = []
    for p in examen.contenido_json:
        # Adaptar el formato de la BD al formato que espera ClsEstudiante.js
        preguntas.append({
            "pregunta": p.get("texto", ""),  # JS espera 'pregunta', BD tiene 'texto'
            "opciones": list(p.get("opciones", {}).values()),  # Solo los textos de opciones
            "respuesta": p.get("respuesta_correcta", ""),  # JS espera 'respuesta'
            "explicacion": p.get("explicacion", ""),
            "contexto": None  # Si usas contextos, adáptalo aquí
        })

    return jsonify({"preguntas": preguntas})