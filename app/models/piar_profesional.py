from datetime import datetime
from app.extensions import db


class PiarProfesional(db.Model):
    __tablename__ = "piar_profesional"
    __table_args__ = (
        db.UniqueConstraint('piar_id', 'profesional_id', name='uq_piar_profesional'),
        {'extend_existing': True}
    )

    id = db.Column(db.Integer, primary_key=True)

    piar_id = db.Column(
        db.Integer,
        db.ForeignKey("piar.id", ondelete="CASCADE"),
        nullable=False
    )

    profesional_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False
    )

    asignado_en = db.Column(
        db.DateTime,
        default=datetime.now,
        nullable=True
    )

    # =====================================================
    # RELACIONES
    # =====================================================

    # La relación "piar" ya está definida en el backref del modelo PIAR,
    # pero la declaramos explícitamente para mayor claridad.
    # profesional se relaciona con el modelo Usuario.
    profesional = db.relationship(
        "Usuario",
        foreign_keys=[profesional_id],
        lazy=True
    )

    def __repr__(self):
        return f"<PiarProfesional piar={self.piar_id} profesional={self.profesional_id}>"