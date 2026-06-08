
# app/models/evaluacion_final.py

from datetime import datetime
from app.extensions import db


class EvaluacionFinal(db.Model):
    __tablename__ = "evaluacion_final"

    id = db.Column(db.Integer, primary_key=True)

    acuerdo_id = db.Column(
        db.Integer,
        db.ForeignKey("acuerdos_evaluacion.id"),
        nullable=False,
        unique=True
    )

    observaciones = db.Column(db.Text)

    puntaje_final = db.Column(db.Float)

    fecha_cierre = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    acuerdo = db.relationship(
        "AcuerdoEvaluacion",
        backref=db.backref(
            "evaluacion_final",
            uselist=False
        )
    )

    def __repr__(self):
        return f"<EvaluacionFinal {self.id}>"

