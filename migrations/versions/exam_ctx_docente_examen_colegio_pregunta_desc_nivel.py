"""docente_examen_colegio_pregunta_desc_nivel

Revision ID: exam_ctx
Revises: permisos_estado
Create Date: 2026-11-05

Agrega:
- examenes.docente_id (FK a docentes)
- indicadores_logro.descripcion_nivel
- preguntas.colegio_id (FK a colegios)
"""
from alembic import op
import sqlalchemy as sa


revision = 'exam_ctx'
down_revision = 'permisos_estado'
branch_labels = None
depends_on = None


def upgrade():
    # 1. examenes.docente_id
    op.add_column('examenes', sa.Column('docente_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_examenes_docente',
        'examenes', 'docentes',
        ['docente_id'], ['id']
    )

    # 2. indicadores_logro.descripcion_nivel
    op.add_column('indicadores_logro', sa.Column('descripcion_nivel', sa.Text(), nullable=True))

    # 3. preguntas.colegio_id
    op.add_column('preguntas', sa.Column('colegio_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_preguntas_colegio',
        'preguntas', 'colegios',
        ['colegio_id'], ['id']
    )


def downgrade():
    op.drop_constraint('fk_preguntas_colegio', 'preguntas', type_='foreignkey')
    op.drop_column('preguntas', 'colegio_id')
    op.drop_column('indicadores_logro', 'descripcion_nivel')
    op.drop_constraint('fk_examenes_docente', 'examenes', type_='foreignkey')
    op.drop_column('examenes', 'docente_id')
