"""bloque_a_jornadas_colegio

Revision ID: blqAjornada
Revises: blqAindlogro
Create Date: 2026-10-08

Alinea 'jornadas_colegio' con el modelo SQLAlchemy.
- Recrea FK 'fk_jornada_sede' con ON DELETE CASCADE
NO elimina el unique 'unique_jornada_colegio' (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAjornada'
down_revision = 'blqAindlogro'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('fk_jornada_sede', 'jornadas_colegio', type_='foreignkey')
    op.create_foreign_key(
        'fk_jornada_sede',
        'jornadas_colegio', 'sedes',
        ['sede_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade():
    op.drop_constraint('fk_jornada_sede', 'jornadas_colegio', type_='foreignkey')
    op.create_foreign_key(
        'fk_jornada_sede',
        'jornadas_colegio', 'sedes',
        ['sede_id'], ['id']
    )
