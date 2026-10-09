"""bloque_a_suscripciones

Revision ID: blqAsuscrip
Revises: blqAseguim
Create Date: 2026-10-07

Alinea 'suscripciones' con el modelo SQLAlchemy.
- Agrega 'plan' (String 100, NOT NULL)
- Cambia fecha_inicio y fecha_fin de TIMESTAMP a Date
- Agrega 'activa' (Boolean)
- Agrega 'fecha_creacion' (DateTime)
NO elimina 'precio_base', 'limite_sedes', 'en_prueba', 'activo' (Bloque C).
NO elimina el unique 'unico_colegio_suscripcion' (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAsuscrip'
down_revision = 'blqAseguim'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Agregar 'plan' (tabla vacía, NOT NULL directo)
    op.add_column('suscripciones', sa.Column('plan', sa.String(length=100), nullable=False))

    # 2. fecha_inicio: TIMESTAMP -> Date
    op.alter_column(
        'suscripciones', 'fecha_inicio',
        type_=sa.Date(),
        postgresql_using='fecha_inicio::date'
    )

    # 3. fecha_fin: TIMESTAMP -> Date
    op.alter_column(
        'suscripciones', 'fecha_fin',
        type_=sa.Date(),
        postgresql_using='fecha_fin::date'
    )

    # 4. Agregar 'activa' (Boolean)
    op.add_column('suscripciones', sa.Column('activa', sa.Boolean(), nullable=True))

    # 5. Agregar 'fecha_creacion' (DateTime)
    op.add_column('suscripciones', sa.Column('fecha_creacion', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('suscripciones', 'fecha_creacion')
    op.drop_column('suscripciones', 'activa')
    op.alter_column(
        'suscripciones', 'fecha_fin',
        type_=sa.TIMESTAMP(),
        postgresql_using='fecha_fin::timestamp'
    )
    op.alter_column(
        'suscripciones', 'fecha_inicio',
        type_=sa.TIMESTAMP(),
        postgresql_using='fecha_inicio::timestamp'
    )
    op.drop_column('suscripciones', 'plan')
