"""empty message

Revision ID: 06760685d24b
Revises: 2033eddb5a46
Create Date: 2020-03-07 16:45:02.930018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06760685d24b'
down_revision = '2033eddb5a46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cards', 'test')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cards', sa.Column('test', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
