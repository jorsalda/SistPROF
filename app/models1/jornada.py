from app.extensions import db
from sqlalchemy import Time


class Jornada(db.Model):
    __tablename__ = "jornadas_colegio"
    __table_args__ = {'extend_existing': True}

    # ========== COLUMNAS ==========
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    hora_inicio = db.Column(Time, nullable=False)
    hora_fin = db.Column(Time, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    tolerancia_minutos = db.Column(db.Integer, default=0)

    # ========== CLAVES FORÁNEAS ==========
    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id", ondelete="CASCADE"),
        nullable=False
    )
    sede_id = db.Column(
        db.Integer,
        db.ForeignKey("sedes.id", ondelete="CASCADE"),
        nullable=True
    )

    # ========== RELACIONES ==========
    colegio = db.relationship(
        "Colegio",
        back_populates="jornadas",
        lazy=True
    )
    sede = db.relationship(
        "Sede",
        back_populates="jornadas",
        lazy=True
    )

    # Estudiantes
    estudiantes = db.relationship(
        "Estudiante",
        foreign_keys="Estudiante.jornada_id",
        back_populates="jornada",
        lazy=True
    )

    def __repr__(self):
        return f'<Jornada {self.nombre} ({self.hora_inicio} - {self.hora_fin})>'