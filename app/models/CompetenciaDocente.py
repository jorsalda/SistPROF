from app.extensions import db
from datetime import datetime
from .competencia_contribucion import competencia_contribucion


class CompetenciaDocente(db.Model):
    __tablename__ = "competencias"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    area_id = db.Column(
        db.Integer,
        db.ForeignKey("areas_gestion.id", ondelete="CASCADE"),
        nullable=False
    )

    nombre = db.Column(
        db.String(150),
        nullable=False
    )

    descripcion = db.Column(
        db.Text,
        nullable=True
    )

    activo = db.Column(
        db.Boolean,
        default=True
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    orden = db.Column(
        db.Integer,
        default=1
    )

    # Relación con AreaGestion
    area_gestion = db.relationship(
        "AreaGestion",
        back_populates="competencias"
    )

    # Relación N:M con Contribucion
    contribuciones = db.relationship(
        "Contribucion",
        secondary=competencia_contribucion,
        back_populates="competencias",
        lazy=True
    )

    def __repr__(self):
        return f"<CompetenciaDocente {self.nombre}>"