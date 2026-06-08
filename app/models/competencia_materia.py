from app.extensions import db


class CompetenciaMateria(db.Model):
    __tablename__ = "competencias_materia"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(
        db.String(150),
        nullable=False
    )

    descripcion = db.Column(
        db.Text,
        nullable=True
    )

    porcentaje = db.Column(
        db.Float,
        default=0
    )

    materia_id = db.Column(
        db.Integer,
        db.ForeignKey("materias.id", ondelete="CASCADE"),
        nullable=False
    )

    materia = db.relationship(
        "Materia",
        back_populates="competencias"
    )

    indicadores = db.relationship(
        "IndicadorLogro",
        back_populates="competencia",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<CompetenciaMateria {self.nombre}>"