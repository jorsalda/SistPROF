from app.extensions import db
from flask_login import UserMixin
from datetime import datetime


class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"
    __table_args__ = {'extend_existing': True}  # ← Agrega SOLO esta línea
    # --------------------
    # Datos básicos
    # --------------------
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(256),
        nullable=False
    )

    nombre = db.Column(
        db.String(100),
        nullable=True
    )

    failed_attempts = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    locked_until = db.Column(
        db.DateTime,
        nullable=True
    )

    # --------------------
    # Relaciones institucionales
    # --------------------

    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey('colegios.id'),
        nullable=True
    )

    colegio = db.relationship(
        'Colegio',
        back_populates='usuarios',
        lazy=True
    )

    # ✅ Sede del usuario
    sede_id = db.Column(
        db.Integer,
        db.ForeignKey('sedes.id'),
        nullable=True
    )

    sede = db.relationship(
        'Sede',
        backref='usuarios'
    )

    # --------------------
    # Control de acceso
    # --------------------

    rol = db.Column(
        db.Enum(
            'superadmin',
            'admin_colegio',
            'coordinador',  # <--- DEBE DECIR SOLO 'coordinador'
            'docente',
            'estudiante',
            'acudiente',
            name='rol_usuario'
        ),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    is_approved = db.Column(
        db.Boolean,
        default=False
    )

    # --------------------
    # Compatibilidad
    # --------------------

    @property
    def is_superadmin(self):
        return self.rol == 'superadmin'

    @property
    def es_admin_colegio(self):
        return self.rol == 'admin_colegio'

    @property
    def es_coordinador(self):
        return self.rol == 'coordinador'

    @property
    def es_docente(self):
        return self.rol == 'docente'

    @property
    def es_estudiante(self):
        return self.rol == 'estudiante'

    @property
    def es_acudiente(self):
        return self.rol == 'acudiente'

    # --------------------
    # Fechas y prueba
    # --------------------

    fecha_registro = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    fecha_aprobacion = db.Column(
        db.DateTime,
        nullable=True
    )

    dias_prueba = db.Column(
        db.Integer,
        default=15
    )

    fecha_expiracion = db.Column(
        db.DateTime,
        nullable=True
    )

    # --------------------
    # Representación
    # --------------------

    def __repr__(self):
        return f'<Usuario {self.email}>'

    # --------------------
    # Lógica de acceso
    # --------------------

    def puede_acceder(self):
        """
        Verifica si el usuario puede acceder al sistema
        Retorna:
            (bool, mensaje)
        """

        # Usuario desactivado
        if not self.is_active:
            return False, "Usuario desactivado por el administrador"

        # Superadmin siempre accede
        if self.is_superadmin:
            return True, "Superadmin"

        # Usuario aprobado
        if self.is_approved:
            return True, "Aprobado"

        # Control por fecha explícita
        if self.fecha_expiracion:

            if datetime.utcnow() <= self.fecha_expiracion:

                dias = (
                    self.fecha_expiracion - datetime.utcnow()
                ).days

                return True, f"Prueba ({dias} días restantes)"

            return False, "Prueba vencida"

        # Compatibilidad por días de prueba
        dias_prueba = (
            self.dias_prueba
            if self.dias_prueba
            else 15
        )

        dias_transcurridos = (
            datetime.utcnow() - self.fecha_registro
        ).days

        dias_restantes = (
            dias_prueba - dias_transcurridos
        )

        if dias_restantes >= 0:
            return True, f"Prueba ({dias_restantes} días restantes)"

        return False, "Bloqueado - Prueba terminada sin aprobación"

    # --------------------
    # Estado legible para UI
    # --------------------

    def estado_detallado(self):

        if not self.is_active:
            return "🚫 Usuario desactivado"

        if self.is_superadmin:
            return "👑 Superadministrador"

        if self.is_approved:

            dias = (
                datetime.utcnow() - self.fecha_aprobacion
            ).days

            return f"✅ Aprobado (hace {dias} días)"

        if self.fecha_expiracion:

            dias = (
                self.fecha_expiracion - datetime.utcnow()
            ).days

            if dias >= 0:
                return f"⏳ En prueba ({dias} días restantes)"

            return "❌ Prueba vencida"

        dias_prueba = (
            self.dias_prueba
            if self.dias_prueba
            else 15
        )

        dias_transcurridos = (
            datetime.utcnow() - self.fecha_registro
        ).days

        dias_restantes = (
            dias_prueba - dias_transcurridos
        )

        if dias_restantes >= 0:
            return f"⏳ En prueba ({dias_restantes} días restantes)"

        return "❌ Bloqueado - Prueba vencida"