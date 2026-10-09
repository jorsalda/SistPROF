"""bloque_a_evaluacion_criterio

Revision ID: blqAevalcrit
Revises: blqAestud
Create Date: 2026-10-08

Alinea 'evaluacion_criterio' con el modelo SQLAlchemy.
- Renombra unique 'unica_eval_por_criterio' -> 'unique_evaluacion_criterio'
- Renombra check 'chk_calificacion_valida' -> 'check_calificacion_rango'
- Cambia tipo de calificacion NUMERIC(4,2) -> Float
Tabla vacia (0 filas), sin riesgo.
NO elimina el indice 'idx_evalcriterio_evalfinal' (Bloque C).
Las FKs se mantienen como estan (con CASCADE util).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAevalcrit'
down_revision = 'blqAestud'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Renombrar unique
    op.drop_constraint('unica_eval_por_criterio', 'evaluacion_criterio', type_='unique')
    op.create_unique_constraint(
        'unique_evaluacion_criterio',
        'evaluacion_criterio',
        ['evaluacion_final_id', 'criterio_id']
    )

    # 2. Renombrar check
    op.drop_constraint('chk_calificacion_valida', 'evaluacion_criterio', type_='check')
    op.create_check_constraint(
        'check_calificacion_rango',
        'evaluacion_criterio',
        'calificacion >= 0 AND calificacion <= 5'
    )

    # 3. Cambiar tipo NUMERIC -> Float
    op.alter_column(
        'evaluacion_criterio', 'calificacion',
        type_=sa.Float(),
        postgresql_using='calificacion::double precision'
    )


def downgrade():
    op.alter_column(
        'evaluacion_criterio', 'calificacion',
        type_=sa.NUMERIC(precision=4, scale=2),
        postgresql_using='calificacion::numeric(4,2)'
    )
    op.drop_constraint('check_calificacion_rango', 'evaluacion_criterio', type_='check')
    op.create_check_constraint(
        'chk_calificacion_valida',
        'evaluacion_criterio',
        'calificacion >= 0 AND calificacion <= 5'
    )
    op.drop_constraint('unique_evaluacion_criterio', 'evaluacion_criterio', type_='unique')
    op.create_unique_constraint(
        'unica_eval_por_criterio',
        'evaluacion_criterio',
        ['evaluacion_final_id', 'criterio_id']
    )
