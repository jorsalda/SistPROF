from app.extensions import db
from datetime import date


class PIAR(db.Model):
    __tablename__ = "piar"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    diagnostico = db.Column(db.Text, nullable=True)
    objetivos = db.Column(db.Text, nullable=True)
    fecha_inicio = db.Column(db.Date, nullable=True)
    fecha_fin = db.Column(db.Date, nullable=True)
    activo = db.Column(db.Boolean, default=True)

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relaciones
    estudiante = db.relationship("Estudiante", backref="piar", lazy=True)

    def __repr__(self):
        return f'<PIAR {self.estudiante_id} - {"Activo" if self.activo else "Inactivo"}>'