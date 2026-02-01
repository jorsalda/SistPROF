from app.extensions import db


class Permiso(db.Model):
    __tablename__ = "permisos"
    __table_args__ = {'extend_existing': True}  # 👈 AGREGA ESTA LÍNEA

    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey("docentes.id"), nullable=False)

    # ⭐⭐ AÑADE ESTA LÍNEA ⭐⭐
    colegio_id = db.Column(db.Integer, db.ForeignKey("colegios.id"), nullable=False)

    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    observacion = db.Column(db.Text)

    # Relaciones (opcional, si las necesitas)
    # docente = db.relationship("Docente", backref="permisos")
    # colegio = db.relationship("Colegio", backref="permisos")