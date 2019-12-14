"""Initial migration

Revision ID: 1fde2eb7fb55
Revises: 
Create Date: 2019-12-14 13:28:41.096516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fde2eb7fb55'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=64), nullable=False))
    op.add_column('users', sa.Column('name', sa.String(length=32), nullable=False))
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'name')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###
