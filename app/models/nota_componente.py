from app.extensions import db
from datetime import datetime

class NotaComponenteEstudiante(db.Model):
    __tablename__ = "notas_componente_estudiante"

    id = db.Column(db.Integer, primary_key=True)

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False
    )

    grupo_materia_id = db.Column(
        db.Integer,
        db.ForeignKey("grupo_materias.id", ondelete="CASCADE"),
        nullable=False
    )

    periodo_academico_id = db.Column(
        db.Integer,
        db.ForeignKey("periodos_academicos.id", ondelete="CASCADE"),
        nullable=False
    )

    # 'autoevaluacion', 'examen_final', 'coevaluacion', etc.
    tipo_componente = db.Column(
        db.String(30),
        nullable=False
    )

    calificacion = db.Column(
        db.Numeric(4, 2),
        nullable=True
    )

    observacion = db.Column(
        db.Text,
        nullable=True
    )

    registrada_por = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=True
    )

    fecha_registro = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    fecha_actualizacion = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ── RELACIONES ORM (backref — crea automáticamente el inverso) ──

    estudiante = db.relationship(
        "Estudiante",
        backref="notas_componente",
        lazy=True
    )

    grupo_materia = db.relationship(
        "GrupoMateria",
        backref="notas_componente_estudiante",
        lazy=True
    )

    periodo_academico = db.relationship(
        "PeriodoAcademico",
        backref="notas_componente_estudiante",
        lazy=True
    )

    registrador = db.relationship(
        "Usuario",
        backref="notas_componente_registradas",
        lazy=True
    )

    def __repr__(self):
        return f"<NotaComponente {self.tipo_componente}: {self.calificacion}>"