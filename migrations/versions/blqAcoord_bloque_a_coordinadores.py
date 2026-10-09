"""bloque_a_coordinadores

Revision ID: blqAcoord
Revises: blqAclases
Create Date: 2026-10-08

Alinea 'coordinadores' con el modelo SQLAlchemy.
- Recrea FK usuario_id con ON DELETE CASCADE
- Reemplaza FK simple 'fk_coordinador_sede' por FK compuesta
  (sede_id, colegio_id) -> sedes(id, colegio_id)
14 filas, todas con FK validas.
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAcoord'
down_revision = 'blqAclases'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Recrear FK usuario_id con CASCADE
    op.drop_constraint('fk_coordinador_usuario', 'coordinadores', type_='foreignkey')
    op.create_foreign_key(
        'fk_coordinador_usuario',
        'coordinadores', 'usuarios',
        ['usuario_id'], ['id'],
        ondelete='CASCADE'
    )

    # 2. Eliminar la FK simple a sedes
    op.drop_constraint('fk_coordinador_sede', 'coordinadores', type_='foreignkey')

    # 3. Agregar FK compuesta
    op.create_foreign_key(
        'fk_coordinador_sede_colegio',
        'coordinadores', 'sedes',
        ['sede_id', 'colegio_id'], ['id', 'colegio_id']
    )


def downgrade():
    op.drop_constraint('fk_coordinador_sede_colegio', 'coordinadores', type_='foreignkey')
    op.create_foreign_key(
        'fk_coordinador_sede',
        'coordinadores', 'sedes',
        ['sede_id'], ['id']
    )
    op.drop_constraint('fk_coordinador_usuario', 'coordinadores', type_='foreignkey')
    op.create_foreign_key(
        'fk_coordinador_usuario',
        'coordinadores', 'usuarios',
        ['usuario_id'], ['id']
    )
