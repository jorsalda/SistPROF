from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import secrets
from app.models.usuario import Usuario
from app.models.colegio import Colegio
from app.models.sede import Sede          # ← AGREGAR ESTO
from app.models.jornada import Jornada    # ← AGREGAR ESTO
from app.extensions import db

MAX_INTENTOS = 5
TIEMPO_BLOQUEO_MIN = 2


def registrar_usuario(email, password, tipo_registro='colegio', nombre_colegio=None,
                      codigo_acceso=None, nombre_completo=None, rol_independiente=None):
    """
    Registra un nuevo usuario (Colegio o Independiente) respetando la arquitectura.
    """
    try:
        # 1. Verificar si el email ya existe (case-insensitive)
        if Usuario.query.filter(db.func.lower(Usuario.email) == email.lower()).first():
            return False, "El correo electrónico ya está registrado en el sistema"

        # ═══════════════════════════════════════════════════════════
        # CASO 1: REGISTRO COMO INDEPENDIENTE
        # ═══════════════════════════════════════════════════════════
        if tipo_registro == 'independiente':

            if not nombre_completo or not rol_independiente:
                return False, "Debes proporcionar tu nombre completo y el tipo de usuario"

            if rol_independiente not in ['docente', 'estudiante']:
                return False, "Rol inválido. Debe ser 'docente' o 'estudiante'"

            # Buscar el colegio "Independientes"
            colegio_independientes = Colegio.query.filter(
                db.func.lower(Colegio.nombre).like('%independiente%')
            ).first()

            if not colegio_independientes:
                colegio_independientes = Colegio(
                    nombre="Estudiantes Independientes",
                    codigo_acceso="IND001",
                    activo=True,
                    en_prueba=False,
                    fecha_expiracion=None
                )
                db.session.add(colegio_independientes)
                db.session.flush()
                colegio_id = colegio_independientes.id
            else:
                colegio_id = colegio_independientes.id

            # Obtener o crear Sede por defecto
            sede_default = Sede.query.filter_by(colegio_id=colegio_id, activo=True).first()
            if not sede_default:
                sede_default = Sede(
                    nombre="Sede Única",
                    direccion="Sede para estudiantes independientes",
                    telefono="",
                    colegio_id=colegio_id,
                    activo=True
                )
                db.session.add(sede_default)
                db.session.flush()

            # Obtener o crear Jornada por defecto
            jornada_default = Jornada.query.filter_by(
                sede_id=sede_default.id, colegio_id=colegio_id, activo=True
            ).first()
            if not jornada_default:
                jornada_default = Jornada(
                    nombre="Jornada Única",
                    hora_inicio=datetime.strptime("07:00", "%H:%M").time(),
                    hora_fin=datetime.strptime("15:00", "%H:%M").time(),
                    tolerancia_minutos=15,
                    sede_id=sede_default.id,
                    colegio_id=colegio_id,
                    activo=True
                )
                db.session.add(jornada_default)
                db.session.flush()

            # Obtener o crear Acudiente por defecto
            from app.models.acudiente import Acudiente
            acudiente_default = Acudiente.query.filter_by(
                colegio_id=colegio_id, email="acudiente.independientes@sistprof.com"
            ).first()
            if not acudiente_default:
                acudiente_default = Acudiente(
                    nombre="Acudiente General Independientes",
                    email="acudiente.independientes@sistprof.com",
                    telefono="",
                    direccion="Acudiente para estudiantes independientes",
                    parentesco="General",
                    colegio_id=colegio_id,
                    usuario_id=None
                )
                db.session.add(acudiente_default)
                db.session.flush()

            # CREAR USUARIO (Aquí estaba el error de indentación)
            dias_prueba = 7
            fecha_expiracion = datetime.utcnow() + timedelta(days=dias_prueba)

            nuevo_usuario = Usuario(
                email=email,
                password_hash=generate_password_hash(password),
                rol=rol_independiente,
                colegio_id=colegio_id,
                nombre=nombre_completo,
                is_active=True,
                is_approved=False,
                fecha_registro=datetime.utcnow(),
                fecha_expiracion=fecha_expiracion,
                dias_prueba=dias_prueba,
                failed_attempts=0
            )
            db.session.add(nuevo_usuario)
            db.session.flush()

            # CREAR REGISTRO EN TABLA ESPECÍFICA (Estudiante o Docente)
            if rol_independiente == 'estudiante':
                from app.models.estudiante import Estudiante
                partes = nombre_completo.split(' ', 1)
                nombre = partes[0]
                apellido = partes[1] if len(partes) > 1 else ''

                estudiante = Estudiante(
                    nombre=nombre,
                    apellido=apellido,
                    tipo_documento='CC',
                    documento='IND-' + email.split('@')[0],
                    email=email,
                    usuario_id=nuevo_usuario.id,
                    direccion="Dirección no registrada",
                    telefono="",
                    acudiente_principal_id=acudiente_default.id,
                    grupo_id=None,
                    colegio_id=colegio_id,
                    sede_id=sede_default.id,
                    jornada_id=jornada_default.id,
                    docente_id=None,
                    qr_token=f"EST-IND-{secrets.token_hex(8).upper()}",
                    activo=True
                )
                db.session.add(estudiante)

            elif rol_independiente == 'docente':
                from app.models.docente import Docente
                docente = Docente(
                    usuario_id=nuevo_usuario.id,
                    nombre=nombre_completo,
                    documento='IND-' + email.split('@')[0],
                    email=email,
                    telefono="",
                    sede_id=sede_default.id,
                    colegio_id=colegio_id,
                    activo=True
                )
                db.session.add(docente)

            db.session.commit()
            return True, f"✅ Registro exitoso como {rol_independiente.capitalize()} independiente. ¡Bienvenido!"

        # ═══════════════════════════════════════════════════════════
        # CASO 2: REGISTRO DE NUEVO COLEGIO
        # ═══════════════════════════════════════════════════════════
        else:
            if not nombre_colegio:
                return False, "Debes proporcionar el nombre del colegio"

            if not codigo_acceso or codigo_acceso.strip() == '':
                codigo_acceso = f"COL-{secrets.token_hex(3).upper()}"
                codigo_generado = True
            else:
                codigo_acceso = codigo_acceso.strip().upper()
                if Colegio.query.filter_by(codigo_acceso=codigo_acceso).first():
                    return False, f"El código de acceso '{codigo_acceso}' ya está en uso. Elige otro."
                codigo_generado = False

            fecha_expiracion = datetime.utcnow() + timedelta(days=15)

            nuevo_colegio = Colegio(
                nombre=nombre_colegio,
                codigo_acceso=codigo_acceso,
                activo=True,
                en_prueba=True,
                fecha_expiracion=fecha_expiracion
            )
            db.session.add(nuevo_colegio)
            db.session.flush()

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

            if codigo_generado:
                return True, f"✅ Registro exitoso. Tu código de acceso es: {codigo_acceso}. ¡Guárdalo!"
            else:
                return True, f"✅ Registro exitoso con código personalizado: {codigo_acceso}"

    except Exception as e:
        db.session.rollback()
        print(f"❌ ERROR en registrar_usuario: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error al registrar: {str(e)}"


def login_usuario(email, password):
    """Verifica las credenciales y realiza el login"""
    ahora = datetime.now()

    # ✅ Búsqueda case-insensitive que funciona sin importar cómo esté guardado el email
    usuario = Usuario.query.filter(
        db.func.lower(Usuario.email) == email.lower().strip()
    ).first()

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


def generar_token_reset(email):
    """Genera un token seguro para resetear contraseña"""
    return secrets.token_urlsafe(32)


def verificar_token_reset(token):
    """Verifica si el token es válido y retorna el email asociado."""
    if token and len(token) > 20:
        return "email_temporal@validacion.com"  # Simplificado para el ejemplo
    return None


def resetear_contrasena_por_email(email, nueva_contrasena):
    """Resetea la contraseña de un usuario por email"""
    try:
        usuario = Usuario.query.filter(
            db.func.lower(Usuario.email) == email.lower().strip()
        ).first()
        if not usuario:
            return False, "Usuario no encontrado"

        usuario.password_hash = generate_password_hash(nueva_contrasena)
        db.session.commit()
        return True, "Contraseña actualizada exitosamente"
    except Exception as e:
        db.session.rollback()
        return False, f"Error al resetear: {str(e)}"