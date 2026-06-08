from app.extensions import db


class Competencia(db.Model):
    __tablename__ = "competencias"

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


    def __repr__(self):
        return f"<Competencia {self.nombre}>"