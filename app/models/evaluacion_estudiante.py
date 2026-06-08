from app.extensions import db


class EvaluacionEstudiante(db.Model):
    __tablename__ = "evaluaciones_estudiante"

    id = db.Column(db.Integer, primary_key=True)

    nota = db.Column(
        db.Float,
        nullable=False
    )

    observacion = db.Column(
        db.Text,
        nullable=True
    )

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False
    )

    indicador_id = db.Column(
        db.Integer,
        db.ForeignKey("indicadores_logro.id", ondelete="CASCADE"),
        nullable=False
    )

    periodo_id = db.Column(
        db.Integer,
        db.ForeignKey("periodos.id", ondelete="CASCADE"),
        nullable=False
    )

    estudiante = db.relationship(
        "Estudiante",
        back_populates="evaluaciones"
    )

    indicador = db.relationship(
        "IndicadorLogro",
        back_populates="evaluaciones"
    )

    periodo = db.relationship(
        "Periodo",
        back_populates="evaluaciones"
    )

    def __repr__(self):
        return f"<EvaluacionEstudiante {self.id}>"