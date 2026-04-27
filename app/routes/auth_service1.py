from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import secrets
from app.models.usuario import Usuario
from app.models.colegio import Colegio
from app.extensions import db

MAX_INTENTOS = 5
TIEMPO_BLOQUEO_MIN = 2


def registrar_usuario(email, password, nombre_colegio):
    """
    Registra un nuevo colegio y su administrador con 15 días de prueba

    Retorna: (bool, mensaje)
        - (True, "Mensaje de éxito") si el registro fue exitoso
        - (False, "Mensaje de error") si hubo un problema
    """
    try:
        # 1. Verificar si el email ya existe
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            return False, "El correo electrónico ya está registrado en el sistema"

        # 2. Generar código de acceso único para el colegio
        codigo_acceso = f"COL-{secrets.token_hex(3).upper()}"

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
        db.session.flush()  # Obtener el ID antes del commit

        # 5. Crear el Usuario Administrador
        nuevo_usuario = Usuario(
            email=email,
            password_hash=generate_password_hash(password),
            rol='admin_colegio',
            colegio_id=nuevo_colegio.id,
            is_active=True,
            is_approved=False,  # Requiere aprobación del superadmin
            fecha_registro=datetime.utcnow(),
            fecha_expiracion=fecha_expiracion,
            dias_prueba=15,
            failed_attempts=0
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        return True, f"✅ Registro exitoso. Tu colegio ha sido registrado con el código: {codigo_acceso}. Tienes 15 días de prueba."

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error en registrar_usuario: {e}")
        return False, "Error al registrar. Inténtalo de nuevo más tarde."


def login_usuario(email, password):
    """
    Verifica las credenciales del usuario y realiza el login

    Retorna: (bool, usuario/mensaje)
        - (True, usuario) si el login es exitoso
        - (False, mensaje_de_error) si falla
    """
    ahora = datetime.now()

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return False, "Credenciales inválidas"

    # 🔒 Ya está bloqueado
    if usuario.locked_until and usuario.locked_until > ahora:
        segundos = int((usuario.locked_until - ahora).total_seconds())
        return False, f"Usuario bloqueado. Intenta en {segundos} segundos"

    # 🔐 Contraseña incorrecta
    if not check_password_hash(usuario.password_hash, password):
        usuario.failed_attempts = (usuario.failed_attempts or 0) + 1

        # 🚨 LLEGÓ AL LÍMITE
        if usuario.failed_attempts >= MAX_INTENTOS:
            usuario.locked_until = ahora + timedelta(minutes=TIEMPO_BLOQUEO_MIN)
            db.session.commit()
            return False, (
                f"Usuario bloqueado temporalmente por exceder {MAX_INTENTOS} intentos. "
                f"Inténtalo nuevamente dentro de {TIEMPO_BLOQUEO_MIN} minutos."
            )

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