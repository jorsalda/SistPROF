from datetime import datetime
from app.extensions import db


class Alerta(db.Model):
    __tablename__ = "alertas"

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey("estudiantes.id", ondelete="CASCADE"), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)

    activa = db.Column(db.Boolean, default=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Columnas de atención
    atendida = db.Column(db.Boolean, default=False, nullable=False)
    atendida_por = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    fecha_atencion = db.Column(db.DateTime, nullable=True)

    # Relaciones
    estudiante = db.relationship("Estudiante", backref=db.backref("alertas", lazy=True, cascade="all, delete-orphan"))
    usuario_atencion = db.relationship("Usuario", foreign_keys=[atendida_por])