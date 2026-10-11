"""Helpers para consultar permisos finos de usuario.

Los permisos viven en la tabla permisos_usuario (usuario_id, clave, valor).
Regla: si NO existe fila para (usuario_id, clave), el permiso es FALSE (denegar por defecto).
Excepcion: el admin del colegio tiene todos los permisos (no requiere filas).
"""
from app.extensions import db
from app.models.permiso_usuario import PermisoUsuario


def tiene_permiso(usuario, clave):
    """Verifica si un usuario tiene un permiso especifico.

    Args:
        usuario: instancia de Usuario (current_user o similar).
        clave: string del permiso, ej: 'secretaria.ver_docentes'.

    Returns:
        bool: True si:
              - El usuario es admin del colegio (siempre tiene todos los permisos).
              - O existe la fila (usuario_id, clave) con valor=True.
              False en cualquier otro caso (no existe la fila, valor=False, usuario None).
    """
    if usuario is None:
        return False

    if not getattr(usuario, 'is_authenticated', False):
        return False

    # El admin del colegio tiene todos los permisos.
    if getattr(usuario, 'es_admin_colegio', False):
        return True

    permiso = PermisoUsuario.query.filter_by(
        usuario_id=usuario.id,
        clave=clave
    ).first()

    if permiso is None:
        return False

    return bool(permiso.valor)


def permisos_de_usuario(usuario):
    """Devuelve un dict {clave: valor} con TODOS los permisos explicitos del usuario.

    Util para cargar todos los permisos de una vez (evita N consultas).

    Nota: NO incluye la excepcion del admin. Devuelve solo filas explicitas.
    Para preguntar "puede hacer X?" usar tiene_permiso(), no este helper.
    """
    if usuario is None or not getattr(usuario, 'is_authenticated', False):
        return {}

    permisos = PermisoUsuario.query.filter_by(usuario_id=usuario.id).all()
    return {p.clave: bool(p.valor) for p in permisos}


def tiene_alguno(usuario, claves):
    """Devuelve True si el usuario tiene AL MENOS UNO de los permisos dados.

    Args:
        usuario: instancia de Usuario.
        claves: lista de strings.

    Returns:
        bool: True si el usuario es admin del colegio, o si tiene al menos
              uno de los permisos listados con valor=True.
    """
    if usuario is None or not getattr(usuario, 'is_authenticated', False):
        return False

    # El admin del colegio tiene todos los permisos.
    if getattr(usuario, 'es_admin_colegio', False):
        return True

    return any(tiene_permiso(usuario, clave) for clave in claves)


# ─────────────────────────────────────────────────────────────
# DECORADOR PARA RUTAS FLASK
# ─────────────────────────────────────────────────────────────

from functools import wraps
from flask import abort
from flask_login import current_user


def requiere_permiso(clave):
    """Decorador que valida que el usuario tenga un permiso especifico.

    Reglas:
    - Si es admin del colegio, siempre pasa.
    - Si NO es admin, debe tener el permiso (via tiene_permiso).
    - Si no cumple, aborta con 403.

    Uso:
        @colegio_bp.route("/docentes")
        @login_required
        @requiere_permiso('secretaria.ver_docentes')
        def lista_docentes():
            ...

    IMPORTANTE: debe ir DESPUES de @login_required para que current_user este cargado.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Admin del colegio siempre pasa
            if getattr(current_user, 'es_admin_colegio', False):
                return f(*args, **kwargs)

            # Verificar permiso
            if not tiene_permiso(current_user, clave):
                abort(403)

            return f(*args, **kwargs)
        return wrapper
    return decorator