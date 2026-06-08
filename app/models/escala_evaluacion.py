#%%
from app.extensions import db


class EscalaEvaluacion(db.Model):
    __tablename__ = "escala_evaluacion"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(
        db.String(50),
        nullable=False
    )

    nota_minima = db.Column(
        db.Float,
        nullable=False
    )

    nota_maxima = db.Column(
        db.Float,
        nullable=False
    )

    descripcion = db.Column(db.Text)

    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id", ondelete="CASCADE"),
        nullable=False
    )

    colegio = db.relationship(
        "Colegio",
        backref="escalas_evaluacion"
    )

    def __repr__(self):
        return f"<EscalaEvaluacion {self.nombre}>"