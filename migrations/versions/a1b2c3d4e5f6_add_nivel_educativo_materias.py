"""Add nivel_educativo to materias table

Revision ID: a1b2c3d4e5f6
Revises: cd49c10c3839
Create Date: 2026-09-03 08:40:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'cd49c10c3839'
branch_labels = None
depends_on = None


def upgrade():
    # Agregar columna nivel_educativo a tabla materias
    # nullable=True permite que filas existentes tengan NULL inicialmente
    op.add_column('materias', sa.Column('nivel_educativo', sa.String(length=50), nullable=True))


def downgrade():
    # Revertir: eliminar la columna
    op.drop_column('materias', 'nivel_educativo')
