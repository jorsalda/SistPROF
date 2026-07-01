from app.extensions import db
from datetime import datetime


class AreaGestion(db.Model):
    __tablename__ = "areas_gestion"

    id = db.Column(db.Integer, primary_key=True)
    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id", ondelete="CASCADE"),
        nullable=False
    )
    nombre = db.Column(db.String(100), nullable=False)
    porcentaje = db.Column(db.Numeric(5, 2), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    colegio = db.relationship("Colegio", backref="areas")

    # Relación 1:N con Competencias
    competencias = db.relationship(
        "CompetenciaDocente",
        back_populates="area_gestion",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # Relación muchos a muchos con Grupos
    grupos = db.relationship(
        "Grupo",
        secondary="grupo_areas",
        back_populates="areas",
        lazy=True
    )

    asignaciones_grupos = db.relationship(
        "GrupoAreas",
        back_populates="area",
        cascade="all, delete-orphan",
        lazy=True,
        overlaps="grupos"
    )

    docentes_asignados = db.relationship(
        "DocenteAreas",
        back_populates="area",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<AreaGestion {self.nombre}>"