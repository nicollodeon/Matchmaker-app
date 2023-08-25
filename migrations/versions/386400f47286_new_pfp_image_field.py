"""new pfp image field

Revision ID: 386400f47286
Revises: c67d0b4d3a6d
Create Date: 2023-05-01 10:33:41.399107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '386400f47286'
down_revision = 'c67d0b4d3a6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pfp_image', sa.String(length=100), server_default='whale.png', nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('pfp_image')

    # ### end Alembic commands ###
