# app/models/ajuste_razonable.py

from datetime import datetime
from app.extensions import db


class AjusteRazonable(db.Model):
    __tablename__ = "ajustes_razonables"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    piar_id = db.Column(
        db.Integer,
        db.ForeignKey("piar.id", ondelete="CASCADE"),
        nullable=False
    )

    descripcion = db.Column(
        db.Text,
        nullable=False
    )

    aplicado = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    fecha_aplicacion = db.Column(
        db.DateTime,
        nullable=True
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.now,
        nullable=False
    )

    # =====================================================
    # NUEVAS LLAVES FORÁNEAS (MATERIA Y DOCENTE)
    # =====================================================

    docente_id = db.Column(
        db.Integer,
        db.ForeignKey("docentes.id", ondelete="SET NULL"),
        nullable=True
    )

    materia_id = db.Column(
        db.Integer,
        db.ForeignKey("materias.id", ondelete="SET NULL"),
        nullable=True
    )

    # =====================================================
    # RELACIONES
    # =====================================================

    docente = db.relationship(
        "Docente",
        backref=db.backref("ajustes_razonables", lazy=True)
    )

    materia = db.relationship(
        "Materia",
        backref=db.backref("ajustes_razonables", lazy=True)
    )

    def __repr__(self):
        estado = "Aplicado" if self.aplicado else "Pendiente"
        return f"<AjusteRazonable {self.id} - {estado}>"