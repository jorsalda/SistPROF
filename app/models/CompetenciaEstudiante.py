from app.extensions import db

class CompetenciaEstudiante(db.Model):
    __tablename__ = "competencias_materia"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(
        db.String(150),
        nullable=False
    )

    descripcion = db.Column(
        db.Text,
        nullable=True
    )

    porcentaje = db.Column(
        db.Float,
        default=0
    )

    # ✅ NUEVO: Código de competencia (ej. B2200, S5500)
    codigo = db.Column(
        db.String(30),
        nullable=True
    )

    # ✅ NUEVO: Nivel educativo para validación
    nivel_educativo = db.Column(
        db.String(50),
        nullable=True
    )

    materia_id = db.Column(
        db.Integer,
        db.ForeignKey("materias.id", ondelete="CASCADE"),
        nullable=False
    )

    # ✅ AGREGADO: Relación con el Grupo para filtrar por grado
    grupo_id = db.Column(
        db.Integer,
        db.ForeignKey("grupos.id", ondelete="SET NULL"),
        nullable=True
    )

    materia = db.relationship(
        "Materia",
        back_populates="competencias"
    )

    # ✅ AGREGADO: Relación con Grupo (opcional, útil para mostrar nombre del grupo)
    grupo = db.relationship(
        "Grupo",
        backref="competencias"
    )

    indicadores = db.relationship(
        "IndicadorLogro",
        back_populates="competencia",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<CompetenciaEstudiante {self.codigo or self.id}: {self.nombre}>"