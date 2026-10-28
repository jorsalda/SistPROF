from datetime import date
from app.extensions import db


class PIAR(db.Model):
    __tablename__ = "piar"
    __table_args__ = (
        db.Index(
            'unico_piar_activo_por_materia',
            'estudiante_id', 'docente_id', 'materia_id',
            unique=True,
            postgresql_where=db.text('activo = true')
        ),
        {'extend_existing': True}
    )

    id = db.Column(db.Integer, primary_key=True)

    # =====================================================
    # CAMPOS DEL PIAR (DECRETO 1421)
    # =====================================================

    diagnostico = db.Column(
        db.Text,
        nullable=True
    )

    contexto_familiar = db.Column(
        db.Text,
        nullable=True
    )

    entidades_apoyo = db.Column(
        db.Text,
        nullable=True
    )

    objetivos = db.Column(
        db.Text,
        nullable=True
    )

    acta_acuerdo = db.Column(
        db.Text,
        nullable=True
    )

    informe_anual = db.Column(
        db.Text,
        nullable=True
    )

    # =====================================================
    # FECHAS Y ESTADO
    # =====================================================

    fecha_inicio = db.Column(
        db.Date,
        default=date.today,
        nullable=False
    )

    fecha_fin = db.Column(
        db.Date,
        nullable=True
    )

    activo = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    # =====================================================
    # LLAVES FORÁNEAS
    # =====================================================

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False
    )

    docente_id = db.Column(
        db.Integer,
        db.ForeignKey("docentes.id", ondelete="CASCADE"),
        nullable=True
    )

    materia_id = db.Column(
        db.Integer,
        db.ForeignKey("materias.id", ondelete="CASCADE"),
        nullable=True
    )

    # =====================================================
    # RELACIONES
    # =====================================================

    estudiante = db.relationship(
        "Estudiante",
        backref=db.backref(
            "piares",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    docente = db.relationship(
        "Docente",
        backref=db.backref(
            "piares",
            lazy=True
        )
    )

    materia = db.relationship(
        "Materia",
        backref=db.backref(
            "piares",
            lazy=True
        )
    )

    ajustes_razonables = db.relationship(
        "AjusteRazonable",
        backref="piar",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # Relación con profesionales del PIAR
    profesionales = db.relationship(
        "PiarProfesional",
        backref="piar",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        estado = "Activo" if self.activo else "Inactivo"
        return f"<PIAR {self.estudiante_id} - {estado}>"