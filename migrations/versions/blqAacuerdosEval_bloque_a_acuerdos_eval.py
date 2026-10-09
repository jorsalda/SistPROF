"""bloque_a_acuerdos_evaluacion

Revision ID: blqAacEval
Revises: blqAacud
Create Date: 2026-10-07

Alinea 'acuerdos_evaluacion' con el modelo SQLAlchemy.
- Aplica NOT NULL en 'estado' y 'fecha_creacion'
- Quita default de BD en 'fecha_creacion'
- Renombra unique 'unico_docente_anio' -> 'unique_docente_anio'
- Recrea FK 'docente_id' sin ON DELETE CASCADE
- Recrea FK 'colegio_id' sin ON DELETE CASCADE
NO toca el enum 'estado_acuerdo' (ya tiene los valores correctos en BD).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAacEval'
down_revision = 'blqAacud'
branch_labels = None
depends_on = None


def upgrade():
    # 1. estado NOT NULL
    op.alter_column('acuerdos_evaluacion', 'estado', nullable=False)

    # 2. fecha_creacion NOT NULL + quitar default de BD
    op.alter_column('acuerdos_evaluacion', 'fecha_creacion', nullable=False)
    op.execute("ALTER TABLE acuerdos_evaluacion ALTER COLUMN fecha_creacion DROP DEFAULT")

    # 3. Renombrar unique
    op.drop_constraint('unico_docente_anio', 'acuerdos_evaluacion', type_='unique')
    op.create_unique_constraint('unique_docente_anio', 'acuerdos_evaluacion', ['docente_id', 'anio'])

    # 4. FK docente_id sin CASCADE
    op.drop_constraint('fk_acuerdo_docente', 'acuerdos_evaluacion', type_='foreignkey')
    op.create_foreign_key(
        'fk_acuerdo_docente',
        'acuerdos_evaluacion', 'docentes',
        ['docente_id'], ['id']
    )

    # 5. FK colegio_id sin CASCADE
    op.drop_constraint('fk_acuerdo_colegio', 'acuerdos_evaluacion', type_='foreignkey')
    op.create_foreign_key(
        'fk_acuerdo_colegio',
        'acuerdos_evaluacion', 'colegios',
        ['colegio_id'], ['id']
    )


def downgrade():
    op.drop_constraint('fk_acuerdo_colegio', 'acuerdos_evaluacion', type_='foreignkey')
    op.create_foreign_key(
        'fk_acuerdo_colegio',
        'acuerdos_evaluacion', 'colegios',
        ['colegio_id'], ['id'],
        ondelete='CASCADE'
    )
    op.drop_constraint('fk_acuerdo_docente', 'acuerdos_evaluacion', type_='foreignkey')
    op.create_foreign_key(
        'fk_acuerdo_docente',
        'acuerdos_evaluacion', 'docentes',
        ['docente_id'], ['id'],
        ondelete='CASCADE'
    )
    op.drop_constraint('unique_docente_anio', 'acuerdos_evaluacion', type_='unique')
    op.create_unique_constraint('unico_docente_anio', 'acuerdos_evaluacion', ['docente_id', 'anio'])
    op.execute("ALTER TABLE acuerdos_evaluacion ALTER COLUMN fecha_creacion SET DEFAULT CURRENT_TIMESTAMP")
    op.alter_column('acuerdos_evaluacion', 'fecha_creacion', nullable=True)
    op.alter_column('acuerdos_evaluacion', 'estado', nullable=True)
