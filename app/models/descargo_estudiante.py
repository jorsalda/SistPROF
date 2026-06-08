from app.extensions import db
from datetime import datetime


class DescargoEstudiante(db.Model):
    __tablename__ = "descargos_estudiante"

    id = db.Column(db.Integer, primary_key=True)

    descripcion = db.Column(db.Text, nullable=False)

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False
    )

    novedad_id = db.Column(
        db.Integer,
        db.ForeignKey("novedades.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    estudiante = db.relationship(
        "Estudiante",
        backref="descargos"
    )

    novedad = db.relationship(
        "Novedad",
        backref=db.backref(
            "descargo",
            uselist=False
        )
    )

    def __repr__(self):
        return f"<DescargoEstudiante {self.id}>"