from app.extensions import db

class Colegio(db.Model):
    __tablename__ = "colegios"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)

    docentes = db.relationship("Docente", backref="colegio", lazy=True)
