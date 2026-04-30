from app.extensions import db
from datetime import datetime


class Docente(db.Model):
    __tablename__ = "docentes"
    __table_args__ = {'extend_existing': True}

    # ========== COLUMNAS ==========
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    documento = db.Column(db.String(20), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)

    # ========== CLAVES FORÁNEAS ==========
    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id"),
        nullable=False
    )
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=True,
        unique=True
    )
    sede_id = db.Column(
        db.Integer,
        db.ForeignKey("sedes.id", ondelete="RESTRICT"),
        nullable=True
    )

    # ========== RELACIONES ==========

    # Colegio
    colegio = db.relationship(
        "Colegio",
        foreign_keys=[colegio_id],
        back_populates="docentes",
        lazy=True
    )

    # Usuario
    usuario = db.relationship(
        "Usuario",
        foreign_keys=[usuario_id],
        lazy=True
    )

    # Sede
    sede = db.relationship(
        "Sede",
        foreign_keys=[sede_id],
        back_populates="docentes_sede",
        lazy=True
    )

    # Estudiantes tutelados
    estudiantes_tutelados = db.relationship(
        "Estudiante",
        foreign_keys="Estudiante.docente_id",
        back_populates="docente_tutor",
        lazy=True
    )

    # ⭐ NUEVO: Clases que imparte este docente
    clases = db.relationship(
        "Clase",
        foreign_keys="Clase.docente_id",
        back_populates="docente",
        lazy=True
    )

    # Permisos
    permisos = db.relationship(
        "Permiso",
        backref="docente",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f'<Docente {self.nombre}>'