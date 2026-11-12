"""add_alertas_recuperacion_justificacion

Revision ID: 52c3a04bdaa1
Revises: exam_ctx
Create Date: 2026-11-12 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52c3a04bdaa1'
down_revision = 'exam_ctx' # O la revisión que tengas actualmente en la cabeza (head)
branch_labels = None
depends_on = None


def upgrade():
    # 1. Nuevas columnas en Colegio
    op.add_column('colegios', sa.Column('activa_recuperacion', sa.Boolean(), nullable=False, server_default=sa.text('false')))
    op.add_column('colegios', sa.Column('nota_minima_recuperacion', sa.Numeric(precision=4, scale=2), nullable=True, server_default=sa.text('3.0')))

    # 2. Nueva columna en JustificacionAcudiente
    op.add_column('justificaciones_acudiente', sa.Column('justificacion', sa.Text(), nullable=True))

    # 3. Nueva tabla Alerta
    op.create_table('alertas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('estudiante_id', sa.Integer(), nullable=False),
        sa.Column('tipo', sa.String(length=100), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=False),
        sa.Column('activa', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('fecha_creacion', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('atendida', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('atendida_por', sa.Integer(), nullable=True),
        sa.Column('fecha_atencion', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['atendida_por'], ['usuarios.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['estudiante_id'], ['estudiantes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # Deshacer los cambios en orden inverso
    op.drop_table('alertas')
    op.drop_column('justificaciones_acudiente', 'justificacion')
    op.drop_column('colegios', 'nota_minima_recuperacion')
    op.drop_column('colegios', 'activa_recuperacion')