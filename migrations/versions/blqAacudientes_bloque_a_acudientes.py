"""bloque_a_acudientes

Revision ID: blqAacud
Revises: blqAsuscrip
Create Date: 2026-10-07

Alinea 'acudientes' con el modelo SQLAlchemy.
- Rellena 'documento' con PENDIENTE-{id} para los 25 NULLs
- Aplica NOT NULL en documento, telefono, direccion
- Agrega UNIQUE en documento
NO elimina el indice 'idx_acudientes_colegio' (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAacud'
down_revision = 'blqAsuscrip'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Rellenar documentos NULL con valor temporal
    op.execute("UPDATE acudientes SET documento = 'PENDIENTE-' || id WHERE documento IS NULL")

    # 2. Aplicar NOT NULL en documento
    op.alter_column('acudientes', 'documento', nullable=False)

    # 3. Aplicar NOT NULL en telefono
    op.alter_column('acudientes', 'telefono', nullable=False)

    # 4. Aplicar NOT NULL en direccion
    op.alter_column('acudientes', 'direccion', nullable=False)

    # 5. UNIQUE en documento
    op.create_unique_constraint(
        'uq_acudientes_documento',
        'acudientes', ['documento']
    )


def downgrade():
    op.drop_constraint('uq_acudientes_documento', 'acudientes', type_='unique')
    op.alter_column('acudientes', 'direccion', nullable=True)
    op.alter_column('acudientes', 'telefono', nullable=True)
    op.alter_column('acudientes', 'documento', nullable=True)
