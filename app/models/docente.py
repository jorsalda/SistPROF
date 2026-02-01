from app.extensions import db

class Docente(db.Model):
    __tablename__ = "docentes"
    __table_args__ = {'extend_existing': True}  # 👈 AGREGA ESTA LÍNEA
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)

    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id"),
        nullable=False
    )

    permisos = db.relationship(
        "Permiso",
        backref="docente",
        cascade="all, delete-orphan"
    )
