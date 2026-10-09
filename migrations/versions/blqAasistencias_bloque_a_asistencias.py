"""bloque_a_asistencias

Revision ID: blqAasist
Revises: blqAacEval
Create Date: 2026-10-07

Alinea 'asistencias' con el modelo SQLAlchemy.
- clase_id: NOT NULL -> nullable
NO elimina el unique 'unica_asistencia_por_clase' (se mantiene por proteccion).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAasist'
down_revision = 'blqAacEval'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('asistencias', 'clase_id', nullable=True)


def downgrade():
    op.alter_column('asistencias', 'clase_id', nullable=False)
