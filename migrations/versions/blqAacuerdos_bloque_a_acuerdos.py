"""bloque_a_acuerdos_correctivos

Revision ID: blqAacuerdos
Revises: blqAalertas
Create Date: 2026-10-07

Alinea 'acuerdos_correctivos' con el modelo SQLAlchemy.
- Renombra 'compromiso' -> 'compromisos'
- Renombra 'estado' -> 'cumplido' y cambia tipo varchar -> boolean
- Quita el default viejo ('ACTIVO'::varchar) antes de cambiar tipo
NO elimina 'descripcion' (queda para Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAacuerdos'
down_revision = 'blqAalertas'
branch_labels = None
depends_on = None


def upgrade():
    # 1. compromiso -> compromisos
    op.alter_column('acuerdos_correctivos', 'compromiso', new_column_name='compromisos')

    # 2. estado -> cumplido (varchar a boolean)
    #    Primero quitar el default viejo 'ACTIVO'::varchar, que es lo que impide
    #    el cambio de tipo.
    op.execute("ALTER TABLE acuerdos_correctivos ALTER COLUMN estado DROP DEFAULT")

    # 3. Cambiar tipo varchar -> boolean
    op.alter_column(
        'acuerdos_correctivos', 'estado',
        type_=sa.Boolean(),
        postgresql_using='estado::boolean'
    )

    # 4. Renombrar estado -> cumplido
    op.alter_column('acuerdos_correctivos', 'estado', new_column_name='cumplido')

    # 5. Aplicar NOT NULL en 'compromisos' (tabla vacía, sin riesgo)
    op.alter_column('acuerdos_correctivos', 'compromisos', nullable=False)


def downgrade():
    op.alter_column('acuerdos_correctivos', 'compromisos', nullable=True)
    op.alter_column('acuerdos_correctivos', 'cumplido', new_column_name='estado')
    op.alter_column(
        'acuerdos_correctivos', 'estado',
        type_=sa.VARCHAR(length=20),
        existing_nullable=True
    )
    op.execute("ALTER TABLE acuerdos_correctivos ALTER COLUMN estado SET DEFAULT 'ACTIVO'")
    op.alter_column('acuerdos_correctivos', 'compromisos', new_column_name='compromiso')
