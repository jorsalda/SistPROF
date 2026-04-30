from app.extensions import db
from datetime import datetime
from enum import Enum as PyEnum


class NivelDesempeno(PyEnum):
    BAJO = "Bajo"
    BASICO = "Basico"
    ALTO = "Alto"
    SUPERIOR = "Superior"


class ResultadoExamen(db.Model):
    __tablename__ = "resultados_examen"
    __table_args__ = {'extend_existing': True}

    # ========== COLUMNAS ==========
    id = db.Column(db.Integer, primary_key=True)
    nota_numerica = db.Column(db.Numeric(3, 2), nullable=True)
    nivel = db.Column(db.Enum(NivelDesempeno), nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    # ========== CLAVES FORÁNEAS ==========
    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False
    )
    examen_id = db.Column(db.Integer, nullable=False)
    materia_id = db.Column(
        db.Integer,
        db.ForeignKey("materias.id"),
        nullable=False
    )

    # ========== RELACIONES (CON back_populates) ==========

    # Estudiante
    estudiante = db.relationship(
        "Estudiante",
        back_populates="resultados_examenes",
        lazy=True
    )

    # Materia (con back_populates)
    materia = db.relationship(
        "Materia",
        back_populates="resultados_examenes",  # ← back_populates (NO backref)
        lazy=True
    )

    def __repr__(self):
        return f'<ResultadoExamen {self.estudiante_id} - {self.nota_numerica}>'