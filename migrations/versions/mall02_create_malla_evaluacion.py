"""crear tablas malla_evaluacion y malla_evaluacion_detalle

Revision ID: mall02
Revises: mall01
Create Date: 2026-10-09

Modulo Malla de Evaluacion: crea las tablas de la malla real de cada docente.
- malla_evaluacion: encabezado (docente + materia + grado + periodo + anio)
- malla_evaluacion_detalle: filas de contenido (una por competencia)
"""
from alembic import op
import sqlalchemy as sa


revision = 'mall02'
down_revision = 'mall01'
branch_labels = None
depends_on = None


def upgrade():
    # 1. malla_evaluacion
    op.create_table(
        'malla_evaluacion',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('colegio_id', sa.Integer(), nullable=False),
        sa.Column('docente_id', sa.Integer(), nullable=False),
        sa.Column('materia_id', sa.Integer(), nullable=False),
        sa.Column('grado', sa.String(length=20), nullable=False),
        sa.Column('periodo_id', sa.Integer(), nullable=False),
        sa.Column('anio_lectivo', sa.Integer(), nullable=False),
        sa.Column('plantilla_id', sa.Integer(), nullable=True),
        sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('fecha_actualizacion', sa.DateTime(), nullable=True),
        sa.Column('activo', sa.Boolean(), server_default=sa.text('true'), nullable=True),
        sa.ForeignKeyConstraint(['colegio_id'], ['colegios.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['docente_id'], ['docentes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['materia_id'], ['materias.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['periodo_id'], ['periodos_academicos.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['plantilla_id'], ['malla_plantilla.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint(
            'docente_id', 'materia_id', 'grado', 'periodo_id', 'anio_lectivo',
            name='uq_malla_evaluacion_unica'
        )
    )
    op.create_index('idx_malla_evaluacion_docente', 'malla_evaluacion', ['docente_id'])
    op.create_index('idx_malla_evaluacion_periodo', 'malla_evaluacion', ['periodo_id'])
    op.create_index('idx_malla_evaluacion_colegio', 'malla_evaluacion', ['colegio_id'])

    # 2. malla_evaluacion_detalle
    op.create_table(
        'malla_evaluacion_detalle',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('malla_id', sa.Integer(), nullable=False),
        sa.Column('orden', sa.Integer(), nullable=False),
        sa.Column('competencia_id', sa.Integer(), nullable=True),
        sa.Column('indicador_id', sa.Integer(), nullable=True),
        sa.Column('competencia_texto', sa.Text(), nullable=True),
        sa.Column('indicador_texto', sa.Text(), nullable=True),
        sa.Column('planeacion_texto', sa.Text(), nullable=True),
        sa.Column('registro_texto', sa.Text(), nullable=True),
        sa.Column('rubrica_texto', sa.Text(), nullable=True),
        sa.Column('resultados_texto', sa.Text(), nullable=True),
        sa.Column('plan_apoyo_texto', sa.Text(), nullable=True),
        sa.Column('analisis_texto', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['malla_id'], ['malla_evaluacion.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['competencia_id'], ['competencias.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['indicador_id'], ['indicadores_logro.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('malla_id', 'orden', name='uq_malla_evaluacion_detalle_orden')
    )
    op.create_index('idx_malla_evaluacion_detalle_malla', 'malla_evaluacion_detalle', ['malla_id'])


def downgrade():
    op.drop_index('idx_malla_evaluacion_detalle_malla', table_name='malla_evaluacion_detalle')
    op.drop_table('malla_evaluacion_detalle')
    op.drop_index('idx_malla_evaluacion_colegio', table_name='malla_evaluacion')
    op.drop_index('idx_malla_evaluacion_periodo', table_name='malla_evaluacion')
    op.drop_index('idx_malla_evaluacion_docente', table_name='malla_evaluacion')
    op.drop_table('malla_evaluacion')
