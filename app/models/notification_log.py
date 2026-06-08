from app.extensions import db
from datetime import datetime


class NotificationLog(db.Model):
    __tablename__ = "notification_logs"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    # Claves foráneas flexibles (pueden ser NULL)
    citacion_id = db.Column(
        db.Integer,
        db.ForeignKey("citaciones_acudiente.id", ondelete="CASCADE"),
        nullable=True
    )
    token_id = db.Column(
        db.Integer,
        db.ForeignKey("tokens_activacion.id", ondelete="CASCADE"),
        nullable=True
    )

    # Tipo de notificación
    tipo = db.Column(
        db.String(50),
        nullable=False,
        index=True
    )

    # Destinatario y contenido
    destinatario = db.Column(db.String(120), nullable=False)
    asunto = db.Column(db.String(200), nullable=True)

    # Proveedor de email
    proveedor = db.Column(db.String(50), default='resend')
    id_proveedor = db.Column(db.String(100), nullable=True)

    # Estado del envío
    estado = db.Column(
        db.String(20),
        nullable=False,
        default='pendiente',
        index=True
    )

    # Mensaje de error si falla
    error_msg = db.Column(db.Text, nullable=True)

    # Payload JSON para datos adicionales
    payload_json = db.Column(db.JSON, nullable=True)

    # Timestamps
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relaciones (opcionales, para acceder a los objetos relacionados)
    citacion = db.relationship(
        "CitacionAcudiente",
        foreign_keys=[citacion_id],
        lazy=True
    )

    token = db.relationship(
        "TokenActivacion",
        foreign_keys=[token_id],
        lazy=True
    )

    def __repr__(self):
        return f'<NotificationLog {self.id} - {self.tipo} - {self.estado}>'

    def to_dict(self):
        """Convierte el registro a diccionario (útil para APIs)"""
        return {
            'id': self.id,
            'tipo': self.tipo,
            'destinatario': self.destinatario,
            'asunto': self.asunto,
            'estado': self.estado,
            'proveedor': self.proveedor,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'payload_json': self.payload_json
        }