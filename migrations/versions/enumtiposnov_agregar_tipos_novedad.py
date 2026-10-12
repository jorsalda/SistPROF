"""agregar tipos de novedad

Revision ID: enumtiposnov
Revises: enumsroles
Create Date: 2026-10-12

Agrega valores al enum tipo_novedad_enum:
- SALUD
- SEGUIMIENTO
- APOYO
- CALAMIDAD
- OTRO
"""
from alembic import op
import sqlalchemy as sa


revision = 'enumtiposnov'
down_revision = 'enumsroles'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE tipo_novedad_enum ADD VALUE IF NOT EXISTS 'SALUD'")
    op.execute("ALTER TYPE tipo_novedad_enum ADD VALUE IF NOT EXISTS 'SEGUIMIENTO'")
    op.execute("ALTER TYPE tipo_novedad_enum ADD VALUE IF NOT EXISTS 'APOYO'")
    op.execute("ALTER TYPE tipo_novedad_enum ADD VALUE IF NOT EXISTS 'CALAMIDAD'")
    op.execute("ALTER TYPE tipo_novedad_enum ADD VALUE IF NOT EXISTS 'OTRO'")


def downgrade():
    # PostgreSQL no permite eliminar valores de un enum facilmente.
    pass
