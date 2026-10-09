"""bloque_a_evidencias

Revision ID: blqAevidencias
Revises: blqAescala
Create Date: 2026-10-07

Alinea 'evidencias' con el modelo SQLAlchemy.
- tipo: VARCHAR(20) NOT NULL -> VARCHAR(100) NULL
- url: TEXT -> VARCHAR(500)
- aprobado: aplicar NOT NULL
- agregar 'fecha_subida' (NOT NULL)
NO elimina 'fecha_creacion' ni 'observacion_admin' (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAevidencias'
down_revision = 'blqAescala'
branch_labels = None
depends_on = None


def upgrade():
    # 1. tipo: VARCHAR(20) NOT NULL -> VARCHAR(100) NULL
    op.alter_column(
        'evidencias', 'tipo',
        existing_type=sa.VARCHAR(length=20),
        type_=sa.String(length=100),
        existing_nullable=False,
        nullable=True
    )

    # 2. url: TEXT -> VARCHAR(500)
    op.alter_column(
        'evidencias', 'url',
        existing_type=sa.Text(),
        type_=sa.String(length=500),
        existing_nullable=True
    )

    # 3. aprobado: aplicar NOT NULL
    op.alter_column('evidencias', 'aprobado', nullable=False)

    # 4. Agregar 'fecha_subida' como nullable primero
    op.add_column('evidencias', sa.Column('fecha_subida', sa.DateTime(), nullable=True))

    # 5. Llenar con NOW() (tabla vacía, práctica correcta)
    op.execute("UPDATE evidencias SET fecha_subida = NOW() WHERE fecha_subida IS NULL")

    # 6. Hacerla NOT NULL
    op.alter_column('evidencias', 'fecha_subida', nullable=False)


def downgrade():
    op.drop_column('evidencias', 'fecha_subida')
    op.alter_column('evidencias', 'aprobado', nullable=True)
    op.alter_column(
        'evidencias', 'url',
        existing_type=sa.String(length=500),
        type_=sa.Text(),
        existing_nullable=True
    )
    op.alter_column(
        'evidencias', 'tipo',
        existing_type=sa.String(length=100),
        type_=sa.VARCHAR(length=20),
        existing_nullable=True,
        nullable=False
    )
