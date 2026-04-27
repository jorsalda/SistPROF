from app.extensions import db
from datetime import datetime


class Asistencia(db.Model):
    __tablename__ = "asistencias"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(20), nullable=False)  # presente, tarde, ausente
    observacion = db.Column(db.Text, nullable=True)
    registrada_por = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False
    )
    clase_id = db.Column(
        db.Integer,
        db.ForeignKey("clases.id", ondelete="CASCADE"),
        nullable=True
    )

    # Relaciones
    estudiante = db.relationship("Estudiante", backref="asistencias", lazy=True)
    clase = db.relationship("Clase", backref="asistencias", lazy=True)

    def __repr__(self):
        return f'<Asistencia {self.estudiante_id} - {self.fecha} ({self.estado})>'