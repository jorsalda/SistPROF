"""
Servicio para gestionar usuarios operativos del colegio:
- secretaria
- portero
- profesional_piar
- psicologo

Reglas:
- Solo el admin_colegio los crea.
- Email único en todo el sistema.
- Sede obligatoria y del mismo colegio.
- Contraseña inicial = documento.
- Activación automática (no requiere aprobación de superadmin).
- Límite sin costo: 3 por rol. La 4ª en adelante requiere confirmación.
"""

from datetime import datetime
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models.usuario import Usuario
from app.models.sede import Sede


ROLES_PERMITIDOS = ['secretaria', 'portero', 'profesional_piar', 'psicologo']

LIMITE_SIN_COSTO = {
    'secretaria': 3,
    'portero': 3,
    'profesional_piar': 3,
    'psicologo': 3,
}

NOMBRES_ROL = {
    'secretaria': 'Secretaria',
    'portero': 'Portero',
    'profesional_piar': 'Profesional PIAR',
    'psicologo': 'Psicólogo',
}


def _contar_activos(colegio_id, rol):
    return Usuario.query.filter_by(
        colegio_id=colegio_id,
        rol=rol,
        is_active=True
    ).count()


def requiere_confirmacion_costo(colegio_id, rol):
    """
    Devuelve (requiere: bool, actuales: int, limite: int)
    """
    if rol not in LIMITE_SIN_COSTO:
        return False, 0, 0

    limite = LIMITE_SIN_COSTO[rol]
    actuales = _contar_activos(colegio_id, rol)
    return actuales >= limite, actuales, limite


def crear_usuario_operativo(
    colegio_id,
    rol,
    nombre,
    apellido,
    email,
    documento,
    sede_id,
    telefono=None,
    confirmar_costo=False,
    password_override=None,
):
    """
    Crea un usuario operativo (secretaria, portero, profesional_piar o psicologo).
    Retorna (ok, mensaje, usuario_o_None).
    """

    if rol not in ROLES_PERMITIDOS:
        return False, f"Rol inválido: {rol}", None

    if not nombre or not nombre.strip():
        return False, "El nombre es obligatorio", None

    if not apellido or not apellido.strip():
        return False, "El apellido es obligatorio", None

    if not email or not email.strip():
        return False, "El correo electrónico es obligatorio", None

    if not documento or not documento.strip():
        return False, "El documento es obligatorio", None

    if not sede_id:
        return False, "Debe seleccionar una sede", None

    nombre = nombre.strip()
    apellido = apellido.strip()
    email = email.strip().lower()
    documento = documento.strip()

    if Usuario.query.filter(db.func.lower(Usuario.email) == email).first():
        return False, "El correo electrónico ya está registrado en el sistema", None

    sede = Sede.query.filter_by(
        id=sede_id,
        colegio_id=colegio_id,
        activo=True
    ).first()

    if not sede:
        return False, "La sede seleccionada no es válida", None

    requiere, actuales, limite = requiere_confirmacion_costo(colegio_id, rol)
    if requiere and not confirmar_costo:
        return False, f"CONFIRMAR_COSTO:{actuales}:{limite}", None

    try:
        usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            password_hash=generate_password_hash(password_override or documento),
            rol=rol,
            colegio_id=colegio_id,
            sede_id=sede_id,
            is_active=True,
            is_approved=True,
            fecha_registro=datetime.utcnow(),
        )
        db.session.add(usuario)
        db.session.commit()
        nombre_rol = NOMBRES_ROL.get(rol, rol)
        return True, f"{nombre_rol} '{nombre} {apellido}' creado correctamente", usuario

    except Exception as e:
        db.session.rollback()
        return False, f"Error al crear usuario: {str(e)}", None


def editar_usuario_operativo(
    colegio_id,
    usuario_id,
    nombre,
    apellido,
    email,
    sede_id,
    activo=True,
    cambiar_password=False,
    nuevo_documento=None,
):
    usuario = Usuario.query.filter_by(
        id=usuario_id,
        colegio_id=colegio_id
    ).first()

    if not usuario:
        return False, "Usuario no encontrado", None

    if usuario.rol not in ROLES_PERMITIDOS:
        return False, "Este usuario no es un usuario operativo válido", None

    if not nombre or not nombre.strip():
        return False, "El nombre es obligatorio", None

    if not apellido or not apellido.strip():
        return False, "El apellido es obligatorio", None

    if not email or not email.strip():
        return False, "El correo electrónico es obligatorio", None

    if not sede_id:
        return False, "Debe seleccionar una sede", None

    nombre = nombre.strip()
    apellido = apellido.strip()
    email = email.strip().lower()

    existente = Usuario.query.filter(
        db.func.lower(Usuario.email) == email,
        Usuario.id != usuario.id
    ).first()

    if existente:
        return False, "El correo ya está registrado por otro usuario", None

    sede = Sede.query.filter_by(
        id=sede_id,
        colegio_id=colegio_id,
        activo=True
    ).first()

    if not sede:
        return False, "La sede seleccionada no es válida", None

    try:
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.email = email
        usuario.sede_id = sede_id
        usuario.is_active = activo

        if cambiar_password and nuevo_documento:
            usuario.password_hash = generate_password_hash(nuevo_documento.strip())

        db.session.commit()
        return True, "Usuario actualizado correctamente", usuario

    except Exception as e:
        db.session.rollback()
        return False, f"Error al actualizar: {str(e)}", None


def listar_usuarios_operativos(colegio_id, rol=None):
    query = Usuario.query.filter(
        Usuario.colegio_id == colegio_id,
        Usuario.rol.in_(ROLES_PERMITIDOS)
    )
    if rol in ROLES_PERMITIDOS:
        query = query.filter(Usuario.rol == rol)
    return query.order_by(Usuario.rol, Usuario.apellido, Usuario.nombre).all()