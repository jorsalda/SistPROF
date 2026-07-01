from app.extensions import db
from .competencia_contribucion import competencia_contribucion


class Contribucion(db.Model):
    __tablename__ = "contribuciones"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    descripcion = db.Column(
        db.Text,
        nullable=False
    )

    criterio_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "criterios_evaluacion.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    criterio = db.relationship(
        "CriterioEvaluacion",
        backref="contribuciones"
    )

    # Relación N:M con CompetenciaDocente
    competencias = db.relationship(
        "CompetenciaDocente",
        secondary=competencia_contribucion,
        back_populates="contribuciones",
        lazy=True
    )

    def __repr__(self):
        return f"<Contribucion {self.id}>"