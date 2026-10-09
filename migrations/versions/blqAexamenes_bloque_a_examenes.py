"""bloque_a_examenes

Revision ID: blqAexamenes
Revises: blqAevalest
Create Date: 2026-10-08

Alinea 'examenes' con el modelo SQLAlchemy.
- Borra examenes de prueba id IN (1, 8) que tenian NULLs
- Cambia 'nombre' a nullable (modelo lo pide asi)
- Aplica NOT NULL en materia_id y colegio_id
- Recrea FK materia_id con ON DELETE CASCADE
- Recrea FK colegio_id con ON DELETE CASCADE
NO elimina 'fecha' ni los indices viejos (Bloque C).
La FK duplicada 'fk_examenes_tipo_examen' se deja (deuda tecnica menor).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAexamenes'
down_revision = 'blqAevalest'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Borrar examenes de prueba (los que tienen NULLs)
    op.execute("DELETE FROM examenes WHERE id IN (1, 8)")

    # 2. nombre: nullable
    op.alter_column('examenes', 'nombre', nullable=True)

    # 3. materia_id NOT NULL
    op.alter_column('examenes', 'materia_id', nullable=False)

    # 4. colegio_id NOT NULL
    op.alter_column('examenes', 'colegio_id', nullable=False)

    # 5. Recrear FK materia_id con CASCADE
    op.drop_constraint('examenes_materia_id_fkey', 'examenes', type_='foreignkey')
    op.create_foreign_key(
        'examenes_materia_id_fkey',
        'examenes', 'materias',
        ['materia_id'], ['id'],
        ondelete='CASCADE'
    )

    # 6. Recrear FK colegio_id con CASCADE
    op.drop_constraint('examenes_colegio_id_fkey', 'examenes', type_='foreignkey')
    op.create_foreign_key(
        'examenes_colegio_id_fkey',
        'examenes', 'colegios',
        ['colegio_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade():
    op.drop_constraint('examenes_colegio_id_fkey', 'examenes', type_='foreignkey')
    op.create_foreign_key(
        'examenes_colegio_id_fkey',
        'examenes', 'colegios',
        ['colegio_id'], ['id']
    )
    op.drop_constraint('examenes_materia_id_fkey', 'examenes', type_='foreignkey')
    op.create_foreign_key(
        'examenes_materia_id_fkey',
        'examenes', 'materias',
        ['materia_id'], ['id']
    )
    op.alter_column('examenes', 'colegio_id', nullable=True)
    op.alter_column('examenes', 'materia_id', nullable=True)
    op.alter_column('examenes', 'nombre', nullable=False)
