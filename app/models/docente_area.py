from app.extensions import db
from datetime import datetime


class DocenteAreas(db.Model):
    """Tabla intermedia: Docente ↔ Áreas"""
    __tablename__ = "docente_areas"

    id = db.Column(db.Integer, primary_key=True)

    docente_id = db.Column(
        db.Integer,
        db.ForeignKey("docentes.id", ondelete="CASCADE"),
        nullable=False
    )

    area_id = db.Column(
        db.Integer,
        db.ForeignKey("areas_gestion.id", ondelete="CASCADE"),
        nullable=False
    )

    activo = db.Column(
        db.Boolean,
        default=True
    )

    fecha_asignacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relaciones
    docente = db.relationship(
        "Docente",
        back_populates="areas_docente_asignadas"
    )

    area = db.relationship(
        "AreaGestion",
        back_populates="docentes_asignados"
    )

    def __repr__(self):
        return f"<DocenteAreas Docente={self.docente_id} Area={self.area_id}>"