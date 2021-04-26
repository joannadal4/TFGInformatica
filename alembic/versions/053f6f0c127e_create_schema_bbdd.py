"""Create schema bbdd

Revision ID: 053f6f0c127e
Revises: 
Create Date: 2021-04-26 01:37:05.227711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '053f6f0c127e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('function',
    sa.Column('idFunction', sa.Integer(), nullable=False),
    sa.Column('codeGO', sa.String(length=15), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('aspect', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('idFunction')
    )
    op.create_table('model',
    sa.Column('idModel', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=100), nullable=False),
    sa.Column('path', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('idModel')
    )
    op.create_table('species',
    sa.Column('idSpecies', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('taxonomy', sa.String(length=20), nullable=False),
    sa.Column('isVirus', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('idSpecies')
    )
    op.create_table('protein',
    sa.Column('idProtein', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=15), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('gene', sa.String(length=15), nullable=False),
    sa.Column('location', sa.String(length=100), nullable=False),
    sa.Column('idSpecies', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['idSpecies'], ['species.idSpecies'], ),
    sa.PrimaryKeyConstraint('idProtein')
    )
    op.create_table('interaction',
    sa.Column('idProteinV', sa.Integer(), nullable=False),
    sa.Column('idProteinH', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idProteinH'], ['protein.idProtein'], ),
    sa.ForeignKeyConstraint(['idProteinV'], ['protein.idProtein'], ),
    sa.PrimaryKeyConstraint('idProteinV', 'idProteinH')
    )
    op.create_table('r_protein_function',
    sa.Column('idProtein', sa.Integer(), nullable=False),
    sa.Column('idFunction', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idFunction'], ['function.idFunction'], ),
    sa.ForeignKeyConstraint(['idProtein'], ['protein.idProtein'], ),
    sa.PrimaryKeyConstraint('idProtein', 'idFunction')
    )
    op.create_table('r_protein_modelVPF',
    sa.Column('idProtein', sa.Integer(), nullable=False),
    sa.Column('idModel', sa.Integer(), nullable=False),
    sa.Column('score', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['idModel'], ['model.idModel'], ),
    sa.ForeignKeyConstraint(['idProtein'], ['protein.idProtein'], ),
    sa.PrimaryKeyConstraint('idProtein', 'idModel')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('r_protein_modelVPF')
    op.drop_table('r_protein_function')
    op.drop_table('interaction')
    op.drop_table('protein')
    op.drop_table('species')
    op.drop_table('model')
    op.drop_table('function')
    # ### end Alembic commands ###
