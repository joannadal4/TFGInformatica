"""code String nullable

Revision ID: 192a071c03d3
Revises: 59099a0a9279
Create Date: 2021-07-28 18:49:35.608141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '192a071c03d3'
down_revision = '59099a0a9279'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('protein', 'codeString',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('protein', 'codeString',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
    # ### end Alembic commands ###
