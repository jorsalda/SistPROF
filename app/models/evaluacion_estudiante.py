from app.extensions import db


class EvaluacionEstudiante(db.Model):
    __tablename__ = "evaluaciones_estudiante"

    id = db.Column(db.Integer, primary_key=True)

    # ✅ COLUMNA CALIFICACIÓN
    calificacion = db.Column(
        "calificacion",
        db.Float,
        nullable=False
    )

    # ✅ NUEVO: Nivel de desempeño cualitativo
    nivel_desempeño = db.Column(
        db.String(20),
        nullable=True
    )

    observacion = db.Column(db.Text, nullable=True)

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
        db.ForeignKey("periodos_academicos.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relaciones
    estudiante = db.relationship("Estudiante", back_populates="evaluaciones")

    indicador = db.relationship(
        "IndicadorLogro",
        back_populates="evaluaciones"
    )

    periodo = db.relationship(
        "PeriodoAcademico",
        foreign_keys=[periodo_id],
        backref="evaluaciones_estudiante"
    )

    def __repr__(self):
        return f"<EvaluacionEstudiante {self.id}>"