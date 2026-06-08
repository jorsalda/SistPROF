
# app/models/evaluacion_criterio.py

from app.extensions import db


class EvaluacionCriterio(db.Model):
    __tablename__ = "evaluacion_criterio"

    id = db.Column(db.Integer, primary_key=True)

    evaluacion_final_id = db.Column(
        db.Integer,
        db.ForeignKey("evaluacion_final.id"),
        nullable=False
    )

    criterio_id = db.Column(
        db.Integer,
        db.ForeignKey("criterios_evaluacion.id"),
        nullable=False
    )

    calificacion = db.Column(
        db.Float,
        nullable=False
    )

    observacion = db.Column(db.Text)

    __table_args__ = (
        db.UniqueConstraint(
            "evaluacion_final_id",
            "criterio_id",
            name="unique_evaluacion_criterio"
        ),
        db.CheckConstraint(
            "calificacion >= 0 AND calificacion <= 5",
            name="check_calificacion_rango"
        ),
    )

    evaluacion_final = db.relationship(
        "EvaluacionFinal",
        backref=db.backref(
            "criterios_evaluados",
            lazy=True
        )
    )

    criterio = db.relationship(
        "CriterioEvaluacion",
        backref=db.backref(
            "evaluaciones",
            lazy=True
        )
    )

    def __repr__(self):
        return f"<EvaluacionCriterio {self.id}>"

