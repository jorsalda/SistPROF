
# app/models/respuesta_novedad.py

from datetime import datetime
from app.extensions import db


class RespuestaNovedad(db.Model):
    __tablename__ = "respuestas_novedad"

    id = db.Column(db.Integer, primary_key=True)

    novedad_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "novedades.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "usuarios.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    mensaje = db.Column(
        db.Text,
        nullable=False
    )

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    novedad = db.relationship(
        "Novedad",
        backref=db.backref(
            "respuestas",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    usuario = db.relationship(
        "Usuario",
        backref=db.backref(
            "respuestas_novedad",
            lazy=True
        )
    )

    def __repr__(self):
        return f"<RespuestaNovedad {self.id}>"

