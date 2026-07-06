from app.extensions import db


class PlanEstudios(db.Model):
    __tablename__ = "plan_estudios"

    id = db.Column(db.Integer, primary_key=True)

    colegio_id = db.Column(
        db.Integer,
        db.ForeignKey("colegios.id", ondelete="CASCADE"),
        nullable=False
    )

    grado = db.Column(
        db.String(20),
        nullable=False
    )

    materia_id = db.Column(
        db.Integer,
        db.ForeignKey("materias.id", ondelete="CASCADE"),
        nullable=False
    )

    horas_semanales = db.Column(
        db.Integer,
        nullable=False
    )

    activo = db.Column(
        db.Boolean,
        default=True
    )

    # Relaciones
    colegio = db.relationship("Colegio", backref="plan_estudios")
    materia = db.relationship("Materia", backref="plan_estudios")

    def __repr__(self):
        return f"<PlanEstudios {self.grado} - {self.materia.nombre}: {self.horas_semanales}h>"

    @classmethod
    def obtener_horas_materia(cls, colegio_id, grado, materia_nombre):
        """
        Método útil para obtener las horas requeridas de una materia
        Ejemplo: PlanEstudios.obtener_horas_materia(32, '6°', 'Matemáticas')
        """
        from sqlalchemy import func

        resultado = db.session.query(cls.horas_semanales).join(
            cls.materia
        ).filter(
            cls.colegio_id == colegio_id,
            cls.grado == grado,
            func.lower(cls.materia.nombre).like(f'%{materia_nombre.lower()}%')
        ).first()

        return resultado[0] if resultado else None