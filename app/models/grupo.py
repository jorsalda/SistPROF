from app.extensions import db
from datetime import datetime


class Grupo(db.Model):
    __tablename__ = "grupos"

    # =========================
    # COLUMNAS
    # =========================

    id = db.Column(db.Integer, primary_key=True)

    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id", ondelete="CASCADE"),
        nullable=False
    )

    sede_id = db.Column(
        db.Integer,
        db.ForeignKey("sedes.id", ondelete="RESTRICT"),
        nullable=False
    )

    jornada_id = db.Column(
        db.Integer,
        db.ForeignKey("jornadas_colegio.id", ondelete="RESTRICT"),
        nullable=False
    )

    anio_lectivo = db.Column(
        db.Integer,
        nullable=False
    )

    grado = db.Column(
        db.String(30),
        nullable=False
    )

    nombre = db.Column(
        db.String(10),
        nullable=False
    )

    director_docente_id = db.Column(
        db.Integer,
        db.ForeignKey("docentes.id", ondelete="SET NULL"),
        nullable=True
    )

    capacidad_maxima = db.Column(
        db.Integer,
        default=40
    )

    activo = db.Column(
        db.Boolean,
        default=True
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.now
    )

    # =========================
    # RELACIONES
    # =========================

    colegio = db.relationship(
        "Colegio",
        backref="grupos",
        lazy=True
    )

    sede = db.relationship(
        "Sede",
        backref="grupos",
        lazy=True
    )

    jornada = db.relationship(
        "Jornada",
        backref="grupos",
        lazy=True
    )

    director = db.relationship(
        "Docente",
        foreign_keys=[director_docente_id],
        lazy=True
    )

    estudiantes = db.relationship(
        "Estudiante",
        back_populates="grupo_rel",
        lazy=True
    )

    # =========================
    # REPRESENTACIÓN
    # =========================

    def __repr__(self):
        return f"<Grupo {self.grado} {self.nombre}>"