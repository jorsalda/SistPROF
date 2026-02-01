from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from app.models.usuario import Usuario
from app.models.colegio import Colegio
from app.extensions import db


def login_usuario(email, password):
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return False, "Usuario no encontrado"

    if not check_password_hash(usuario.password_hash, password):
        return False, "Contraseña incorrecta"

    if usuario.estatus != 'activo':
        return False, "Usuario no activo"

    return True, usuario


def registrar_usuario(email, password, colegio_nombre):
    if Usuario.query.filter_by(email=email).first():
        return False, "El email ya está registrado"

    colegio = Colegio.query.filter_by(nombre=colegio_nombre).first()
    if not colegio:
        colegio = Colegio(nombre=colegio_nombre)
        db.session.add(colegio)
        db.session.commit()

    # ⭐⭐ DETERMINAR ROL: Primer usuario = admin, demás = colegio ⭐⭐
    # Contar usuarios existentes
    total_usuarios = Usuario.query.count()
    es_admin = total_usuarios == 0  # Si es el primer usuario, es admin

    usuario = Usuario(
        email=email,
        password_hash=generate_password_hash(password),
        colegio_id=colegio.id,
        fecha_registro=datetime.utcnow(),
        estatus='activo',
        rol='admin' if es_admin else 'colegio'  # ⭐⭐ ASIGNAR ROL
    )

    db.session.add(usuario)
    db.session.commit()

    return True, "OK"