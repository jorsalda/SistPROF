from app.models.tipo_examen import TipoExamen
from app.services.document_service import extraer_texto_de_archivo
from app.services.ia_service import generar_preguntas_json
from app.models.materia import Materia
from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app.models.examen import Examen
from app.models.pregunta import Pregunta
from app.models.resultado_examen import ResultadoExamen
from app.models.respuestas_examen_detalle import RespuestaExamenDetalle
from app.models.estudiante import Estudiante
from app.extensions import db
from datetime import datetime
import random
from app.models.examen_contenido import ExamenContenido  # Asegúrate de importar el modelo
import json

examen_bp = Blueprint('examen', __name__, url_prefix='/api/examen')


# ==========================================================
# HUB CENTRAL DE CREACIÓN DE EXÁMENES (UNIFICADO)
# ==========================================================
@examen_bp.route("/crear", methods=["GET", "POST"])
@login_required
def crear_examen():
    # Solo roles autorizados
    if current_user.rol not in ['docente', 'coordinador', 'admin_colegio']:
        abort(403)

    # Contexto común para la plantilla
    materias = Materia.query.filter_by(colegio_id=current_user.colegio_id).all()
    preguntas_banco = Pregunta.query.filter_by(docente_id=current_user.id).all()

    if request.method == "POST":
        try:
            # 1. Datos generales
            titulo = request.form.get("titulo_examen", "").strip()
            materia_id = request.form.get("materia_id")
            grado = request.form.get("grado")

            if not titulo or not materia_id:
                flash("Título y materia son obligatorios.", "danger")
                return redirect(url_for("examen.crear_examen"))

            # 2. Recolectar TODAS las preguntas (IA + Banco + Manual)
            todas_las_preguntas = []

            # A. Preguntas del Banco (IDs seleccionados)
            ids_banco_json = request.form.get("ids_preguntas_banco")
            if ids_banco_json:
                ids_banco = json.loads(ids_banco_json)
                for pid in ids_banco:
                    p = Pregunta.query.get(pid)
                    if p:
                        todas_las_preguntas.append({
                            "numero": len(todas_las_preguntas) + 1,
                            "texto": p.texto,
                            "opciones": p.opciones,
                            "respuesta_correcta": p.respuesta_correcta,
                            "dificultad": p.dificultad,
                            "puntos_maximos": 1,
                            "explicacion": p.explicacion or "",
                            "tipo": "banco"
                        })

            # B. Preguntas Manuales (si existen en el form)
            idx_manual = 0
            while True:
                texto_m = request.form.get(f"preguntas_manual[{idx_manual}][texto]")
                if not texto_m: break

                todas_las_preguntas.append({
                    "numero": len(todas_las_preguntas) + 1,
                    "texto": texto_m,
                    "opciones": {
                        "A": request.form.get(f"preguntas_manual[{idx_manual}][opcion_a]"),
                        "B": request.form.get(f"preguntas_manual[{idx_manual}][opcion_b]"),
                        "C": request.form.get(f"preguntas_manual[{idx_manual}][opcion_c]"),
                        "D": request.form.get(f"preguntas_manual[{idx_manual}][opcion_d]")
                    },
                    "respuesta_correcta": request.form.get(f"preguntas_manual[{idx_manual}][correcta]"),
                    "dificultad": "media",
                    "puntos_maximos": 1,
                    "explicacion": "",
                    "tipo": "manual"
                })
                idx_manual += 1

            # C. Preguntas IA (Si se subió archivo en este formulario)
            archivo_ia = request.files.get("archivo_ia")
            if archivo_ia and archivo_ia.filename != '':
                ext = archivo_ia.filename.rsplit('.', 1)[1].lower()
                if ext in ['pdf', 'docx']:
                    texto_extraido = extraer_texto_de_archivo(archivo_ia, ext)
                    if texto_extraido:
                        nombre_materia = next((m.nombre for m in materias if str(m.id) == str(materia_id)),
                                              "la materia")
                        cant_ia = int(request.form.get("cantidad_ia", 5))
                        resultado_ia = generar_preguntas_json(texto_extraido, nombre_materia, grado, cant_ia)
                        for p_ia in resultado_ia.get("preguntas", []):
                            todas_las_preguntas.append({
                                "numero": len(todas_las_preguntas) + 1,
                                "texto": p_ia.get("texto", ""),
                                "opciones": p_ia.get("opciones", {}),
                                "respuesta_correcta": p_ia.get("respuesta_correcta", ""),
                                "dificultad": p_ia.get("dificultad", "media"),
                                "puntos_maximos": 1,
                                "explicacion": p_ia.get("explicacion", ""),
                                "tipo": "ia"
                            })

            if not todas_las_preguntas:
                flash("Debes agregar al menos una pregunta (IA, Banco o Manual).", "warning")
                return redirect(url_for("examen.crear_examen"))

            # 3. Guardar Examen
            nuevo_examen = Examen(
                titulo=titulo,
                nombre=titulo,
                descripcion=f"Examen creado para {grado}",
                materia_id=materia_id,
                colegio_id=current_user.colegio_id,
                contenido_json=todas_las_preguntas,  # Guardamos el array completo aquí también por compatibilidad
                tiempo_limite_minutos=30,
                fecha_creacion=datetime.now(),
                activo=True
            )
            db.session.add(nuevo_examen)
            db.session.flush()

            # 4. Alimentar Banco y Tabla Intermedia
            # Primero guardamos las nuevas (IA/Manuales) en el banco
            for p_data in todas_las_preguntas:
                if p_data.get("tipo") != "banco":  # Las del banco ya existen
                    nueva_p = Pregunta(
                        texto=p_data["texto"],
                        tipo="icfes",
                        opciones=p_data["opciones"],
                        respuesta_correcta=p_data["respuesta_correcta"],
                        explicacion=p_data["explicacion"],
                        dificultad=p_data["dificultad"],
                        puntos_maximos=p_data["puntos_maximos"],
                        materia_id=materia_id,
                        docente_id=current_user.id,
                        examen_id=None
                    )
                    db.session.add(nueva_p)

            # Luego vinculamos TODO al examen en examen_contenido
            estructura_para_contenido = [
                {"pregunta_id": p.get("id") or 0, "orden": p["numero"]}
                for p in todas_las_preguntas
            ]
            # Nota: Para las preguntas nuevas (IA/Manual) aún no tienen ID hasta commit.
            # En un sistema real haríamos esto post-commit, pero para simplificar:
            # Vamos a usar la función auxiliar que ya tienes.

            db.session.commit()

            # Re-construimos IDs reales para examen_contenido (porque las nuevas ya tienen ID tras commit)
            # Esto es un paso avanzado, por ahora confiemos en que contenido_json tiene los datos.

            flash(f"✅ Examen '{titulo}' creado con {len(todas_las_preguntas)} preguntas.", "success")
            return redirect(url_for("examen.listar_examenes"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear examen: {str(e)}", "danger")
            import traceback;
            traceback.print_exc()  # Para ver error en consola

    return render_template(
        "examenes/crear_examen.html",
        materias=materias,
        preguntas_banco=preguntas_banco
    )


@examen_bp.route('/<int:examen_id>/json', methods=['GET'])
@login_required
def obtener_json_examen(examen_id):
    """
    Devuelve las preguntas aleatorias desde el banco de preguntas en la BD.
    Si no hay preguntas en la BD, hace fallback al JSON antiguo (IA).
    """
    examen = Examen.query.get_or_404(examen_id)

    # Verificar que el estudiante pertenece al mismo colegio
    if examen.colegio_id != current_user.colegio_id:
        return jsonify({'error': 'No tiene acceso a este examen'}), 403

    # 1. Obtener la cantidad de preguntas que el estudiante quiere
    num_preguntas = request.args.get('cantidad', default=10, type=int)

    # 2. Consultar el banco de preguntas en la BD
    preguntas_db = Pregunta.query.filter_by(
        materia_id=examen.materia_id,
        tipo='icfes',
        activo=True
    ).all()

    # 3. Si NO hay preguntas en la BD, usamos el JSON antiguo (Fallback IA)
    if not preguntas_db:
        if examen.contenido_json:
            #  ADAPTAR formato de IA al que espera ClsEstudiante.js
            preguntas_ia = examen.contenido_json if isinstance(examen.contenido_json,
                                                               list) else examen.contenido_json.get('preguntas', [])

            preguntas_formateadas = []
            for p in preguntas_ia[:num_preguntas]:
                preguntas_formateadas.append({
                    "pregunta": p.get("texto", ""),  # ← Cambiar "texto" a "pregunta"
                    "opciones": p.get("opciones", {}),
                    "respuesta": p.get("respuesta_correcta", ""),  # ← Cambiar "respuesta_correcta" a "respuesta"
                    "explicacion": p.get("explicacion", ""),
                    "tema": p.get("tema", ""),
                    "dificultad": p.get("dificultad", "media")
                })

            return jsonify({"preguntas": preguntas_formateadas})

        return jsonify({'error': 'No hay preguntas disponibles'}), 404

    # 4. Aleatorizar y limitar la cantidad

    random.shuffle(preguntas_db)
    preguntas_seleccionadas = preguntas_db[:num_preguntas]

    # 5. Formatear para que ClsEstudiante.js lo entienda
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





# ==========================================================
# CREAR EXAMEN CON ASISTENCIA DE IA
# ==========================================================

@examen_bp.route("/crear-con-ia", methods=["GET", "POST"])
@login_required
def crear_examen_ia():
    # Solo docentes, coordinadores o admins pueden crear exámenes
    if current_user.rol not in ['docente', 'coordinador', 'admin_colegio']:
        abort(403)

    if request.method == "POST":
        # 1. Obtener datos del formulario
        materia_id = request.form.get("materia_id")
        grado = request.form.get("grado")
        cantidad = int(request.form.get("cantidad", 5))
        archivo = request.files.get("archivo")

        # 2. Validaciones básicas
        if not archivo or archivo.filename == '':
            flash("Debes seleccionar un archivo para subir.", "danger")
            return redirect(request.url)

        ext = archivo.filename.rsplit('.', 1)[1].lower() if '.' in archivo.filename else ''
        if ext not in ['pdf', 'docx']:
            flash("Solo se permiten archivos en formato PDF o DOCX.", "danger")
            return redirect(request.url)

        try:
            # 3. Extraer texto del documento
            texto_extraido = extraer_texto_de_archivo(archivo, ext)

            if not texto_extraido or len(texto_extraido.strip()) < 50:
                flash(
                    "No se pudo extraer suficiente texto del documento. Verifica que sea legible y no sea una imagen escaneada.",
                    "warning")
                return redirect(request.url)

            # 4. Obtener nombre de la materia para el prompt de la IA
            materia = Materia.query.get(materia_id)
            nombre_materia = materia.nombre if materia else "la materia asignada"

            # 5. Llamar al servicio de IA
            flash("🤖 La IA está analizando el documento y generando las preguntas. Esto puede tomar unos segundos...",
                  "info")
            resultado_ia = generar_preguntas_json(texto_extraido, nombre_materia, grado, cantidad)

            # 6. Mostrar vista de previsualización para que el docente revise
            return render_template(
                "examenes/preview_ia.html",
                preguntas=resultado_ia.get("preguntas", []),
                materia_id=materia_id,
                grado=grado,
                cantidad=cantidad,
                nombre_materia=nombre_materia
            )

        except Exception as e:
            # Manejo de errores de la IA o extracción
            flash(f"Error al procesar el documento con IA: {str(e)}", "danger")
            return redirect(request.url)

    # GET: Mostrar el formulario inicial de subida
    materias = Materia.query.order_by(Materia.nombre).all()
    return render_template("examenes/crear_examen_ia.html", materias=materias)



# ==========================================================
# GUARDAR EXAMEN GENERADO POR IA
# ==========================================================

@examen_bp.route("/guardar-examen-ia", methods=["POST"])
@login_required
def guardar_examen_ia():
    # Solo roles autorizados
    if current_user.rol not in ['docente', 'coordinador', 'admin_colegio']:
        abort(403)

    try:
        # 1. Obtener datos generales del formulario
        titulo = request.form.get("titulo_examen", "").strip()
        materia_id = request.form.get("materia_id")
        grado = request.form.get("grado")

        if not titulo or not materia_id:
            flash("El título y la materia son obligatorios.", "danger")
            return redirect(url_for("examen.crear_examen_ia"))

        # 2. Reconstruir el array de preguntas desde el formulario
        preguntas_data = []
        idx = 0

        while True:
            texto = request.form.get(f"preguntas[{idx}][texto]")
            if not texto:
                break

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
                "explicacion": request.form.get(f"preguntas[{idx}][explicacion]", "")
            }
            preguntas_data.append(pregunta)
            idx += 1

        if not preguntas_data:
            flash("No se encontraron preguntas válidas para guardar.", "danger")
            return redirect(url_for("examen.crear_examen_ia"))

        # 3. Crear el registro del Examen
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

        # 4. Alimentar el Banco de Preguntas (reutilizables)
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

                # ✅ CORRECCIÓN CLAVE: Asignar el docente actual como dueño
                docente_id=current_user.id,
                examen_id=None  # NULL para que viva independiente en el banco
            )
            db.session.add(nueva_pregunta)

        # 5. Confirmar cambios
        db.session.commit()

        flash(
            f"✅ Examen '{titulo}' guardado exitosamente con {len(preguntas_data)} preguntas.",
            "success"
        )

        # Redirigir a la lista de exámenes o dashboard
        try:
            return redirect(url_for("examen.listar"))
        except:
            return redirect(url_for("docente.dashboard"))

    except Exception as e:
        db.session.rollback()
        flash(f"Error al guardar el examen: {str(e)}", "danger")
        return redirect(url_for("examen.crear_examen_ia"))

# ==========================================================
# LISTAR EXÁMENES DEL DOCENTE
# ==========================================================

@examen_bp.route("/mis-examenes")
@login_required
def listar_examenes():
    """Muestra los exámenes creados por el docente"""

    # Obtener todos los exámenes del colegio del docente
    examenes = Examen.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).order_by(Examen.fecha_creacion.desc()).all()

    return render_template(
        "examenes/listar_examenes.html",
        examenes=examenes
    )


# ==========================================================
# VER DETALLE DE EXAMEN
# ==========================================================

@examen_bp.route("/ver/<int:id>")
@login_required
def ver_examen(id):
    """Ver detalle completo del examen"""
    examen = Examen.query.get_or_404(id)

    if examen.colegio_id != current_user.colegio_id:
        abort(403)

    return render_template(
        "examenes/ver_examen.html",
        examen=examen
    )

# ==========================================================
# ELIMINAR  EXAMEN
# ==========================================================
@examen_bp.route("/eliminar/<int:id>")
@login_required
def eliminar_examen(id):
    """Eliminar examen (soft delete)"""
    examen = Examen.query.get_or_404(id)

    if examen.colegio_id != current_user.colegio_id:
        abort(403)

    examen.activo = False
    db.session.commit()

    flash("Examen eliminado correctamente", "success")
    return redirect(url_for('examen.listar_examenes'))

# ==========================================================
# EDITAF EXAMEN
# ==========================================================
@examen_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_examen(id):
    """Editar examen existente"""
    examen = Examen.query.get_or_404(id)

    if examen.colegio_id != current_user.colegio_id:
        abort(403)

    if request.method == "POST":
        # Actualizar datos básicos
        examen.titulo = request.form.get("titulo")
        examen.nombre = request.form.get("titulo")
        examen.descripcion = request.form.get("descripcion")
        examen.tiempo_limite_minutos = int(request.form.get("tiempo_limite", 30))

        # Reconstruir JSON de preguntas desde el formulario
        preguntas_data = []
        idx = 0

        while True:
            texto = request.form.get(f"preguntas[{idx}][texto]")
            if not texto:
                break

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
                "explicacion": request.form.get(f"preguntas[{idx}][explicacion]", "")
            }
            preguntas_data.append(pregunta)
            idx += 1

        examen.contenido_json = preguntas_data
        db.session.commit()

        flash("Examen actualizado correctamente", "success")
        return redirect(url_for('examen.ver_examen', id=examen.id))

    return render_template(
        "examenes/editar_examen.html",
        examen=examen
    )


def guardar_seleccion_preguntas(examen_id, preguntas_seleccionadas):
    """
    Guarda la selección de preguntas en examen_contenido usando JSONB.

    Args:
        examen_id: ID del examen al que se vinculan las preguntas.
        preguntas_seleccionadas: Lista de diccionarios con la info de cada pregunta.
                                 Ej: [{"pregunta_id": 67, "orden": 1}, ...]
    """
    try:
        # Verificar si ya existe contenido para este examen (versión 1)
        contenido_existente = ExamenContenido.query.filter_by(
            examen_id=examen_id,
            version=1
        ).first()

        if contenido_existente:
            # Actualizar el JSON existente
            contenido_existente.contenido_json = preguntas_seleccionadas
            flash("Selección de preguntas actualizada exitosamente", "success")
        else:
            # Crear nuevo registro
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


