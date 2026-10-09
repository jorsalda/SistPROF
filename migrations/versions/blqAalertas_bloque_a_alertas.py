"""bloque_a_alertas

Revision ID: blqAalertas
Revises: 1fd66a0c5a1a
Create Date: 2026-10-07

Renombra columnas de 'alertas' para alinearlas con el modelo SQLAlchemy.
NO elimina datos: usa RENAME en vez de DROP + ADD.
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAalertas'
down_revision = '1fd66a0c5a1a'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Renombrar 'atendida' -> 'activa' (preserva datos)
    op.alter_column('alertas', 'atendida', new_column_name='activa')

    # 2. Renombrar 'fecha' -> 'fecha_creacion' (preserva datos)
    op.alter_column('alertas', 'fecha', new_column_name='fecha_creacion')

    # 3. Ampliar 'tipo' de VARCHAR(50) a VARCHAR(100)
    op.alter_column(
        'alertas', 'tipo',
        existing_type=sa.VARCHAR(length=50),
        type_=sa.String(length=100),
        existing_nullable=False
    )


def downgrade():
    op.alter_column(
        'alertas', 'tipo',
        existing_type=sa.String(length=100),
        type_=sa.VARCHAR(length=50),
        existing_nullable=False
    )
    op.alter_column('alertas', 'fecha_creacion', new_column_name='fecha')
    op.alter_column('alertas', 'activa', new_column_name='atendida')
