"""agregar roles psicologo y profesional_piar

Revision ID: enumsroles
Revises: evalnullable
Create Date: 2026-10-12

Agrega valores al enum rol_usuario:
- profesional_piar (ya existia en BD local, se agrega al modelo tambien)
- psicologo (nuevo)
"""
from alembic import op
import sqlalchemy as sa


revision = 'enumsroles'
down_revision = 'evalnullable'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE rol_usuario ADD VALUE IF NOT EXISTS 'profesional_piar'")
    op.execute("ALTER TYPE rol_usuario ADD VALUE IF NOT EXISTS 'psicologo'")


def downgrade():
    # PostgreSQL no permite eliminar valores de un enum facilmente.
    # El downgrade no remueve los valores (requeriria recrear el tipo).
    pass
