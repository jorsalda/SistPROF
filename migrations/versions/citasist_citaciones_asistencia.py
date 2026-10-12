"""agregar columnas de asistencia a citaciones_acudiente

Revision ID: citasist
Revises: noveditada
Create Date: 2026-10-12

Agrega a citaciones_acudiente:
- asistio boolean DEFAULT false (si el acudiente asistio)
- fecha_asistencia timestamp NULL (cuando asistio)
- registrado_por int4 NULL FK usuarios(id) ON DELETE SET NULL (quien registro)
- notificado_inasistencia boolean DEFAULT false (si ya se notifico la inasistencia)
"""
from alembic import op
import sqlalchemy as sa


revision = 'citasist'
down_revision = 'noveditada'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('citaciones_acudiente', sa.Column('asistio', sa.Boolean(), server_default=sa.text('false'), nullable=True))
    op.add_column('citaciones_acudiente', sa.Column('fecha_asistencia', sa.DateTime(), nullable=True))
    op.add_column('citaciones_acudiente', sa.Column('registrado_por', sa.Integer(), nullable=True))
    op.add_column('citaciones_acudiente', sa.Column('notificado_inasistencia', sa.Boolean(), server_default=sa.text('false'), nullable=True))
    op.create_foreign_key(
        'fk_citaciones_registrado_por',
        'citaciones_acudiente', 'usuarios',
        ['registrado_por'], ['id'],
        ondelete='SET NULL'
    )


def downgrade():
    op.drop_constraint('fk_citaciones_registrado_por', 'citaciones_acudiente', type_='foreignkey')
    op.drop_column('citaciones_acudiente', 'notificado_inasistencia')
    op.drop_column('citaciones_acudiente', 'registrado_por')
    op.drop_column('citaciones_acudiente', 'fecha_asistencia')
    op.drop_column('citaciones_acudiente', 'asistio')
