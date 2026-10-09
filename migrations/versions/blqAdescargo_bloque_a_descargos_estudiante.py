"""bloque_a_descargos_estudiante

Revision ID: blqAdescargo
Revises: blqAcoord
Create Date: 2026-10-08

Alinea 'descargos_estudiante' con el modelo SQLAlchemy.
- Agrega unique en 'novedad_id' (una novedad solo puede tener un descargo)
Tabla vacia (0 filas), sin riesgo.
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAdescargo'
down_revision = 'blqAcoord'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(
        'uq_descargos_estudiante_novedad_id',
        'descargos_estudiante',
        ['novedad_id']
    )


def downgrade():
    op.drop_constraint(
        'uq_descargos_estudiante_novedad_id',
        'descargos_estudiante',
        type_='unique'
    )
