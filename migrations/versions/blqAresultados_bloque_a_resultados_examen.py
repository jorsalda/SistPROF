"""bloque_a_resultados_examen

Revision ID: blqAresultados
Revises: blqArespnov
Create Date: 2026-10-08

Alinea resultados_examen con el modelo SQLAlchemy.
- Cambia tipo de nivel de VARCHAR(20) a ENUM niveldesempeno
  (el tipo ENUM ya existe en la BD)
Los 2 registros existentes tienen nivel=NULL, cambio seguro.
NO elimina total_preguntas (Bloque C).
NO toca el unique resultado_unico_estudiante_examen (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAresultados'
down_revision = 'blqArespnov'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'resultados_examen', 'nivel',
        type_=sa.Enum('Bajo', 'Basico', 'Alto', 'Superior', name='niveldesempeno'),
        postgresql_using='nivel::niveldesempeno',
        existing_nullable=True
    )


def downgrade():
    op.alter_column(
        'resultados_examen', 'nivel',
        type_=sa.VARCHAR(length=20),
        postgresql_using='nivel::text',
        existing_nullable=True
    )
