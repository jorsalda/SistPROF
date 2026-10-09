"""bloque_a_contribuciones

Revision ID: blqAcontrib
Revises: blqAajustes
Create Date: 2026-10-07

Alinea 'contribuciones' con el modelo SQLAlchemy.
- Agrega columna 'criterio_id' (FK a criterios_evaluacion)
NO elimina 'competencia_id', 'orden', 'fecha_creacion', 'activo' (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAcontrib'
down_revision = 'blqAajustes'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Agregar 'criterio_id' como nullable primero (para no fallar si hay filas)
    op.add_column('contribuciones', sa.Column('criterio_id', sa.Integer(), nullable=True))

    # 2. FK
    op.create_foreign_key(
        'fk_contribuciones_criterio_id',
        'contribuciones', 'criterios_evaluacion',
        ['criterio_id'], ['id'],
        ondelete='CASCADE'
    )

    # 3. NOT NULL (tabla vacía, sin riesgo)
    op.alter_column('contribuciones', 'criterio_id', nullable=False)


def downgrade():
    op.drop_constraint('fk_contribuciones_criterio_id', 'contribuciones', type_='foreignkey')
    op.drop_column('contribuciones', 'criterio_id')
