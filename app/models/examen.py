# models/examen.py
from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB


class Examen(db.Model):
    __tablename__ = "examenes"

    id = db.Column(db.Integer, primary_key=True)

    # ✅ Título visible para estudiantes y docentes
    titulo = db.Column(
        db.String(200),
        nullable=False
    )

    # ✅ Nombre interno (puede ser igual al título o un identificador)
    nombre = db.Column(
        db.String(200),
        nullable=True
    )

    descripcion = db.Column(db.Text)

    tiempo_limite_minutos = db.Column(db.Integer, default=60)

    activo = db.Column(db.Boolean, default=True)

    # ✅ CAMPO PARA BORRADO LÓGICO (UBICADO CORRECTAMENTE DENTRO DE LA CLASE)
    eliminado = db.Column(db.Boolean, default=False)

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    materia_id = db.Column(
        db.Integer,
        db.ForeignKey("materias.id", ondelete="CASCADE"),
        nullable=False
    )

    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id", ondelete="CASCADE"),
        nullable=False
    )

    archivo_json = db.Column(db.String(200))

    contenido_json = db.Column(JSONB)

    tipo_examen_id = db.Column(
        db.Integer,
        db.ForeignKey("tipo_examen.id"),
        nullable=True
    )

    # Relaciones
    materia = db.relationship(
        "Materia",
        backref="examenes"
    )

    colegio = db.relationship(
        "Colegio",
        backref="examenes"
    )

    tipo_examen = db.relationship(
        "TipoExamen",
        backref="examenes",
        lazy=True
    )

    def __repr__(self):
        return f"<Examen {self.titulo}>"


class ProgramacionExamen(db.Model):
    __tablename__ = 'programacion_examenes'

    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey('examenes.id'), nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=False)
    fecha_apertura = db.Column(db.DateTime, nullable=False)
    fecha_cierre = db.Column(db.DateTime, nullable=False)
    activo = db.Column(db.Boolean, default=True)

    # ✅ NOTA: Se eliminó 'eliminado' de aquí porque pertenece a Examen

    # Relaciones
    examen = db.relationship('Examen', backref='programaciones')
    grupo = db.relationship('Grupo', backref='programaciones_examen')