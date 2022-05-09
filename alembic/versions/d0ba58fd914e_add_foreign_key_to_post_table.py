"""add foreign key to post table

Revision ID: d0ba58fd914e
Revises: 78371551c55a
Create Date: 2022-05-09 15:05:20.486683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0ba58fd914e'
down_revision = '78371551c55a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable = False))
    op.create_foreign_key("posts_users_fk", "posts", "users", local_cols= ["owner_id"], remote_cols= ["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("posts_users_fk", "posts")
    op.drop_column("posts", "owner_id")
    pass
