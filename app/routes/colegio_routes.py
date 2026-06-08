from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, session
from flask_login import login_required, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash

from app import Coordinador
from app.extensions import db
from app.models.colegio import Colegio
from app.models.docente import Docente
from app.models.permiso import Permiso
from app.models.sede import Sede
from app.models.estudiante import Estudiante
from app.models.jornada import Jornada
from app.models.usuario import Usuario

colegio_bp = Blueprint(
    "colegio",
    __name__,
    url_prefix="/dashboard"
)


# ==========================================================
# DASHBOARD PRINCIPAL
# ==========================================================
@colegio_bp.route("/")
@login_required
def dashboard():
    if current_user.is_superadmin:
        return redirect(url_for("admin.dashboard"))

    colegio = Colegio.query.get_or_404(current_user.colegio_id)
    hoy = datetime.utcnow().date()

    total_sedes = Sede.query.filter_by(colegio_id=current_user.colegio_id, activo=True).count()
    total_jornadas = Jornada.query.filter_by(colegio_id=current_user.colegio_id, activo=True).count()
    total_docentes = Docente.query.filter_by(colegio_id=current_user.colegio_id, activo=True).count()
    total_estudiantes = Estudiante.query.filter_by(colegio_id=current_user.colegio_id, activo=True).count()
    total_permisos = Permiso.query.filter_by(colegio_id=current_user.colegio_id).count()

    permisos_activos = Permiso.query.filter(
        Permiso.colegio_id == current_user.colegio_id,
        Permiso.fecha_inicio <= hoy,
        Permiso.fecha_fin >= hoy
    ).count()

    permisos_pendientes = Permiso.query.filter(
        Permiso.colegio_id == current_user.colegio_id,
        Permiso.fecha_inicio > hoy
    ).count()

    ultimos_permisos = Permiso.query.filter_by(
        colegio_id=current_user.colegio_id
    ).order_by(Permiso.fecha_inicio.desc()).limit(5).all()

    return render_template(
        "colegio/dashboard.html",
        colegio=colegio,
        total_sedes=total_sedes,
        total_jornadas=total_jornadas,
        total_docentes=total_docentes,
        total_estudiantes=total_estudiantes,
        total_permisos=total_permisos,
        permisos_activos=permisos_activos,
        permisos_pendientes=permisos_pendientes,
        ultimos_permisos=ultimos_permisos,
        hoy=hoy
    )


# ==========================================================
# SEDES
# ==========================================================
@colegio_bp.route("/sedes")
@login_required
def sedes():
    colegio = Colegio.query.get_or_404(current_user.colegio_id)
    sedes = colegio.sedes
    return render_template("colegio/sedes.html", colegio=colegio, sedes=sedes)


@colegio_bp.route("/sedes/nueva", methods=["GET", "POST"])
@login_required
def nueva_sede():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        direccion = request.form.get("direccion", "").strip()
        telefono = request.form.get("telefono", "").strip()
        activo = request.form.get("activo") == "on"

        if not nombre:
            flash("El nombre de la sede es obligatorio", "danger")
            return redirect(url_for("colegio.nueva_sede"))

        existe = Sede.query.filter_by(nombre=nombre, colegio_id=current_user.colegio_id).first()
        if existe:
            flash("Ya existe una sede con ese nombre", "warning")
            return redirect(url_for("colegio.nueva_sede"))

        sede = Sede(
            nombre=nombre,
            direccion=direccion if direccion else None,
            telefono=telefono if telefono else None,
            activo=activo,
            colegio_id=current_user.colegio_id
        )
        db.session.add(sede)
        db.session.commit()
        flash("Sede registrada correctamente", "success")
        return redirect(url_for("colegio.sedes"))

    return render_template("colegio/formulario_sede.html")


@colegio_bp.route("/sedes/<int:sede_id>")
@login_required
def detalle_sede(sede_id):
    sede = Sede.query.filter_by(id=sede_id, colegio_id=current_user.colegio_id).first_or_404()
    docentes = Docente.query.filter_by(sede_id=sede.id, activo=True).order_by(Docente.nombre).all()
    estudiantes = Estudiante.query.filter_by(sede_id=sede.id, activo=True).all()
    jornadas = Jornada.query.filter_by(sede_id=sede.id, activo=True).all()
    return render_template("colegio/detalle_sede.html", sede=sede, docentes=docentes, estudiantes=estudiantes,
                           jornadas=jornadas)


@colegio_bp.route("/sedes/<int:sede_id>/editar", methods=["GET", "POST"])
@login_required
def editar_sede(sede_id):
    sede = Sede.query.filter_by(id=sede_id, colegio_id=current_user.colegio_id).first_or_404()
    if request.method == "POST":
        sede.nombre = request.form.get("nombre")
        sede.direccion = request.form.get("direccion")
        sede.telefono = request.form.get("telefono")
        sede.activo = request.form.get("activo") == "on"
        db.session.commit()
        flash("Sede actualizada correctamente", "success")
        return redirect(url_for("colegio.detalle_sede", sede_id=sede.id))
    return render_template("colegio/formulario_sede.html", sede=sede)


@colegio_bp.route("/sedes/<int:sede_id>/desactivar", methods=["POST"])
@login_required
def desactivar_sede(sede_id):
    sede = Sede.query.filter_by(id=sede_id, colegio_id=current_user.colegio_id).first_or_404()
    sede.activo = False
    db.session.commit()
    flash("Sede desactivada correctamente", "warning")
    return redirect(url_for("colegio.sedes"))


@colegio_bp.route("/sedes/<int:sede_id>/activar", methods=["POST"])
@login_required
def activar_sede(sede_id):
    sede = Sede.query.filter_by(id=sede_id, colegio_id=current_user.colegio_id).first_or_404()
    sede.activo = True
    db.session.commit()
    flash("Sede activada correctamente", "success")
    return redirect(url_for("colegio.sedes"))


@colegio_bp.route('/seleccionar-sede/<int:sede_id>')
@login_required
def seleccionar_sede(sede_id):
    sede = Sede.query.filter_by(id=sede_id, colegio_id=current_user.colegio_id).first()
    if sede:
        session['sede_actual_id'] = sede_id
        flash(f'Sede seleccionada: {sede.nombre}', 'success')
    else:
        flash('Sede no válida', 'danger')
    return redirect(url_for('colegio.dashboard'))


# ==========================================================
# JORNADAS
# ==========================================================
@colegio_bp.route("/sedes/<int:sede_id>/jornadas")
@login_required
def jornadas_sede(sede_id):
    sede = Sede.query.filter_by(id=sede_id, colegio_id=current_user.colegio_id).first_or_404()
    jornadas = sede.jornadas
    return render_template("colegio/jornadas_sede.html", sede=sede, jornadas=jornadas)


@colegio_bp.route("/sedes/<int:sede_id>/jornadas/nueva", methods=["GET", "POST"])
@login_required
def nueva_jornada(sede_id):
    sede = Sede.query.filter_by(id=sede_id, colegio_id=current_user.colegio_id).first_or_404()
    if request.method == "POST":
        nombre = request.form.get("nombre")
        hora_inicio = request.form.get("hora_inicio")
        hora_fin = request.form.get("hora_fin")
        tolerancia_minutos = request.form.get("tolerancia_minutos", 0)
        jornada = Jornada(
            nombre=nombre,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            tolerancia_minutos=tolerancia_minutos,
            sede_id=sede.id,
            colegio_id=current_user.colegio_id,
            activo=True
        )
        db.session.add(jornada)
        db.session.commit()
        flash("Jornada registrada correctamente", "success")
        return redirect(url_for("colegio.jornadas_sede", sede_id=sede.id))
    return render_template("colegio/formulario_jornada.html", sede=sede)


# ==========================================================
# DOCENTES
# ==========================================================
# ==========================================================
# DOCENTES (CORREGIDO - CON USUARIO Y CONTRASEÑA)
# ==========================================================

@colegio_bp.route("/docentes")
@login_required
def lista_docentes():
    sede_id = request.args.get("sede_id")
    docentes_query = Docente.query.filter_by(colegio_id=current_user.colegio_id)
    if sede_id:
        docentes_query = docentes_query.filter_by(sede_id=sede_id)
    docentes = docentes_query.order_by(Docente.nombre).all()
    sedes = Sede.query.filter_by(colegio_id=current_user.colegio_id, activo=True).order_by(Sede.nombre).all()
    return render_template("colegio/docentes.html", docentes=docentes, sedes=sedes, sede_id=sede_id)


@colegio_bp.route("/docentes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_docente():
    if not current_user.es_admin_colegio:
        abort(403)

    sedes = Sede.query.filter_by(colegio_id=current_user.colegio_id, activo=True).order_by(Sede.nombre).all()

    if request.method == "POST":
        try:
            nombre = request.form.get("nombre", "").strip()
            documento = request.form.get("documento", "").strip()
            telefono = request.form.get("telefono", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "").strip()
            sede_id = request.form.get("sede_id")

            # Validaciones
            if not nombre:
                flash("El nombre completo es obligatorio", "danger")
                return redirect(url_for("colegio.nuevo_docente"))

            if not email:
                flash("El correo electrónico es obligatorio", "danger")
                return redirect(url_for("colegio.nuevo_docente"))

            if not password or len(password) < 6:
                flash("La contraseña debe tener al menos 6 caracteres", "danger")
                return redirect(url_for("colegio.nuevo_docente"))

            if not sede_id:
                flash("Debe seleccionar una sede", "danger")
                return redirect(url_for("colegio.nuevo_docente"))

            # Verificar email existente
            if Usuario.query.filter_by(email=email).first():
                flash("El correo electrónico ya está registrado", "danger")
                return redirect(url_for("colegio.nuevo_docente"))

            # 1. Crear Usuario
            usuario = Usuario(
                nombre=nombre,
                email=email,
                password_hash=generate_password_hash(password),
                rol='docente',
                colegio_id=current_user.colegio_id,
                sede_id=sede_id,
                is_active=True,
                is_approved=True
            )
            db.session.add(usuario)
            db.session.flush()

            # 2. Crear Docente vinculado al Usuario
            docente = Docente(
                usuario_id=usuario.id,
                nombre=nombre,
                documento=documento if documento else None,
                telefono=telefono if telefono else None,
                email=email if email else None,
                sede_id=sede_id,
                colegio_id=current_user.colegio_id,
                activo=True
            )
            db.session.add(docente)
            db.session.commit()

            flash(f"Docente '{nombre}' registrado correctamente", "success")
            return redirect(url_for("colegio.lista_docentes"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar docente: {str(e)}", "danger")
            return redirect(url_for("colegio.nuevo_docente"))

    # ✅ Corregido: apunta a docentes/formulario.html
    return render_template("docentes/formulario.html", docente=None, titulo="Nuevo Docente", sedes=sedes)


@colegio_bp.route("/docentes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_docente(id):
    docente = Docente.query.filter_by(id=id, colegio_id=current_user.colegio_id).first_or_404()
    sedes = Sede.query.filter_by(colegio_id=current_user.colegio_id, activo=True).order_by(Sede.nombre).all()

    if request.method == "POST":
        try:
            nombre = request.form.get("nombre", "").strip()
            documento = request.form.get("documento", "").strip()
            telefono = request.form.get("telefono", "").strip()
            email = request.form.get("email", "").strip()
            sede_id = request.form.get("sede_id")
            activo = (request.form.get("activo") == "on")

            if not nombre:
                flash("El nombre es obligatorio", "danger")
                return redirect(url_for("colegio.editar_docente", id=docente.id))

            if not sede_id:
                flash("Debe seleccionar una sede", "danger")
                return redirect(url_for("colegio.editar_docente", id=docente.id))

            # Verificar email no duplicado (excluyendo el actual)
            if docente.usuario:
                email_existente = Usuario.query.filter(
                    Usuario.email == email,
                    Usuario.id != docente.usuario_id
                ).first()

                if email_existente:
                    flash("El correo electrónico ya está registrado por otro usuario", "danger")
                    return redirect(url_for("colegio.editar_docente", id=docente.id))

                # Actualizar Usuario
                docente.usuario.nombre = nombre
                docente.usuario.email = email
                docente.usuario.sede_id = sede_id
            else:
                # Si por alguna razón no tiene usuario, crear uno
                usuario = Usuario(
                    nombre=nombre,
                    email=email,
                    password_hash=generate_password_hash("cambiarmepronto123"),
                    rol='docente',
                    colegio_id=current_user.colegio_id,
                    sede_id=sede_id,
                    is_active=activo,
                    is_approved=True
                )
                db.session.add(usuario)
                db.session.flush()
                docente.usuario_id = usuario.id

            # Actualizar Docente
            docente.nombre = nombre
            docente.documento = documento if documento else None
            docente.telefono = telefono if telefono else None
            docente.email = email if email else None
            docente.sede_id = sede_id
            docente.activo = activo

            db.session.commit()
            flash("Docente actualizado correctamente", "success")
            return redirect(url_for("colegio.lista_docentes"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar docente: {str(e)}", "danger")
            return redirect(url_for("colegio.editar_docente", id=docente.id))

    # ✅ Corregido: apunta a docentes/formulario.html
    return render_template("docentes/formulario.html", docente=docente, titulo="Editar Docente", sedes=sedes)


@colegio_bp.route("/docentes/<int:id>/cambiar-estado")
@login_required
def cambiar_estado_docente(id):
    docente = Docente.query.filter_by(id=id, colegio_id=current_user.colegio_id).first_or_404()

    try:
        docente.activo = not docente.activo
        if docente.usuario:
            docente.usuario.is_active = docente.activo
        db.session.commit()

        estado = "activado" if docente.activo else "desactivado"
        flash(f"Docente {estado} correctamente", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", "danger")

    return redirect(url_for("colegio.lista_docentes"))


@colegio_bp.route("/docentes/<int:id>/cambiar-password", methods=["GET", "POST"])
@login_required
def cambiar_password_docente(id):
    docente = Docente.query.filter_by(id=id, colegio_id=current_user.colegio_id).first_or_404()

    if request.method == "POST":
        nueva_password = request.form.get("password", "").strip()

        if not nueva_password or len(nueva_password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres", "danger")
            return redirect(url_for("colegio.cambiar_password_docente", id=docente.id))

        try:
            if docente.usuario:
                docente.usuario.password_hash = generate_password_hash(nueva_password)
            else:
                # Si no tiene usuario, crear uno
                usuario = Usuario(
                    nombre=docente.nombre,
                    email=docente.email,
                    password_hash=generate_password_hash(nueva_password),
                    rol='docente',
                    colegio_id=current_user.colegio_id,
                    sede_id=docente.sede_id,
                    is_active=docente.activo,
                    is_approved=True
                )
                db.session.add(usuario)
                db.session.flush()
                docente.usuario_id = usuario.id

            db.session.commit()
            flash("Contraseña actualizada correctamente", "success")
            return redirect(url_for("colegio.lista_docentes"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")

    # ✅ Corregido: apunta a docentes/cambiar_password.html
    return render_template("docentes/cambiar_password.html", docente=docente)


@colegio_bp.route("/docentes/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_docente(id):
    docente = Docente.query.filter_by(id=id, colegio_id=current_user.colegio_id).first_or_404()

    tiene_permisos = Permiso.query.filter_by(docente_id=id).first()

    try:
        if tiene_permisos:
            docente.activo = False
            if docente.usuario:
                docente.usuario.is_active = False
            db.session.commit()
            flash("Docente desactivado (tiene permisos asociados)", "warning")
        else:
            usuario = docente.usuario
            db.session.delete(docente)
            if usuario:
                db.session.delete(usuario)
            db.session.commit()
            flash("Docente eliminado correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", "danger")

    return redirect(url_for("colegio.lista_docentes"))
# ==========================================================
# PERMISOS
# ==========================================================
@colegio_bp.route("/permisos")
@login_required
def lista_permisos():
    permisos = Permiso.query.filter_by(colegio_id=current_user.colegio_id).order_by(Permiso.fecha_inicio.desc()).all()
    hoy = datetime.utcnow().date()
    return render_template("colegio/permisos.html", permisos=permisos, hoy=hoy)


@colegio_bp.route("/docentes/<int:docente_id>/permisos")
@login_required
def permisos_docente(docente_id):
    docente = Docente.query.filter_by(id=docente_id, colegio_id=current_user.colegio_id).first_or_404()
    permisos = Permiso.query.filter_by(docente_id=docente_id, colegio_id=current_user.colegio_id).order_by(
        Permiso.fecha_inicio.desc()).all()
    hoy = datetime.utcnow().date()
    return render_template("colegio/permisos_docente.html", docente=docente, permisos=permisos, hoy=hoy)


@colegio_bp.route("/permisos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_permiso():
    docentes = Docente.query.filter_by(colegio_id=current_user.colegio_id, activo=True).all()
    if request.method == "POST":
        permiso = Permiso(
            docente_id=request.form.get("docente_id"),
            fecha_inicio=request.form.get("fecha_inicio"),
            fecha_fin=request.form.get("fecha_fin"),
            tipo=request.form.get("tipo"),
            observacion=request.form.get("observacion"),
            colegio_id=current_user.colegio_id
        )
        db.session.add(permiso)
        db.session.commit()
        flash("Permiso registrado correctamente", "success")
        return redirect(url_for("colegio.lista_permisos"))
    return render_template("colegio/formulario_permiso.html", docentes=docentes)


@colegio_bp.route("/permisos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_permiso(id):
    permiso = Permiso.query.filter_by(id=id, colegio_id=current_user.colegio_id).first_or_404()
    db.session.delete(permiso)
    db.session.commit()
    flash("Permiso eliminado correctamente", "success")
    return redirect(url_for("colegio.lista_permisos"))


# ==========================================================
# COORDINADORES (CORREGIDO Y LIMPIO)
# ==========================================================

# ==========================================================
# COORDINADORES (CORREGIDO - CON RUTAS A TU ESTRUCTURA)
# ==========================================================

@colegio_bp.route('/coordinadores')
@login_required
def lista_coordinadores():
    sede_id = request.args.get('sede_id', type=int)
    consulta = Coordinador.query.filter_by(colegio_id=current_user.colegio_id)

    if sede_id:
        consulta = consulta.filter_by(sede_id=sede_id)

    coordinadores = consulta.all()
    sedes = Sede.query.filter_by(colegio_id=current_user.colegio_id).all()

    # ✅ Corregido: apunta a coordinador/coordinadores.html
    return render_template(
        'coordinador/coordinadores.html',  # ← Cambiado de colegio/ a coordinador/
        coordinadores=coordinadores,
        sedes=sedes,
        sede_actual_id=sede_id
    )


@colegio_bp.route('/coordinadores/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_coordinador():
    if not current_user.es_admin_colegio:
        abort(403)

    sedes = Sede.query.filter_by(colegio_id=current_user.colegio_id).all()

    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '').strip()
            documento = request.form.get('documento', '').strip()
            telefono = request.form.get('telefono', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()
            sede_id = request.form.get('sede_id')

            if not nombre:
                flash('El nombre completo es obligatorio', 'danger')
                return redirect(url_for('colegio.nuevo_coordinador'))

            if not email:
                flash('El correo electrónico es obligatorio', 'danger')
                return redirect(url_for('colegio.nuevo_coordinador'))

            if not password or len(password) < 6:
                flash('La contraseña debe tener al menos 6 caracteres', 'danger')
                return redirect(url_for('colegio.nuevo_coordinador'))

            if not sede_id:
                flash('Debe seleccionar una sede', 'danger')
                return redirect(url_for('colegio.nuevo_coordinador'))

            if Usuario.query.filter_by(email=email).first():
                flash('El correo electrónico ya está registrado', 'danger')
                return redirect(url_for('colegio.nuevo_coordinador'))

            usuario = Usuario(
                nombre=nombre,
                email=email,
                password_hash=generate_password_hash(password),
                rol='coordinador',
                colegio_id=current_user.colegio_id,
                sede_id=sede_id,
                is_active=True,
                is_approved=True
            )
            db.session.add(usuario)
            db.session.flush()

            coordinador = Coordinador(
                usuario_id=usuario.id,
                colegio_id=current_user.colegio_id,
                sede_id=sede_id,
                documento=documento if documento else None,
                telefono=telefono if telefono else None,
                cargo='Coordinador Académico'
            )
            db.session.add(coordinador)
            db.session.commit()

            flash(f'Coordinador {nombre} registrado correctamente', 'success')
            return redirect(url_for('colegio.lista_coordinadores'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar coordinador: {str(e)}', 'danger')
            return redirect(url_for('colegio.nuevo_coordinador'))

    # ✅ Corregido: apunta a coordinador/formulario_coordinador.html
    return render_template('coordinador/formulario_coordinador.html', sedes=sedes)


@colegio_bp.route('/coordinadores/<int:coordinador_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_coordinador(coordinador_id):
    coordinador = Coordinador.query.filter_by(
        id=coordinador_id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    sedes = Sede.query.filter_by(colegio_id=current_user.colegio_id).all()

    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '').strip()
            documento = request.form.get('documento', '').strip()
            telefono = request.form.get('telefono', '').strip()
            email = request.form.get('email', '').strip()
            sede_id = request.form.get('sede_id')

            if not nombre:
                flash('El nombre completo es obligatorio', 'danger')
                return redirect(url_for('colegio.editar_coordinador', coordinador_id=coordinador.id))

            if not email:
                flash('El correo electrónico es obligatorio', 'danger')
                return redirect(url_for('colegio.editar_coordinador', coordinador_id=coordinador.id))

            if not sede_id:
                flash('Debe seleccionar una sede', 'danger')
                return redirect(url_for('colegio.editar_coordinador', coordinador_id=coordinador.id))

            email_existente = Usuario.query.filter(
                Usuario.email == email,
                Usuario.id != coordinador.usuario_id
            ).first()

            if email_existente:
                flash('El correo electrónico ya está registrado por otro usuario', 'danger')
                return redirect(url_for('colegio.editar_coordinador', coordinador_id=coordinador.id))

            coordinador.usuario.nombre = nombre
            coordinador.usuario.email = email
            coordinador.documento = documento if documento else None
            coordinador.telefono = telefono if telefono else None
            coordinador.sede_id = sede_id

            db.session.commit()
            flash('Coordinador actualizado correctamente', 'success')
            return redirect(url_for('colegio.lista_coordinadores'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}', 'danger')
            return redirect(url_for('colegio.editar_coordinador', coordinador_id=coordinador.id))

    # ✅ Corregido: apunta a coordinador/editar_coordinador.html
    return render_template('coordinador/editar_coordinador.html', coordinador=coordinador, sedes=sedes)


@colegio_bp.route('/coordinadores/<int:coordinador_id>/cambiar-estado')
@login_required
def cambiar_estado_coordinador(coordinador_id):
    coordinador = Coordinador.query.filter_by(
        id=coordinador_id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    try:
        usuario = coordinador.usuario
        usuario.is_active = not usuario.is_active
        db.session.commit()

        estado = "activado" if usuario.is_active else "desactivado"
        flash(f'Coordinador {estado} correctamente', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('colegio.lista_coordinadores'))


@colegio_bp.route('/coordinadores/<int:coordinador_id>/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password_coordinador(coordinador_id):
    coordinador = Coordinador.query.filter_by(
        id=coordinador_id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    if request.method == 'POST':
        nueva_password = request.form.get('password', '').strip()

        if not nueva_password or len(nueva_password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'danger')
            return redirect(url_for('colegio.cambiar_password_coordinador', coordinador_id=coordinador.id))

        try:
            coordinador.usuario.password_hash = generate_password_hash(nueva_password)
            db.session.commit()
            flash('Contraseña actualizada correctamente', 'success')
            return redirect(url_for('colegio.lista_coordinadores'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    # ✅ Corregido: apunta a coordinador/cambiar_password.html
    return render_template('coordinador/cambiar_password.html', coordinador=coordinador)


@colegio_bp.route('/coordinadores/<int:coordinador_id>/eliminar')
@login_required
def eliminar_coordinador(coordinador_id):
    if not current_user.es_admin_colegio:
        abort(403)

    coordinador = Coordinador.query.filter_by(
        id=coordinador_id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    try:
        usuario = coordinador.usuario
        db.session.delete(coordinador)
        if usuario:
            db.session.delete(usuario)
        db.session.commit()
        flash('Coordinador eliminado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar coordinador: {str(e)}', 'danger')

    return redirect(url_for('colegio.lista_coordinadores'))




# ==========================================================
# CONFIGURACIÓN DISCIPLINARIA
# ==========================================================
@colegio_bp.route('/configuracion/disciplina')
@login_required
def configuracion_disciplina():
    if not current_user.es_admin_colegio:
        abort(403)

    from app.models.configuracion_disciplinaria import ConfiguracionDisciplinaria

    config = ConfiguracionDisciplinaria.query.filter_by(
        colegio_id=current_user.colegio_id
    ).first()

    if not config:
        config = ConfiguracionDisciplinaria(
            dias_prescripcion=30,
            max_tipo2=3,
            colegio_id=current_user.colegio_id
        )
        db.session.add(config)
        db.session.commit()

    return render_template('colegio/configuracion_disciplina.html', config=config)


@colegio_bp.route('/configuracion/disciplina/guardar', methods=['POST'])
@login_required
def guardar_configuracion_disciplina():
    if not current_user.es_admin_colegio:
        abort(403)

    dias_prescripcion = request.form.get('dias_prescripcion', type=int)
    max_tipo2 = request.form.get('max_tipo2', type=int)

    from app.models.configuracion_disciplinaria import ConfiguracionDisciplinaria

    config = ConfiguracionDisciplinaria.query.filter_by(
        colegio_id=current_user.colegio_id
    ).first()

    if config:
        config.dias_prescripcion = dias_prescripcion
        config.max_tipo2 = max_tipo2
        db.session.commit()
        flash('Configuración guardada correctamente', 'success')
    else:
        flash('Error: configuración no encontrada', 'danger')

    return redirect(url_for('colegio.configuracion_disciplina'))


# ==========================================================
# CONFIGURACIÓN DE ESCALAMIENTO
# ==========================================================
@colegio_bp.route('/configuracion/escalamiento')
@login_required
def configuracion_escalamiento():
    if not current_user.es_admin_colegio:
        abort(403)

    from app.models.configuracion_escalamiento import ConfiguracionEscalamiento

    configuraciones = ConfiguracionEscalamiento.query.filter_by(
        colegio_id=current_user.colegio_id
    ).all()

    return render_template('colegio/configuracion_escalamiento.html', configuraciones=configuraciones)


@colegio_bp.route('/configuracion/escalamiento/guardar', methods=['POST'])
@login_required
def guardar_configuracion_escalamiento():
    if not current_user.es_admin_colegio:
        abort(403)

    tipo_origen = request.form.get('tipo_origen')
    cantidad = request.form.get('cantidad', type=int)
    tipo_destino = request.form.get('tipo_destino')

    from app.models.configuracion_escalamiento import ConfiguracionEscalamiento

    config = ConfiguracionEscalamiento.query.filter_by(
        colegio_id=current_user.colegio_id,
        tipo_origen=tipo_origen
    ).first()

    if config:
        config.cantidad = cantidad
        config.tipo_destino = tipo_destino
    else:
        config = ConfiguracionEscalamiento(
            tipo_origen=tipo_origen,
            cantidad=cantidad,
            tipo_destino=tipo_destino,
            colegio_id=current_user.colegio_id
        )
        db.session.add(config)

    db.session.commit()
    flash('Configuración de escalamiento guardada correctamente', 'success')
    return redirect(url_for('colegio.configuracion_escalamiento'))

# ==========================================================
# ESTUDIANTES - Redirige al módulo de estudiantes
# ==========================================================



@colegio_bp.route("/estudiantes")
@login_required
def lista_estudiantes():
    """Redirige al listado de estudiantes del módulo estudiante"""
    return redirect(url_for('estudiante.listar'))
# ==========================================================
# ACUDIENTES
# ==========================================================

@colegio_bp.route("/acudientes")
@login_required
def lista_acudientes():
    """Lista todos los acudientes del colegio"""
    from app.models.acudiente import Acudiente

    acudientes = Acudiente.query.filter_by(
        colegio_id=current_user.colegio_id
    ).order_by(Acudiente.nombre).all()

    return render_template(
        "acudientes/acudientes.html",
        acudientes=acudientes
    )


@colegio_bp.route("/acudientes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_acudiente():
    from app.models.acudiente import Acudiente
    """Crear un nuevo acudiente con su usuario de acceso"""
    if not current_user.es_admin_colegio:
        abort(403)


    if request.method == "POST":
        try:
            nombre = request.form.get("nombre", "").strip()
            email = request.form.get("email", "").strip()
            telefono = request.form.get("telefono", "").strip()
            direccion = request.form.get("direccion", "").strip()
            parentesco = request.form.get("parentesco", "").strip()
            password = request.form.get("password", "").strip()

            # Validaciones
            if not nombre:
                flash("El nombre completo es obligatorio", "danger")
                return redirect(url_for("colegio.nuevo_acudiente"))

            if not email:
                flash("El correo electrónico es obligatorio", "danger")
                return redirect(url_for("colegio.nuevo_acudiente"))

            if not password or len(password) < 6:
                flash("La contraseña debe tener al menos 6 caracteres", "danger")
                return redirect(url_for("colegio.nuevo_acudiente"))

            # Verificar email existente
            if Usuario.query.filter_by(email=email).first():
                flash("El correo electrónico ya está registrado", "danger")
                return redirect(url_for("colegio.nuevo_acudiente"))

            # 1. Crear Usuario con rol 'acudiente'
            usuario = Usuario(
                nombre=nombre,
                email=email,
                password_hash=generate_password_hash(password),
                rol='acudiente',
                colegio_id=current_user.colegio_id,
                is_active=True,
                is_approved=True
            )
            db.session.add(usuario)
            db.session.flush()

            # 2. Crear Acudiente vinculado al usuario y al colegio
            acudiente = Acudiente(
                usuario_id=usuario.id,
                nombre=nombre,
                email=email,
                telefono=telefono if telefono else None,
                direccion=direccion if direccion else None,
                parentesco=parentesco if parentesco else None,
                colegio_id=current_user.colegio_id
            )
            db.session.add(acudiente)
            db.session.commit()

            flash(f"Acudiente '{nombre}' registrado correctamente", "success")
            return redirect(url_for("colegio.lista_acudientes"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar acudiente: {str(e)}", "danger")
            return redirect(url_for("colegio.nuevo_acudiente"))

    return render_template("acudientes/formulario_acudiente.html", acudiente=None, titulo="Nuevo Acudiente")


@colegio_bp.route("/acudientes/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_acudiente(id):
    """Editar un acudiente existente"""
    from app.models.acudiente import Acudiente

    acudiente = Acudiente.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    if request.method == "POST":
        try:
            nombre = request.form.get("nombre", "").strip()
            email = request.form.get("email", "").strip()
            telefono = request.form.get("telefono", "").strip()
            direccion = request.form.get("direccion", "").strip()
            parentesco = request.form.get("parentesco", "").strip()

            if not nombre:
                flash("El nombre es obligatorio", "danger")
                return redirect(url_for("colegio.editar_acudiente", id=acudiente.id))

            if not email:
                flash("El correo electrónico es obligatorio", "danger")
                return redirect(url_for("colegio.editar_acudiente", id=acudiente.id))

            # Verificar email no duplicado (excluyendo el actual)
            email_existente = Usuario.query.filter(
                Usuario.email == email,
                Usuario.id != acudiente.usuario_id
            ).first()

            if email_existente:
                flash("El correo electrónico ya está registrado por otro usuario", "danger")
                return redirect(url_for("colegio.editar_acudiente", id=acudiente.id))

            # Actualizar Usuario
            if acudiente.usuario:
                acudiente.usuario.nombre = nombre
                acudiente.usuario.email = email

            # Actualizar Acudiente
            acudiente.nombre = nombre
            acudiente.email = email
            acudiente.telefono = telefono if telefono else None
            acudiente.direccion = direccion if direccion else None
            acudiente.parentesco = parentesco if parentesco else None

            db.session.commit()
            flash("Acudiente actualizado correctamente", "success")
            return redirect(url_for("colegio.lista_acudientes"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar acudiente: {str(e)}", "danger")
            return redirect(url_for("colegio.editar_acudiente", id=acudiente.id))

    return render_template(
        "acudientes/formulario_acudiente.html",
        acudiente=acudiente,
        titulo="Editar Acudiente"
    )


@colegio_bp.route("/acudientes/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar_acudiente(id):
    """Eliminar un acudiente y su usuario asociado"""
    from app.models.acudiente import Acudiente

    acudiente = Acudiente.query.filter_by(
        id=id,
        colegio_id=current_user.colegio_id
    ).first_or_404()

    try:
        usuario = acudiente.usuario
        db.session.delete(acudiente)
        if usuario:
            db.session.delete(usuario)
        db.session.commit()
        flash("Acudiente eliminado correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar acudiente: {str(e)}", "danger")

    return redirect(url_for("colegio.lista_acudientes"))

@colegio_bp.route("/observador")
@login_required
def observador():
    flash("El módulo del Observador del Alumno está en construcción.", "info")
    return redirect(url_for('colegio.dashboard'))


@colegio_bp.route("/citaciones")
@login_required
def citaciones():
    flash("El módulo de Citaciones está en construcción.", "info")
    return redirect(url_for('colegio.dashboard'))


@colegio_bp.route("/convivencia")
@login_required
def convivencia():
    flash("El módulo de Convivencia está en construcción.", "info")
    return redirect(url_for('colegio.dashboard'))


@colegio_bp.route("/seguimiento")
@login_required
def seguimiento():
    flash("El módulo de Seguimiento Académico está en construcción.", "info")
    return redirect(url_for('colegio.dashboard'))


@colegio_bp.route("/piar")
@login_required
def piar():
    flash("El módulo de PIAR está en construcción.", "info")
    return redirect(url_for('colegio.dashboard'))