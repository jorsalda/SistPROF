from app.extensions import db
from datetime import datetime


class Acudiente(db.Model):
    __tablename__ = "acudientes"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=True)

    # ✅ CAMPO AGREGADO: Documento de identidad
    documento = db.Column(db.String(20), unique=True, nullable=False)

    telefono = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    parentesco = db.Column(db.String(50), nullable=True)

    # Relación con colegio
    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id", ondelete="SET NULL"),
        nullable=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete="SET NULL"),
        nullable=True,
        unique=True
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    usuario = db.relationship("Usuario", foreign_keys=[usuario_id], lazy=True)
    colegio = db.relationship("Colegio", foreign_keys=[colegio_id], lazy=True)

    # Relación con estudiantes a través de la tabla intermedia
    estudiantes = db.relationship(
        "Estudiante",
        secondary="estudiante_acudiente",
        back_populates="acudientes",
        lazy=True
    )

    @property
    def nombre_completo(self):
        """Retorna el nombre completo combinando nombre y apellido"""
        if self.apellido:
            return f"{self.nombre} {self.apellido}"
        return self.nombre

    def __repr__(self):
        return f'<Acudiente {self.nombre_completo}>'