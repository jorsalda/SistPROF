from app.extensions import db


class EstudianteAcudiente(db.Model):
    """Tabla intermedia para relación muchos-a-muchos entre
    estudiantes y acudientes"""
    __tablename__ = "estudiante_acudiente"

    id = db.Column(db.Integer, primary_key=True)

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False
    )

    acudiente_id = db.Column(
        db.Integer,
        db.ForeignKey("acudientes.id", ondelete="CASCADE"),
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            'estudiante_id',
            'acudiente_id',
            name='unica_relacion'
        ),
    )

    def __repr__(self):
        return f"<EstudianteAcudiente est={self.estudiante_id} acu={self.acudiente_id}>"
