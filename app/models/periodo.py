from app.extensions import db


class Periodo(db.Model):
    __tablename__ = "periodos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    anio_lectivo = db.Column(db.Integer, nullable=True)
    fecha_inicio = db.Column(db.Date, nullable=True)
    fecha_fin = db.Column(db.Date, nullable=True)
    activo = db.Column(db.Boolean, default=True)

    # ✅ CORRECCIÓN: Eliminar la relación 'evaluaciones' que causa colisión
    # con PeriodoAcademico. Si necesitas acceder a evaluaciones desde aquí,
    # hazlo mediante consultas explícitas o usa solo PeriodoAcademico.

    # evaluaciones = db.relationship( ... )  <-- ELIMINADO O COMENTADO

    def __repr__(self):
        return f"<Periodo {self.nombre}>"