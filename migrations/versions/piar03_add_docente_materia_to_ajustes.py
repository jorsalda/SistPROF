"""modificar ajustes_razonables: agregar docente_id y materia_id

Revision ID: piar03
Revises: piar02
Create Date: 2026-10-08

Modulo PIAR: registra quien aplico el ajuste y en que materia.
- Agrega docente_id (FK a docentes, ON DELETE SET NULL)
- Agrega materia_id (FK a materias, ON DELETE SET NULL)
Tabla vacia (0 filas), sin riesgo.
"""
from alembic import op
import sqlalchemy as sa


revision = 'piar03'
down_revision = 'piar02'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('ajustes_razonables', sa.Column('docente_id', sa.Integer(), nullable=True))
    op.add_column('ajustes_razonables', sa.Column('materia_id', sa.Integer(), nullable=True))

    op.create_foreign_key(
        'fk_ajustes_docente',
        'ajustes_razonables', 'docentes',
        ['docente_id'], ['id'],
        ondelete='SET NULL'
    )
    op.create_foreign_key(
        'fk_ajustes_materia',
        'ajustes_razonables', 'materias',
        ['materia_id'], ['id'],
        ondelete='SET NULL'
    )


def downgrade():
    op.drop_constraint('fk_ajustes_materia', 'ajustes_razonables', type_='foreignkey')
    op.drop_constraint('fk_ajustes_docente', 'ajustes_razonables', type_='foreignkey')
    op.drop_column('ajustes_razonables', 'materia_id')
    op.drop_column('ajustes_razonables', 'docente_id')
