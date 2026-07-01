from app.extensions import db
from datetime import datetime


class Grupo(db.Model):
    __tablename__ = "grupos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(10), nullable=False)  # "A", "B", "C"
    grado = db.Column(db.String(20), nullable=False)  # "6", "7", "10", "11"

    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id"),
        nullable=False
    )

    sede_id = db.Column(
        db.Integer,
        db.ForeignKey("sedes.id"),
        nullable=False
    )

    jornada_id = db.Column(
        db.Integer,
        db.ForeignKey("jornadas_colegio.id"),
        nullable=False
    )

    director_docente_id = db.Column(
        db.Integer,
        db.ForeignKey("docentes.id"),
        nullable=True
    )

    capacidad_maxima = db.Column(db.Integer, default=40)
    anio_lectivo = db.Column(db.Integer, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # =====================================================
    # RELACIONES
    # =====================================================

    colegio = db.relationship("Colegio", backref="grupos")
    sede = db.relationship("Sede", backref="grupos")
    jornada = db.relationship("Jornada", backref="grupos")
    director = db.relationship("Docente", backref="grupos_dirigidos")

    # Relación con tabla intermedia GrupoAreas
    asignaciones_areas = db.relationship(
        "GrupoAreas",
        back_populates="grupo",
        cascade="all, delete-orphan",
        lazy=True,
        overlaps="grupos"
    )
    # Relación M:N directa con áreas
    areas = db.relationship(
        "AreaGestion",
        secondary="grupo_areas",
        back_populates="grupos",
        lazy=True,
        overlaps="asignaciones_areas,grupo,asignaciones_grupos,area"
    )

    # Estudiantes
    estudiantes = db.relationship(
        "Estudiante",
        back_populates="grupo_rel",
        lazy=True
    )

    def __repr__(self):
        return (
            f"<Grupo {self.grado}{self.nombre} - "
            f"{self.sede.nombre if self.sede else 'Sin Sede'}>"
        )


class GrupoAreas(db.Model):
    """Tabla intermedia: Grupo ↔ Área"""

    __tablename__ = "grupo_areas"

    id = db.Column(db.Integer, primary_key=True)

    grupo_id = db.Column(
        db.Integer,
        db.ForeignKey("grupos.id", ondelete="CASCADE"),
        nullable=False
    )

    area_id = db.Column(
        db.Integer,
        db.ForeignKey("areas_gestion.id", ondelete="CASCADE"),
        nullable=False
    )

    docente_id = db.Column(
        db.Integer,
        db.ForeignKey("docentes.id", ondelete="SET NULL"),
        nullable=True
    )

    horario = db.Column(db.String(100), nullable=True)
    salon = db.Column(db.String(50), nullable=True)
    activo = db.Column(db.Boolean, default=True)

    fecha_asignacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # =====================================================
    # RELACIONES
    # =====================================================

    grupo = db.relationship(
        "Grupo",
        back_populates="asignaciones_areas",
        overlaps="areas,grupos"
    )

    area = db.relationship(
        "AreaGestion",
        back_populates="asignaciones_grupos",
        overlaps="grupos"
    )

    docente = db.relationship(
        "Docente",
        backref="asignaciones_areas_grupo"
    )



    def __repr__(self):
        return f"<GrupoAreas Grupo={self.grupo_id} Area={self.area_id}>"


class DirectoresGrupo(db.Model):
    """Historial de directores de grupo"""

    __tablename__ = "directores_grupo"

    id = db.Column(db.Integer, primary_key=True)

    grupo_id = db.Column(
        db.Integer,
        db.ForeignKey("grupos.id", ondelete="CASCADE"),
        nullable=False
    )

    docente_id = db.Column(
        db.Integer,
        db.ForeignKey("docentes.id", ondelete="CASCADE"),
        nullable=False
    )

    fecha_inicio = db.Column(
        db.Date,
        nullable=False,
        default=datetime.utcnow().date
    )

    fecha_fin = db.Column(
        db.Date,
        nullable=True
    )

    activo = db.Column(
        db.Boolean,
        default=True
    )

    grupo = db.relationship(
        "Grupo",
        backref="historial_directores"
    )

    docente = db.relationship(
        "Docente",
        backref="historial_direccion"
    )

    def __repr__(self):
        return (
            f"<DirectoresGrupo Grupo={self.grupo_id} "
            f"Docente={self.docente_id}>"
        )

class FusionGrupo(db.Model):
    """
    Historial de fusiones de grupos
    """

    __tablename__ = "fusion_grupos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    grupo_origen_id = db.Column(
        db.Integer,
        db.ForeignKey("grupos.id"),
        nullable=False
    )

    grupo_destino_id = db.Column(
        db.Integer,
        db.ForeignKey("grupos.id"),
        nullable=False
    )

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    observacion = db.Column(
        db.Text
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=True
    )

    grupo_origen = db.relationship(
        "Grupo",
        foreign_keys=[grupo_origen_id]
    )

    grupo_destino = db.relationship(
        "Grupo",
        foreign_keys=[grupo_destino_id]
    )

    usuario = db.relationship(
        "Usuario"
    )

    def __repr__(self):
        return (
            f"<FusionGrupo "
            f"{self.grupo_origen_id} -> "
            f"{self.grupo_destino_id}>"
        )