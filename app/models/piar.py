
from datetime import date
from app.extensions import db


class PIAR(db.Model):
    __tablename__ = "piar"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    diagnostico = db.Column(
        db.Text,
        nullable=True
    )

    objetivos = db.Column(
        db.Text,
        nullable=True
    )

    fecha_inicio = db.Column(
        db.Date,
        default=date.today,
        nullable=False
    )

    fecha_fin = db.Column(
        db.Date,
        nullable=True
    )

    activo = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "estudiantes.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    # Relaciones
    estudiante = db.relationship(
        "Estudiante",
        backref=db.backref(
            "piares",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    ajustes_razonables = db.relationship(
        "AjusteRazonable",
        backref="piar",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        estado = "Activo" if self.activo else "Inactivo"
        return f"<PIAR {self.estudiante_id} - {estado}>"
