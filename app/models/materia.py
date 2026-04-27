from app.extensions import db


class Materia(db.Model):
    __tablename__ = "materias"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    # Clases que usan esta materia (apunta a 'materia_obj' en Clase)
    clases = db.relationship(
        "Clase",
        foreign_keys="Clase.materia_id",
        back_populates="materia_obj",  # ← Debe coincidir con Clase.materia_obj
        lazy=True
    )

    # Resultados de exámenes
    resultados_examenes = db.relationship(
        "ResultadoExamen",
        back_populates="materia",
        lazy=True
    )

    def __repr__(self):
        return f'<Materia {self.nombre}>'