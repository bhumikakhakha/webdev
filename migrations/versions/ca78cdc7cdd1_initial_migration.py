"""Initial migration

Revision ID: ca78cdc7cdd1
Revises: 
Create Date: 2021-03-13 02:16:09.058604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca78cdc7cdd1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contact', 'query',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contact', 'query',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    # ### end Alembic commands ###
