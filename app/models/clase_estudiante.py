from app.extensions import db


class ClaseEstudiante(db.Model):
    __tablename__ = "clase_estudiantes"
    __table_args__ = {'extend_existing': True}

    # ========= CLAVES =========
    clase_id = db.Column(
        db.Integer,
        db.ForeignKey("clases.id", ondelete="CASCADE"),
        primary_key=True
    )

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        primary_key=True
    )

    # ========= RELACIONES =========
    clase = db.relationship(
        "Clase",
        back_populates="estudiantes_matriculados",
        lazy=True
    )

    estudiante = db.relationship(
        "Estudiante",
        back_populates="clases_matriculadas",
        lazy=True
    )

    def __repr__(self):
        return f'<ClaseEstudiante {self.clase_id}-{self.estudiante_id}>'