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

    # NUEVAS COLUMNAS PARA EL BANCO DE PREGUNTAS
    docente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    examen_id = db.Column(db.Integer, db.ForeignKey('examenes.id'), nullable=True)

    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)

    # Relaciones existentes y nuevas
    materia = db.relationship("Materia", backref="preguntas")

    # NUEVAS RELACIONES
    docente = db.relationship("Usuario", backref="preguntas_creadas", foreign_keys=[docente_id])
    examen = db.relationship("Examen", backref="preguntas_asignadas", foreign_keys=[examen_id])

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
            'materia_id': self.materia_id,
            # Agregamos los nuevos campos al diccionario por si los necesitas en APIs
            'docente_id': self.docente_id,
            'examen_id': self.examen_id
        }

    def __repr__(self):
        return f"<Pregunta {self.id} - {self.tema}>"