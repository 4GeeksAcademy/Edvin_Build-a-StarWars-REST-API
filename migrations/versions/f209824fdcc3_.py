"""empty message

Revision ID: f209824fdcc3
Revises: 7f1c66221c82
Create Date: 2024-12-07 22:34:53.657473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f209824fdcc3'
down_revision = '7f1c66221c82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articlestags', schema=None) as batch_op:
        batch_op.add_column(sa.Column('article_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('tag_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'tags', ['tag_id'], ['id'])
        batch_op.create_foreign_key(None, 'articles', ['article_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articlestags', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('tag_id')
        batch_op.drop_column('article_id')

    # ### end Alembic commands ###
