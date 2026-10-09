"""bloque_a_usuarios

Revision ID: blqAusuarios
Revises: blqAresultados
Create Date: 2026-10-08

Alinea usuarios con el modelo SQLAlchemy.
- Elimina la columna is_superadmin (redundante con la property Python,
  verificacion previa confirmo que su valor coincide 100% con rol)
NO elimina los indices idx_usuarios_* (Bloque C, utiles).
NO elimina la FK compuesta fk_usuario_sede_colegio (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAusuarios'
down_revision = 'blqAresultados'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('usuarios', 'is_superadmin')


def downgrade():
    op.add_column(
        'usuarios',
        sa.Column('is_superadmin', sa.Boolean(), nullable=True, server_default=sa.text('false'))
    )
