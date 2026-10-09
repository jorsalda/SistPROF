"""bloque_a_clases

Revision ID: blqAclases
Revises: blqAclaseest
Create Date: 2026-10-08

Alinea 'clases' con el modelo SQLAlchemy.
- Agrega FK colegio_id -> colegios(id)
- Agrega FK grupo_materia_id -> grupo_materias(id) ON DELETE CASCADE
- Aplica NOT NULL en grupo_materia_id
Tabla vacia (0 filas), sin riesgo.
NO elimina 'grupo_id', 'materia_id', unique 'horario_unico', indice 'idx_clases_grupo_materia' (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAclases'
down_revision = 'blqAclaseest'
branch_labels = None
depends_on = None


def upgrade():
    # 1. FK colegio_id -> colegios
    op.create_foreign_key(
        'fk_clase_colegio',
        'clases', 'colegios',
        ['colegio_id'], ['id']
    )

    # 2. FK grupo_materia_id -> grupo_materias ON DELETE CASCADE
    op.create_foreign_key(
        'fk_clase_grupo_materia',
        'clases', 'grupo_materias',
        ['grupo_materia_id'], ['id'],
        ondelete='CASCADE'
    )

    # 3. NOT NULL en grupo_materia_id
    op.alter_column('clases', 'grupo_materia_id', nullable=False)


def downgrade():
    op.alter_column('clases', 'grupo_materia_id', nullable=True)
    op.drop_constraint('fk_clase_grupo_materia', 'clases', type_='foreignkey')
    op.drop_constraint('fk_clase_colegio', 'clases', type_='foreignkey')
