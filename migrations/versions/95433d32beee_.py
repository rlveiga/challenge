"""empty message

Revision ID: 95433d32beee
Revises: 86de63495c40
Create Date: 2020-02-11 18:27:17.042136

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '95433d32beee'
down_revision = '86de63495c40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('room_association', 'discarded_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('room_association', sa.Column('discarded_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
