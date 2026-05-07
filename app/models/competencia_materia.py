from app.extensions import db


class CompetenciaMateria(db.Model):
    __tablename__ = "competencias_materia"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    materia_id = db.Column(
        db.Integer,
        db.ForeignKey("materias.id"),
        nullable=False
    )

    nombre = db.Column(
        db.String(255),
        nullable=False
    )

    descripcion = db.Column(
        db.Text,
        nullable=True
    )

    peso_porcentual = db.Column(
        db.Numeric(5, 2),
        nullable=True
    )

    orden = db.Column(
        db.Integer,
        nullable=True
    )

    materia = db.relationship(
        "Materia",
        backref="competencias",
        lazy=True
    )

    def __repr__(self):
        return f"<CompetenciaMateria {self.nombre}>"