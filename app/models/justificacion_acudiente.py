from app.extensions import db
from datetime import datetime


class JustificacionAcudiente(db.Model):
    __tablename__ = "justificaciones_acudiente"

    id = db.Column(db.Integer, primary_key=True)

    descripcion = db.Column(db.Text, nullable=False)

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    novedad_id = db.Column(
        db.Integer,
        db.ForeignKey("novedades.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    acudiente_id = db.Column(
        db.Integer,
        db.ForeignKey("acudientes.id", ondelete="CASCADE"),
        nullable=False
    )

    novedad = db.relationship(
        "Novedad",
        backref=db.backref(
            "justificacion",
            uselist=False,
            cascade="all, delete-orphan"
        )
    )

    acudiente = db.relationship(
        "Acudiente",
        backref="justificaciones"
    )

    def __repr__(self):
        return f"<JustificacionAcudiente {self.id}>"