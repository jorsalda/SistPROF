"""permisos_usuario, fusion_grupos, competencia_contribucion

Revision ID: 1fd66a0c5a1a
Revises: 6b174b4735cd
Create Date: 2026-10-07 12:44:40.627079

Migración mínima: solo crea las 3 tablas nuevas detectadas.
NO elimina columnas, NO cambia tipos, NO toca constraints existentes.
"""
from alembic import op
import sqlalchemy as sa


revision = '1fd66a0c5a1a'
down_revision = '6b174b4735cd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'permisos_usuario',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('clave', sa.String(length=80), nullable=False),
        sa.Column('valor', sa.Boolean(), nullable=False),
        sa.Column('creado_en', sa.DateTime(), nullable=True),
        sa.Column('creado_por', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['creado_por'], ['usuarios.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('usuario_id', 'clave', name='permisos_usuario_usuario_clave_unico'),
    )
    op.create_index('idx_permisos_usuario_id', 'permisos_usuario', ['usuario_id'], unique=False)

    op.create_table(
        'fusion_grupos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('grupo_origen_id', sa.Integer(), nullable=False),
        sa.Column('grupo_destino_id', sa.Integer(), nullable=False),
        sa.Column('fecha', sa.DateTime(), nullable=True),
        sa.Column('observacion', sa.Text(), nullable=True),
        sa.Column('usuario_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['grupo_destino_id'], ['grupos.id']),
        sa.ForeignKeyConstraint(['grupo_origen_id'], ['grupos.id']),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'competencia_contribucion',
        sa.Column('competencia_id', sa.Integer(), nullable=False),
        sa.Column('contribucion_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['competencia_id'], ['competencias.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['contribucion_id'], ['contribuciones.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('competencia_id', 'contribucion_id')
    )


def downgrade():
    op.drop_table('competencia_contribucion')
    op.drop_table('fusion_grupos')
    op.drop_index('idx_permisos_usuario_id', table_name='permisos_usuario')
    op.drop_table('permisos_usuario')
