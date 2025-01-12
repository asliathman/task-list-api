"""updated task model to inculde a to_dict() instance method

Revision ID: a1d8b40c86bd
Revises: e6ab93caa2d3
Create Date: 2021-11-04 11:23:22.509777

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1d8b40c86bd'
down_revision = 'e6ab93caa2d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('goal', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('goal', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
