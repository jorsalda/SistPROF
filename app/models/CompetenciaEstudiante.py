# app/models/CompetenciaEstudiante.py
from app.extensions import db


class CompetenciaEstudiante(db.Model):
    __tablename__ = "competencias_materia"

    id = db.Column(db.Integer, primary_key=True)

    # ✅ NUEVA COLUMNA: Código único para planillas
    codigo = db.Column(db.String(30), unique=True, nullable=False)

    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    porcentaje = db.Column(db.Float, default=0)
    nivel_educativo = db.Column(db.String(50))
    materia_id = db.Column(
        db.Integer,
        db.ForeignKey("materias.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relación bidireccional
    materia = db.relationship("Materia", back_populates="competencias")
    indicadores = db.relationship(
        "IndicadorLogro",
        back_populates="competencia",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<CompetenciaEstudiante {self.codigo} - {self.nombre}>"