"""crear tabla piar_profesional

Revision ID: piar01
Revises: blqAusuarios
Create Date: 2026-10-08

Modulo PIAR: crea la tabla intermedia piar_profesional para permitir
multiples profesionales asignados a un mismo PIAR.

- Tabla nueva: piar_profesional
- FK piar_id -> piar(id) ON DELETE CASCADE
- FK profesional_id -> usuarios(id) ON DELETE CASCADE
- UNIQUE(piar_id, profesional_id)
- Indices en piar_id y profesional_id
"""
from alembic import op
import sqlalchemy as sa


revision = 'piar01'
down_revision = 'blqAusuarios'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'piar_profesional',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('piar_id', sa.Integer(), nullable=False),
        sa.Column('profesional_id', sa.Integer(), nullable=False),
        sa.Column('asignado_en', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['piar_id'], ['piar.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['profesional_id'], ['usuarios.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('piar_id', 'profesional_id', name='uq_piar_profesional')
    )
    op.create_index('idx_piar_profesional_piar', 'piar_profesional', ['piar_id'])
    op.create_index('idx_piar_profesional_prof', 'piar_profesional', ['profesional_id'])


def downgrade():
    op.drop_index('idx_piar_profesional_prof', table_name='piar_profesional')
    op.drop_index('idx_piar_profesional_piar', table_name='piar_profesional')
    op.drop_table('piar_profesional')
