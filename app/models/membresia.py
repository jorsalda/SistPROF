from app.extensions import db
from datetime import datetime


class Membresia(db.Model):
    __tablename__ = "membresias"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    # Tipo de plan
    tipo_plan = db.Column(db.Enum(
        'mensual',
        'anual',
        'vitalicio',
        name='tipo_plan_membresia'
    ), nullable=False)

    # Estado
    estado = db.Column(db.Enum(
        'pendiente',
        'aprobado',
        'rechazado',
        'vencido',
        name='estado_membresia'
    ), default='pendiente', nullable=False)

    # Fechas
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_fin = db.Column(db.DateTime, nullable=True)
    fecha_pago = db.Column(db.DateTime, nullable=True)

    # Monto
    monto = db.Column(db.Float, nullable=False)
    metodo_pago = db.Column(db.String(50), nullable=True)  # 'transferencia', 'efectivo', etc.
    comprobante = db.Column(db.String(255), nullable=True)  # URL o referencia

    # Relación
    usuario = db.relationship('Usuario', backref='membresias')

    def __repr__(self):
        return f'<Membresia {self.tipo_plan} - {self.estado}>'