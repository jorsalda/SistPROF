"""campos_piar_y_matricula_estudiante

Revision ID: 7f266f11d152
Revises: 
Create Date: 2026-10-25

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7f266f11d152'
down_revision = 'cfgasistlab' # ⚠️ ALEMBIC LO LLENA AL GENERAR
branch_labels = None
depends_on = None


def upgrade():
    # 1. Ajustes a la tabla 'estudiantes'
    op.add_column('estudiantes', sa.Column('diagnostico_base', sa.Text(), nullable=True))
    op.add_column('estudiantes', sa.Column('requiere_piar', sa.Boolean(), server_default=sa.text('false'), nullable=False))

    # 2. Ajustes a la tabla 'piar' (Decreto 1421)
    op.add_column('piar', sa.Column('contexto_familiar', sa.Text(), nullable=True))
    op.add_column('piar', sa.Column('entidades_apoyo', sa.Text(), nullable=True))
    op.add_column('piar', sa.Column('acta_acuerdo', sa.Text(), nullable=True))
    op.add_column('piar', sa.Column('informe_anual', sa.Text(), nullable=True))


def downgrade():
    # 1. Revertir ajustes a 'piar'
    op.drop_column('piar', 'informe_anual')
    op.drop_column('piar', 'acta_acuerdo')
    op.drop_column('piar', 'entidades_apoyo')
    op.drop_column('piar', 'contexto_familiar')

    # 2. Revertir ajustes a 'estudiantes'
    op.drop_column('estudiantes', 'requiere_piar')
    op.drop_column('estudiantes', 'diagnostico_base')
