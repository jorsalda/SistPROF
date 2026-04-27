from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from datetime import datetime


def superuser_required(f):
    """
    Decorador que restringe el acceso solo a superusuarios.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not current_user.is_authenticated:
            flash('Por favor, inicia sesión primero.', 'warning')
            return redirect(url_for('auth.login'))

        # ✅ CAMBIO CLAVE: usar rol en vez de is_superadmin
        if getattr(current_user, 'rol', None) != 'superadmin':
            flash('🚫 Acceso denegado: Necesitas permisos de superusuario.', 'danger')
            return redirect(url_for('auth.estado_cuenta'))

        return f(*args, **kwargs)

    return decorated_function


def acceso_permitido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))

        # 🔥 SUPERADMIN SIEMPRE PASA (ANTES DE TODO)
        if getattr(current_user, 'rol', None) == 'superadmin':
            return f(*args, **kwargs)

        # -------------------------
        # Lógica normal de acceso
        # -------------------------
        if hasattr(current_user, 'puede_acceder'):
            puede_acceder, razon = current_user.puede_acceder()

            if not puede_acceder:
                flash(f'Acceso restringido: {razon}. Contacta al administrador.', 'danger')
                return redirect(url_for('auth.estado_cuenta'))

        # Advertencia de prueba
        if not getattr(current_user, 'is_approved', False):
            fecha_registro = getattr(current_user, 'fecha_registro', datetime.utcnow())
            dias_transcurridos = (datetime.utcnow() - fecha_registro).days
            dias_prueba = getattr(current_user, 'dias_prueba', 15)
            dias_restantes = dias_prueba - dias_transcurridos

            if 0 < dias_restantes <= 3:
                flash(
                    f'⚠️ Tu período de prueba termina en {dias_restantes} día(s). '
                    f'Solicita aprobación al administrador.',
                    'warning'
                )

        return f(*args, **kwargs)

    return decorated_function