
# app/models/evidencia.py

from datetime import datetime
from app.extensions import db


class Evidencia(db.Model):
    __tablename__ = "evidencias"

    id = db.Column(db.Integer, primary_key=True)

    criterio_id = db.Column(
        db.Integer,
        db.ForeignKey("criterios_evaluacion.id"),
        nullable=False
    )

    descripcion = db.Column(db.Text, nullable=False)

    tipo = db.Column(db.String(100))

    url = db.Column(db.String(500))

    aprobado = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    fecha_subida = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    criterio = db.relationship(
        "CriterioEvaluacion",
        backref=db.backref("evidencias", lazy=True)
    )

    def __repr__(self):
        return f"<Evidencia {self.id}>"

