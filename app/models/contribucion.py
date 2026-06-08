from app.extensions import db


class Contribucion(db.Model):
    __tablename__ = "contribuciones"

    id = db.Column(db.Integer, primary_key=True)

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

    def __repr__(self):
        return f"<Contribucion {self.id}>"