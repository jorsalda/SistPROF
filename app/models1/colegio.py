from app.extensions import db


class Colegio(db.Model):
    __tablename__ = "colegios"
    __table_args__ = {'extend_existing': True}

    # ========== COLUMNAS ==========
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    codigo_acceso = db.Column(db.String(20), unique=True, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    en_prueba = db.Column(db.Boolean, default=True)
    fecha_expiracion = db.Column(db.DateTime, nullable=True)

    # ========== RELACIONES ==========

    # Usuarios
    usuarios = db.relationship(
        "Usuario",
        back_populates="colegio",
        lazy=True
    )

    # Docentes
    docentes = db.relationship(
        "Docente",
        foreign_keys="Docente.colegio_id",
        back_populates="colegio",
        lazy=True
    )

    # Estudiantes
    estudiantes = db.relationship(
        "Estudiante",
        foreign_keys="Estudiante.colegio_id",
        back_populates="colegio",
        lazy=True
    )

    # Sedes
    sedes = db.relationship(
        "Sede",
        back_populates="colegio",
        cascade="all, delete-orphan",
        lazy=True
    )

    # Jornadas
    jornadas = db.relationship(
        "Jornada",
        back_populates="colegio",
        cascade="all, delete-orphan",
        lazy=True
    )

    # ⭐ NUEVO: Clases del colegio (nombre único para evitar conflicto)
    clases_colegio = db.relationship(  # ← Nombre único
        "Clase",
        foreign_keys="Clase.colegio_id",
        back_populates="colegio",
        lazy=True
    )

    def __repr__(self):
        return f'<Colegio {self.nombre}>'