from app.extensions import db


class EstudianteAcudiente(db.Model):
    __tablename__ = "estudiante_acudiente"
    __table_args__ = {'extend_existing': True}

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        primary_key=True
    )
    acudiente_id = db.Column(
        db.Integer,
        db.ForeignKey("acudientes.id", ondelete="CASCADE"),
        primary_key=True
    )

    # Relaciones helper
    estudiante = db.relationship("Estudiante", backref="acudientes_relacion", lazy=True)
    acudiente = db.relationship("Acudiente", backref="estudiantes_relacion", lazy=True)

    def __repr__(self):
        return f'<EstudianteAcudiente {self.estudiante_id}-{self.acudiente_id}>'