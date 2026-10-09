"""crear tablas malla_plantilla y malla_plantilla_columna

Revision ID: mall01
Revises: piar04
Create Date: 2026-10-09

Modulo Malla de Evaluacion: crea el sistema de plantillas.
- malla_plantilla: formato general del admin (una por colegio)
- malla_plantilla_columna: columnas que componen la plantilla
"""
from alembic import op
import sqlalchemy as sa


revision = 'mall01'
down_revision = 'piar04'
branch_labels = None
depends_on = None


def upgrade():
    # 1. malla_plantilla
    op.create_table(
        'malla_plantilla',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('colegio_id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('creado_por', sa.Integer(), nullable=False),
        sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('activo', sa.Boolean(), server_default=sa.text('true'), nullable=True),
        sa.ForeignKeyConstraint(['colegio_id'], ['colegios.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['creado_por'], ['usuarios.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('colegio_id', 'nombre', name='uq_malla_plantilla_nombre')
    )
    op.create_index('idx_malla_plantilla_colegio', 'malla_plantilla', ['colegio_id'])

    # 2. malla_plantilla_columna
    op.create_table(
        'malla_plantilla_columna',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plantilla_id', sa.Integer(), nullable=False),
        sa.Column('orden', sa.Integer(), nullable=False),
        sa.Column('clave', sa.String(length=50), nullable=False),
        sa.Column('titulo', sa.String(length=150), nullable=False),
        sa.Column('tipo', sa.String(length=30), server_default='texto', nullable=True),
        sa.Column('requerida', sa.Boolean(), server_default=sa.text('false'), nullable=True),
        sa.ForeignKeyConstraint(['plantilla_id'], ['malla_plantilla.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('plantilla_id', 'orden', name='uq_malla_plantilla_columna_orden')
    )
    op.create_index('idx_malla_plantilla_columna_plantilla', 'malla_plantilla_columna', ['plantilla_id'])


def downgrade():
    op.drop_index('idx_malla_plantilla_columna_plantilla', table_name='malla_plantilla_columna')
    op.drop_table('malla_plantilla_columna')
    op.drop_index('idx_malla_plantilla_colegio', table_name='malla_plantilla')
    op.drop_table('malla_plantilla')
