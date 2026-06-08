
# app/models/acuerdo_evaluacion.py

from datetime import datetime
from app.extensions import db


class AcuerdoEvaluacion(db.Model):
    __tablename__ = "acuerdos_evaluacion"

    id = db.Column(db.Integer, primary_key=True)

    docente_id = db.Column(
        db.Integer,
        db.ForeignKey("docentes.id"),
        nullable=False
    )

    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id"),
        nullable=False
    )

    anio = db.Column(db.Integer, nullable=False)

    estado = db.Column(
        db.Enum("BORRADOR", "CERRADO", name="estado_acuerdo"),
        default="BORRADOR",
        nullable=False
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            "docente_id",
            "anio",
            name="unique_docente_anio"
        ),
    )

    docente = db.relationship(
        "Docente",
        backref=db.backref("acuerdos_evaluacion", lazy=True)
    )

    colegio = db.relationship(
        "Colegio",
        backref=db.backref("acuerdos_evaluacion", lazy=True)
    )

    def __repr__(self):
        return f"<AcuerdoEvaluacion {self.id}>"

