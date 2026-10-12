"""eval_calificacion_nullable

Revision ID: evalnullable
Revises: mall02
Create Date: 2026-10-12

Cambia evaluaciones_estudiante.calificacion de NOT NULL a NULL.
Razon: SistPROF soporta calificacion numerica Y cualitativa.
Un docente puede dejar la calificacion numerica NULL si solo usa el nivel cualitativo.
"""
from alembic import op
import sqlalchemy as sa


revision = 'evalnullable'
down_revision = 'fbca069576ee'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'evaluaciones_estudiante', 'calificacion',
        existing_type=sa.Float(),
        nullable=True
    )


def downgrade():
    op.alter_column(
        'evaluaciones_estudiante', 'calificacion',
        existing_type=sa.Float(),
        nullable=False
    )
