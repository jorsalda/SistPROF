from app.extensions import db


class NivelMateria(db.Model):
    __tablename__ = "nivel_materia"

    id = db.Column(db.Integer, primary_key=True)

    nivel_educativo = db.Column(
        db.String(50),
        nullable=False
    )

    materia_id = db.Column(
        db.Integer,
        db.ForeignKey("materias.id"),
        nullable=False
    )

    orden = db.Column(
        db.Integer,
        default=0
    )

    activo = db.Column(
        db.Boolean,
        default=True
    )

    # Relaciones
    materia = db.relationship("Materia", backref="niveles_materia")

    def __repr__(self):
        return f"<NivelMateria {self.nivel_educativo} - {self.materia.nombre}>"