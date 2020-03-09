"""empty message

Revision ID: afe010c26a14
Revises: 1435f410810b
Create Date: 2020-03-07 19:39:58.164337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afe010c26a14'
down_revision = '1435f410810b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('collections', sa.Column('editable', sa.Boolean(), nullable=True))
    op.drop_column('collections', 'is_deletable')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('collections', sa.Column('is_deletable', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('collections', 'editable')
    # ### end Alembic commands ###
