"""bloque_a_docentes

Revision ID: blqAdocentes
Revises: blqAasist
Create Date: 2026-10-08

Alinea 'docentes' con el modelo SQLAlchemy.
- Cambia 'nombre' de VARCHAR(150) a String(100)
  (verificado: el nombre mas largo tiene 19 caracteres)
NO elimina el indice 'idx_docentes_apellido' (Bloque C).
NO elimina la FK 'fk_docente_sede_colegio' (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAdocentes'
down_revision = 'blqAasist'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'docentes', 'nombre',
        existing_type=sa.VARCHAR(length=150),
        type_=sa.String(length=100),
        existing_nullable=False
    )


def downgrade():
    op.alter_column(
        'docentes', 'nombre',
        existing_type=sa.String(length=100),
        type_=sa.VARCHAR(length=150),
        existing_nullable=False
    )
