from app.extensions import db


class ConfiguracionDisciplinaria(db.Model):
    __tablename__ = "configuracion_disciplinaria"

    id = db.Column(db.Integer, primary_key=True)

    dias_prescripcion = db.Column(
        db.Integer,
        default=30
    )

    max_tipo2 = db.Column(
        db.Integer,
        default=3
    )

    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id", ondelete="CASCADE"),
        nullable=False
    )

    colegio = db.relationship(
        "Colegio",
        backref="configuracion_disciplinaria"
    )