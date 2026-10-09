from app.extensions import db
from datetime import datetime


class PermisoUsuario(db.Model):
    __tablename__ = "permisos_usuario"

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False
    )

    clave = db.Column(
        db.String(80),
        nullable=False
    )

    valor = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    creado_en = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    creado_por = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete="SET NULL"),
        nullable=True
    )

    __table_args__ = (
        db.UniqueConstraint(
            "usuario_id", "clave",
            name="permisos_usuario_usuario_clave_unico"
        ),
    )

    usuario = db.relationship(
        "Usuario",
        foreign_keys=[usuario_id],
        backref="permisos_asignados"
    )

    creador = db.relationship(
        "Usuario",
        foreign_keys=[creado_por],
        backref="permisos_otorgados"
    )

    def __repr__(self):
        return f"<PermisoUsuario usuario_id={self.usuario_id} clave={self.clave} valor={self.valor}>"