"""bloque_a_estudiantes

Revision ID: blqAestud
Revises: blqAdescargo
Create Date: 2026-10-08

Alinea 'estudiantes' con el modelo SQLAlchemy.
- Aplica NOT NULL en 'apellido' (53/53 filas con valor)
- Recrea FK 'docente_id' con ON DELETE SET NULL
- Recrea FK 'grupo_id' con ON DELETE SET NULL
- Recrea FK 'jornada_id' como FK simple (modelo no declara compuesta)
NO toca FK compuesta (sede_id, colegio_id) (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAestud'
down_revision = 'blqAdescargo'
branch_labels = None
depends_on = None


def upgrade():
    # 1. apellido NOT NULL
    op.alter_column('estudiantes', 'apellido', nullable=False)

    # 2. FK docente_id -> docentes(id) ON DELETE SET NULL
    op.drop_constraint('fk_estudiante_docente', 'estudiantes', type_='foreignkey')
    op.create_foreign_key(
        'fk_estudiante_docente',
        'estudiantes', 'docentes',
        ['docente_id'], ['id'],
        ondelete='SET NULL'
    )

    # 3. FK grupo_id -> grupos(id) ON DELETE SET NULL
    op.drop_constraint('fk_estudiante_grupo', 'estudiantes', type_='foreignkey')
    op.create_foreign_key(
        'fk_estudiante_grupo',
        'estudiantes', 'grupos',
        ['grupo_id'], ['id'],
        ondelete='SET NULL'
    )

    # 4. FK jornada_id -> jornadas_colegio(id) ON DELETE RESTRICT (simple)
    op.drop_constraint('fk_estudiante_jornada', 'estudiantes', type_='foreignkey')
    op.create_foreign_key(
        'fk_estudiante_jornada',
        'estudiantes', 'jornadas_colegio',
        ['jornada_id'], ['id'],
        ondelete='RESTRICT'
    )


def downgrade():
    op.drop_constraint('fk_estudiante_jornada', 'estudiantes', type_='foreignkey')
    op.create_foreign_key(
        'fk_estudiante_jornada',
        'estudiantes', 'jornadas_colegio',
        ['colegio_id', 'jornada_id'], ['colegio_id', 'id'],
        ondelete='RESTRICT'
    )
    op.drop_constraint('fk_estudiante_grupo', 'estudiantes', type_='foreignkey')
    op.create_foreign_key(
        'fk_estudiante_grupo',
        'estudiantes', 'grupos',
        ['grupo_id'], ['id'],
        ondelete='RESTRICT'
    )
    op.drop_constraint('fk_estudiante_docente', 'estudiantes', type_='foreignkey')
    op.create_foreign_key(
        'fk_estudiante_docente',
        'estudiantes', 'docentes',
        ['docente_id'], ['id'],
        ondelete='RESTRICT'
    )
    op.alter_column('estudiantes', 'apellido', nullable=True)
