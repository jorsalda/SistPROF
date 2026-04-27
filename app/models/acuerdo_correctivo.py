from app.extensions import db
from datetime import datetime


class AcuerdoCorrectivo(db.Model):
    __tablename__ = "acuerdos_correctivos"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.Text, nullable=False)
    compromiso = db.Column(db.Text, nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default="ACTIVO")

    novedad_id = db.Column(
        db.Integer,
        db.ForeignKey("novedades.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relaciones
    novedad = db.relationship("Novedad", backref="acuerdos_correctivos", lazy=True)
    estudiante = db.relationship("Estudiante", backref="acuerdos_correctivos", lazy=True)

    def __repr__(self):
        return f'<AcuerdoCorrectivo {self.novedad_id} - {self.estado}>'