from app.extensions import db


class EvaluacionEstudiante(db.Model):
    __tablename__ = "evaluaciones_estudiante"

    id = db.Column(db.Integer, primary_key=True)

    # ✅ COLUMNA CALIFICACIÓN (Corrección anterior mantenida)
    calificacion = db.Column(
        "calificacion",  # Nombre real en BD
        db.Float,
        nullable=False
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

    # ✅ CORRECCIÓN CRÍTICA: FK explícita a periodos_academicos
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

    # ✅ CORRECCIÓN CRÍTICA: Relación explícita al modelo correcto
    # Usamos 'primaryjoin' para evitar que SQLAlchemy se confunda con otros modelos 'Periodo'
    periodo = db.relationship(
        "PeriodoAcademico",
        foreign_keys=[periodo_id],  # Forzamos el uso de esta FK específica
        backref="evaluaciones_estudiante"  # Usamos backref simple para evitar colisiones con back_populates
    )

    def __repr__(self):
        return f"<EvaluacionEstudiante {self.id}>"