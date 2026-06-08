from app.extensions import db


class Materia(db.Model):
    __tablename__ = "materias"
    __table_args__ = {'extend_existing': True}

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    # ================= RELACIONES =================

    # Clases asociadas
    clases = db.relationship(
        "Clase",
        foreign_keys="Clase.materia_id",
        back_populates="materia_obj",
        lazy=True
    )

    # Competencias de la materia
    competencias = db.relationship(
        "CompetenciaMateria",
        back_populates="materia",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # Resultados de exámenes
    resultados_examenes = db.relationship(
        "ResultadoExamen",
        back_populates="materia",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Materia {self.nombre}>"