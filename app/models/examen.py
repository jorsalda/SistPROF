# models/examen.py
from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB


class Examen(db.Model):
    __tablename__ = "examenes"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(
        db.String(200),
        nullable=False
    )

    descripcion = db.Column(db.Text)
    tiempo_limite_minutos = db.Column(db.Integer, default=60)

    activo = db.Column(db.Boolean, default=True)

    fecha_creacion= db.Column(
        db.Date,
        nullable=False
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    materia_id = db.Column(
        db.Integer,
        db.ForeignKey("materias.id", ondelete="CASCADE"),
        nullable=False
    )

    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id", ondelete="CASCADE"),
        nullable=False
    )

    archivo_json = db.Column(db.String(200))

    contenido_json = db.Column(JSONB)

    tipo_examen_id = db.Column(
        db.Integer,
        db.ForeignKey("tipo_examen.id"),
        nullable=True
    )

    # 🔥 AGREGAR ESTA LÍNEA
    activo = db.Column(db.Boolean, default=True)

    # Relaciones existentes
    materia = db.relationship(
        "Materia",
        backref="examenes"
    )

    colegio = db.relationship(
        "Colegio",
        backref="examenes"
    )

    tipo_examen = db.relationship(
        "TipoExamen",
        backref="examenes",
        lazy=True
    )

    def __repr__(self):
        return f"<Examen {self.nombre}>"