"""Add e-value

Revision ID: d4e4a3813115
Revises: 71e637e629c5
Create Date: 2021-05-01 12:58:09.799197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4e4a3813115'
down_revision = '71e637e629c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('protein', 'gene',
               existing_type=sa.VARCHAR(length=15),
               nullable=True)
    op.add_column('r_protein_modelvpf', sa.Column('e_value', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('r_protein_modelvpf', 'e_value')
    op.alter_column('protein', 'gene',
               existing_type=sa.VARCHAR(length=15),
               nullable=False)
    # ### end Alembic commands ###