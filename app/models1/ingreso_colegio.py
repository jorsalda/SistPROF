from app.extensions import db
from datetime import datetime, date, time
from enum import Enum as PyEnum


class TipoEvento(PyEnum):
    INGRESO = "ingreso"
    SALIDA = "salida"


class IngresoColegio(db.Model):
    __tablename__ = "ingresos_colegio"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False, default=date.today)
    hora = db.Column(db.Time, nullable=False, default=datetime.utcnow)
    metodo = db.Column(db.String(20), default="QR")
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    tipo_evento = db.Column(db.Enum(TipoEvento), default=TipoEvento.INGRESO)

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False
    )
    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relaciones
    estudiante = db.relationship("Estudiante", backref="ingresos", lazy=True)
    colegio = db.relationship("Colegio", backref="ingresos", lazy=True)

    def __repr__(self):
        return f'<Ingreso {self.estudiante_id} - {self.fecha} ({self.tipo_evento})>'