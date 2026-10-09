"""agregar profesional_piar al enum rol_usuario

Revision ID: piar04
Revises: piar03
Create Date: 2026-10-08

Modulo PIAR: agrega un nuevo rol de usuario profesional_piar.
- ALTER TYPE rol_usuario ADD VALUE IF NOT EXISTS 'profesional_piar'
"""
from alembic import op
import sqlalchemy as sa


revision = 'piar04'
down_revision = 'piar03'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE rol_usuario ADD VALUE IF NOT EXISTS 'profesional_piar'")


def downgrade():
    # PostgreSQL no permite eliminar valores de un enum facilmente.
    # El downgrade deja el valor en el enum (no se puede remover sin recrear).
    pass
