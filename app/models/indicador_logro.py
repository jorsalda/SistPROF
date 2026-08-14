# app/models/indicador_logro.py
from app.extensions import db


class IndicadorLogro(db.Model):
    __tablename__ = "indicadores_logro"

    id = db.Column(db.Integer, primary_key=True)

    # Código único para planillas
    codigo = db.Column(db.String(40), unique=True, nullable=False)

    descripcion = db.Column(db.Text, nullable=False)

    # ✅ CORRECCIÓN DEFINITIVA:
    # En Python sigue llamándose 'competencia_id' (para que tus relaciones funcionen)
    # Pero en la BD mapeamos explícitamente a 'competencia_materia_id'
    competencia_id = db.Column(
        "competencia_materia_id",  # <--- NOMBRE REAL EN LA BASE DE DATOS
        db.Integer,
        db.ForeignKey("competencias_materia.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relación bidireccional con CompetenciaEstudiante (NO CAMBIAR ESTO)
    competencia = db.relationship(
        "CompetenciaEstudiante",
        back_populates="indicadores"
    )

    # Relación con Evaluaciones (NO CAMBIAR ESTO)
    evaluaciones = db.relationship(
        "EvaluacionEstudiante",
        back_populates="indicador",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<IndicadorLogro {self.codigo} - {self.descripcion[:30]}>"