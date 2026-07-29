# app/models/examen_contenido.py
from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB


class ExamenContenido(db.Model):
    __tablename__ = 'examen_contenido'

    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey('examenes.id'), nullable=False)
    contenido_json = db.Column(JSONB, nullable=False)
    version = db.Column(db.Integer, default=1)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación inversa (opcional pero muy útil para acceder fácil desde el examen)
    examen = db.relationship('Examen', backref='contenido_detalle', foreign_keys=[examen_id])

    def __repr__(self):
        return f'<ExamenContenido {self.id} - Examen {self.examen_id}>'