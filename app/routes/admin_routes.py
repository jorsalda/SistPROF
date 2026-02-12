from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.usuario import Usuario
from app.models.colegio import Colegio
from app.models.docente import Docente
from app.models.permiso import Permiso
from app.middleware.superuser_middleware import superuser_required
from datetime import datetime, timedelta

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ════════════════════════════════════════════════════════════════
# DASHBOARD PRINCIPAL
# ════════════════════════════════════════════════════════════════

@admin_bp.route("/dashboard")
@login_required
@superuser_required
def dashboard():
    """Panel principal de administración con estadísticas"""

    # Estadísticas generales
    total_usuarios = Usuario.query.count()
    superadmins = Usuario.query.filter_by(is_superadmin=True).count()
    usuarios_aprobados = Usuario.query.filter_by(is_approved=True).count()
    usuarios_pendientes = Usuario.query.filter_by(is_approved=False, is_superadmin=False).count()
    usuarios_activos = Usuario.query.filter_by(is_active=True).count()

    # Estadísticas de colegios y docentes
    total_colegios = Colegio.query.count()
    total_docentes = Docente.query.count()
    total_permisos = Permiso.query.count()

    # Usuarios en prueba (últimos 7 días)
    hace_7_dias = datetime.utcnow() - timedelta(days=7)
    nuevos_usuarios = Usuario.query.filter(Usuario.fecha_registro >= hace_7_dias).count()

    # Usuarios próximos a vencer (3 días o menos)
    proximos_vencer = []
    todos_usuarios = Usuario.query.filter_by(is_superadmin=False, is_approved=False).all()
    for usuario in todos_usuarios:
        if usuario.fecha_expiracion:
            dias_restantes = (usuario.fecha_expiracion - datetime.utcnow()).days
            if 0 <= dias_restantes <= 3:
                proximos_vencer.append({
                    'usuario': usuario,
                    'dias': dias_restantes
                })

    return render_template(
        "admin/dashboard.html",
        total_usuarios=total_usuarios,
        superadmins=superadmins,
        usuarios_aprobados=usuarios_aprobados,
        usuarios_pendientes=usuarios_pendientes,
        usuarios_activos=usuarios_activos,
        total_colegios=total_colegios,
        total_docentes=total_docentes,
        total_permisos=total_permisos,
        nuevos_usuarios=nuevos_usuarios,
        proximos_vencer=proximos_vencer
    )


# ════════════════════════════════════════════════════════════════
# LISTADO DE USUARIOS
# ════════════════════════════════════════════════════════════════

@admin_bp.route("/usuarios")
@login_required
@superuser_required
def lista_usuarios():
    """Muestra todos los usuarios del sistema"""
    usuarios = Usuario.query.order_by(Usuario.fecha_registro.desc()).all()
    return render_template("admin/usuarios.html", usuarios=usuarios)


# ════════════════════════════════════════════════════════════════
# DETALLE DE USUARIO
# ════════════════════════════════════════════════════════════════

@admin_bp.route("/usuarios/<int:usuario_id>")
@login_required
@superuser_required
def detalle_usuario(usuario_id):
    """Muestra el detalle de un usuario específico"""
    usuario = Usuario.query.get_or_404(usuario_id)
    return render_template("admin/usuario_detalle.html", usuario=usuario)


# ════════════════════════════════════════════════════════════════
# APROBAR USUARIO
# ════════════════════════════════════════════════════════════════

@admin_bp.route("/usuarios/<int:usuario_id>/aprobar", methods=["POST"])
@login_required
@superuser_required
def aprobar_usuario(usuario_id):
    """Aprueba un usuario para acceso permanente"""
    usuario = Usuario.query.get_or_404(usuario_id)

    if usuario.is_superadmin:
        flash("No puedes modificar un superadministrador", "warning")
        return redirect(url_for("admin.lista_usuarios"))

    usuario.is_approved = True
    usuario.fecha_aprobacion = datetime.utcnow()
    usuario.fecha_expiracion = None  # Eliminar fecha de expiración

    db.session.commit()

    flash(f"✅ Usuario {usuario.email} aprobado correctamente", "success")
    return redirect(url_for("admin.detalle_usuario", usuario_id=usuario_id))


# ════════════════════════════════════════════════════════════════
# BLOQUEAR USUARIO
# ════════════════════════════════════════════════════════════════

@admin_bp.route("/usuarios/<int:usuario_id>/bloquear", methods=["POST"])
@login_required
@superuser_required
def bloquear_usuario(usuario_id):
    """Bloquea/desactiva un usuario"""
    usuario = Usuario.query.get_or_404(usuario_id)

    if usuario.is_superadmin:
        flash("No puedes bloquear a un superadministrador", "warning")
        return redirect(url_for("admin.lista_usuarios"))

    usuario.is_active = False
    usuario.is_approved = False

    db.session.commit()

    flash(f"🚫 Usuario {usuario.email} bloqueado", "danger")
    return redirect(url_for("admin.detalle_usuario", usuario_id=usuario_id))


# ════════════════════════════════════════════════════════════════
# ACTIVAR USUARIO
# ════════════════════════════════════════════════════════════════

@admin_bp.route("/usuarios/<int:usuario_id>/activar", methods=["POST"])
@login_required
@superuser_required
def activar_usuario(usuario_id):
    """Activa un usuario bloqueado"""
    usuario = Usuario.query.get_or_404(usuario_id)

    usuario.is_active = True

    db.session.commit()

    flash(f"✅ Usuario {usuario.email} activado", "success")
    return redirect(url_for("admin.detalle_usuario", usuario_id=usuario_id))


# ════════════════════════════════════════════════════════════════
# MODIFICAR DÍAS DE PRUEBA
# ════════════════════════════════════════════════════════════════

@admin_bp.route("/usuarios/<int:usuario_id>/modificar_dias", methods=["POST"])
@login_required
@superuser_required
def modificar_dias_prueba(usuario_id):
    """Modifica los días de prueba de un usuario"""
    usuario = Usuario.query.get_or_404(usuario_id)

    if usuario.is_superadmin:
        flash("No puedes modificar a un superadministrador", "warning")
        return redirect(url_for("admin.detalle_usuario", usuario_id=usuario_id))

    dias_nuevos = request.form.get("dias_prueba")

    try:
        dias_nuevos = int(dias_nuevos)
        if dias_nuevos < 0:
            flash("Los días deben ser positivos", "danger")
            return redirect(url_for("admin.detalle_usuario", usuario_id=usuario_id))

        # Calcular nueva fecha de expiración
        usuario.dias_prueba = dias_nuevos
        usuario.fecha_expiracion = usuario.fecha_registro + timedelta(days=dias_nuevos)

        db.session.commit()

        flash(f"✅ Días de prueba actualizados a {dias_nuevos} días", "success")
    except ValueError:
        flash("Por favor ingresa un número válido", "danger")

    return redirect(url_for("admin.detalle_usuario", usuario_id=usuario_id))


# ════════════════════════════════════════════════════════════════
# ESTADÍSTICAS
# ════════════════════════════════════════════════════════════════

@admin_bp.route("/estadisticas")
@login_required
@superuser_required
def estadisticas():
    """Página de estadísticas detalladas"""
    # Usuarios por estado
    usuarios_activos = Usuario.query.filter_by(is_active=True).count()
    usuarios_bloqueados = Usuario.query.filter_by(is_active=False).count()
    usuarios_aprobados = Usuario.query.filter_by(is_approved=True).count()
    usuarios_pendientes = Usuario.query.filter_by(is_approved=False, is_superadmin=False).count()

    # Colegios con más docentes
    colegios = Colegio.query.all()
    colegios_data = []
    for colegio in colegios:
        docentes_count = len(colegio.docentes)
        usuarios_count = len(colegio.usuarios)
        colegios_data.append({
            "nombre": colegio.nombre,
            "docentes": docentes_count,
            "usuarios": usuarios_count
        })

    colegios_data.sort(key=lambda x: x["docentes"], reverse=True)

    return render_template(
        "admin/estadisticas.html",
        usuarios_activos=usuarios_activos,
        usuarios_bloqueados=usuarios_bloqueados,
        usuarios_aprobados=usuarios_aprobados,
        usuarios_pendientes=usuarios_pendientes,
        colegios_data=colegios_data
    )