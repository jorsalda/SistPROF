from app.extensions import db
from datetime import datetime


class DescargoEstudiante(db.Model):
    __tablename__ = "descargos_estudiante"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    novedad_id = db.Column(
        db.Integer,
        db.ForeignKey("novedades.id", ondelete="CASCADE"),
        nullable=False
    )
    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relaciones
    novedad = db.relationship("Novedad", backref="descargos", lazy=True)
    estudiante = db.relationship("Estudiante", backref="descargos", lazy=True)

    def __repr__(self):
        return f'<Descargo {self.novedad_id} - {self.estudiante_id}>'