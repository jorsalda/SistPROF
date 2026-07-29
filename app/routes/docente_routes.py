from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user
from datetime import datetime

from app.models.pregunta import Pregunta
from app.models.materia import Materia
from app.extensions import db
from app.models.docente import Docente
from app.models.permiso import Permiso
from app.models.estudiante import Estudiante
from app.models.grupo import Grupo
from app.models.usuario import Usuario
from app.models.sede import Sede
from werkzeug.security import generate_password_hash
from app.models.grupo import Grupo, GrupoAreas
from app.models.examen import Examen
from app.models.examen_contenido import ExamenContenido
import json
docente_bp = Blueprint("docente", __name__, url_prefix="/docentes")


# ==========================================================
# DASHBOARD DEL DOCENTE (NUEVO - PARA DOCENTE LOGUEADO)
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

    # =====================================================
    # 1. GRUPOS QUE DIRIGE (rol administrativo)
    # =====================================================
    grupos_dirigidos = Grupo.query.filter_by(
        director_docente_id=docente.id,
        activo=True
    ).all()

    ids_grupos_dirigidos = [g.id for g in grupos_dirigidos]

    # Contar estudiantes de grupos dirigidos
    if ids_grupos_dirigidos:
        total_estudiantes_dirigidos = Estudiante.query.filter(
            Estudiante.grupo_id.in_(ids_grupos_dirigidos),
            Estudiante.activo == True
        ).count()
    else:
        total_estudiantes_dirigidos = 0

    # =====================================================
    # 2. ÁREAS QUE ENSEÑA (rol académico) - NUEVO
    # =====================================================
    # Obtener todas las asignaciones de áreas del docente
    asignaciones_areas = db.session.query(GrupoAreas).filter_by(
        docente_id=docente.id,
        activo=True
    ).all()

    # Estructura: {area_nombre: [grupos]}
    carga_academica = {}
    grupos_ids_academicos = set()

    for asignacion in asignaciones_areas:
        area_nombre = asignacion.area.nombre if asignacion.area else "Sin área"
        grupo = asignacion.grupo

        if area_nombre not in carga_academica:
            carga_academica[area_nombre] = []

        grupo_info = {
            'id': grupo.id,
            'nombre': f"{grupo.grado}{grupo.nombre}",
            'sede': grupo.sede.nombre if grupo.sede else "N/A"
        }

        # Evitar duplicados
        if grupo_info not in carga_academica[area_nombre]:
            carga_academica[area_nombre].append(grupo_info)
            grupos_ids_academicos.add(grupo.id)

    # =====================================================
    # 3. ESTUDIANTES DE GRUPOS ACADÉMICOS - NUEVO
    # =====================================================
    # Obtener estudiantes de los grupos donde enseña
    if grupos_ids_academicos:
        estudiantes_academicos = Estudiante.query.filter(
            Estudiante.grupo_id.in_(list(grupos_ids_academicos)),
            Estudiante.activo == True
        ).order_by(Estudiante.nombre).all()
    else:
        estudiantes_academicos = []

    # =====================================================
    # 4. PERMISOS (sin cambios)
    # =====================================================
    total_permisos = Permiso.query.filter_by(
        docente_id=docente.id
    ).count()

    permisos_activos = Permiso.query.filter(
        Permiso.docente_id == docente.id,
        Permiso.fecha_inicio <= hoy,
        Permiso.fecha_fin >= hoy
    ).count()

    ultimos_permisos = Permiso.query.filter_by(
        docente_id=docente.id
    ).order_by(Permiso.fecha_inicio.desc()).limit(5).all()

    # =====================================================
    # RETORNAR TEMPLATE
    # =====================================================
    return render_template(
        "docentes/dashboard.html",
        docente=docente,
        total_estudiantes=total_estudiantes_dirigidos,  # Para mantener compatibilidad
        total_permisos=total_permisos,
        permisos_activos=permisos_activos,
        ultimos_permisos=ultimos_permisos,
        hoy=hoy,
        # NUEVO: Carga académica
        carga_academica=carga_academica,
        estudiantes_academicos=estudiantes_academicos,
        total_areas=len(carga_academica),
        total_grupos_academicos=len(grupos_ids_academicos)
    )

@docente_bp.route("/mis-estudiantes")
@login_required
def mis_estudiantes():
    if current_user.rol != 'docente':
        abort(403)

    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    if not docente:
        flash("No se encontró información del docente", "danger")
        return redirect(url_for("auth.logout"))

    # Obtener filtros
    search = request.args.get('search', '').strip()
    sede_id = request.args.get('sede_id', type=int)

    # Buscar estudiantes a través de los grupos que dirige
    grupos_del_docente = Grupo.query.filter_by(
        director_docente_id=docente.id,
        activo=True
    ).all()

    ids_grupos = [g.id for g in grupos_del_docente]

    # Consulta base
    if ids_grupos:
        consulta = Estudiante.query.filter(
            Estudiante.grupo_id.in_(ids_grupos),
            Estudiante.activo == True
        )

        # Aplicar filtros
        if search:
            from sqlalchemy import or_
            consulta = consulta.filter(
                or_(
                    Estudiante.nombre.ilike(f"%{search}%"),
                    Estudiante.apellido.ilike(f"%{search}%")
                )
            )

        if sede_id:
            consulta = consulta.filter_by(sede_id=sede_id)

        estudiantes_lista = consulta.order_by(Estudiante.nombre).all()
    else:
        estudiantes_lista = []

    # Obtener sedes para el filtro
    from app.models.sede import Sede
    sedes = Sede.query.filter_by(
        colegio_id=docente.colegio_id,
        activo=True
    ).order_by(Sede.nombre).all()

    # Estadísticas
    total_estudiantes = len(estudiantes_lista)
    activos = sum(1 for e in estudiantes_lista if e.activo)

    return render_template(
        "docentes/estudiantes.html",
        estudiantes=estudiantes_lista,
        docente=docente,
        sedes=sedes,
        search=search,
        current_sede_id=sede_id,
        total_estudiantes=total_estudiantes,
        activos=activos
    )

@docente_bp.route("/mis-permisos")
@login_required
def mis_permisos():
    if current_user.rol != 'docente':
        abort(403)

    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    if not docente:
        flash("No se encontró información del docente", "danger")
        return redirect(url_for("auth.logout"))

    permisos_lista = Permiso.query.filter_by(
        docente_id=docente.id
    ).order_by(Permiso.fecha_inicio.desc()).all()

    hoy = datetime.now().date()

    return render_template(
        "docentes/permisos.html",
        permisos=permisos_lista,
        docente=docente,
        hoy=hoy
    )


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
                docente_id=docente.id,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                tipo=tipo,
                observacion=observacion if observacion else None,
                colegio_id=docente.colegio_id
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

    permiso = Permiso.query.filter_by(
        id=permiso_id,
        docente_id=docente.id
    ).first_or_404()

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

            email_existente = Usuario.query.filter(
                Usuario.email == email,
                Usuario.id != current_user.id
            ).first()

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


# ==========================================================
# MÓDULOS FUTUROS DEL DOCENTE
# ==========================================================

@docente_bp.route("/observador")
@login_required
def observador():
    if current_user.rol != 'docente':
        abort(403)

    return render_template("docentes/observador.html")


@docente_bp.route("/citaciones")
@login_required
def citaciones():
    if current_user.rol != 'docente':
        abort(403)

    return render_template("docentes/citaciones.html")


@docente_bp.route("/seguimiento")
@login_required
def seguimiento():
    if current_user.rol != 'docente':
        abort(403)

    return render_template("docentes/seguimiento.html")


# ==========================================================
# CRUD DE DOCENTES (PARA EL COLEGIO) - ADMIN COLEGIO
# ==========================================================

# ========== LISTAR DOCENTES ==========
@docente_bp.route("/")
@login_required
def listar():
    docentes = Docente.query.filter_by(
        colegio_id=current_user.colegio_id
    ).order_by(Docente.nombre).all()

    return render_template("docentes/listado.html", docentes=docentes)


# ========== NUEVO DOCENTE ==========
@docente_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    # Obtener sedes para el formulario
    sedes = Sede.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).order_by(Sede.nombre).all()

    if request.method == "POST":
        # Capturar campos del formulario
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        documento = request.form.get("documento", "").strip()
        email = request.form.get("email", "").strip().lower()
        telefono = request.form.get("telefono", "").strip()
        sede_id = request.form.get("sede_id", "").strip()

        # ==========================================
        # VALIDACIONES
        # ==========================================
        if not nombre:
            flash("El nombre es requerido", "danger")
            return redirect(url_for("docente.nuevo"))

        if not apellido:
            flash("El apellido es requerido", "danger")
            return redirect(url_for("docente.nuevo"))

        if not documento:
            flash("El documento de identidad es requerido", "danger")
            return redirect(url_for("docente.nuevo"))

        if len(documento) < 6:
            flash("El documento debe tener al menos 6 caracteres (será la contraseña inicial)", "danger")
            return redirect(url_for("docente.nuevo"))

        if not email:
            flash("El correo electrónico es requerido", "danger")
            return redirect(url_for("docente.nuevo"))

        # Validar formato de email
        import re
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            flash("El correo electrónico no tiene un formato válido", "danger")
            return redirect(url_for("docente.nuevo"))

        # Validar sede
        if not sede_id:
            flash("Debe seleccionar una sede", "danger")
            return redirect(url_for("docente.nuevo"))

        # ==========================================
        # VERIFICAR DUPLICADOS
        # ==========================================

        # Verificar si ya existe un docente con ese documento en el colegio
        existe_docente_doc = Docente.query.filter_by(
            documento=documento,
            colegio_id=current_user.colegio_id
        ).first()

        if existe_docente_doc:
            flash("Ya existe un docente registrado con ese documento de identidad", "danger")
            return redirect(url_for("docente.nuevo"))

        # Verificar si ya existe un usuario con ese email
        existe_usuario = Usuario.query.filter_by(email=email).first()
        if existe_usuario:
            flash("El correo electrónico ya está registrado en el sistema", "danger")
            return redirect(url_for("docente.nuevo"))

        # ==========================================
        # CREAR USUARIO Y DOCENTE
        # ==========================================
        try:
            # 1️⃣ Crear el usuario (credenciales de acceso)
            usuario = Usuario(
                email=email,
                password_hash=generate_password_hash(documento),
                nombre=nombre,
                apellido=apellido,
                rol='docente',
                colegio_id=current_user.colegio_id,
                sede_id=int(sede_id),
                is_active=True,
                is_approved=True,
                fecha_aprobacion=datetime.now(),
                failed_attempts=0
            )
            db.session.add(usuario)
            db.session.flush()

            # 2️⃣ Crear el docente vinculado al usuario
            docente = Docente(
                nombre=nombre,
                apellido=apellido,
                documento=documento,
                telefono=telefono if telefono else None,
                email=email,
                colegio_id=current_user.colegio_id,
                usuario_id=usuario.id,
                sede_id=int(sede_id),
                activo=True
            )
            db.session.add(docente)
            db.session.commit()

            flash(
                f"✅ Docente '{nombre} {apellido}' registrado correctamente. "
                f"📧 Usuario: {email} | 🔑 Contraseña inicial: {documento}",
                "success"
            )
            return redirect(url_for("docente.listar"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar el docente: {str(e)}", "danger")

    return render_template(
        "docentes/formulario.html",
        docente=None,
        titulo="Nuevo Docente",
        sedes=sedes
    )


# ========== EDITAR DOCENTE ==========
@docente_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    docente = Docente.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    # Obtener sedes para el formulario
    sedes = Sede.query.filter_by(
        colegio_id=current_user.colegio_id,
        activo=True
    ).order_by(Sede.nombre).all()

    if request.method == "POST":
        # Capturar campos
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        documento = request.form.get("documento", "").strip()
        email = request.form.get("email", "").strip().lower()
        telefono = request.form.get("telefono", "").strip()
        sede_id = request.form.get("sede_id", "").strip()
        activo = request.form.get("activo") == "on"

        # ==========================================
        # VALIDACIONES
        # ==========================================
        if not nombre:
            flash("El nombre es requerido", "danger")
            return redirect(url_for("docente.editar", id=id))

        if not apellido:
            flash("El apellido es requerido", "danger")
            return redirect(url_for("docente.editar", id=id))

        if not email:
            flash("El correo electrónico es requerido", "danger")
            return redirect(url_for("docente.editar", id=id))

        # ==========================================
        # VERIFICAR DUPLICADOS (excluyendo este docente)
        # ==========================================

        # Verificar email duplicado
        existe_email = Usuario.query.filter(
            Usuario.email == email,
            Usuario.id != docente.usuario_id
        ).first()

        if existe_email:
            flash("El correo electrónico ya está registrado por otro usuario", "danger")
            return redirect(url_for("docente.editar", id=id))

        # Verificar documento duplicado
        if documento:
            existe_doc = Docente.query.filter(
                Docente.documento == documento,
                Docente.colegio_id == current_user.colegio_id,
                Docente.id != id
            ).first()

            if existe_doc:
                flash("Ya existe otro docente con ese documento de identidad", "danger")
                return redirect(url_for("docente.editar", id=id))

        # ==========================================
        # ACTUALIZAR DATOS
        # ==========================================
        try:
            # Actualizar docente
            docente.nombre = nombre
            docente.apellido = apellido
            docente.documento = documento if documento else None
            docente.telefono = telefono if telefono else None
            docente.email = email
            docente.sede_id = int(sede_id) if sede_id else None
            docente.activo = activo

            # Actualizar usuario asociado (si existe)
            if docente.usuario:
                docente.usuario.nombre = nombre
                docente.usuario.apellido = apellido
                docente.usuario.email = email
                docente.usuario.sede_id = int(sede_id) if sede_id else None

            db.session.commit()

            flash(f"✅ Docente '{nombre} {apellido}' actualizado correctamente", "success")
            return redirect(url_for("docente.listar"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar: {str(e)}", "danger")

    return render_template(
        "docentes/formulario.html",
        docente=docente,
        titulo="Editar Docente",
        sedes=sedes
    )


# ========== ELIMINAR DOCENTE ==========
@docente_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    docente = Docente.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    nombre = docente.nombre

    # Verificar si tiene permisos asociados
    tiene_permisos = Permiso.query.filter_by(docente_id=id).first()

    if tiene_permisos:
        # No eliminar, marcar como inactivo
        docente.activo = False
        db.session.commit()
        flash(f"Docente '{nombre}' desactivado (tiene permisos asociados)", "warning")
    else:
        # Eliminar permanentemente
        db.session.delete(docente)
        db.session.commit()
        flash(f"Docente '{nombre}' eliminado permanentemente", "success")

    return redirect(url_for("docente.listar"))


# ========== VER DETALLE ==========
@docente_bp.route("/ver/<int:id>")
@login_required
def ver(id):
    docente = Docente.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    # Obtener permisos del docente
    permisos = Permiso.query.filter_by(
        docente_id=id
    ).order_by(Permiso.fecha_inicio.desc()).all()

    return render_template("docentes/detalle.html", docente=docente, permisos=permisos)


# ========== API: CAMBIAR ESTADO ==========
@docente_bp.route("/cambiar-estado/<int:id>", methods=["POST"])
@login_required
def cambiar_estado(id):
    docente = Docente.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    docente.activo = not docente.activo
    db.session.commit()

    estado = "activado" if docente.activo else "desactivado"
    return jsonify({
        "success": True,
        "message": f"Docente {estado} correctamente",
        "activo": docente.activo
    })


@docente_bp.route("/banco-preguntas")
@login_required
def banco_preguntas():
    # AHORA: Trae TODAS las preguntas del docente, estén o no en exámenes
    preguntas_banco = Pregunta.query.filter_by(
        docente_id=current_user.id
    ).order_by(Pregunta.fecha_creacion.desc()).all()

    materias = Materia.query.all()

    return render_template(
        "docentes/banco_preguntas.html",
        preguntas=preguntas_banco,
        materias=materias
    )


# ==========================================================
# CREAR EXAMEN DESDE EL BANCO (NUEVO)
# ==========================================================
@docente_bp.route("/crear-desde-banco", methods=["GET", "POST"])
@login_required
def crear_desde_banco():
    """Ruta dedicada para armar exámenes seleccionando del banco"""
    if current_user.rol not in ['docente', 'coordinador', 'admin_colegio']:
        abort(403)

    # Obtener contexto necesario
    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    materias = Materia.query.all()
    preguntas_banco = Pregunta.query.filter_by(docente_id=current_user.id).all()

    if request.method == "POST":
        try:
            # 1. Datos generales
            titulo = request.form.get("titulo_examen", "").strip()
            materia_id = request.form.get("materia_id")
            grado = request.form.get("grado")

            if not titulo or not materia_id:
                flash("Título y materia son obligatorios.", "danger")
                return redirect(url_for("docente.crear_desde_banco"))

            # 2. Obtener IDs seleccionados del banco
            ids_seleccionados_json = request.form.get("ids_preguntas_banco")
            if not ids_seleccionados_json:
                flash("Debes seleccionar al menos una pregunta del banco.", "warning")
                return redirect(url_for("docente.crear_desde_banco"))

            import json
            ids_seleccionados = json.loads(ids_seleccionados_json)

            # Validar que existan las preguntas
            preguntas_validas = Pregunta.query.filter(Pregunta.id.in_(ids_seleccionados)).all()
            if len(preguntas_validas) != len(ids_seleccionados):
                flash("Algunas preguntas seleccionadas no son válidas.", "danger")
                return redirect(url_for("docente.crear_desde_banco"))

            # 3. Crear el Examen
            nuevo_examen = Examen(
                titulo=titulo,
                nombre=titulo,
                descripcion=f"Examen creado desde banco para {grado}",
                materia_id=materia_id,
                colegio_id=current_user.colegio_id,
                tiempo_limite_minutos=30,
                fecha_creacion=datetime.now(),
                activo=True
            )
            db.session.add(nuevo_examen)
            db.session.flush()  # Para obtener el ID

            # 4. Guardar en examen_contenido (JSONB)
            contenido_para_guardar = [
                {"pregunta_id": p.id, "orden": idx + 1}
                for idx, p in enumerate(preguntas_validas)
            ]

            from app.models.examen_contenido import ExamenContenido
            nuevo_contenido = ExamenContenido(
                examen_id=nuevo_examen.id,
                contenido_json=contenido_para_guardar,
                version=1,
                activo=True
            )
            db.session.add(nuevo_contenido)

            db.session.commit()

            flash(f"✅ Examen '{titulo}' creado con {len(preguntas_validas)} preguntas.", "success")
            return redirect(url_for("examen.listar_examenes"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear examen: {str(e)}", "danger")
            import traceback;
            traceback.print_exc()

    return render_template(
        "examenes/crear_examen.html",
        docente=docente,
        materias=materias,
        preguntas_banco=preguntas_banco
    )