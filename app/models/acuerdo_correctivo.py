from app.extensions import db
from datetime import datetime


class AcuerdoCorrectivo(db.Model):
    __tablename__ = "acuerdos_correctivos"

    id = db.Column(db.Integer, primary_key=True)

    compromisos = db.Column(
        db.Text,
        nullable=False
    )

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    cumplido = db.Column(
        db.Boolean,
        default=False
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
        backref="acuerdos_correctivos"
    )

    novedad = db.relationship(
        "Novedad",
        backref=db.backref(
            "acuerdo_correctivo",
            uselist=False
        )
    )

    def __repr__(self):
        return f"<AcuerdoCorrectivo {self.id}>"