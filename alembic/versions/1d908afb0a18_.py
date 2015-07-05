"""init database

Revision ID: 1d908afb0a18
Revises: 
Create Date: 2015-07-05 12:19:04.736644

"""

# revision identifiers, used by Alembic.
revision = '1d908afb0a18'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'image',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(250)),
        sa.Column('create_date', sa.String(50))
        )
    op.create_table(
        'group',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(250))
        )
    op.create_table(
        'image_group',
        sa.Column('image_id', sa.Integer, sa.ForeignKey('image.id'),
                  primary_key=True),
        sa.Column('group_id', sa.Integer, sa.ForeignKey('group.id'),
                  primary_key=True)
        )
    op.create_table('operation_type',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('name', sa.String(250)))
    op.create_table('operation', sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('name', sa.String(250)),
                    sa.Column('operation_type_id', sa.Integer,
                              sa.ForeignKey('operation_type.id')))
    op.create_table('operation_group', sa.Column('operation_id', sa.Integer,
                                                 sa.ForeignKey('operation.id'),
                                                 primary_key=True),
                                        sa.Column('group_id', sa.Integer,
                                                  sa.ForeignKey('group.id'),
                                                  primary_key=True))


def downgrade():
    op.drop_table('operation_group')
    op.drop_table('operation')
    op.drop_table('operation_type')
    op.drop_table('image_group')
    op.drop_table('group')
    op.drop_table('image')
