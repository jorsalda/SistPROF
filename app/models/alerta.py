
# app/models/alerta.py

from datetime import datetime
from app.extensions import db


class Alerta(db.Model):
    __tablename__ = "alertas"

    id = db.Column(db.Integer, primary_key=True)

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "estudiantes.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    tipo = db.Column(
        db.String(100),
        nullable=False
    )

    descripcion = db.Column(
        db.Text,
        nullable=False
    )

    activa = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    estudiante = db.relationship(
        "Estudiante",
        backref=db.backref(
            "alertas",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    def __repr__(self):
        estado = "Activa" if self.activa else "Cerrada"
        return f"<Alerta {self.tipo} - {estado}>"

