from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from app.models.usuario import Usuario
from app.extensions import db


MAX_INTENTOS = 5
TIEMPO_BLOQUEO_MIN = 2


def login_usuario(email, password):
    ahora = datetime.utcnow()

    usuario = Usuario.query.filter_by(email=email).first()

    # ❌ No existe el usuario (mensaje genérico)
    if not usuario:
        return False, "Credenciales inválidas"

    # 🔒 Usuario bloqueado temporalmente
    if usuario.locked_until and usuario.locked_until > ahora:
        segundos = int((usuario.locked_until - ahora).total_seconds())
        return False, f"Cuenta bloqueada. Intenta en {segundos} segundos"

    # 🔐 Contraseña incorrecta
    if not check_password_hash(usuario.password_hash, password):
        usuario.failed_attempts = (usuario.failed_attempts or 0) + 1

        if usuario.failed_attempts >= MAX_INTENTOS:
            usuario.locked_until = ahora + timedelta(minutes=TIEMPO_BLOQUEO_MIN)
            usuario.failed_attempts = 0  # reset tras bloqueo

        db.session.commit()
        return False, "Credenciales inválidas"

    # 🚫 Usuario inactivo
    if not usuario.is_active:
        return False, "Usuario no activo"

    # ⏳ Cuenta expirada
    if usuario.fecha_expiracion and usuario.fecha_expiracion < ahora:
        return False, "Cuenta expirada. Contacte al administrador"

    # ✅ LOGIN EXITOSO → limpiar seguridad
    usuario.failed_attempts = 0
    usuario.locked_until = None
    db.session.commit()

    return True, usuario