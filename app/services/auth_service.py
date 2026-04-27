from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import secrets  # ← ESTE IMPORT ES EL QUE FALTABA
from app.models.usuario import Usuario
from app.models.colegio import Colegio
from app.extensions import db

MAX_INTENTOS = 5
TIEMPO_BLOQUEO_MIN = 2


def registrar_usuario(email, password, nombre_colegio, codigo_acceso=None):
    """
    Registra un nuevo colegio y su administrador con 15 días de prueba.

    Args:
        codigo_acceso: Código personalizado (opcional). Si es None o vacío, se genera automáticamente.

    Retorna: (bool, mensaje)
    """
    try:
        # 1. Verificar si el email ya existe
        if Usuario.query.filter_by(email=email).first():
            return False, "El correo electrónico ya está registrado en el sistema"

        # 2. Generar o usar código de acceso proporcionado
        if not codigo_acceso or codigo_acceso.strip() == '':
            # Generar automáticamente si no lo proporcionaron
            codigo_acceso = f"COL-{secrets.token_hex(3).upper()}"
            codigo_generado = True
        else:
            # Usar el código proporcionado (validar que no exista)
            codigo_acceso = codigo_acceso.strip().upper()

            # Verificar que el código no esté en uso
            if Colegio.query.filter_by(codigo_acceso=codigo_acceso).first():
                return False, f"El código de acceso '{codigo_acceso}' ya está en uso. Elige otro."

            codigo_generado = False

        # 3. Calcular fecha de expiración (15 días desde hoy)
        fecha_expiracion = datetime.utcnow() + timedelta(days=15)

        # 4. Crear el Colegio
        nuevo_colegio = Colegio(
            nombre=nombre_colegio,
            codigo_acceso=codigo_acceso,
            activo=True,
            en_prueba=True,
            fecha_expiracion=fecha_expiracion
        )
        db.session.add(nuevo_colegio)
        db.session.flush()

        # 5. Crear el Usuario Administrador
        nuevo_usuario = Usuario(
            email=email,
            password_hash=generate_password_hash(password),
            rol='admin_colegio',
            colegio_id=nuevo_colegio.id,
            is_active=True,
            is_approved=False,
            fecha_registro=datetime.utcnow(),
            fecha_expiracion=fecha_expiracion,
            dias_prueba=15,
            failed_attempts=0
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        # 6. Mensaje personalizado según si se generó o no el código
        if codigo_generado:
            return True, f"✅ Registro exitoso. Tu código de acceso es: {codigo_acceso}. ¡Guárdalo!"
        else:
            return True, f"✅ Registro exitoso con código personalizado: {codigo_acceso}"

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error en registrar_usuario: {e}")
        return False, f"Error al registrar: {str(e)}"


def login_usuario(email, password):
    """Verifica las credenciales y realiza el login"""
    ahora = datetime.now()
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return False, "Credenciales inválidas"

    if usuario.locked_until and usuario.locked_until > ahora:
        segundos = int((usuario.locked_until - ahora).total_seconds())
        return False, f"Usuario bloqueado. Intenta en {segundos} segundos"

    if not check_password_hash(usuario.password_hash, password):
        usuario.failed_attempts = (usuario.failed_attempts or 0) + 1

        if usuario.failed_attempts >= MAX_INTENTOS:
            usuario.locked_until = ahora + timedelta(minutes=TIEMPO_BLOQUEO_MIN)
            db.session.commit()
            return False, f"Usuario bloqueado por {MAX_INTENTOS} intentos fallidos."

        db.session.commit()
        return False, "Credenciales inválidas"

    if not usuario.is_active:
        return False, "Usuario no activo"

    if usuario.fecha_expiracion and usuario.fecha_expiracion < ahora:
        return False, "Cuenta expirada. Contacte al administrador."

    usuario.failed_attempts = 0
    usuario.locked_until = None
    db.session.commit()

    return True, usuario


# ════════════════════════════════════════════════════════════════
# FUNCIONES DE RECUPERACIÓN DE CONTRASEÑA (AGREGAR ESTO AL FINAL)
# ════════════════════════════════════════════════════════════════

def generar_token_reset(email):
    """Genera un token seguro para resetear contraseña"""
    token = secrets.token_urlsafe(32)
    return token


def verificar_token_reset(token):
    """Verifica si el token es válido y retorna el email asociado."""
    if token and len(token) > 20:
        # En producción aquí validarías contra la tabla de tokens en la BD
        return "email_temporal@validacion.com"
    return None


def resetear_contrasena_por_email(email, nueva_contrasena):
    """Resetea la contraseña de un usuario por email"""
    try:
        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            return False, "Usuario no encontrado"

        usuario.password_hash = generate_password_hash(nueva_contrasena)
        db.session.commit()
        return True, "Contraseña actualizada exitosamente"
    except Exception as e:
        db.session.rollback()
        return False, f"Error al resetear: {str(e)}"

