
from app.extensions import db


class RespuestaExamenDetalle(db.Model):
    __tablename__ = "respuestas_examen_detalle"

    id = db.Column(db.Integer, primary_key=True)

    resultado_examen_id = db.Column(
        db.Integer,
        db.ForeignKey("resultados_examen.id", ondelete="CASCADE"),
        nullable=False
    )

    numero_pregunta = db.Column(
        db.Integer,
        nullable=False
    )

    texto_pregunta = db.Column(
        db.Text,
        nullable=False
    )

    respuesta_seleccionada = db.Column(
        db.String(300),
        nullable=False
    )

    respuesta_correcta = db.Column(
        db.String(300),
        nullable=False
    )

    es_correcta = db.Column(
        db.Boolean,
        default=False
    )

    tiempo_respuesta_seg = db.Column(
        db.Integer,
        nullable=True
    )

    resultado = db.relationship(
        "ResultadoExamen",
        back_populates="detalles"
    )

    def __repr__(self):
        return f'<Detalle P{self.numero_pregunta} - Correcta: {self.es_correcta}>'

