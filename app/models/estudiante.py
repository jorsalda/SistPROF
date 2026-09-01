from app.extensions import db
from datetime import datetime
import secrets


class Estudiante(db.Model):
    __tablename__ = "estudiantes"
    __table_args__ = {'extend_existing': True}

    # =====================================================
    # COLUMNAS
    # =====================================================

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(
        db.String(150),
        nullable=False
    )

    apellido = db.Column(
        db.String(150),
        nullable=False,
        default=""
    )
    tipo_documento = db.Column(
        db.String(20),
        nullable=True,
        default='TI'
    )
    documento = db.Column(
        db.String(20),
        unique=True,
        nullable=True
    )
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=True
    )
    # Compatibilidad temporal
    grado = db.Column(
        db.String(20),
        nullable=True
    )

    grupo = db.Column(
        db.String(20),
        nullable=True
    )

    # NUEVO CAMPO RELACIONAL
    grupo_id = db.Column(
        db.Integer,
        db.ForeignKey("grupos.id", ondelete="SET NULL"),
        nullable=True
    )

    # =====================================================
    # DATOS PERSONALES
    # =====================================================

    direccion = db.Column(
        db.String(255),
        nullable=False
    )

    telefono = db.Column(
        db.String(20),
        nullable=False
    )

    # =====================================================
    # ACUDIENTE PRINCIPAL
    # =====================================================

    acudiente_principal_id = db.Column(
        db.Integer,
        db.ForeignKey("acudientes.id", ondelete="RESTRICT"),
        nullable=False
    )

    # =====================================================
    # CLAVES FORÁNEAS
    # =====================================================

    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id", ondelete="CASCADE"),
        nullable=False
    )

    # ✅ AJUSTE 1: docente_id ahora es NULL y flexible
    docente_id = db.Column(
        db.Integer,
        db.ForeignKey("docentes.id", ondelete="SET NULL"),
        nullable=True  # ✅ CAMBIADO: Ahora es NULL
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

    # =====================================================
    # ESTADO
    # =====================================================

    activo = db.Column(
        db.Boolean,
        default=True
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.now
    )

    qr_token = db.Column(
        db.String(80),
        unique=True,
        nullable=True
    )

    # =====================================================
    # RELACIONES
    # =====================================================

    # Acudiente principal
    acudiente_principal = db.relationship(
        "Acudiente",
        foreign_keys=[acudiente_principal_id],
        lazy=True
    )

    # ✅ AJUSTE 2: Relación muchos-a-muchos con acudientes adicionales
    acudientes = db.relationship(
        "Acudiente",
        secondary="estudiante_acudiente",
        back_populates="estudiantes",
        lazy=True
    )

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

    # Grupo
    grupo_rel = db.relationship(
        "Grupo",
        foreign_keys=[grupo_id],
        back_populates="estudiantes",
        lazy=True
    )

    # Resultados exámenes
    resultados_examenes = db.relationship(
        "ResultadoExamen",
        back_populates="estudiante",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # Evaluaciones
    evaluaciones = db.relationship(
        "EvaluacionEstudiante",
        back_populates="estudiante",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # Clases matriculadas
    clases_matriculadas = db.relationship(
        "ClaseEstudiante",
        back_populates="estudiante",
        cascade="all, delete-orphan",
        lazy=True
    )

    # =====================================================
    # MÉTODOS
    # =====================================================

    def generar_qr_token(self):
        self.qr_token = secrets.token_urlsafe(32)
        return self.qr_token

    # ✅ AJUSTE 3: Método para actualizar datos automáticamente
    def actualizar_datos_grupo(self):
        """Actualiza automáticamente grado, grupo, sede, jornada
        basado en el grupo seleccionado"""
        if self.grupo_rel:
            self.grado = self.grupo_rel.grado
            self.grupo = self.grupo_rel.nombre
            self.sede_id = self.grupo_rel.sede_id
            self.jornada_id = self.grupo_rel.jornada_id
            self.colegio_id = self.grupo_rel.colegio_id

    def tiene_piar_activo(self):
        return False

    # =====================================================
    # REPRESENTACIÓN
    # =====================================================

    def __repr__(self):
        return (
            f"<Estudiante "
            f"{self.apellido}, {self.nombre} "
            f"- {self.grado}{self.grupo or ''}>"
        )

