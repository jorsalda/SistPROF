from app.extensions import db
from datetime import datetime


class CitacionAcudiente(db.Model):
    __tablename__ = "citaciones_acudiente"

    id = db.Column(db.Integer, primary_key=True)

    motivo = db.Column(db.Text, nullable=False)

    fecha_citacion = db.Column(db.DateTime, nullable=False)

    estado = db.Column(
        db.String(20),
        default="PENDIENTE"
    )

    # ✅ NUEVA COLUMNA AGREGADA
    fecha_notificacion = db.Column(db.DateTime)

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

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
        db.ForeignKey("novedades.id", ondelete="SET NULL")
    )

    estudiante = db.relationship(
        "Estudiante",
        backref="citaciones"
    )

    acudiente = db.relationship(
        "Acudiente",
        backref="citaciones"
    )

    novedad = db.relationship(
        "Novedad",
        backref="citacion"
    )

    def __repr__(self):
        return f"<CitacionAcudiente {self.id}>"