"""bloque_a_escala_evaluacion

Revision ID: blqAescala
Revises: blqAcriterios
Create Date: 2026-10-07

Alinea 'escala_evaluacion' con el modelo SQLAlchemy.
- Borra filas de prueba (4 filas con colegio_id NULL)
- Renombra nota_min -> nota_minima, nota_max -> nota_maxima
- Cambia tipo numeric -> float
- Agrega 'descripcion'
- Amplia 'nombre' a VARCHAR(50)
- Aplica NOT NULL en colegio_id
NO elimina 'tipo_escala' (Bloque C).
"""
from alembic import op
import sqlalchemy as sa


revision = 'blqAescala'
down_revision = 'blqAcriterios'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Borrar filas de prueba
    op.execute("DELETE FROM escala_evaluacion")

    # 2. Renombrar nota_min -> nota_minima
    op.alter_column('escala_evaluacion', 'nota_min', new_column_name='nota_minima')

    # 3. Renombrar nota_max -> nota_maxima
    op.alter_column('escala_evaluacion', 'nota_max', new_column_name='nota_maxima')

    # 4. Cambiar tipo numeric -> float
    op.alter_column(
        'escala_evaluacion', 'nota_minima',
        type_=sa.Float(),
        postgresql_using='nota_minima::double precision'
    )
    op.alter_column(
        'escala_evaluacion', 'nota_maxima',
        type_=sa.Float(),
        postgresql_using='nota_maxima::double precision'
    )

    # 5. Agregar 'descripcion'
    op.add_column('escala_evaluacion', sa.Column('descripcion', sa.Text(), nullable=True))

    # 6. Ampliar 'nombre' a VARCHAR(50)
    op.alter_column(
        'escala_evaluacion', 'nombre',
        existing_type=sa.VARCHAR(length=20),
        type_=sa.String(length=50),
        existing_nullable=False
    )

    # 7. Aplicar NOT NULL en colegio_id (tabla vacía)
    op.alter_column('escala_evaluacion', 'colegio_id', nullable=False)


def downgrade():
    op.alter_column('escala_evaluacion', 'colegio_id', nullable=True)
    op.alter_column(
        'escala_evaluacion', 'nombre',
        existing_type=sa.String(length=50),
        type_=sa.VARCHAR(length=20),
        existing_nullable=False
    )
    op.drop_column('escala_evaluacion', 'descripcion')
    op.alter_column(
        'escala_evaluacion', 'nota_minima',
        type_=sa.NUMERIC(precision=3, scale=2),
        postgresql_using='nota_minima::numeric(3,2)'
    )
    op.alter_column(
        'escala_evaluacion', 'nota_maxima',
        type_=sa.NUMERIC(precision=3, scale=2),
        postgresql_using='nota_maxima::numeric(3,2)'
    )
    op.alter_column('escala_evaluacion', 'nota_maxima', new_column_name='nota_max')
    op.alter_column('escala_evaluacion', 'nota_minima', new_column_name='nota_min')
