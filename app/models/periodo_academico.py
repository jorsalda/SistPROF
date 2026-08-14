# app/models/periodo_academico.py
from app.extensions import db


class PeriodoAcademico(db.Model):
    __tablename__ = "periodos_academicos"

    id = db.Column(db.Integer, primary_key=True)

    # Campos básicos del periodo
    nombre = db.Column(db.String(50), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    orden = db.Column(db.Integer, default=1)  # ✅ AGREGADO (Faltaba en tu modelo)
    es_final = db.Column(db.Boolean, default=False)  # ✅ AGREGADO

    # Fechas de vigencia
    fecha_inicio = db.Column(db.Date)  # ✅ AGREGADO
    fecha_fin = db.Column(db.Date)  # ✅ AGREGADO

    # Estado y relación
    activo = db.Column(db.Boolean, default=True)
    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relación bidireccional limpia
    colegio = db.relationship("Colegio", backref="periodos")

    def __repr__(self):
        return f"<PeriodoAcademico {self.nombre} ({self.anio})>"