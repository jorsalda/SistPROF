"""bloque_a_ajustes_razonables

Revision ID: blqAajustes
Revises: blqAacuerdos
Create Date: 2026-10-07

Alinea 'ajustes_razonables' con el modelo SQLAlchemy.
- Agrega columna nueva 'fecha_creacion' (NOT NULL, con default)
- Cambia tipo de 'fecha_aplicacion' DATE -> DateTime
- Aplica NOT NULL en 'aplicado'
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


revision = 'blqAajustes'
down_revision = 'blqAacuerdos'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Agregar 'fecha_creacion' como nullable primero
    op.add_column('ajustes_razonables', sa.Column('fecha_creacion', sa.DateTime(), nullable=True))

    # 2. Llenar con NOW() (tabla vacía, pero es la práctica correcta)
    op.execute("UPDATE ajustes_razonables SET fecha_creacion = NOW() WHERE fecha_creacion IS NULL")

    # 3. Hacerla NOT NULL
    op.alter_column('ajustes_razonables', 'fecha_creacion', nullable=False)

    # 4. Cambiar tipo de 'fecha_aplicacion' DATE -> DateTime
    op.alter_column(
        'ajustes_razonables', 'fecha_aplicacion',
        type_=sa.DateTime(),
        postgresql_using='fecha_aplicacion::timestamp',
        existing_nullable=True
    )

    # 5. Aplicar NOT NULL en 'aplicado' (tabla vacía, sin riesgo)
    op.alter_column('ajustes_razonables', 'aplicado', nullable=False)


def downgrade():
    op.alter_column('ajustes_razonables', 'aplicado', nullable=True)
    op.alter_column(
        'ajustes_razonables', 'fecha_aplicacion',
        type_=sa.Date(),
        postgresql_using='fecha_aplicacion::date',
        existing_nullable=True
    )
    op.drop_column('ajustes_razonables', 'fecha_creacion')
