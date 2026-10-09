"""bloque_a_criterios_evaluacion

Revision ID: blqAcriterios
Revises: blqAcontrib
Create Date: 2026-10-07

Alinea 'criterios_evaluacion' con el modelo SQLAlchemy.
- Agrega columnas: area_gestion_id, nombre, porcentaje
- Cambia descripcion de NOT NULL a nullable
NO elimina 'contribucion_id' ni 'fecha_creacion' (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAcriterios'
down_revision = 'blqAcontrib'
branch_labels = None
depends_on = None


def upgrade():
    # 1. area_gestion_id (FK a areas_gestion, nullable)
    op.add_column('criterios_evaluacion', sa.Column('area_gestion_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_criterios_area_gestion',
        'criterios_evaluacion', 'areas_gestion',
        ['area_gestion_id'], ['id']
    )

    # 2. nombre (VARCHAR 255, NOT NULL - tabla vacía)
    op.add_column('criterios_evaluacion', sa.Column('nombre', sa.String(length=255), nullable=False))

    # 3. porcentaje (Float, default 0)
    op.add_column('criterios_evaluacion', sa.Column('porcentaje', sa.Float(), nullable=True))

    # 4. descripcion: NOT NULL -> nullable
    op.alter_column('criterios_evaluacion', 'descripcion', nullable=True)


def downgrade():
    op.alter_column('criterios_evaluacion', 'descripcion', nullable=False)
    op.drop_column('criterios_evaluacion', 'porcentaje')
    op.drop_column('criterios_evaluacion', 'nombre')
    op.drop_constraint('fk_criterios_area_gestion', 'criterios_evaluacion', type_='foreignkey')
    op.drop_column('criterios_evaluacion', 'area_gestion_id')
