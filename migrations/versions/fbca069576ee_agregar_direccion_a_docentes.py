"""agregar direccion a docentes

Revision ID: fbca069576ee
Revises: mall02
Create Date: 2026-10-11 10:37:16.933331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbca069576ee'
down_revision = 'mall02'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'docentes',
        sa.Column('direccion', sa.String(length=200), nullable=True)
    )


def downgrade():
    op.drop_column('docentes', 'direccion')
