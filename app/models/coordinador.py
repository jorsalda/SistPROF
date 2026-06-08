from app.extensions import db


class Coordinador(db.Model):
    __tablename__ = "coordinadores"

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    colegio_id = db.Column(db.Integer, nullable=False)

    sede_id = db.Column(db.Integer, nullable=False)

    # ✅ ESTE CAMPO YA EXISTE - NO SE DEBE QUITAR
    cargo = db.Column(db.String(100), nullable=True)

    # ✅ CAMPOS NUEVOS A AGREGAR
    documento = db.Column(db.String(20), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)

    __table_args__ = (
        db.ForeignKeyConstraint(["colegio_id"], ["colegios.id"]),
        db.ForeignKeyConstraint(
            ["sede_id", "colegio_id"],
            ["sedes.id", "sedes.colegio_id"]
        ),
    )

    # Relaciones
    usuario = db.relationship(
        "Usuario",
        backref=db.backref("coordinador", uselist=False)
    )

    colegio = db.relationship(
        "Colegio",
        backref=db.backref("coordinadores", lazy=True)
    )

    sede = db.relationship(
        "Sede",
        back_populates="coordinadores",
        overlaps="colegio,coordinadores"
    )

    def __repr__(self):
        return f"<Coordinador {self.id}>"