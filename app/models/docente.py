from app.extensions import db


class Docente(db.Model):
    __tablename__ = "docentes"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id"),
        nullable=False
    )

    # ⭐ NUEVOS CAMPOS
    documento = db.Column(db.String(20), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())

    # Relaciones
    permisos = db.relationship(
        "Permiso",
        backref="docente",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f'<Docente {self.nombre}>'