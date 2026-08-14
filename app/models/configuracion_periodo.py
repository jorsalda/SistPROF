# app/models/configuracion_periodo.py

from app.extensions import db  # Ajusta según cómo importes db en tu proyecto
from datetime import datetime


class ConfiguracionPeriodo(db.Model):
    __tablename__ = 'configuracion_periodo'

    id = db.Column(db.Integer, primary_key=True)
    colegio_id = db.Column(db.Integer, db.ForeignKey('colegios.id', ondelete='CASCADE'), nullable=False)
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodos_academicos.id', ondelete='CASCADE'), nullable=False)
    estado = db.Column(db.String(20), default='CERRADO')  # ABIERTO, CERRADO, SOLO_CONSULTA
    fecha_apertura = db.Column(db.DateTime, nullable=True)
    fecha_cierre = db.Column(db.DateTime, nullable=True)
    permite_editar_competencias = db.Column(db.Boolean, default=False)
    permite_editar_notas = db.Column(db.Boolean, default=False)
    creado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    colegio = db.relationship('Colegio', backref='configuraciones_periodo')
    periodo = db.relationship('PeriodoAcademico', backref='configuracion')
    creador = db.relationship('Usuario', foreign_keys=[creado_por])

    def __repr__(self):
        return f'<ConfiguracionPeriodo {self.estado} - Periodo {self.periodo_id}>'