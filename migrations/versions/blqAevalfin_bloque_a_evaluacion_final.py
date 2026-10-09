"""bloque_a_evaluacion_final

Revision ID: blqAevalfin
Revises: blqAevalcrit
Create Date: 2026-10-08

Alinea 'evaluacion_final' con el modelo SQLAlchemy.
- Agrega 'observaciones' (Text, nullable)
- Agrega 'puntaje_final' (Float, nullable)
- Aplica NOT NULL en 'fecha_cierre'
Tabla vacia (0 filas), sin riesgo.
NO toca el unique existente.
NO elimina 'estado' ni 'observaciones_finales' (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAevalfin'
down_revision = 'blqAevalcrit'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('evaluacion_final', sa.Column('observaciones', sa.Text(), nullable=True))
    op.add_column('evaluacion_final', sa.Column('puntaje_final', sa.Float(), nullable=True))
    op.alter_column('evaluacion_final', 'fecha_cierre', nullable=False)


def downgrade():
    op.alter_column('evaluacion_final', 'fecha_cierre', nullable=True)
    op.drop_column('evaluacion_final', 'puntaje_final')
    op.drop_column('evaluacion_final', 'observaciones')
