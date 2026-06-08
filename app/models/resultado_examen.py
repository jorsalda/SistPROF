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

    # Nota académica oficial
    nota_numerica = db.Column(db.Numeric(3, 2), nullable=True)  # Escala 0.00 - 5.00
    nivel = db.Column(db.Enum(NivelDesempeno), nullable=True)

    # Métricas de EstudianteJS (nuevas)
    respuestas_correctas = db.Column(db.Integer, default=0)
    respuestas_incorrectas = db.Column(db.Integer, default=0)
    porcentaje = db.Column(db.Float, default=0.0)  # 0-100%
    literal = db.Column(db.String(1))  # S / A / B / b / I
    cuestionario_archivo = db.Column(db.String(200))  # ej: "2026_1.json"

    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_finalizacion = db.Column(db.DateTime, nullable=True)

    # ========== CLAVES FORÁNEAS ==========
    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False
    )
    examen_id = db.Column(
        db.Integer,
        db.ForeignKey("examenes.id", ondelete="CASCADE"),  # ✅ CORREGIDO: ahora es ForeignKey
        nullable=False
    )
    materia_id = db.Column(
        db.Integer,
        db.ForeignKey("materias.id"),
        nullable=False
    )

    # ========== RELACIONES ==========
    estudiante = db.relationship(
        "Estudiante",
        back_populates="resultados_examenes",
        lazy=True
    )
    materia = db.relationship(
        "Materia",
        back_populates="resultados_examenes",
        lazy=True
    )
    examen = db.relationship(
        "Examen",
        backref="resultados"  # ← Para acceder: examen.resultados
    )
    # Relación con detalles de respuestas

    detalles = db.relationship(
        "RespuestaExamenDetalle",
        back_populates="resultado",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<ResultadoExamen {self.estudiante_id} - Nota: {self.nota_numerica} - Literal: {self.literal}>'


