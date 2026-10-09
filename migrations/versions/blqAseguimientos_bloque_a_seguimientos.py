"""bloque_a_seguimientos

Revision ID: blqAseguim
Revises: blqAjustif
Create Date: 2026-10-07

Alinea 'seguimientos' con el modelo SQLAlchemy.
- Renombra 'observaciones' -> 'observacion'
- Aplica NOT NULL en 'fecha'
NO elimina 'recomendaciones' (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAseguim'
down_revision = 'blqAjustif'
branch_labels = None
depends_on = None


def upgrade():
    # 1. observaciones -> observacion
    op.alter_column('seguimientos', 'observaciones', new_column_name='observacion')

    # 2. Aplicar NOT NULL en 'fecha'
    op.alter_column('seguimientos', 'fecha', nullable=False)


def downgrade():
    op.alter_column('seguimientos', 'fecha', nullable=True)
    op.alter_column('seguimientos', 'observacion', new_column_name='observaciones')
