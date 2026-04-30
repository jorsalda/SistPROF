from app.extensions import db
from datetime import datetime


class Estudiante(db.Model):
    __tablename__ = "estudiantes"
    __table_args__ = {'extend_existing': True}

    # ========== COLUMNAS ==========
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    grado = db.Column(db.String(20), nullable=True)
    grupo = db.Column(db.String(20), nullable=True)

    # ========== CLAVES FORÁNEAS ==========
    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id", ondelete="CASCADE"),
        nullable=False
    )

    docente_id = db.Column(
        db.Integer,
        db.ForeignKey("docentes.id", ondelete="RESTRICT"),
        nullable=False
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete="SET NULL"),
        nullable=True,
        unique=True
    )

    sede_id = db.Column(
        db.Integer,
        db.ForeignKey("sedes.id", ondelete="RESTRICT"),
        nullable=True
    )

    jornada_id = db.Column(
        db.Integer,
        db.ForeignKey("jornadas_colegio.id", ondelete="RESTRICT"),
        nullable=False
    )

    institucion_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id"),
        nullable=True
    )

    # ========== ESTADO Y TOKEN ==========
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    qr_token = db.Column(db.String(80), unique=True, nullable=True)

    # ========== RELACIONES ==========

    # Colegio
    colegio = db.relationship(
        "Colegio",
        foreign_keys=[colegio_id],
        back_populates="estudiantes",
        lazy=True
    )

    # Docente tutor
    docente_tutor = db.relationship(
        "Docente",
        foreign_keys=[docente_id],
        back_populates="estudiantes_tutelados",
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
        back_populates="estudiantes",
        lazy=True
    )

    # Jornada
    jornada = db.relationship(
        "Jornada",
        foreign_keys=[jornada_id],
        back_populates="estudiantes",
        lazy=True
    )

    # Resultados de exámenes
    resultados_examenes = db.relationship(
        "ResultadoExamen",
        back_populates="estudiante",
        lazy=True
    )

    # Clases matriculadas (tabla intermedia)
    clases_matriculadas = db.relationship(
        "ClaseEstudiante",
        back_populates="estudiante",
        cascade="all, delete-orphan",
        lazy=True
    )

    # ========== MÉTODOS ==========

    def generar_qr_token(self):
        import secrets
        self.qr_token = secrets.token_urlsafe(32)
        return self.qr_token

    def __repr__(self):
        return f'<Estudiante {self.nombre} - {self.grado}{self.grupo or ""}>'