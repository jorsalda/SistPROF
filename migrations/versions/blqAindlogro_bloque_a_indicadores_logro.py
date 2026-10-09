"""bloque_a_indicadores_logro

Revision ID: blqAindlogro
Revises: blqAexamenes
Create Date: 2026-10-08

Alinea 'indicadores_logro' con el modelo SQLAlchemy.
- Aplica NOT NULL en 'descripcion' (48/48 filas con valor)
NO elimina el indice 'uq_indicador_competencia_codigo' (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAindlogro'
down_revision = 'blqAexamenes'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('indicadores_logro', 'descripcion', nullable=False)


def downgrade():
    op.alter_column('indicadores_logro', 'descripcion', nullable=True)
