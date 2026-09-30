from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from sqlalchemy import func

from app.extensions import db
from app.models.usuario import Usuario
from app.models.colegio import Colegio
from app.models.docente import Docente
from app.models.permiso import Permiso
from app.middleware.superuser_middleware import superuser_required
from datetime import datetime, timedelta

from app.models.periodo_academico import PeriodoAcademico

from app.models.configuracion_periodo import ConfiguracionPeriodo

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ════════════════════════════════════════════════════════════════
# DASHBOARD PRINCIPAL
# ════════════════════════════════════════════════════════════════

@admin_bp.route("/dashboard")
@login_required
@superuser_required
def dashboard():
    """Panel principal de administración con estadísticas"""

    # ── Estadísticas generales ────────────────────────────────
    total_usuarios = Usuario.query.count()
    superadmins = Usuario.query.filter_by(rol='superadmin').count()
    usuarios_aprobados = Usuario.query.filter_by(is_approved=True).count()
    usuarios_pendientes = (
        Usuario.query.filter_by(is_approved=False)
        .filter(Usuario.rol != 'superadmin')
        .count()
    )
    usuarios_activos = Usuario.query.filter_by(is_active=True).count()

    # ── Estadísticas de colegios ──────────────────────────────
    total_colegios = Colegio.query.count()
    total_permisos = Permiso.query.count()

    # ── Colegios por estado (para gráfico de dona) ────────────
    colegios_aprobados = Colegio.query.filter_by(activo=True, en_prueba=False).count()
    colegios_en_prueba = Colegio.query.filter_by(activo=True, en_prueba=True).count()
    colegios_bloqueados = Colegio.query.filter_by(activo=False).count()

    # ── Usuarios por rol (para gráfico de barras) ─────────────
    roles_query = (
        db.session.query(Usuario.rol, func.count(Usuario.id))
        .group_by(Usuario.rol)
        .all()
    )
    usuarios_por_rol = {
        'superadmin': 0,
        'admin_colegio': 0,
        'docente': 0,
        'estudiante': 0,
        'acudiente': 0,
        'coordinador': 0,
    }
    for rol, cantidad in roles_query:
        rol_str = rol.value if hasattr(rol, 'value') else str(rol)
        usuarios_por_rol[rol_str] = cantidad

    # ── Top 5 colegios con más usuarios ───────────────────────
    top_colegios_query = (
        db.session.query(Colegio.nombre, func.count(Usuario.id).label('total'))
        .join(Usuario, Usuario.colegio_id == Colegio.id)
        .group_by(Colegio.id, Colegio.nombre)
        .order_by(func.count(Usuario.id).desc())
        .limit(5)
        .all()
    )
    top_colegios = [{'nombre': nombre, 'total': total} for nombre, total in top_colegios_query]

    # ── Lista de colegios para superadmin (últimos 5) ─────────
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

    # ── Nuevos usuarios (últimos 7 días) ──────────────────────
    hace_7_dias = datetime.utcnow() - timedelta(days=7)
    nuevos_usuarios = Usuario.query.filter(Usuario.fecha_registro >= hace_7_dias).count()

    # ── Próximos a vencer (pendiente de implementar) ──────────
    proximos_vencer = []

    return render_template(
        "admin/dashboard.html",
        # Tarjetas KPI
        total_usuarios=total_usuarios,
        superadmins=superadmins,
        usuarios_aprobados=usuarios_aprobados,
        usuarios_pendientes=usuarios_pendientes,
        usuarios_activos=usuarios_activos,
        total_colegios=total_colegios,
        total_permisos=total_permisos,
        nuevos_usuarios=nuevos_usuarios,
        proximos_vencer=proximos_vencer,
        lista_colegios=lista_colegios,
        # Datos para gráficos
        colegios_aprobados=colegios_aprobados,
        colegios_en_prueba=colegios_en_prueba,
        colegios_bloqueados=colegios_bloqueados,
        usuarios_por_rol=usuarios_por_rol,
        top_colegios=top_colegios,
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

    # Limpiar fecha_expiracion de TODOS los usuarios del colegio
    usuarios_del_colegio = Usuario.query.filter_by(colegio_id=colegio.id).all()
    for usuario in usuarios_del_colegio:
        usuario.fecha_expiracion = None
        usuario.is_approved = True
        usuario.dias_prueba = 0

    db.session.commit()

    flash(f"Colegio '{colegio.nombre}' ha sido APROBADO exitosamente. "
          f"Se actualizaron {len(usuarios_del_colegio)} usuario(s).", "success")
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

    nueva_fecha = datetime.utcnow() + timedelta(days=dias)

    colegio.fecha_expiracion = nueva_fecha
    colegio.en_prueba = True

    # Actualizar también la fecha de TODOS los usuarios
    Usuario.query.filter_by(colegio_id=colegio.id).update({
        'fecha_expiracion': nueva_fecha,
        'is_approved': False,
        'dias_prueba': dias
    })

    db.session.commit()

    flash(f"Período de prueba modificado a {dias} días. "
          f"Nueva fecha: {nueva_fecha.strftime('%d/%m/%Y')}", "info")
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


# ════════════════════════════════════════════════════════════════
# [TEMPORAL] CREAR ADMIN COLEGIO INDEPENDIENTES
# ════════════════════════════════════════════════════════════════

@admin_bp.route("/crear-admin-independientes")
@login_required
@superuser_required
def crear_admin_independientes():
    """
    [TEMPORAL] Crear usuario admin para el colegio independiente (ID 46)
    ELIMINAR ESTA RUTA DESPUÉS DE USARLA UNA VEZ
    """
    import os

    # Verificar si ya existe
    usuario_existente = Usuario.query.filter_by(
        email='admin.independientes@sistprof.com'
    ).first()

    if usuario_existente:
        return "⚠️ El usuario ya existe en la base de datos"

    try:
        # Obtener contraseña desde variable de entorno o usar valor por defecto seguro
        password_inicial = os.environ.get('ADMIN_INDEPENDIENTES_PASSWORD', 'Cambiar123!Segura')

        # Crear usuario admin
        usuario = Usuario(
            nombre='Admin Independientes',
            email='admin.independientes@sistprof.com',
            password_hash=generate_password_hash(password_inicial),
            rol='admin_colegio',
            colegio_id=46,
            is_active=True,
            is_approved=True
        )

        db.session.add(usuario)
        db.session.commit()

        return f"✅ Usuario admin.independientes@sistprof.com creado exitosamente. Contraseña inicial: {password_inicial}"
    except Exception as e:
        db.session.rollback()
        return f"❌ Error al crear usuario: {str(e)}"