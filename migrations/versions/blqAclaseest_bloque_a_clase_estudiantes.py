"""bloque_a_clase_estudiantes

Revision ID: blqAclaseest
Revises: blqAcmpmat
Create Date: 2026-10-08

Alinea 'clase_estudiantes' con el modelo SQLAlchemy.
Convierte la tabla a PK compuesta (clase_id, estudiante_id).
- Elimina unique 'unica_matricula' (reemplazado por la PK compuesta)
- Elimina columna 'id' (ya no se usa)
- Establece PK compuesta (clase_id, estudiante_id)
Tabla vacia (0 filas), sin riesgo.
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAclaseest'
down_revision = 'blqAcmpmat'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Eliminar el unique (sera redundante con la PK compuesta)
    op.drop_constraint('unica_matricula', 'clase_estudiantes', type_='unique')

    # 2. Eliminar la PK actual (id)
    op.drop_constraint('clase_estudiantes_pkey', 'clase_estudiantes', type_='primary')

    # 3. Eliminar la columna id
    op.drop_column('clase_estudiantes', 'id')

    # 4. Crear la PK compuesta
    op.create_primary_key(
        'clase_estudiantes_pkey',
        'clase_estudiantes',
        ['clase_id', 'estudiante_id']
    )


def downgrade():
    op.drop_constraint('clase_estudiantes_pkey', 'clase_estudiantes', type_='primary')
    op.add_column(
        'clase_estudiantes',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True)
    )
    op.create_primary_key(
        'clase_estudiantes_pkey',
        'clase_estudiantes',
        ['id']
    )
    op.create_unique_constraint(
        'unica_matricula',
        'clase_estudiantes',
        ['clase_id', 'estudiante_id']
    )
