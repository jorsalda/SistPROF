# models/tipo_examen.py
from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB


class TipoExamen(db.Model):
    __tablename__ = "tipo_examen"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    tiene_contexto = db.Column(db.Boolean, default=False)
    tiene_json = db.Column(db.Boolean, default=True)
    requiere_grupo = db.Column(db.Boolean, default=False)
    tiempo_por_defecto = db.Column(db.Integer, default=30)
    configuracion = db.Column(JSONB)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TipoExamen {self.nombre}>"