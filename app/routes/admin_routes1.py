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
    superadmins = Usuario.query.filter_by(rol='superadmin').count()
    usuarios_aprobados = Usuario.query.filter_by(is_approved=True).count()
    usuarios_pendientes = Usuario.query.filter_by(is_approved=False).filter(Usuario.rol != 'superadmin').count()
    usuarios_activos = Usuario.query.filter_by(is_active=True).count()

    # Estadísticas de colegios
    total_colegios = Colegio.query.count()
    total_permisos = Permiso.query.count()

    # Lista de colegios para superadmin (Los "Usuarios" del sistema)
    if current_user.rol == 'superadmin':
        lista_colegios_raw = Colegio.query.order_by(Colegio.id.desc()).limit(5).all()
        lista_colegios = []
        for colegio in lista_colegios_raw:
            estado_info = _calcular_estado_colegio(colegio)
            lista_colegios.append({
                'colegio': colegio,
                'estado': estado_info['estado'],
                'badge_class': estado_info['badge_class'],
                'dias_restantes': estado_info['dias_restantes']
            })
    else:
        lista_colegios = []

    # Nuevos usuarios (últimos 7 días)
    hace_7_dias = datetime.utcnow() - timedelta(days=7)
    nuevos_usuarios = Usuario.query.filter(Usuario.fecha_registro >= hace_7_dias).count()

    # Próximos a vencer (lógica simplificada para el dashboard)
    proximos_vencer = []

    return render_template(
        "admin/dashboard.html",
        total_usuarios=total_usuarios,
        superadmins=superadmins,
        usuarios_aprobados=usuarios_aprobados,
        usuarios_pendientes=usuarios_pendientes,
        usuarios_activos=usuarios_activos,
        total_colegios=total_colegios,
        total_permisos=total_permisos,
        nuevos_usuarios=nuevos_usuarios,
        proximos_vencer=proximos_vencer,
        lista_colegios=lista_colegios
    )


# ════════════════════════════════════════════════════════════════
# GESTIÓN DE COLEGIOS
# ════════════════════════════════════════════════════════════════

@admin_bp.route("/colegio/<int:colegio_id>/detalle")
@login_required
@superuser_required
def detalle_colegio(colegio_id):
    """Muestra los detalles de un colegio específico"""
    colegio = Colegio.query.get_or_404(colegio_id)

    # Calcular estado
    estado_info = _calcular_estado_colegio(colegio)

    # Contar usuarios del colegio
    total_usuarios = len(colegio.usuarios)
    usuarios_activos = sum(1 for u in colegio.usuarios if u.is_active)

    return render_template(
        "admin/detalle_colegio.html",
        colegio=colegio,
        estado=estado_info['estado'],
        badge_class=estado_info['badge_class'],
        dias_restantes=estado_info['dias_restantes'],
        total_usuarios=total_usuarios,
        usuarios_activos=usuarios_activos
    )


@admin_bp.route("/colegio/<int:colegio_id>/aprobar", methods=["POST"])
@login_required
@superuser_required
def aprobar_colegio(colegio_id):
    """Aprueba un colegio - lo saca de período de prueba"""
    colegio = Colegio.query.get_or_404(colegio_id)

    # Marcar como aprobado (ya no está en prueba)
    colegio.en_prueba = False
    colegio.activo = True
    colegio.fecha_expiracion = None  # Ya no tiene fecha de vencimiento

    db.session.commit()

    flash(f"Colegio '{colegio.nombre}' ha sido APROBADO exitosamente", "success")
    return redirect(url_for('admin.detalle_colegio', colegio_id=colegio.id))


@admin_bp.route("/colegio/<int:colegio_id>/bloquear", methods=["POST"])
@login_required
@superuser_required
def bloquear_colegio(colegio_id):
    """Bloquea un colegio - impide el acceso"""
    colegio = Colegio.query.get_or_404(colegio_id)

    colegio.activo = False

    db.session.commit()

    flash(f"Colegio '{colegio.nombre}' ha sido BLOQUEADO", "warning")
    return redirect(url_for('admin.detalle_colegio', colegio_id=colegio.id))


@admin_bp.route("/colegio/<int:colegio_id>/desbloquear", methods=["POST"])
@login_required
@superuser_required
def desbloquear_colegio(colegio_id):
    """Desbloquea un colegio previamente bloqueado"""
    colegio = Colegio.query.get_or_404(colegio_id)

    colegio.activo = True

    db.session.commit()

    flash(f"Colegio '{colegio.nombre}' ha sido DESBLOQUEADO", "success")
    return redirect(url_for('admin.detalle_colegio', colegio_id=colegio.id))


@admin_bp.route("/colegio/<int:colegio_id>/modificar_dias", methods=["POST"])
@login_required
@superuser_required
def modificar_dias_prueba(colegio_id):
    """Modifica los días de prueba de un colegio"""
    colegio = Colegio.query.get_or_404(colegio_id)

    dias = int(request.form.get('dias_prueba', 15))

    # Calcular nueva fecha de expiración desde hoy
    from datetime import datetime, timedelta
    nueva_fecha = datetime.utcnow() + timedelta(days=dias)

    colegio.fecha_expiracion = nueva_fecha
    colegio.en_prueba = True  # Asegurar que siga en prueba

    db.session.commit()

    flash(f"Período de prueba modificado a {dias} días. Nueva fecha: {nueva_fecha.strftime('%d/%m/%Y')}", "info")
    return redirect(url_for('admin.detalle_colegio', colegio_id=colegio.id))
# ════════════════════════════════════════════════════════════════
# HELPER INTERNO
# ════════════════════════════════════════════════════════════════

def _calcular_estado_colegio(colegio):
    """Calcula el estado visual de un colegio"""
    hoy = datetime.utcnow()

    if not colegio.activo:
        return {'estado': 'Inactivo', 'badge_class': 'secondary', 'dias_restantes': None}

    if colegio.en_prueba and colegio.fecha_expiracion:
        dias = (colegio.fecha_expiracion - hoy).days
        if dias >= 0:
            return {'estado': f'En Prueba ({dias} días)', 'badge_class': 'warning', 'dias_restantes': dias}
        return {'estado': 'Prueba Vencida', 'badge_class': 'danger', 'dias_restantes': dias}

    return {'estado': 'Aprobado', 'badge_class': 'success', 'dias_restantes': None}