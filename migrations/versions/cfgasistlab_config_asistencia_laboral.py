"""crear tabla configuracion_asistencia_laboral

Revision ID: cfgasistlab
Revises: ingremp
Create Date: 2026-10-12

Crea la tabla donde el admin del colegio configura:
- hora_inicio_laboral (hora de entrada laboral)
- tolerancia_minutos (margen antes de marcar tarde)
- marcar_ausente_despues_minutos (cuando se considera ausente)
- activo (si la funcionalidad esta habilitada)
"""
from alembic import op
import sqlalchemy as sa


revision = 'cfgasistlab'
down_revision = 'ingremp'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'configuracion_asistencia_laboral',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('colegio_id', sa.Integer(), nullable=False),
        sa.Column('hora_inicio_laboral', sa.Time(), nullable=False),
        sa.Column('tolerancia_minutos', sa.Integer(), server_default=sa.text('0'), nullable=True),
        sa.Column('marcar_ausente_despues_minutos', sa.Integer(), server_default=sa.text('60'), nullable=True),
        sa.Column('activo', sa.Boolean(), server_default=sa.text('true'), nullable=True),
        sa.ForeignKeyConstraint(['colegio_id'], ['colegios.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('colegio_id', name='uq_config_asistencia_colegio')
    )


def downgrade():
    op.drop_table('configuracion_asistencia_laboral')
