
# app/models/ajuste_razonable.py

from datetime import datetime
from app.extensions import db


class AjusteRazonable(db.Model):
    __tablename__ = "ajustes_razonables"

    id = db.Column(db.Integer, primary_key=True)

    piar_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "piar.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    descripcion = db.Column(
        db.Text,
        nullable=False
    )

    aplicado = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    fecha_aplicacion = db.Column(
        db.DateTime,
        nullable=True
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        estado = "Aplicado" if self.aplicado else "Pendiente"
        return f"<AjusteRazonable {self.id} - {estado}>"

