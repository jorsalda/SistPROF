"""bloque_a_evaluaciones_estudiante

Revision ID: blqAevalest
Revises: blqAevalfin
Create Date: 2026-10-08

Alinea 'evaluaciones_estudiante' con el modelo SQLAlchemy.
- Cambia tipo de calificacion NUMERIC(4,2) -> Float
- Aplica NOT NULL en calificacion, estudiante_id, indicador_id, periodo_id
  (20/20 filas con valor)
- Recrea FK estudiante_id con ON DELETE CASCADE
- Recrea FK periodo_id con ON DELETE CASCADE
La FK indicador_id ya tiene CASCADE, no se toca.
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAevalest'
down_revision = 'blqAevalfin'
branch_labels = None
depends_on = None


def upgrade():
    # 1. calificacion: NUMERIC -> Float
    op.alter_column(
        'evaluaciones_estudiante', 'calificacion',
        type_=sa.Float(),
        postgresql_using='calificacion::double precision'
    )

    # 2. NOT NULL en las columnas (todas tienen valor)
    op.alter_column('evaluaciones_estudiante', 'calificacion', nullable=False)
    op.alter_column('evaluaciones_estudiante', 'estudiante_id', nullable=False)
    op.alter_column('evaluaciones_estudiante', 'indicador_id', nullable=False)
    op.alter_column('evaluaciones_estudiante', 'periodo_id', nullable=False)

    # 3. Recrear FK estudiante_id con CASCADE
    op.drop_constraint(
        'evaluaciones_estudiante_estudiante_id_fkey',
        'evaluaciones_estudiante', type_='foreignkey'
    )
    op.create_foreign_key(
        'evaluaciones_estudiante_estudiante_id_fkey',
        'evaluaciones_estudiante', 'estudiantes',
        ['estudiante_id'], ['id'],
        ondelete='CASCADE'
    )

    # 4. Recrear FK periodo_id con CASCADE
    op.drop_constraint(
        'evaluaciones_estudiante_periodo_id_fkey',
        'evaluaciones_estudiante', type_='foreignkey'
    )
    op.create_foreign_key(
        'evaluaciones_estudiante_periodo_id_fkey',
        'evaluaciones_estudiante', 'periodos_academicos',
        ['periodo_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade():
    op.drop_constraint(
        'evaluaciones_estudiante_periodo_id_fkey',
        'evaluaciones_estudiante', type_='foreignkey'
    )
    op.create_foreign_key(
        'evaluaciones_estudiante_periodo_id_fkey',
        'evaluaciones_estudiante', 'periodos_academicos',
        ['periodo_id'], ['id']
    )
    op.drop_constraint(
        'evaluaciones_estudiante_estudiante_id_fkey',
        'evaluaciones_estudiante', type_='foreignkey'
    )
    op.create_foreign_key(
        'evaluaciones_estudiante_estudiante_id_fkey',
        'evaluaciones_estudiante', 'estudiantes',
        ['estudiante_id'], ['id']
    )
    op.alter_column('evaluaciones_estudiante', 'periodo_id', nullable=True)
    op.alter_column('evaluaciones_estudiante', 'indicador_id', nullable=True)
    op.alter_column('evaluaciones_estudiante', 'estudiante_id', nullable=True)
    op.alter_column('evaluaciones_estudiante', 'calificacion', nullable=True)
    op.alter_column(
        'evaluaciones_estudiante', 'calificacion',
        type_=sa.NUMERIC(precision=4, scale=2),
        postgresql_using='calificacion::numeric(4,2)'
    )
