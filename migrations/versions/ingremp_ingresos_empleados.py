"""extender ingresos_colegio para empleados

Revision ID: ingremp
Revises: citasist
Create Date: 2026-10-12

Extiende ingresos_colegio para permitir registrar asistencia laboral:
- usuario_id int4 NULL FK usuarios(id) ON DELETE CASCADE
- tipo_persona varchar(20) DEFAULT 'estudiante'
- estado_asistencia varchar(20) NULL
- estudiante_id pasa a ser nullable

Valores esperados:
- tipo_persona: 'estudiante', 'empleado'
- estado_asistencia: 'tarde', 'ausente'
"""
from alembic import op
import sqlalchemy as sa


revision = 'ingremp'
down_revision = 'citasist'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('ingresos_colegio', sa.Column('usuario_id', sa.Integer(), nullable=True))
    op.add_column('ingresos_colegio', sa.Column('tipo_persona', sa.String(length=20), server_default=sa.text("'estudiante'"), nullable=True))
    op.add_column('ingresos_colegio', sa.Column('estado_asistencia', sa.String(length=20), nullable=True))
    op.create_foreign_key(
        'fk_ingresos_usuario',
        'ingresos_colegio', 'usuarios',
        ['usuario_id'], ['id'],
        ondelete='CASCADE'
    )
    op.alter_column('ingresos_colegio', 'estudiante_id', nullable=True)


def downgrade():
    op.alter_column('ingresos_colegio', 'estudiante_id', nullable=False)
    op.drop_constraint('fk_ingresos_usuario', 'ingresos_colegio', type_='foreignkey')
    op.drop_column('ingresos_colegio', 'estado_asistencia')
    op.drop_column('ingresos_colegio', 'tipo_persona')
    op.drop_column('ingresos_colegio', 'usuario_id')
