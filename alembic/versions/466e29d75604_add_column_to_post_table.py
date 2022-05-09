"""add column to post table

Revision ID: 466e29d75604
Revises: e97e54cf3150
Create Date: 2022-05-09 14:52:13.890828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '466e29d75604'
down_revision = 'e97e54cf3150'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String, nullable = False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
