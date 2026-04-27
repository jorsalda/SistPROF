from app.extensions import db


class Sede(db.Model):
    __tablename__ = "sedes"
    __table_args__ = {'extend_existing': True}

    # ========== COLUMNAS ==========
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    direccion = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(30), nullable=True)
    activo = db.Column(db.Boolean, default=True)

    # ========== CLAVES FORÁNEAS ==========
    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id", ondelete="CASCADE"),
        nullable=False
    )

    # ========== RELACIONES ==========
    colegio = db.relationship(
        "Colegio",
        back_populates="sedes",
        lazy=True
    )

    # Estudiantes (relación bidireccional)
    estudiantes = db.relationship(
        "Estudiante",
        foreign_keys="Estudiante.sede_id",
        back_populates="sede",
        lazy=True
    )

    # Docentes (relación bidireccional - nombre único)
    docentes_sede = db.relationship(  # ← Nombre único para evitar conflicto
        "Docente",
        foreign_keys="Docente.sede_id",
        back_populates="sede",
        lazy=True
    )

    # Jornadas
    jornadas = db.relationship(
        "Jornada",
        back_populates="sede",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f'<Sede {self.nombre}>'