from app.extensions import db
from datetime import datetime

class NotaComponenteEstudiante(db.Model):
    __tablename__ = "notas_componente_estudiante"

    id = db.Column(db.Integer, primary_key=True)

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False
    )

    grupo_materia_id = db.Column(
        db.Integer,
        db.ForeignKey("grupo_materias.id", ondelete="CASCADE"),
        nullable=False
    )

    periodo_academico_id = db.Column(
        db.Integer,
        db.ForeignKey("periodos_academicos.id", ondelete="CASCADE"),
        nullable=False
    )

    # 'autoevaluacion', 'examen_final', 'coevaluacion', etc.
    tipo_componente = db.Column(
        db.String(30),
        nullable=False
    )

    calificacion = db.Column(
        db.Numeric(4, 2),
        nullable=True
    )

    observacion = db.Column(
        db.Text,
        nullable=True
    )

    registrada_por = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=True
    )

    fecha_registro = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    fecha_actualizacion = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<NotaComponente {self.tipo_componente}: {self.calificacion}>"