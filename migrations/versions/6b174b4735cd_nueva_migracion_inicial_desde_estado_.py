"""Baseline del estado actual de la base de datos.

Esta revisión se usa para reiniciar la historia de Alembic tomando como
punto de partida un esquema que YA existe y que representa el estado actual
del proyecto.

Revision ID: 6b174b4735cd
Revises:
Create Date: 2026-09-03 17:30:30.741337
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6b174b4735cd"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Baseline: no modifica la base de datos existente."""
    pass


def downgrade():
    """No hay migración anterior a la cual regresar."""
    pass
