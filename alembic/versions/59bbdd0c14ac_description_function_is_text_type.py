"""Description function is Text type

Revision ID: 59bbdd0c14ac
Revises: d4e4a3813115
Create Date: 2021-05-01 14:22:54.622000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59bbdd0c14ac'
down_revision = 'd4e4a3813115'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('function', 'aspect',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('function', 'aspect',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
    # ### end Alembic commands ###