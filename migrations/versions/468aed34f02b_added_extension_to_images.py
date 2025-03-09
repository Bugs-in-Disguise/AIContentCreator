"""added extension to images

Revision ID: 468aed34f02b
Revises: 274a2d26c03c
Create Date: 2025-03-09 04:33:45.427925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '468aed34f02b'
down_revision = '274a2d26c03c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.add_column(sa.Column('extension', sa.String(length=10), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.drop_column('extension')

    # ### end Alembic commands ###
