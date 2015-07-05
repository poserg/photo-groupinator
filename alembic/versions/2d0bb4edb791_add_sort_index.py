"""Add sort index

Revision ID: 2d0bb4edb791
Revises: 1d908afb0a18
Create Date: 2015-07-05 12:41:50.335527

"""

# revision identifiers, used by Alembic.
revision = '2d0bb4edb791'
down_revision = '1d908afb0a18'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('operation_group', sa.Column('sort_index', sa.Integer,
                                               default=0))


def downgrade():
    op.drop_column('operation_group', 'sort_index')
