from app.extensions import db
from datetime import datetime


class Suscripcion(db.Model):
    __tablename__ = "suscripciones"

    id = db.Column(db.Integer, primary_key=True)

    plan = db.Column(
        db.String(100),
        nullable=False
    )

    fecha_inicio = db.Column(
        db.Date,
        nullable=False
    )

    fecha_fin = db.Column(
        db.Date,
        nullable=False
    )

    activa = db.Column(
        db.Boolean,
        default=True
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id", ondelete="CASCADE"),
        nullable=False
    )

    colegio = db.relationship(
        "Colegio",
        backref="suscripciones"
    )

    def __repr__(self):
        return f"<Suscripcion {self.plan}>"