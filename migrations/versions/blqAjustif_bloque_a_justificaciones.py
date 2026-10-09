"""bloque_a_justificaciones_acudiente

Revision ID: blqAjustif
Revises: blqAevidencias
Create Date: 2026-10-07

Alinea 'justificaciones_acudiente' con el modelo SQLAlchemy.
- Agrega 'descripcion' (Text, NOT NULL)
- Aplica NOT NULL en 'fecha'
NO elimina 'justificacion' (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAjustif'
down_revision = 'blqAevidencias'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Agregar 'descripcion' (tabla vacía, NOT NULL directo)
    op.add_column('justificaciones_acudiente', sa.Column('descripcion', sa.Text(), nullable=False))

    # 2. Aplicar NOT NULL en 'fecha'
    op.alter_column('justificaciones_acudiente', 'fecha', nullable=False)


def downgrade():
    op.alter_column('justificaciones_acudiente', 'fecha', nullable=True)
    op.drop_column('justificaciones_acudiente', 'descripcion')
