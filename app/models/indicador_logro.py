from app.extensions import db


class IndicadorLogro(db.Model):
    __tablename__ = "indicadores_logro"

    id = db.Column(db.Integer, primary_key=True)

    descripcion = db.Column(
        db.Text,
        nullable=False
    )

    competencia_id = db.Column(
        db.Integer,
        db.ForeignKey("competencias_materia.id", ondelete="CASCADE"),
        nullable=False
    )

    competencia = db.relationship(
        "CompetenciaEstudiante",
        back_populates="indicadores"
    )

    evaluaciones = db.relationship(
        "EvaluacionEstudiante",
        back_populates="indicador",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<IndicadorLogro {self.id}>"