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
    grado = db.Column(db.String(20), nullable=False)
    grupo = db.Column(db.String(10), nullable=False)
    materia = db.Column(db.String(100), nullable=False)
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
    materia_id = db.Column(
        db.Integer,
        db.ForeignKey("materias.id"),
        nullable=True
    )

    # ========== RELACIONES (CON back_populates) ==========

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
        back_populates="clases_colegio",  # ← Nombre único para evitar conflicto
        lazy=True
    )

    # Materia (relación bidireccional)
    materia_obj = db.relationship(
        "Materia",
        foreign_keys=[materia_id],
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

    def __repr__(self):
        return f'<Clase {self.materia} - {self.grado}{self.grupo} ({self.dia})>'