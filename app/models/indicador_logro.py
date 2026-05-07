from app.extensions import db


class IndicadorLogro(db.Model):
    __tablename__ = "indicadores_logro"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    competencia_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "competencias_materia.id"
        ),
        nullable=False
    )

    descripcion = db.Column(
        db.Text,
        nullable=False
    )

    nivel_desempeno = db.Column(
        db.String(50),
        nullable=True
    )

    peso_porcentual = db.Column(
        db.Numeric(5, 2),
        nullable=True
    )

    orden = db.Column(
        db.Integer,
        nullable=True
    )

    competencia = db.relationship(
        "CompetenciaMateria",
        backref="indicadores",
        lazy=True
    )

    def __repr__(self):
        return (
            f"<IndicadorLogro "
            f"{self.id}>"
        )