"""modificar piar: agregar docente_id, materia_id y cambiar unico

Revision ID: piar02
Revises: piar01
Create Date: 2026-10-08

Modulo PIAR: convierte el PIAR en uno-por-estudiante-por-docente-por-materia.
- Agrega docente_id (FK a docentes, ON DELETE CASCADE)
- Agrega materia_id (FK a materias, ON DELETE CASCADE)
- Elimina el indice unico_piar_activo (ya no aplica)
- Crea nuevo indice unico por (estudiante_id, docente_id, materia_id) WHERE activo = true
Tabla vacia (0 filas), sin riesgo.
"""
from alembic import op
import sqlalchemy as sa


revision = 'piar02'
down_revision = 'piar01'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Agregar columnas
    op.add_column('piar', sa.Column('docente_id', sa.Integer(), nullable=True))
    op.add_column('piar', sa.Column('materia_id', sa.Integer(), nullable=True))

    # 2. FKs
    op.create_foreign_key(
        'fk_piar_docente',
        'piar', 'docentes',
        ['docente_id'], ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'fk_piar_materia',
        'piar', 'materias',
        ['materia_id'], ['id'],
        ondelete='CASCADE'
    )

    # 3. Eliminar el unique viejo
    op.drop_index('unico_piar_activo', table_name='piar')

    # 4. Crear el nuevo unique parcial
    op.create_index(
        'unico_piar_activo_por_materia',
        'piar',
        ['estudiante_id', 'docente_id', 'materia_id'],
        unique=True,
        postgresql_where=sa.text('activo = true')
    )


def downgrade():
    op.drop_index('unico_piar_activo_por_materia', table_name='piar')
    op.create_index(
        'unico_piar_activo',
        'piar',
        ['estudiante_id'],
        unique=True,
        postgresql_where=sa.text('activo = true')
    )
    op.drop_constraint('fk_piar_materia', 'piar', type_='foreignkey')
    op.drop_constraint('fk_piar_docente', 'piar', type_='foreignkey')
    op.drop_column('piar', 'materia_id')
    op.drop_column('piar', 'docente_id')
