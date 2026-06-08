
# app/models/areas_gestion.py

from app.extensions import db


class AreaGestion(db.Model):
    __tablename__ = "areas_gestion"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False, unique=True)
    descripcion = db.Column(db.Text)

    criterios = db.relationship(
        "CriterioEvaluacion",
        backref="area_gestion",
        lazy=True
    )

    def __repr__(self):
        return f"<AreaGestion {self.nombre}>"

