
# app/models/criterio_evaluacion.py

from app.extensions import db


class CriterioEvaluacion(db.Model):
    __tablename__ = "criterios_evaluacion"

    id = db.Column(db.Integer, primary_key=True)

    acuerdo_id = db.Column(
        db.Integer,
        db.ForeignKey("acuerdos_evaluacion.id"),
        nullable=False
    )

    area_gestion_id = db.Column(
        db.Integer,
        db.ForeignKey("areas_gestion.id"),
        nullable=True
    )

    nombre = db.Column(db.String(255), nullable=False)

    descripcion = db.Column(db.Text)

    porcentaje = db.Column(db.Float, default=0)

    acuerdo = db.relationship(
        "AcuerdoEvaluacion",
        backref=db.backref("criterios", lazy=True)
    )

    def __repr__(self):
        return f"<CriterioEvaluacion {self.nombre}>"

