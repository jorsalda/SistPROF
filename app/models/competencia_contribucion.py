from app.extensions import db

competencia_contribucion = db.Table(
    "competencia_contribucion",

    db.Column(
        "competencia_id",
        db.Integer,
        db.ForeignKey("competencias.id", ondelete="CASCADE"),
        primary_key=True
    ),

    db.Column(
        "contribucion_id",
        db.Integer,
        db.ForeignKey("contribuciones.id", ondelete="CASCADE"),
        primary_key=True
    )
)