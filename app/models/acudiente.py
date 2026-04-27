from app.extensions import db


class Acudiente(db.Model):
    __tablename__ = "acudientes"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    parentesco = db.Column(db.String(50), nullable=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete="SET NULL"),
        nullable=True,
        unique=True
    )

    # Relaciones
    usuario = db.relationship("Usuario", foreign_keys=[usuario_id], lazy=True)

    def __repr__(self):
        return f'<Acudiente {self.nombre}>'