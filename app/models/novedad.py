from app.extensions import db
from datetime import datetime
from enum import Enum as PyEnum


class TipoNovedad(PyEnum):
    DISCIPLINA = "DISCIPLINA"
    ACADEMICO = "ACADEMICO"
    LLEGADA_TARDE = "LLegada_Tarde"


class TipoGravedad(PyEnum):
    TIPO_1 = "Tipo 1"
    TIPO_2 = "Tipo 2"
    TIPO_3 = "Tipo 3"


class Novedad(db.Model):
    __tablename__ = "novedades"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    tipo_novedad = db.Column(db.Enum(TipoNovedad), nullable=False)
    informe = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    hora = db.Column(db.Time, nullable=False, default=datetime.utcnow)
    categoria = db.Column(db.String(20), nullable=True)
    gravedad = db.Column(db.Enum(TipoGravedad), nullable=False)

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False
    )
    registrada_por = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=True
    )

    # Relaciones
    estudiante = db.relationship("Estudiante", backref="novedades", lazy=True)

    def __repr__(self):
        return f'<Novedad {self.estudiante_id} - {self.tipo_novedad} ({self.gravedad})>'