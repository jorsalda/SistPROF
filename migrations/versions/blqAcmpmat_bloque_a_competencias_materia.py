"""bloque_a_competencias_materia

Revision ID: blqAcmpmat
Revises: blqAdocentes
Create Date: 2026-10-08

Alinea 'competencias_materia' con el modelo SQLAlchemy.
- Aplica NOT NULL en nombre y materia_id (12/12 filas con valor)
- Cambia porcentaje de NUMERIC a Float
- Recrea FK materia_id con ON DELETE CASCADE
- Agrega FK grupo_id -> grupos (la columna ya existe, solo falta la FK)
NO elimina 'activo' (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAcmpmat'
down_revision = 'blqAdocentes'
branch_labels = None
depends_on = None


def upgrade():
    # 1. nombre: NOT NULL
    op.alter_column('competencias_materia', 'nombre', nullable=False)

    # 2. materia_id: NOT NULL
    op.alter_column('competencias_materia', 'materia_id', nullable=False)

    # 3. porcentaje: NUMERIC -> Float
    op.alter_column(
        'competencias_materia', 'porcentaje',
        type_=sa.Float(),
        postgresql_using='porcentaje::double precision'
    )

    # 4. Recrear FK materia_id con CASCADE
    op.drop_constraint(
        'competencias_materia_materia_id_fkey',
        'competencias_materia', type_='foreignkey'
    )
    op.create_foreign_key(
        'competencias_materia_materia_id_fkey',
        'competencias_materia', 'materias',
        ['materia_id'], ['id'],
        ondelete='CASCADE'
    )

    # 5. Agregar FK grupo_id -> grupos (la columna ya existe, solo la FK)
    op.create_foreign_key(
        'fk_competencias_materia_grupo',
        'competencias_materia', 'grupos',
        ['grupo_id'], ['id'],
        ondelete='SET NULL'
    )


def downgrade():
    op.drop_constraint('fk_competencias_materia_grupo', 'competencias_materia', type_='foreignkey')
    op.drop_constraint('competencias_materia_materia_id_fkey', 'competencias_materia', type_='foreignkey')
    op.create_foreign_key(
        'competencias_materia_materia_id_fkey',
        'competencias_materia', 'materias',
        ['materia_id'], ['id']
    )
    op.alter_column(
        'competencias_materia', 'porcentaje',
        type_=sa.NUMERIC(precision=5, scale=2),
        postgresql_using='porcentaje::numeric(5,2)'
    )
    op.alter_column('competencias_materia', 'materia_id', nullable=True)
    op.alter_column('competencias_materia', 'nombre', nullable=True)
