from app.extensions import db


class PeriodoAcademico(db.Model):
    __tablename__ = "periodos_academicos"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(
        db.String(50),
        nullable=False
    )

    anio = db.Column(
        db.Integer,
        nullable=False
    )

    activo = db.Column(
        db.Boolean,
        default=True
    )

    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id", ondelete="CASCADE"),
        nullable=False
    )

    colegio = db.relationship(
        "Colegio",
        backref="periodos_academicos"
    )

    def __repr__(self):
        return f"<PeriodoAcademico {self.nombre}>"