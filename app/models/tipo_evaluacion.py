from app.extensions import db
from datetime import datetime


class TipoEvaluacion(db.Model):
    __tablename__ = "tipos_evaluacion"

    id = db.Column(db.Integer, primary_key=True)

    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id", ondelete="CASCADE"),
        nullable=False
    )

    nombre = db.Column(
        db.String(50),
        nullable=False
    )

    porcentaje = db.Column(
        db.Numeric(5, 2),
        nullable=False,
        default=0
    )

    activo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    fecha_creacion = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    colegio = db.relationship(
        "Colegio",
        backref="tipos_evaluacion"
    )

    def __repr__(self):
        return f"<TipoEvaluacion {self.nombre} {self.porcentaje}%>"