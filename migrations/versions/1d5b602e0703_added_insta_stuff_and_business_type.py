"""Added insta stuff and business type

Revision ID: 1d5b602e0703
Revises: 84ddec2c7b8c
Create Date: 2025-03-20 18:26:37.966068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d5b602e0703'
down_revision = '84ddec2c7b8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('business_type', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('insta_username', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('insta_password', sa.String(length=255), nullable=False))
        batch_op.create_unique_constraint(None, ['insta_username'])
        batch_op.create_unique_constraint(None, ['insta_password'])
        batch_op.create_unique_constraint(None, ['business_type'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('insta_password')
        batch_op.drop_column('insta_username')
        batch_op.drop_column('business_type')

    # ### end Alembic commands ###
