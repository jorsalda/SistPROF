from app.extensions import db


class ConfiguracionEscalamiento(db.Model):
    __tablename__ = "configuracion_escalamiento"

    id = db.Column(db.Integer, primary_key=True)

    tipo_origen = db.Column(
        db.String(20),
        nullable=False
    )

    cantidad = db.Column(
        db.Integer,
        nullable=False
    )

    tipo_destino = db.Column(
        db.String(20),
        nullable=False
    )

    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id", ondelete="CASCADE"),
        nullable=False
    )

    colegio = db.relationship(
        "Colegio",
        backref="configuraciones_escalamiento"
    )