print(">>> 🚨 ARCHIVO CARGADO: auth_service.py VERSIÓN FINAL 🚨 <<<")

from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import random
import string
import secrets
from app.models.usuario import Usuario
from app.models.colegio import Colegio
from app.extensions import db

MAX_INTENTOS = 5
TIEMPO_BLOQUEO_MIN = 2


# ════════════════════════════════════════════════════════════════
# REGISTRO DE USUARIO (CON CÓDIGO DE ACCESO)
# ════════════════════════════════════════════════════════════════

def registrar_usuario(email, password, nombre_colegio, codigo_acceso=None):
    """
    Registra un nuevo colegio y su administrador con 15 días de prueba.
    """
    try:
        # 1. Verificar si el email ya existe
        if Usuario.query.filter_by(email=email).first():
            return False, "El correo electrónico ya está registrado en el sistema"

        # 2. Lógica del Código de Acceso
        if not codigo_acceso or codigo_acceso.strip() == '':
            caracteres = string.ascii_uppercase + string.digits
            codigo_generado = 'COL-' + ''.join(random.choices(caracteres, k=6))
            es_personalizado = False
        else:
            codigo_generado = codigo_acceso.strip().upper()
            # Validar que no exista
            if Colegio.query.filter_by(codigo_acceso=codigo_generado).first():
                return False, f"El código '{codigo_generado}' ya está en uso."
            es_personalizado = True

        # 3. Fecha de expiración
        fecha_expiracion = datetime.utcnow() + timedelta(days=15)

        # 4. Crear Colegio
        nuevo_colegio = Colegio(
            nombre=nombre_colegio,
            codigo_acceso=codigo_generado,
            activo=True,
            en_prueba=True,
            fecha_expiracion=fecha_expiracion
        )
        db.session.add(nuevo_colegio)
        db.session.flush()

        # 5. Crear Usuario
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

        if es_personalizado:
            return True, f"✅ Registro exitoso con código: {codigo_generado}"
        else:
            return True, f"✅ Registro exitoso. Tu código es: {codigo_generado}. ¡Guárdalo!"

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error en registrar_usuario: {e}")
        return False, f"Error al registrar: {str(e)}"


# ════════════════════════════════════════════════════════════════
# LOGIN DE USUARIO
# ════════════════════════════════════════════════════════════════

def login_usuario(email, password):
    """Verifica credenciales y realiza login"""
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
            return False, f"Usuario bloqueado por {MAX_INTENTOS} intentos."
        db.session.commit()
        return False, "Credenciales inválidas"

    if not usuario.is_active:
        return False, "Usuario no activo"

    if usuario.fecha_expiracion and usuario.fecha_expiracion < ahora:
        return False, "Cuenta expirada."

    usuario.failed_attempts = 0
    usuario.locked_until = None
    db.session.commit()

    return True, usuario


# ════════════════════════════════════════════════════════════════
# FUNCIONES DE RECUPERACIÓN DE CONTRASEÑA (LAS QUE FALTABAN)
# ════════════════════════════════════════════════════════════════

def generar_token_reset(email):
    """Genera un token seguro para resetear contraseña"""
    # Usamos secrets aquí porque es para seguridad crítica
    token = secrets.token_urlsafe(32)
    # Aquí podrías guardar el token en la BD con su email y fecha de expiración
    # Por ahora, retornamos el token (en producción deberías persistirlo)
    return token


def verificar_token_reset(token):
    """
    Verifica si el token es válido y retorna el email asociado.
    En una implementación completa, consultarías la tabla de tokens en la BD.
    """
    # Implementación simplificada: en producción, verifica contra la BD
    # y que no haya expirado (ej: 1 hora)

    # Por ahora, asumimos que es válido si no es vacío
    # ⚠️ EN PRODUCCIÓN: Validar contra tabla 'tokens_activacion'
    if token and len(token) > 20:
        # Aquí deberías hacer: 
        # token_registrado = TokenActivacion.query.filter_by(token=token, usado=False).first()
        # if token_registrado and token_registrado.fecha_expiracion > datetime.utcnow():
        #     return token_registrado.usuario.email
        return "email_ejemplo@temp.com"  # Placeholder
    return None


def resetear_contrasena_por_email(email, nueva_contrasena):
    """Resetea la contraseña de un usuario por email"""
    try:
        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            return False, "Usuario no encontrado"

        usuario.password_hash = generate_password_hash(nueva_contrasena)
        # Marcar tokens como usados (en producción)
        db.session.commit()
        return True, "Contraseña actualizada exitosamente"
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error en resetear_contrasena_por_email: {e}")
        return False, f"Error al resetear contraseña: {str(e)}"


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