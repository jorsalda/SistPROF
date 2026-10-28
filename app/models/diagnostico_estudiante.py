from app.extensions import db
from datetime import datetime


class DiagnosticoEstudiante(db.Model):
    __tablename__ = "diagnosticos_estudiante"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False
    )

    descripcion = db.Column(
        db.Text,
        nullable=False
    )

    fecha_registro = db.Column(
        db.DateTime,
        default=datetime.now,
        nullable=True
    )

    def __repr__(self):
        return f"<DiagnosticoEstudiante {self.id} - {self.descripcion[:20]}>"