"""agregar columnas notificada y editada a novedades

Revision ID: noveditada
Revises: enumtiposnov
Create Date: 2026-10-12

Agrega a la tabla novedades:
- notificada boolean DEFAULT false (si se envio correo al acudiente)
- editada_en timestamp NULL (cuando se edito por ultima vez)
- editada_por int4 NULL FK usuarios(id) ON DELETE SET NULL (quien edito)
"""
from alembic import op
import sqlalchemy as sa


revision = 'noveditada'
down_revision = 'enumtiposnov'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('novedades', sa.Column('notificada', sa.Boolean(), server_default=sa.text('false'), nullable=True))
    op.add_column('novedades', sa.Column('editada_en', sa.DateTime(), nullable=True))
    op.add_column('novedades', sa.Column('editada_por', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_novedades_editada_por',
        'novedades', 'usuarios',
        ['editada_por'], ['id'],
        ondelete='SET NULL'
    )


def downgrade():
    op.drop_constraint('fk_novedades_editada_por', 'novedades', type_='foreignkey')
    op.drop_column('novedades', 'editada_por')
    op.drop_column('novedades', 'editada_en')
    op.drop_column('novedades', 'notificada')
