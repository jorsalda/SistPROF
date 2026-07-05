from app.extensions import db
from datetime import datetime


class GrupoMateria(db.Model):
    __tablename__ = "grupo_materias"

    # =====================================================
    # COLUMNAS
    # =====================================================

    id = db.Column(db.Integer, primary_key=True)

    grupo_id = db.Column(
        db.Integer,
        db.ForeignKey("grupos.id", ondelete="CASCADE"),
        nullable=False
    )

    materia_id = db.Column(
        db.Integer,
        db.ForeignKey("materias.id"),
        nullable=False
    )

    docente_id = db.Column(
        db.Integer,
        db.ForeignKey("docentes.id", ondelete="SET NULL"),
        nullable=True
    )

    horas_semanales = db.Column(
        db.Integer,
        default=2
    )

    activo = db.Column(
        db.Boolean,
        default=True
    )

    fecha_asignacion = db.Column(
        db.DateTime,
        default=datetime.now
    )

    # =====================================================
    # RELACIONES
    # =====================================================

    grupo = db.relationship(
        "Grupo",
        back_populates="materias_asignadas",
        lazy=True
    )

    materia = db.relationship(
        "Materia",
        lazy=True
    )

    docente = db.relationship(
        "Docente",
        lazy=True
    )

    # Una materia de grupo tiene muchas clases (horarios)
    clases = db.relationship(
        "Clase",
        back_populates="grupo_materia",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # =====================================================
    # REPRESENTACIÓN
    # =====================================================

    def __repr__(self):
        return (
            f"<GrupoMateria "
            f"Grupo={self.grupo_id} "
            f"Materia={self.materia_id}>"
        )

    @property
    def nombre_materia(self):
        return self.materia.nombre if self.materia else "N/A"

    @property
    def nombre_docente(self):
        return self.docente.nombre if self.docente else "Sin asignar"