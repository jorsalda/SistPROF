# app/models/pregunta.py
from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB


class Pregunta(db.Model):
    __tablename__ = "preguntas"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), default='icfes', nullable=False)
    texto = db.Column(db.Text, nullable=False)

    # Usamos JSONB para aprovechar PostgreSQL, igual que en Examen
    opciones = db.Column(JSONB)
    respuesta_correcta = db.Column(db.String(300))

    rubrica_ia = db.Column(db.Text)
    puntos_maximos = db.Column(db.Integer, default=0)
    explicacion = db.Column(db.Text)

    tema = db.Column(db.String(100))
    dificultad = db.Column(db.String(20))

    materia_id = db.Column(db.Integer, db.ForeignKey("materias.id"))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)

    # Relación con Materia (opcional pero muy útil)
    materia = db.relationship("Materia", backref="preguntas")

    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'texto': self.texto,
            'opciones': self.opciones,
            'respuesta_correcta': self.respuesta_correcta,
            'explicacion': self.explicacion,
            'tema': self.tema,
            'dificultad': self.dificultad,
            'materia_id': self.materia_id
        }

    def __repr__(self):
        return f"<Pregunta {self.id} - {self.tema}>"