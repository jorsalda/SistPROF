"""crear_tabla_diagnosticos_estudiante

Revision ID: a7de58d1f356
Revises: 7f266f11d152
Create Date: 2026-10-27
"""
from alembic import op
import sqlalchemy as sa

revision = 'a7de58d1f356'
down_revision = '7f266f11d152'
branch_labels = None
depends_on = None



def upgrade():
    op.create_table(
        'diagnosticos_estudiante',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('estudiante_id', sa.Integer(), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=False),
        sa.Column('fecha_registro', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['estudiante_id'], ['estudiantes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_diagnosticos_estudiante_estudiante_id'), 'diagnosticos_estudiante', ['estudiante_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_diagnosticos_estudiante_estudiante_id'), table_name='diagnosticos_estudiante')
    op.drop_table('diagnosticos_estudiante')
