from app.extensions import db
from datetime import datetime


class CitacionAcudiente(db.Model):
    __tablename__ = "citaciones_acudiente"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    motivo = db.Column(db.Text, nullable=False)
    fecha_citacion = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(20), default="pendiente")
    observaciones = db.Column(db.Text, nullable=True)
    tipo_origen = db.Column(db.String(50), nullable=True)
    fecha = db.Column(db.Date, default=datetime.utcnow)

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False
    )
    acudiente_id = db.Column(
        db.Integer,
        db.ForeignKey("acudientes.id", ondelete="CASCADE"),
        nullable=False
    )
    novedad_id = db.Column(
        db.Integer,
        db.ForeignKey("novedades.id", ondelete="SET NULL"),
        nullable=True
    )

    # Relaciones
    estudiante = db.relationship("Estudiante", backref="citaciones", lazy=True)
    acudiente = db.relationship("Acudiente", backref="citaciones", lazy=True)
    novedad = db.relationship("Novedad", backref="citaciones", lazy=True)

    def __repr__(self):
        return f'<Citacion {self.estudiante_id} - {self.estado}>'