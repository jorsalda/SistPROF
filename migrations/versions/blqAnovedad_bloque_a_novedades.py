"""bloque_a_novedades

Revision ID: blqAnovedad
Revises: blqAjornada
Create Date: 2026-10-08

Alinea 'novedades' con el modelo SQLAlchemy.
- Agrega FK 'registrada_por' -> usuarios(id)
Tabla vacia (0 filas), sin riesgo.
NO toca enums (ya alineados).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAnovedad'
down_revision = 'blqAjornada'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(
        'fk_novedades_registrada_por',
        'novedades', 'usuarios',
        ['registrada_por'], ['id']
    )


def downgrade():
    op.drop_constraint('fk_novedades_registrada_por', 'novedades', type_='foreignkey')
