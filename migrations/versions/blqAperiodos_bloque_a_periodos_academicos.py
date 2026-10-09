"""bloque_a_periodos_academicos

Revision ID: blqAperiodos
Revises: blqAnovedad
Create Date: 2026-10-08

Alinea 'periodos_academicos' con el modelo SQLAlchemy.
- Actualiza el periodo de prueba (id=100) con anio=2026
  (en vez de borrarlo, para no disparar el trigger fn_auditar_evaluacion)
- Aplica NOT NULL en 'nombre' y 'anio'
- Recrea FK colegio_id con ON DELETE CASCADE
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAperiodos'
down_revision = 'blqAnovedad'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Actualizar el periodo de prueba (en vez de borrarlo)
    op.execute("UPDATE periodos_academicos SET anio = 2026 WHERE id = 100")

    # 2. nombre NOT NULL
    op.alter_column('periodos_academicos', 'nombre', nullable=False)

    # 3. anio NOT NULL
    op.alter_column('periodos_academicos', 'anio', nullable=False)

    # 4. FK colegio_id con CASCADE
    op.drop_constraint(
        'periodos_academicos_colegio_id_fkey',
        'periodos_academicos', type_='foreignkey'
    )
    op.create_foreign_key(
        'periodos_academicos_colegio_id_fkey',
        'periodos_academicos', 'colegios',
        ['colegio_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade():
    op.drop_constraint(
        'periodos_academicos_colegio_id_fkey',
        'periodos_academicos', type_='foreignkey'
    )
    op.create_foreign_key(
        'periodos_academicos_colegio_id_fkey',
        'periodos_academicos', 'colegios',
        ['colegio_id'], ['id']
    )
    op.alter_column('periodos_academicos', 'anio', nullable=True)
    op.alter_column('periodos_academicos', 'nombre', nullable=True)
