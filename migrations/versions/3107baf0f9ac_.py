"""empty message

Revision ID: 3107baf0f9ac
Revises: 6dce884bb111
Create Date: 2019-12-17 13:37:25.603855

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3107baf0f9ac'
down_revision = '6dce884bb111'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('association', 'date_joined',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('association', 'room_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('association', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.add_column('rooms', sa.Column('created_by', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rooms', 'created_by')
    op.alter_column('association', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('association', 'room_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('association', 'date_joined',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###
