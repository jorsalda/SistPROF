"""bloque_a_respuestas_novedad

Revision ID: blqArespnov
Revises: blqApiar
Create Date: 2026-10-08

Alinea 'respuestas_novedad' con el modelo SQLAlchemy.
- Aplica NOT NULL en usuario_id
- Recrea FK usuario_id con ON DELETE CASCADE
- Aplica NOT NULL en fecha
Tabla vacia (0 filas), sin riesgo.
NO elimina la columna 'rol' (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqArespnov'
down_revision = 'blqApiar'
branch_labels = None
depends_on = None


def upgrade():
    # 1. usuario_id NOT NULL
    op.alter_column('respuestas_novedad', 'usuario_id', nullable=False)

    # 2. FK usuario_id con CASCADE
    op.drop_constraint('fk_respuesta_usuario', 'respuestas_novedad', type_='foreignkey')
    op.create_foreign_key(
        'fk_respuesta_usuario',
        'respuestas_novedad', 'usuarios',
        ['usuario_id'], ['id'],
        ondelete='CASCADE'
    )

    # 3. fecha NOT NULL
    op.alter_column('respuestas_novedad', 'fecha', nullable=False)


def downgrade():
    op.alter_column('respuestas_novedad', 'fecha', nullable=True)
    op.drop_constraint('fk_respuesta_usuario', 'respuestas_novedad', type_='foreignkey')
    op.create_foreign_key(
        'fk_respuesta_usuario',
        'respuestas_novedad', 'usuarios',
        ['usuario_id'], ['id'],
        ondelete='SET NULL'
    )
    op.alter_column('respuestas_novedad', 'usuario_id', nullable=True)
