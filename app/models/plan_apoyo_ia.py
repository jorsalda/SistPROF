from app.extensions import db
from datetime import datetime

class PlanApoyoIA(db.Model):
    __tablename__ = "planes_apoyo_ia"

    id = db.Column(db.Integer, primary_key=True)

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False
    )

    materia_id = db.Column(
        db.Integer,
        db.ForeignKey("materias.id", ondelete="CASCADE"),
        nullable=False
    )

    periodo_academico_id = db.Column(
        db.Integer,
        db.ForeignKey("periodos_academicos.id", ondelete="CASCADE"),
        nullable=False
    )

    docente_id = db.Column(
        db.Integer,
        db.ForeignKey("docentes.id", ondelete="CASCADE"),
        nullable=False
    )

    fortalezas = db.Column(
        db.JSON,
        default=list
    )

    debilidades = db.Column(
        db.JSON,
        default=list
    )

    plan_apoyo = db.Column(
        db.Text,
        nullable=True
    )

    # Snapshot de notas usadas para detectar si cambiaron
    notas_contexto = db.Column(
        db.JSON,
        default=dict
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<PlanApoyoIA estudiante={self.estudiante_id} materia={self.materia_id}>"