"""Relation modelVPF - 

Revision ID: 45cd24480154
Revises: 053f6f0c127e
Create Date: 2021-04-26 18:01:23.537931

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '45cd24480154'
down_revision = '053f6f0c127e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('r_protein_modelVPF')
    op.add_column('protein', sa.Column('idModel', sa.Integer(), nullable=True))
    op.add_column('protein', sa.Column('score', sa.Float(), nullable=True))
    op.create_foreign_key(None, 'protein', 'model', ['idModel'], ['idModel'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'protein', type_='foreignkey')
    op.drop_column('protein', 'score')
    op.drop_column('protein', 'idModel')
    op.create_table('r_protein_modelVPF',
    sa.Column('idProtein', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('idModel', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['idModel'], ['model.idModel'], name='r_protein_modelVPF_idModel_fkey'),
    sa.ForeignKeyConstraint(['idProtein'], ['protein.idProtein'], name='r_protein_modelVPF_idProtein_fkey'),
    sa.PrimaryKeyConstraint('idProtein', 'idModel', name='r_protein_modelVPF_pkey')
    )
    # ### end Alembic commands ###
