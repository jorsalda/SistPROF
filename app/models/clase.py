from app.extensions import db
from sqlalchemy import Time
from enum import Enum as PyEnum


class DiaSemana(PyEnum):
    LUNES = "lunes"
    MARTES = "martes"
    MIERCOLES = "miercoles"
    JUEVES = "jueves"
    VIERNES = "viernes"


class Clase(db.Model):
    __tablename__ = "clases"
    __table_args__ = {'extend_existing': True}

    # ========== COLUMNAS ==========
    id = db.Column(db.Integer, primary_key=True)

    hora_inicio = db.Column(Time, nullable=False)
    hora_fin = db.Column(Time, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    dia = db.Column(db.Enum(DiaSemana), nullable=False)

    # ========== CLAVES FORÁNEAS ==========
    docente_id = db.Column(
        db.Integer,
        db.ForeignKey("docentes.id", ondelete="CASCADE"),
        nullable=False
    )

    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id"),
        nullable=False
    )

    # ✅ NUEVA CLAVE: Vincula directamente a la materia asignada al grupo
    grupo_materia_id = db.Column(
        db.Integer,
        db.ForeignKey("grupo_materias.id", ondelete="CASCADE"),
        nullable=False
    )

    # ========== RELACIONES ==========

    # Docente que imparte la clase
    docente = db.relationship(
        "Docente",
        foreign_keys=[docente_id],
        back_populates="clases",
        lazy=True
    )

    # Colegio al que pertenece
    colegio = db.relationship(
        "Colegio",
        foreign_keys=[colegio_id],
        back_populates="clases_colegio",
        lazy=True
    )

    # ✅ NUEVA RELACIÓN: Acceso a la materia y grupo
    grupo_materia = db.relationship(
        "GrupoMateria",
        back_populates="clases",
        lazy=True
    )

    # Estudiantes matriculados (tabla intermedia)
    estudiantes_matriculados = db.relationship(
        "ClaseEstudiante",
        back_populates="clase",
        cascade="all, delete-orphan",
        lazy=True
    )

    # ========== PROPIEDADES DE ACCESO RÁPIDO ==========

    @property
    def nombre_materia(self):
        if self.grupo_materia and self.grupo_materia.materia:
            return self.grupo_materia.materia.nombre
        return "N/A"

    @property
    def nombre_grupo(self):
        if self.grupo_materia and self.grupo_materia.grupo:
            return f"{self.grupo_materia.grupo.grado}{self.grupo_materia.grupo.nombre}"
        return "N/A"

    def __repr__(self):
        return f'<Clase {self.nombre_materia} - {self.nombre_grupo} ({self.dia})>'