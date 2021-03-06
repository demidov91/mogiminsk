"""Initial migration.

Revision ID: d1e16f83f626
Revises: 
Create Date: 2018-11-26 15:54:17.399506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1e16f83f626'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mogiminsk_trip', sa.Column('external_identifier', sa.String(length=63), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mogiminsk_trip', 'external_identifier')
    # ### end Alembic commands ###
