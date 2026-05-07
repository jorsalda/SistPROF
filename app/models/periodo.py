from app.extensions import db


class Periodo(db.Model):
    __tablename__ = "periodos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(50),
        nullable=False
    )

    anio_lectivo = db.Column(
        db.Integer,
        nullable=True
    )

    fecha_inicio = db.Column(
        db.Date,
        nullable=True
    )

    fecha_fin = db.Column(
        db.Date,
        nullable=True
    )

    activo = db.Column(
        db.Boolean,
        default=True
    )

    def __repr__(self):
        return f"<Periodo {self.nombre}>"