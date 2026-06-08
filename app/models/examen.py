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

    fecha = db.Column(
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

    archivo_json = db.Column(db.String(200))  # ← Nombre del archivo (legacy)

    # 🔥 NUEVO CAMPO (opcional, si decide guardar JSON directamente en esta tabla)
    contenido_json = db.Column(JSONB)  # ← Contenido completo del examen

    # 🔥 RELACIÓN CON TIPO_EXAMEN
    tipo_examen_id = db.Column(
        db.Integer,
        db.ForeignKey("tipo_examen.id"),
        nullable=True
    )

    # Relaciones existentes
    materia = db.relationship(
        "Materia",
        backref="examenes"
    )

    colegio = db.relationship(
        "Colegio",
        backref="examenes"
    )

    # 🔥 NUEVA RELACIÓN
    tipo_examen = db.relationship(
        "TipoExamen",
        backref="examenes",
        lazy=True
    )

    def __repr__(self):
        return f"<Examen {self.nombre}>"