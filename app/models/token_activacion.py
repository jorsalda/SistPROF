from app.extensions import db
from datetime import datetime
import secrets


class TokenActivacion(db.Model):
    __tablename__ = "tokens_activacion"

    id = db.Column(db.Integer, primary_key=True)

    token = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        default=lambda: secrets.token_urlsafe(32)
    )

    usado = db.Column(
        db.Boolean,
        default=False
    )

    fecha_expiracion = db.Column(
        db.DateTime,
        nullable=False
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False
    )

    usuario = db.relationship(
        "Usuario",
        backref="tokens_activacion"
    )

    def __repr__(self):
        return f"<TokenActivacion {self.id}>"