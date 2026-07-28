from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from datetime import datetime


def requiere_membresia_activa(f):
    """
    Decorador para verificar si el usuario tiene membresía activa
    o está dentro del periodo de prueba.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):

        # Superadmin siempre pasa
        if current_user.rol == 'superadmin':
            return f(*args, **kwargs)

        # Verificar si puede acceder (usa el método que ya tienes)
        puede_acceder, mensaje = current_user.puede_acceder()

        if not puede_acceder:
            flash(f"️ {mensaje}. Por favor, renueva tu membresía.", "warning")
            return redirect(url_for('membresia.ver_plan'))

        # Verificar si tiene membresía aprobada o está en prueba
        if not current_user.is_approved and not current_user.fecha_expiracion:
            flash("Tu cuenta requiere aprobación. Contacta al administrador.", "warning")
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)

    return decorated_function