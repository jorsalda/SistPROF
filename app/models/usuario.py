# app/models/usuario.py
from datetime import datetime, timedelta
from flask_login import UserMixin
from app.extensions import db


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    colegio_id = db.Column(db.Integer, db.ForeignKey("colegios.id"), nullable=False)

    # ⭐⭐ NUEVO CAMPO: ROL ⭐⭐
    rol = db.Column(db.String(20), default="colegio")  # "admin" o "colegio"

    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_expiracion = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.utcnow() + timedelta(days=15)
    )
    estatus = db.Column(db.String(20), default="pendiente")

    colegio = db.relationship("Colegio", backref="usuarios")

    def get_id(self):
        return str(self.id)

    def acceso_valido(self):
        if self.estatus != "activo":
            return False
        return datetime.utcnow() <= self.fecha_expiracion

    # ⭐⭐ MÉTODO PARA VERIFICAR SI ES ADMIN ⭐⭐
    def es_admin(self):
        return self.rol == "admin"