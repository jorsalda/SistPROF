from typing import Optional
import datetime
import decimal
import enum

from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, Enum, ForeignKeyConstraint, Index, Integer, Numeric, PrimaryKeyConstraint, String, Text, Time, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class DiaSemana(str, enum.Enum):
    LUNES = 'lunes'
    MARTES = 'martes'
    MIERCOLES = 'miercoles'
    JUEVES = 'jueves'
    VIERNES = 'viernes'


class NivelDesempeno(str, enum.Enum):
    BAJO = 'Bajo'
    BASICO = 'Basico'
    ALTO = 'Alto'
    SUPERIOR = 'Superior'


class RolUsuario(str, enum.Enum):
    SUPERADMIN = 'superadmin'
    ADMIN_COLEGIO = 'admin_colegio'
    DOCENTE = 'docente'
    ESTUDIANTE = 'estudiante'
    ACUDIENTE = 'acudiente'


class TipoEventoColegio(str, enum.Enum):
    INGRESO = 'ingreso'
    SALIDA = 'salida'


class TipoGravedad(str, enum.Enum):
    TIPO_1 = 'Tipo 1'
    TIPO_2 = 'Tipo 2'
    TIPO_3 = 'Tipo 3'


class TipoNovedadEnum(str, enum.Enum):
    DISCIPLINA = 'DISCIPLINA'
    ACADEMICO = 'ACADEMICO'
    LLEGADA_TARDE = 'LLEGADA_TARDE'


class Colegios(Base):
    __tablename__ = 'colegios'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='colegios_pkey'),
        UniqueConstraint('codigo_acceso', name='colegios_codigo_acceso_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    codigo_acceso: Mapped[str] = mapped_column(String(20), nullable=False)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    fecha_expiracion: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("(now() + '15 days'::interval)"))
    en_prueba: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    areas_gestion: Mapped[list['AreasGestion']] = relationship('AreasGestion', back_populates='colegio')
    configuracion_escalamiento: Mapped['ConfiguracionEscalamiento'] = relationship('ConfiguracionEscalamiento', uselist=False, back_populates='institucion')
    jornadas_colegio: Mapped[list['JornadasColegio']] = relationship('JornadasColegio', back_populates='colegio')
    periodos_academicos: Mapped[list['PeriodosAcademicos']] = relationship('PeriodosAcademicos', back_populates='colegio')
    sedes: Mapped[list['Sedes']] = relationship('Sedes', back_populates='colegio')
    suscripciones: Mapped['Suscripciones'] = relationship('Suscripciones', uselist=False, back_populates='colegio')
    usuarios: Mapped[list['Usuarios']] = relationship('Usuarios', back_populates='colegio')
    docentes: Mapped[list['Docentes']] = relationship('Docentes', back_populates='colegio')
    acuerdos_evaluacion: Mapped[list['AcuerdosEvaluacion']] = relationship('AcuerdosEvaluacion', back_populates='colegio')
    estudiantes: Mapped[list['Estudiantes']] = relationship('Estudiantes', back_populates='colegio')
    permisos: Mapped[list['Permisos']] = relationship('Permisos', back_populates='colegio')
    ingresos_colegio: Mapped[list['IngresosColegio']] = relationship('IngresosColegio', back_populates='colegio')


class ConfiguracionDisciplinaria(Base):
    __tablename__ = 'configuracion_disciplinaria'
    __table_args__ = (
        CheckConstraint('cantidad_para_citacion > 0', name='configuracion_disciplinaria_cantidad_para_citacion_check'),
        PrimaryKeyConstraint('id', name='configuracion_disciplinaria_pkey'),
        UniqueConstraint('tipo_novedad', name='configuracion_disciplinaria_tipo_novedad_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo_novedad: Mapped[str] = mapped_column(String(20), nullable=False)
    cantidad_para_citacion: Mapped[int] = mapped_column(Integer, nullable=False)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))


class EscalaEvaluacion(Base):
    __tablename__ = 'escala_evaluacion'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='escala_evaluacion_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(20), nullable=False)
    nota_min: Mapped[decimal.Decimal] = mapped_column(Numeric(3, 2), nullable=False)
    nota_max: Mapped[decimal.Decimal] = mapped_column(Numeric(3, 2), nullable=False)


class Materias(Base):
    __tablename__ = 'materias'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='materias_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)

    competencias_materia: Mapped[list['CompetenciasMateria']] = relationship('CompetenciasMateria', back_populates='materia')
    clases: Mapped[list['Clases']] = relationship('Clases', back_populates='materia_')


class ResultadosExamen(Base):
    __tablename__ = 'resultados_examen'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='resultados_examen_pkey'),
        UniqueConstraint('estudiante_id', 'examen_id', name='resultado_unico_estudiante_examen')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    estudiante_id: Mapped[int] = mapped_column(Integer, nullable=False)
    examen_id: Mapped[int] = mapped_column(Integer, nullable=False)
    materia_id: Mapped[int] = mapped_column(Integer, nullable=False)
    nota_numerica: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(3, 2))
    nivel: Mapped[Optional[NivelDesempeno]] = mapped_column(Enum(NivelDesempeno, values_callable=lambda cls: [member.value for member in cls], name='nivel_desempeno'))
    fecha: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))


class AreasGestion(Base):
    __tablename__ = 'areas_gestion'
    __table_args__ = (
        CheckConstraint('porcentaje > 0::numeric AND porcentaje <= 100::numeric', name='porcentaje_valido'),
        ForeignKeyConstraint(['colegio_id'], ['colegios.id'], ondelete='CASCADE', name='fk_area_colegio'),
        PrimaryKeyConstraint('id', name='areas_gestion_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    colegio_id: Mapped[int] = mapped_column(Integer, nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    porcentaje: Mapped[decimal.Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    fecha_creacion: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    colegio: Mapped['Colegios'] = relationship('Colegios', back_populates='areas_gestion')
    competencias: Mapped[list['Competencias']] = relationship('Competencias', back_populates='area')


class CompetenciasMateria(Base):
    __tablename__ = 'competencias_materia'
    __table_args__ = (
        ForeignKeyConstraint(['materia_id'], ['materias.id'], name='competencias_materia_materia_id_fkey'),
        PrimaryKeyConstraint('id', name='competencias_materia_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    materia_id: Mapped[int] = mapped_column(Integer, nullable=False)
    nombre: Mapped[Optional[str]] = mapped_column(String(150))
    porcentaje: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))

    materia: Mapped['Materias'] = relationship('Materias', back_populates='competencias_materia')
    indicadores_logro: Mapped[list['IndicadoresLogro']] = relationship('IndicadoresLogro', back_populates='competencia_materia')


class ConfiguracionEscalamiento(Base):
    __tablename__ = 'configuracion_escalamiento'
    __table_args__ = (
        ForeignKeyConstraint(['institucion_id'], ['colegios.id'], ondelete='CASCADE', name='fk_config_escalamiento_colegio'),
        PrimaryKeyConstraint('id', name='configuracion_escalamiento_pkey'),
        UniqueConstraint('institucion_id', name='unique_institucion')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    institucion_id: Mapped[int] = mapped_column(Integer, nullable=False)
    usar_tiempo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    dias_evaluacion: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('30'))
    cantidad_tipo2: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('3'))

    institucion: Mapped['Colegios'] = relationship('Colegios', back_populates='configuracion_escalamiento')


class JornadasColegio(Base):
    __tablename__ = 'jornadas_colegio'
    __table_args__ = (
        CheckConstraint('hora_inicio < hora_fin', name='chk_horario_valido'),
        ForeignKeyConstraint(['colegio_id'], ['colegios.id'], ondelete='CASCADE', name='fk_jornada_colegio'),
        PrimaryKeyConstraint('id', name='jornadas_colegio_pkey'),
        UniqueConstraint('colegio_id', 'id', name='unique_jornada_colegio'),
        UniqueConstraint('colegio_id', 'nombre', name='unique_jornada_nombre_por_colegio'),
        Index('unique_jornada_colegio_lower', 'colegio_id', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    colegio_id: Mapped[int] = mapped_column(Integer, nullable=False)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    hora_inicio: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    tolerancia_minutos: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))

    colegio: Mapped['Colegios'] = relationship('Colegios', back_populates='jornadas_colegio')
    estudiantes: Mapped[list['Estudiantes']] = relationship('Estudiantes', back_populates='jornadas_colegio')


class PeriodosAcademicos(Base):
    __tablename__ = 'periodos_academicos'
    __table_args__ = (
        ForeignKeyConstraint(['colegio_id'], ['colegios.id'], name='periodos_academicos_colegio_id_fkey'),
        PrimaryKeyConstraint('id', name='periodos_academicos_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    colegio_id: Mapped[int] = mapped_column(Integer, nullable=False)
    nombre: Mapped[Optional[str]] = mapped_column(String(50))
    fecha_inicio: Mapped[Optional[datetime.date]] = mapped_column(Date)
    fecha_fin: Mapped[Optional[datetime.date]] = mapped_column(Date)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    colegio: Mapped['Colegios'] = relationship('Colegios', back_populates='periodos_academicos')
    evaluaciones_estudiante: Mapped[list['EvaluacionesEstudiante']] = relationship('EvaluacionesEstudiante', back_populates='periodo')


class Sedes(Base):
    __tablename__ = 'sedes'
    __table_args__ = (
        ForeignKeyConstraint(['colegio_id'], ['colegios.id'], ondelete='CASCADE', name='fk_sede_colegio'),
        PrimaryKeyConstraint('id', name='sedes_pkey'),
        UniqueConstraint('id', 'colegio_id', name='sede_colegio_unico')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    colegio_id: Mapped[int] = mapped_column(Integer, nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    direccion: Mapped[Optional[str]] = mapped_column(String(255))
    telefono: Mapped[Optional[str]] = mapped_column(String(30))
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    colegio: Mapped['Colegios'] = relationship('Colegios', back_populates='sedes')
    usuarios: Mapped[list['Usuarios']] = relationship('Usuarios', back_populates='sedes')
    docentes_sede_colegio: Mapped[list['Docentes']] = relationship('Docentes', foreign_keys='[Docentes.sede_id, Docentes.colegio_id]', back_populates='sede_colegio')
    docentes_sede: Mapped[list['Docentes']] = relationship('Docentes', foreign_keys='[Docentes.sede_id]', back_populates='sede')
    estudiantes_sede_colegio: Mapped[list['Estudiantes']] = relationship('Estudiantes', foreign_keys='[Estudiantes.sede_id, Estudiantes.colegio_id]', back_populates='sede_colegio')
    estudiantes_sede: Mapped[list['Estudiantes']] = relationship('Estudiantes', foreign_keys='[Estudiantes.sede_id]', back_populates='sede')


class Suscripciones(Base):
    __tablename__ = 'suscripciones'
    __table_args__ = (
        ForeignKeyConstraint(['colegio_id'], ['colegios.id'], ondelete='CASCADE', name='fk_suscripcion_colegio'),
        PrimaryKeyConstraint('id', name='suscripciones_pkey'),
        UniqueConstraint('colegio_id', name='unico_colegio_suscripcion')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    colegio_id: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_fin: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    fecha_inicio: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    en_prueba: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    limite_sedes: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))
    precio_base: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2), server_default=text('0'))

    colegio: Mapped['Colegios'] = relationship('Colegios', back_populates='suscripciones')


class Competencias(Base):
    __tablename__ = 'competencias'
    __table_args__ = (
        ForeignKeyConstraint(['area_id'], ['areas_gestion.id'], ondelete='CASCADE', name='fk_competencia_area'),
        PrimaryKeyConstraint('id', name='competencias_pkey'),
        UniqueConstraint('area_id', 'nombre', name='unica_competencia_por_area'),
        UniqueConstraint('area_id', 'orden', name='unico_orden_por_area')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    orden: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('1'))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    fecha_creacion: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    area: Mapped['AreasGestion'] = relationship('AreasGestion', back_populates='competencias')
    contribuciones: Mapped[list['Contribuciones']] = relationship('Contribuciones', back_populates='competencia')


class IndicadoresLogro(Base):
    __tablename__ = 'indicadores_logro'
    __table_args__ = (
        ForeignKeyConstraint(['competencia_materia_id'], ['competencias_materia.id'], ondelete='CASCADE', name='fk_indicador_competencia_materia'),
        PrimaryKeyConstraint('id', name='indicadores_logro_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    competencia_materia_id: Mapped[int] = mapped_column(Integer, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    competencia_materia: Mapped['CompetenciasMateria'] = relationship('CompetenciasMateria', back_populates='indicadores_logro')
    evaluaciones_estudiante: Mapped[list['EvaluacionesEstudiante']] = relationship('EvaluacionesEstudiante', back_populates='indicador')


class Usuarios(Base):
    __tablename__ = 'usuarios'
    __table_args__ = (
        ForeignKeyConstraint(['colegio_id'], ['colegios.id'], name='usuarios_colegio_id_fkey'),
        ForeignKeyConstraint(['sede_id', 'colegio_id'], ['sedes.id', 'sedes.colegio_id'], name='fk_usuario_sede_colegio'),
        PrimaryKeyConstraint('id', name='usuarios_pkey'),
        UniqueConstraint('email', name='usuarios_email_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    failed_attempts: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    rol: Mapped[RolUsuario] = mapped_column(Enum(RolUsuario, values_callable=lambda cls: [member.value for member in cls], name='rol_usuario'), nullable=False)
    colegio_id: Mapped[Optional[int]] = mapped_column(Integer)
    fecha_registro: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    nombre: Mapped[Optional[str]] = mapped_column(String(100))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    is_approved: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    fecha_aprobacion: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    locked_until: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    sede_id: Mapped[Optional[int]] = mapped_column(Integer)
    is_superadmin: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    dias_prueba: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('15'))
    fecha_expiracion: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    colegio: Mapped[Optional['Colegios']] = relationship('Colegios', back_populates='usuarios')
    sedes: Mapped[Optional['Sedes']] = relationship('Sedes', back_populates='usuarios')
    acudientes: Mapped[Optional['Acudientes']] = relationship('Acudientes', uselist=False, back_populates='usuario')
    docentes: Mapped[Optional['Docentes']] = relationship('Docentes', uselist=False, back_populates='usuario')
    tokens_activacion: Mapped[list['TokensActivacion']] = relationship('TokensActivacion', back_populates='usuario')
    estudiantes: Mapped[Optional['Estudiantes']] = relationship('Estudiantes', uselist=False, back_populates='usuario')
    respuestas_novedad: Mapped[list['RespuestasNovedad']] = relationship('RespuestasNovedad', back_populates='usuario')


class Acudientes(Base):
    __tablename__ = 'acudientes'
    __table_args__ = (
        ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='SET NULL', name='fk_acudiente_usuario'),
        PrimaryKeyConstraint('id', name='acudientes_pkey'),
        UniqueConstraint('email', name='acudientes_email_key'),
        UniqueConstraint('usuario_id', name='acudientes_usuario_id_unique')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    parentesco: Mapped[Optional[str]] = mapped_column(String(50))
    usuario_id: Mapped[Optional[int]] = mapped_column(Integer)

    usuario: Mapped[Optional['Usuarios']] = relationship('Usuarios', back_populates='acudientes')
    estudiante_acudiente: Mapped[list['EstudianteAcudiente']] = relationship('EstudianteAcudiente', back_populates='acudiente')
    citaciones_acudiente: Mapped[list['CitacionesAcudiente']] = relationship('CitacionesAcudiente', back_populates='acudiente')
    justificaciones_acudiente: Mapped[list['JustificacionesAcudiente']] = relationship('JustificacionesAcudiente', back_populates='acudiente')


class Contribuciones(Base):
    __tablename__ = 'contribuciones'
    __table_args__ = (
        ForeignKeyConstraint(['competencia_id'], ['competencias.id'], ondelete='CASCADE', name='fk_contribucion_competencia'),
        PrimaryKeyConstraint('id', name='contribuciones_pkey'),
        UniqueConstraint('competencia_id', 'orden', name='unico_orden_por_competencia')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    competencia_id: Mapped[int] = mapped_column(Integer, nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    orden: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('1'))
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    fecha_creacion: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    competencia: Mapped['Competencias'] = relationship('Competencias', back_populates='contribuciones')
    criterios_evaluacion: Mapped[list['CriteriosEvaluacion']] = relationship('CriteriosEvaluacion', back_populates='contribucion')


class Docentes(Base):
    __tablename__ = 'docentes'
    __table_args__ = (
        ForeignKeyConstraint(['colegio_id'], ['colegios.id'], name='fk_colegio'),
        ForeignKeyConstraint(['sede_id', 'colegio_id'], ['sedes.id', 'sedes.colegio_id'], name='fk_docente_sede_colegio'),
        ForeignKeyConstraint(['sede_id'], ['sedes.id'], ondelete='RESTRICT', name='fk_docente_sede'),
        ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='CASCADE', name='fk_docente_usuario'),
        PrimaryKeyConstraint('id', name='docentes_pkey'),
        UniqueConstraint('usuario_id', name='docentes_usuario_id_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    colegio_id: Mapped[int] = mapped_column(Integer, nullable=False)
    documento: Mapped[Optional[str]] = mapped_column(String(20))
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(120))
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    fecha_creacion: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    usuario_id: Mapped[Optional[int]] = mapped_column(Integer)
    sede_id: Mapped[Optional[int]] = mapped_column(Integer)

    colegio: Mapped['Colegios'] = relationship('Colegios', back_populates='docentes')
    sede_colegio: Mapped[Optional['Sedes']] = relationship('Sedes', foreign_keys=[sede_id, colegio_id], back_populates='docentes_sede_colegio')
    sede: Mapped[Optional['Sedes']] = relationship('Sedes', foreign_keys=[sede_id], back_populates='docentes_sede')
    usuario: Mapped[Optional['Usuarios']] = relationship('Usuarios', back_populates='docentes')
    acuerdos_evaluacion: Mapped[list['AcuerdosEvaluacion']] = relationship('AcuerdosEvaluacion', back_populates='docente')
    clases: Mapped[list['Clases']] = relationship('Clases', back_populates='docente')
    estudiantes: Mapped[list['Estudiantes']] = relationship('Estudiantes', back_populates='docente')
    permisos: Mapped[list['Permisos']] = relationship('Permisos', back_populates='docente')


class TokensActivacion(Base):
    __tablename__ = 'tokens_activacion'
    __table_args__ = (
        ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='CASCADE', name='tokens_activacion_usuario_id_fkey'),
        PrimaryKeyConstraint('id', name='tokens_activacion_pkey'),
        UniqueConstraint('token', name='tokens_activacion_token_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(Integer, nullable=False)
    token: Mapped[str] = mapped_column(String(120), nullable=False)
    fecha_expiracion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    usado: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    usuario: Mapped['Usuarios'] = relationship('Usuarios', back_populates='tokens_activacion')


class AcuerdosEvaluacion(Base):
    __tablename__ = 'acuerdos_evaluacion'
    __table_args__ = (
        ForeignKeyConstraint(['colegio_id'], ['colegios.id'], ondelete='CASCADE', name='fk_acuerdo_colegio'),
        ForeignKeyConstraint(['docente_id'], ['docentes.id'], ondelete='CASCADE', name='fk_acuerdo_docente'),
        PrimaryKeyConstraint('id', name='acuerdos_pkey'),
        UniqueConstraint('docente_id', 'anio', name='unico_docente_anio')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    docente_id: Mapped[int] = mapped_column(Integer, nullable=False)
    colegio_id: Mapped[int] = mapped_column(Integer, nullable=False)
    anio: Mapped[int] = mapped_column(Integer, nullable=False)
    estado: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'BORRADOR'::character varying"))
    fecha_creacion: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    colegio: Mapped['Colegios'] = relationship('Colegios', back_populates='acuerdos_evaluacion')
    docente: Mapped['Docentes'] = relationship('Docentes', back_populates='acuerdos_evaluacion')
    criterios_evaluacion: Mapped[list['CriteriosEvaluacion']] = relationship('CriteriosEvaluacion', back_populates='acuerdo')
    evaluacion_final: Mapped['EvaluacionFinal'] = relationship('EvaluacionFinal', uselist=False, back_populates='acuerdo')
    seguimientos: Mapped[list['Seguimientos']] = relationship('Seguimientos', back_populates='acuerdo')


class Clases(Base):
    __tablename__ = 'clases'
    __table_args__ = (
        ForeignKeyConstraint(['docente_id'], ['docentes.id'], ondelete='CASCADE', name='fk_clase_docente'),
        ForeignKeyConstraint(['materia_id'], ['materias.id'], name='clases_materia_id_fkey'),
        PrimaryKeyConstraint('id', name='clases_pkey'),
        UniqueConstraint('docente_id', 'dia', 'hora_inicio', 'hora_fin', name='horario_unico')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    docente_id: Mapped[int] = mapped_column(Integer, nullable=False)
    colegio_id: Mapped[int] = mapped_column(Integer, nullable=False)
    grado: Mapped[str] = mapped_column(String(20), nullable=False)
    grupo: Mapped[str] = mapped_column(String(10), nullable=False)
    materia: Mapped[str] = mapped_column(String(100), nullable=False)
    hora_inicio: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    dia: Mapped[DiaSemana] = mapped_column(Enum(DiaSemana, values_callable=lambda cls: [member.value for member in cls], name='dia_semana'), nullable=False)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    materia_id: Mapped[Optional[int]] = mapped_column(Integer)

    docente: Mapped['Docentes'] = relationship('Docentes', back_populates='clases')
    materia_: Mapped[Optional['Materias']] = relationship('Materias', back_populates='clases')
    asistencias: Mapped[list['Asistencias']] = relationship('Asistencias', back_populates='clase')
    clase_estudiantes: Mapped[list['ClaseEstudiantes']] = relationship('ClaseEstudiantes', back_populates='clase')


class Estudiantes(Base):
    __tablename__ = 'estudiantes'
    __table_args__ = (
        ForeignKeyConstraint(['colegio_id', 'jornada_id'], ['jornadas_colegio.colegio_id', 'jornadas_colegio.id'], ondelete='RESTRICT', name='fk_estudiante_jornada'),
        ForeignKeyConstraint(['colegio_id'], ['colegios.id'], ondelete='CASCADE', name='fk_estudiante_colegio'),
        ForeignKeyConstraint(['docente_id'], ['docentes.id'], ondelete='RESTRICT', name='fk_estudiante_docente'),
        ForeignKeyConstraint(['sede_id', 'colegio_id'], ['sedes.id', 'sedes.colegio_id'], name='fk_estudiante_sede_colegio'),
        ForeignKeyConstraint(['sede_id'], ['sedes.id'], ondelete='RESTRICT', name='fk_estudiante_sede'),
        ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='SET NULL', name='fk_estudiante_usuario'),
        PrimaryKeyConstraint('id', name='estudiantes_pkey'),
        UniqueConstraint('qr_token', name='estudiantes_qr_token_key'),
        UniqueConstraint('usuario_id', name='estudiantes_usuario_id_unique')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    colegio_id: Mapped[int] = mapped_column(Integer, nullable=False)
    docente_id: Mapped[int] = mapped_column(Integer, nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    jornada_id: Mapped[int] = mapped_column(Integer, nullable=False)
    grado: Mapped[Optional[str]] = mapped_column(String(20))
    grupo: Mapped[Optional[str]] = mapped_column(String(20))
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    fecha_creacion: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    usuario_id: Mapped[Optional[int]] = mapped_column(Integer)
    qr_token: Mapped[Optional[str]] = mapped_column(String(80))
    institucion_id: Mapped[Optional[int]] = mapped_column(Integer)
    sede_id: Mapped[Optional[int]] = mapped_column(Integer)

    jornadas_colegio: Mapped['JornadasColegio'] = relationship('JornadasColegio', back_populates='estudiantes')
    colegio: Mapped['Colegios'] = relationship('Colegios', back_populates='estudiantes')
    docente: Mapped['Docentes'] = relationship('Docentes', back_populates='estudiantes')
    sede_colegio: Mapped[Optional['Sedes']] = relationship('Sedes', foreign_keys=[sede_id, colegio_id], back_populates='estudiantes_sede_colegio')
    sede: Mapped[Optional['Sedes']] = relationship('Sedes', foreign_keys=[sede_id], back_populates='estudiantes_sede')
    usuario: Mapped[Optional['Usuarios']] = relationship('Usuarios', back_populates='estudiantes')
    alertas: Mapped[list['Alertas']] = relationship('Alertas', back_populates='estudiante')
    asistencias: Mapped[list['Asistencias']] = relationship('Asistencias', back_populates='estudiante')
    clase_estudiantes: Mapped[list['ClaseEstudiantes']] = relationship('ClaseEstudiantes', back_populates='estudiante')
    estudiante_acudiente: Mapped[list['EstudianteAcudiente']] = relationship('EstudianteAcudiente', back_populates='estudiante')
    evaluaciones_estudiante: Mapped[list['EvaluacionesEstudiante']] = relationship('EvaluacionesEstudiante', back_populates='estudiante')
    ingresos_colegio: Mapped[list['IngresosColegio']] = relationship('IngresosColegio', back_populates='estudiante')
    novedades: Mapped[list['Novedades']] = relationship('Novedades', back_populates='estudiante')
    piar: Mapped[list['Piar']] = relationship('Piar', back_populates='estudiante')
    acuerdos_correctivos: Mapped[list['AcuerdosCorrectivos']] = relationship('AcuerdosCorrectivos', back_populates='estudiante')
    citaciones_acudiente: Mapped[list['CitacionesAcudiente']] = relationship('CitacionesAcudiente', back_populates='estudiante')
    descargos_estudiante: Mapped[list['DescargosEstudiante']] = relationship('DescargosEstudiante', back_populates='estudiante')


class Permisos(Base):
    __tablename__ = 'permisos'
    __table_args__ = (
        CheckConstraint('fecha_fin >= fecha_inicio', name='chk_permiso_fechas'),
        ForeignKeyConstraint(['colegio_id'], ['colegios.id'], name='fk_colegio'),
        ForeignKeyConstraint(['docente_id'], ['docentes.id'], name='fk_docente'),
        PrimaryKeyConstraint('id', name='permisos_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    docente_id: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_inicio: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    tipo: Mapped[str] = mapped_column(String(100), nullable=False)
    colegio_id: Mapped[int] = mapped_column(Integer, nullable=False)
    observacion: Mapped[Optional[str]] = mapped_column(Text)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'), comment='Indica si el permiso académico está vigente. No controla acceso al sistema.')

    colegio: Mapped['Colegios'] = relationship('Colegios', back_populates='permisos')
    docente: Mapped['Docentes'] = relationship('Docentes', back_populates='permisos')


class Alertas(Base):
    __tablename__ = 'alertas'
    __table_args__ = (
        ForeignKeyConstraint(['estudiante_id'], ['estudiantes.id'], ondelete='CASCADE', name='fk_alerta_estudiante'),
        PrimaryKeyConstraint('id', name='alertas_pkey'),
        Index('unica_alerta_activa', 'estudiante_id', 'tipo', postgresql_where='(atendida = false)', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    estudiante_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    fecha: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    atendida: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    estudiante: Mapped['Estudiantes'] = relationship('Estudiantes', back_populates='alertas')


class Asistencias(Base):
    __tablename__ = 'asistencias'
    __table_args__ = (
        ForeignKeyConstraint(['clase_id'], ['clases.id'], ondelete='CASCADE', name='fk_asistencia_clase'),
        ForeignKeyConstraint(['estudiante_id'], ['estudiantes.id'], ondelete='CASCADE', name='fk_asistencia_estudiante'),
        PrimaryKeyConstraint('id', name='asistencias_pkey'),
        UniqueConstraint('estudiante_id', 'clase_id', 'fecha', name='unica_asistencia_por_clase')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    estudiante_id: Mapped[int] = mapped_column(Integer, nullable=False)
    clase_id: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
    observacion: Mapped[Optional[str]] = mapped_column(Text)
    registrada_por: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    clase: Mapped['Clases'] = relationship('Clases', back_populates='asistencias')
    estudiante: Mapped['Estudiantes'] = relationship('Estudiantes', back_populates='asistencias')


class ClaseEstudiantes(Base):
    __tablename__ = 'clase_estudiantes'
    __table_args__ = (
        ForeignKeyConstraint(['clase_id'], ['clases.id'], ondelete='CASCADE', name='fk_ce_clase'),
        ForeignKeyConstraint(['estudiante_id'], ['estudiantes.id'], ondelete='CASCADE', name='fk_ce_estudiante'),
        PrimaryKeyConstraint('id', name='clase_estudiantes_pkey'),
        UniqueConstraint('clase_id', 'estudiante_id', name='unica_matricula')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clase_id: Mapped[int] = mapped_column(Integer, nullable=False)
    estudiante_id: Mapped[int] = mapped_column(Integer, nullable=False)

    clase: Mapped['Clases'] = relationship('Clases', back_populates='clase_estudiantes')
    estudiante: Mapped['Estudiantes'] = relationship('Estudiantes', back_populates='clase_estudiantes')


class CriteriosEvaluacion(Base):
    __tablename__ = 'criterios_evaluacion'
    __table_args__ = (
        ForeignKeyConstraint(['acuerdo_id'], ['acuerdos_evaluacion.id'], ondelete='CASCADE', name='fk_criterio_acuerdo'),
        ForeignKeyConstraint(['contribucion_id'], ['contribuciones.id'], ondelete='CASCADE', name='fk_criterio_contribucion'),
        PrimaryKeyConstraint('id', name='criterios_pkey'),
        Index('idx_criterio_acuerdo', 'acuerdo_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    acuerdo_id: Mapped[int] = mapped_column(Integer, nullable=False)
    contribucion_id: Mapped[int] = mapped_column(Integer, nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_creacion: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    acuerdo: Mapped['AcuerdosEvaluacion'] = relationship('AcuerdosEvaluacion', back_populates='criterios_evaluacion')
    contribucion: Mapped['Contribuciones'] = relationship('Contribuciones', back_populates='criterios_evaluacion')
    evaluacion_criterio: Mapped[list['EvaluacionCriterio']] = relationship('EvaluacionCriterio', back_populates='criterio')
    evidencias: Mapped[list['Evidencias']] = relationship('Evidencias', back_populates='criterio')


class EstudianteAcudiente(Base):
    __tablename__ = 'estudiante_acudiente'
    __table_args__ = (
        ForeignKeyConstraint(['acudiente_id'], ['acudientes.id'], ondelete='CASCADE', name='fk_ea_acudiente'),
        ForeignKeyConstraint(['estudiante_id'], ['estudiantes.id'], ondelete='CASCADE', name='fk_ea_estudiante'),
        PrimaryKeyConstraint('id', name='estudiante_acudiente_pkey'),
        UniqueConstraint('estudiante_id', 'acudiente_id', name='unica_relacion')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    estudiante_id: Mapped[int] = mapped_column(Integer, nullable=False)
    acudiente_id: Mapped[int] = mapped_column(Integer, nullable=False)

    acudiente: Mapped['Acudientes'] = relationship('Acudientes', back_populates='estudiante_acudiente')
    estudiante: Mapped['Estudiantes'] = relationship('Estudiantes', back_populates='estudiante_acudiente')


class EvaluacionFinal(Base):
    __tablename__ = 'evaluacion_final'
    __table_args__ = (
        ForeignKeyConstraint(['acuerdo_id'], ['acuerdos_evaluacion.id'], ondelete='CASCADE', name='fk_eval_acuerdo'),
        PrimaryKeyConstraint('id', name='evaluacion_final_pkey'),
        UniqueConstraint('acuerdo_id', name='unica_evaluacion_por_acuerdo')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    acuerdo_id: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_cierre: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    estado: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'ABIERTO'::character varying"))
    observaciones_finales: Mapped[Optional[str]] = mapped_column(Text)

    acuerdo: Mapped['AcuerdosEvaluacion'] = relationship('AcuerdosEvaluacion', back_populates='evaluacion_final')
    evaluacion_criterio: Mapped[list['EvaluacionCriterio']] = relationship('EvaluacionCriterio', back_populates='evaluacion_final')


class EvaluacionesEstudiante(Base):
    __tablename__ = 'evaluaciones_estudiante'
    __table_args__ = (
        ForeignKeyConstraint(['estudiante_id'], ['estudiantes.id'], name='evaluaciones_estudiante_estudiante_id_fkey'),
        ForeignKeyConstraint(['indicador_id'], ['indicadores_logro.id'], ondelete='CASCADE', name='evaluaciones_estudiante_indicador_id_fkey'),
        ForeignKeyConstraint(['periodo_id'], ['periodos_academicos.id'], name='evaluaciones_estudiante_periodo_id_fkey'),
        PrimaryKeyConstraint('id', name='evaluaciones_estudiante_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    estudiante_id: Mapped[Optional[int]] = mapped_column(Integer)
    indicador_id: Mapped[Optional[int]] = mapped_column(Integer)
    periodo_id: Mapped[Optional[int]] = mapped_column(Integer)
    calificacion: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(4, 2))
    observacion: Mapped[Optional[str]] = mapped_column(Text)

    estudiante: Mapped[Optional['Estudiantes']] = relationship('Estudiantes', back_populates='evaluaciones_estudiante')
    indicador: Mapped[Optional['IndicadoresLogro']] = relationship('IndicadoresLogro', back_populates='evaluaciones_estudiante')
    periodo: Mapped[Optional['PeriodosAcademicos']] = relationship('PeriodosAcademicos', back_populates='evaluaciones_estudiante')


class IngresosColegio(Base):
    __tablename__ = 'ingresos_colegio'
    __table_args__ = (
        ForeignKeyConstraint(['colegio_id'], ['colegios.id'], ondelete='CASCADE', name='fk_ingreso_colegio'),
        ForeignKeyConstraint(['estudiante_id'], ['estudiantes.id'], ondelete='CASCADE', name='fk_ingreso_estudiante'),
        PrimaryKeyConstraint('id', name='ingresos_colegio_pkey'),
        Index('unico_evento_por_dia', 'estudiante_id', 'fecha', 'tipo_evento', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    estudiante_id: Mapped[int] = mapped_column(Integer, nullable=False)
    colegio_id: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('CURRENT_DATE'))
    hora: Mapped[datetime.time] = mapped_column(Time, nullable=False, server_default=text('CURRENT_TIME'))
    metodo: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'QR'::character varying"))
    creado_en: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    tipo_evento: Mapped[Optional[TipoEventoColegio]] = mapped_column(Enum(TipoEventoColegio, values_callable=lambda cls: [member.value for member in cls], name='tipo_evento_colegio'), server_default=text("'ingreso'::tipo_evento_colegio"))

    colegio: Mapped['Colegios'] = relationship('Colegios', back_populates='ingresos_colegio')
    estudiante: Mapped['Estudiantes'] = relationship('Estudiantes', back_populates='ingresos_colegio')


class Novedades(Base):
    __tablename__ = 'novedades'
    __table_args__ = (
        ForeignKeyConstraint(['estudiante_id'], ['estudiantes.id'], ondelete='CASCADE', name='fk_estudiante'),
        PrimaryKeyConstraint('id', name='novedades_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    estudiante_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo_novedad: Mapped[TipoNovedadEnum] = mapped_column(Enum(TipoNovedadEnum, values_callable=lambda cls: [member.value for member in cls], name='tipo_novedad_enum'), nullable=False)
    informe: Mapped[str] = mapped_column(Text, nullable=False)
    fecha: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('CURRENT_DATE'))
    hora: Mapped[datetime.time] = mapped_column(Time, nullable=False, server_default=text('CURRENT_TIME'))
    gravedad: Mapped[TipoGravedad] = mapped_column(Enum(TipoGravedad, values_callable=lambda cls: [member.value for member in cls], name='tipo_gravedad'), nullable=False)
    registrada_por: Mapped[Optional[int]] = mapped_column(Integer)
    categoria: Mapped[Optional[str]] = mapped_column(String(20))

    estudiante: Mapped['Estudiantes'] = relationship('Estudiantes', back_populates='novedades')
    acuerdos_correctivos: Mapped['AcuerdosCorrectivos'] = relationship('AcuerdosCorrectivos', uselist=False, back_populates='novedad')
    citaciones_acudiente: Mapped[list['CitacionesAcudiente']] = relationship('CitacionesAcudiente', back_populates='novedad')
    descargos_estudiante: Mapped[list['DescargosEstudiante']] = relationship('DescargosEstudiante', back_populates='novedad')
    justificaciones_acudiente: Mapped['JustificacionesAcudiente'] = relationship('JustificacionesAcudiente', uselist=False, back_populates='novedad')
    respuestas_novedad: Mapped[list['RespuestasNovedad']] = relationship('RespuestasNovedad', back_populates='novedad')


class Piar(Base):
    __tablename__ = 'piar'
    __table_args__ = (
        ForeignKeyConstraint(['estudiante_id'], ['estudiantes.id'], ondelete='CASCADE', name='piar_estudiante_id_fkey'),
        PrimaryKeyConstraint('id', name='piar_pkey'),
        Index('unico_piar_activo', 'estudiante_id', postgresql_where='(activo = true)', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    estudiante_id: Mapped[int] = mapped_column(Integer, nullable=False)
    diagnostico: Mapped[Optional[str]] = mapped_column(Text)
    objetivos: Mapped[Optional[str]] = mapped_column(Text)
    fecha_inicio: Mapped[Optional[datetime.date]] = mapped_column(Date)
    fecha_fin: Mapped[Optional[datetime.date]] = mapped_column(Date)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    estudiante: Mapped['Estudiantes'] = relationship('Estudiantes', back_populates='piar')
    ajustes_razonables: Mapped[list['AjustesRazonables']] = relationship('AjustesRazonables', back_populates='piar')


class Seguimientos(Base):
    __tablename__ = 'seguimientos'
    __table_args__ = (
        ForeignKeyConstraint(['acuerdo_id'], ['acuerdos_evaluacion.id'], ondelete='CASCADE', name='fk_seguimiento_acuerdo'),
        PrimaryKeyConstraint('id', name='seguimientos_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    acuerdo_id: Mapped[int] = mapped_column(Integer, nullable=False)
    observaciones: Mapped[str] = mapped_column(Text, nullable=False)
    recomendaciones: Mapped[str] = mapped_column(Text, nullable=False)
    fecha: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    acuerdo: Mapped['AcuerdosEvaluacion'] = relationship('AcuerdosEvaluacion', back_populates='seguimientos')


class AcuerdosCorrectivos(Base):
    __tablename__ = 'acuerdos_correctivos'
    __table_args__ = (
        ForeignKeyConstraint(['estudiante_id'], ['estudiantes.id'], ondelete='CASCADE', name='fk_acuerdo_estudiante'),
        ForeignKeyConstraint(['novedad_id'], ['novedades.id'], ondelete='CASCADE', name='fk_acuerdo_novedad'),
        PrimaryKeyConstraint('id', name='acuerdos_correctivos_pkey'),
        UniqueConstraint('novedad_id', name='unica_novedad_acuerdo')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    novedad_id: Mapped[int] = mapped_column(Integer, nullable=False)
    estudiante_id: Mapped[int] = mapped_column(Integer, nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    compromiso: Mapped[Optional[str]] = mapped_column(Text)
    fecha: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    estado: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'ACTIVO'::character varying"))

    estudiante: Mapped['Estudiantes'] = relationship('Estudiantes', back_populates='acuerdos_correctivos')
    novedad: Mapped['Novedades'] = relationship('Novedades', back_populates='acuerdos_correctivos')


class AjustesRazonables(Base):
    __tablename__ = 'ajustes_razonables'
    __table_args__ = (
        ForeignKeyConstraint(['piar_id'], ['piar.id'], ondelete='CASCADE', name='ajustes_razonables_piar_id_fkey'),
        PrimaryKeyConstraint('id', name='ajustes_razonables_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    piar_id: Mapped[int] = mapped_column(Integer, nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    aplicado: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    fecha_aplicacion: Mapped[Optional[datetime.date]] = mapped_column(Date)

    piar: Mapped['Piar'] = relationship('Piar', back_populates='ajustes_razonables')


class CitacionesAcudiente(Base):
    __tablename__ = 'citaciones_acudiente'
    __table_args__ = (
        ForeignKeyConstraint(['acudiente_id'], ['acudientes.id'], ondelete='CASCADE', name='citaciones_acudiente_acudiente_id_fkey'),
        ForeignKeyConstraint(['estudiante_id'], ['estudiantes.id'], ondelete='CASCADE', name='citaciones_acudiente_estudiante_id_fkey'),
        ForeignKeyConstraint(['novedad_id'], ['novedades.id'], ondelete='SET NULL', name='citaciones_acudiente_novedad_id_fkey'),
        PrimaryKeyConstraint('id', name='citaciones_acudiente_pkey'),
        Index('unique_citacion_por_novedad', 'novedad_id', 'tipo_origen', postgresql_where='(tipo_origen IS NOT NULL)', unique=True),
        Index('unique_citacion_por_tipo', 'estudiante_id', 'tipo_origen', postgresql_where='(tipo_origen IS NOT NULL)', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    estudiante_id: Mapped[int] = mapped_column(Integer, nullable=False)
    acudiente_id: Mapped[int] = mapped_column(Integer, nullable=False)
    motivo: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_citacion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    novedad_id: Mapped[Optional[int]] = mapped_column(Integer)
    estado: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'pendiente'::character varying"))
    observaciones: Mapped[Optional[str]] = mapped_column(Text)
    tipo_origen: Mapped[Optional[str]] = mapped_column(String(50))
    fecha: Mapped[Optional[datetime.date]] = mapped_column(Date, server_default=text('CURRENT_DATE'))

    acudiente: Mapped['Acudientes'] = relationship('Acudientes', back_populates='citaciones_acudiente')
    estudiante: Mapped['Estudiantes'] = relationship('Estudiantes', back_populates='citaciones_acudiente')
    novedad: Mapped[Optional['Novedades']] = relationship('Novedades', back_populates='citaciones_acudiente')


class DescargosEstudiante(Base):
    __tablename__ = 'descargos_estudiante'
    __table_args__ = (
        ForeignKeyConstraint(['estudiante_id'], ['estudiantes.id'], ondelete='CASCADE', name='fk_descargo_estudiante'),
        ForeignKeyConstraint(['novedad_id'], ['novedades.id'], ondelete='CASCADE', name='fk_descargo_novedad'),
        PrimaryKeyConstraint('id', name='descargos_estudiante_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    novedad_id: Mapped[int] = mapped_column(Integer, nullable=False)
    estudiante_id: Mapped[int] = mapped_column(Integer, nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    fecha: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    estudiante: Mapped['Estudiantes'] = relationship('Estudiantes', back_populates='descargos_estudiante')
    novedad: Mapped['Novedades'] = relationship('Novedades', back_populates='descargos_estudiante')


class EvaluacionCriterio(Base):
    __tablename__ = 'evaluacion_criterio'
    __table_args__ = (
        CheckConstraint('calificacion >= 0::numeric AND calificacion <= 5::numeric', name='chk_calificacion_valida'),
        ForeignKeyConstraint(['criterio_id'], ['criterios_evaluacion.id'], ondelete='CASCADE', name='fk_evalcriterio_criterio'),
        ForeignKeyConstraint(['evaluacion_final_id'], ['evaluacion_final.id'], ondelete='CASCADE', name='fk_evalcriterio_evalfinal'),
        PrimaryKeyConstraint('id', name='evaluacion_criterio_pkey'),
        UniqueConstraint('evaluacion_final_id', 'criterio_id', name='unica_eval_por_criterio'),
        Index('idx_evalcriterio_evalfinal', 'evaluacion_final_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    evaluacion_final_id: Mapped[int] = mapped_column(Integer, nullable=False)
    criterio_id: Mapped[int] = mapped_column(Integer, nullable=False)
    calificacion: Mapped[decimal.Decimal] = mapped_column(Numeric(4, 2), nullable=False)
    observacion: Mapped[Optional[str]] = mapped_column(Text)

    criterio: Mapped['CriteriosEvaluacion'] = relationship('CriteriosEvaluacion', back_populates='evaluacion_criterio')
    evaluacion_final: Mapped['EvaluacionFinal'] = relationship('EvaluacionFinal', back_populates='evaluacion_criterio')


class Evidencias(Base):
    __tablename__ = 'evidencias'
    __table_args__ = (
        ForeignKeyConstraint(['criterio_id'], ['criterios_evaluacion.id'], ondelete='CASCADE', name='fk_evidencia_criterio'),
        PrimaryKeyConstraint('id', name='evidencias_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    criterio_id: Mapped[int] = mapped_column(Integer, nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    url: Mapped[Optional[str]] = mapped_column(Text)
    aprobado: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    observacion_admin: Mapped[Optional[str]] = mapped_column(Text)
    fecha_creacion: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    criterio: Mapped['CriteriosEvaluacion'] = relationship('CriteriosEvaluacion', back_populates='evidencias')


class JustificacionesAcudiente(Base):
    __tablename__ = 'justificaciones_acudiente'
    __table_args__ = (
        ForeignKeyConstraint(['acudiente_id'], ['acudientes.id'], ondelete='CASCADE', name='justificaciones_acudiente_acudiente_id_fkey'),
        ForeignKeyConstraint(['novedad_id'], ['novedades.id'], ondelete='CASCADE', name='justificaciones_acudiente_novedad_id_fkey'),
        PrimaryKeyConstraint('id', name='justificaciones_acudiente_pkey'),
        UniqueConstraint('novedad_id', name='justificaciones_acudiente_novedad_id_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    novedad_id: Mapped[int] = mapped_column(Integer, nullable=False)
    acudiente_id: Mapped[int] = mapped_column(Integer, nullable=False)
    justificacion: Mapped[str] = mapped_column(Text, nullable=False)
    fecha: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    acudiente: Mapped['Acudientes'] = relationship('Acudientes', back_populates='justificaciones_acudiente')
    novedad: Mapped['Novedades'] = relationship('Novedades', back_populates='justificaciones_acudiente')


class RespuestasNovedad(Base):
    __tablename__ = 'respuestas_novedad'
    __table_args__ = (
        ForeignKeyConstraint(['novedad_id'], ['novedades.id'], ondelete='CASCADE', name='fk_respuesta_novedad'),
        ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='SET NULL', name='fk_respuesta_usuario'),
        PrimaryKeyConstraint('id', name='respuestas_novedad_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    novedad_id: Mapped[int] = mapped_column(Integer, nullable=False)
    rol: Mapped[RolUsuario] = mapped_column(Enum(RolUsuario, values_callable=lambda cls: [member.value for member in cls], name='rol_usuario'), nullable=False)
    mensaje: Mapped[str] = mapped_column(Text, nullable=False)
    usuario_id: Mapped[Optional[int]] = mapped_column(Integer)
    fecha: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    novedad: Mapped['Novedades'] = relationship('Novedades', back_populates='respuestas_novedad')
    usuario: Mapped[Optional['Usuarios']] = relationship('Usuarios', back_populates='respuestas_novedad')
