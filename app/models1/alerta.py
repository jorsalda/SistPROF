from app.extensions import db
from datetime import datetime


class Alerta(db.Model):
    __tablename__ = "alertas"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    atendida = db.Column(db.Boolean, default=False)

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relaciones
    estudiante = db.relationship("Estudiante", backref="alertas", lazy=True)

    def __repr__(self):
        return f'<Alerta {self.estudiante_id} - {self.tipo}>'