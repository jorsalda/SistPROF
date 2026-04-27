from app.extensions import db


class EvaluacionEstudiante(db.Model):
    __tablename__ = "evaluaciones_estudiante"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    calificacion = db.Column(db.Numeric(4, 2), nullable=True)
    observacion = db.Column(db.Text, nullable=True)

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id"),
        nullable=True
    )
    indicador_id = db.Column(
        db.Integer,
        db.ForeignKey("indicadores_logro.id", ondelete="CASCADE"),
        nullable=True
    )
    periodo_id = db.Column(
        db.Integer,
        db.ForeignKey("periodos_academicos.id"),
        nullable=True
    )

    # Relaciones
    estudiante = db.relationship("Estudiante", backref="evaluaciones", lazy=True)

    def __repr__(self):
        return f'<Evaluacion {self.estudiante_id} - {self.calificacion}>'