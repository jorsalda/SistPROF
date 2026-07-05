from app.extensions import db
from datetime import datetime


class JornadaBloque(db.Model):
    __tablename__ = "jornada_bloques"

    id = db.Column(db.Integer, primary_key=True)

    jornada_id = db.Column(
        db.Integer,
        db.ForeignKey("jornadas_colegio.id", ondelete="CASCADE"),
        nullable=False
    )

    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)

    tipo = db.Column(
        db.String(20),
        nullable=False
    )  # 'clase' o 'descanso'

    nombre = db.Column(db.String(50))

    orden = db.Column(db.Integer, nullable=False)

    activo = db.Column(db.Boolean, default=True)

    # Relación con jornada
    jornada = db.relationship(
        "Jornada",
        backref="bloques"
    )

    def __repr__(self):
        return f"<JornadaBloque {self.nombre} - {self.hora_inicio} a {self.hora_fin}>"

    @property
    def duracion_minutos(self):
        if self.hora_inicio and self.hora_fin:
            # Convertir time a datetime para poder restarlos
            hoy = datetime.today().date()
            inicio_dt = datetime.combine(hoy, self.hora_inicio)
            fin_dt = datetime.combine(hoy, self.hora_fin)
            diferencia = fin_dt - inicio_dt
            return int(diferencia.total_seconds() / 60)
        return 0