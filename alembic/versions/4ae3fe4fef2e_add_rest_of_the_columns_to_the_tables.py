"""add rest of the columns to the tables

Revision ID: 4ae3fe4fef2e
Revises: d0ba58fd914e
Create Date: 2022-05-09 15:10:27.680957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ae3fe4fef2e'
down_revision = 'd0ba58fd914e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean, nullable = False, server_default = "true"))
    op.add_column( "posts", sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
    server_default = sa.func.now(), nullable = False))
    pass


def downgrade():
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")
    pass
