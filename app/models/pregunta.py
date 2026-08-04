# app/models/pregunta.py
from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB


class Pregunta(db.Model):
    __tablename__ = "preguntas"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), default='icfes', nullable=False)
    texto = db.Column(db.Text, nullable=False)
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

    # ✅ AGREGAR ESTAS DOS LÍNEAS (Faltaban)
    url_contexto = db.Column(db.String(300), nullable=True)
    tipo_contexto = db.Column(db.String(20), nullable=True)

    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)

    # Relaciones
    materia = db.relationship("Materia", backref="preguntas")
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
            'docente_id': self.docente_id,
            'examen_id': self.examen_id,
            # ✅ Incluir contexto en el diccionario
            'url_contexto': self.url_contexto,
            'tipo_contexto': self.tipo_contexto
        }

    def __repr__(self):
        return f"<Pregunta {self.id} - {self.tema}>"