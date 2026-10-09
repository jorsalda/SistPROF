"""bloque_a_piar

Revision ID: blqApiar
Revises: blqAperiodos
Create Date: 2026-10-08

Alinea 'piar' con el modelo SQLAlchemy.
- Aplica NOT NULL en 'fecha_inicio' y 'activo'
Tabla vacia (0 filas), sin riesgo.
NO elimina el indice 'unico_piar_activo' (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqApiar'
down_revision = 'blqAperiodos'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('piar', 'fecha_inicio', nullable=False)
    op.alter_column('piar', 'activo', nullable=False)


def downgrade():
    op.alter_column('piar', 'activo', nullable=True)
    op.alter_column('piar', 'fecha_inicio', nullable=True)
