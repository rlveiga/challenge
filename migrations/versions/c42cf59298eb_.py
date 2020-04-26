"""empty message

Revision ID: c42cf59298eb
Revises: b52d1ceb6798
Create Date: 2020-04-26 18:50:50.037783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c42cf59298eb'
down_revision = 'b52d1ceb6798'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('fb_id', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('profile_img', sa.String(), nullable=True))
    op.drop_column('users', 'username')
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('username', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.drop_column('users', 'profile_img')
    op.drop_column('users', 'name')
    op.drop_column('users', 'fb_id')
    # ### end Alembic commands ###
