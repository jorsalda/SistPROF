from app.extensions import db
from sqlalchemy.dialects.postgresql import ENUM

# Define el tipo ENUM (debe coincidir exactamente con tu DDL)
NivelDesempenoEnum = ENUM('Bajo', 'Basico', 'Alto', 'Superior',
                          name='nivel_desempeno', create_type=False)


class IndicadorLogro(db.Model):
    __tablename__ = "indicadores_logro"

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.Text, nullable=False)
    codigo = db.Column(db.String(40), nullable=True)

    # ✅ USAR EL TIPO ENUM NATIVO DE POSTGRESQL
    nivel = db.Column(NivelDesempenoEnum, nullable=True)

    orden = db.Column(db.Integer, default=1, nullable=False)

    competencia_materia_id = db.Column(
        db.Integer,
        db.ForeignKey("competencias_materia.id", ondelete="CASCADE"),
        nullable=False
    )

    competencia = db.relationship(
        "CompetenciaEstudiante",
        back_populates="indicadores"
    )

    evaluaciones = db.relationship(
        "EvaluacionEstudiante",
        back_populates="indicador",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<IndicadorLogro {self.codigo}: {self.nivel}>"