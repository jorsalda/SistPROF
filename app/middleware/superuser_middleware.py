from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def superuser_required(f):
    """
    Decorador que restringe el acceso solo a superusuarios.
    Redirige a login si no está autenticado.
    Redirige al panel principal con mensaje de error si no es superadmin.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar autenticación
        if not current_user.is_authenticated:
            flash('Por favor, inicia sesión primero.', 'warning')
            return redirect(url_for('auth.login'))

        # Verificar permisos de superusuario
        if not getattr(current_user, 'is_superadmin', False):
            flash('🚫 Acceso denegado: Necesitas permisos de superusuario.', 'danger')
            return redirect(url_for('auth.estado_cuenta'))

        return f(*args, **kwargs)

    return decorated_function