"""agregar_estado_a_permisos

Revision ID: permisos_estado
Revises: a7de58d1f356
Create Date: 2026-10-28

Agrega columna estado a la tabla permisos.
"""
from alembic import op
import sqlalchemy as sa


revision = 'permisos_estado'
down_revision = 'a7de58d1f356'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'permisos',
        sa.Column('estado', sa.String(length=20), server_default='pendiente', nullable=False)
    )


def downgrade():
    op.drop_column('permisos', 'estado')
