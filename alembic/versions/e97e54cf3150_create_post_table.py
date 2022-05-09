"""create post table

Revision ID: e97e54cf3150
Revises: 
Create Date: 2022-05-09 14:39:27.148536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e97e54cf3150'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column('id', sa.Integer, nullable = False, primary_key = True), sa.Column('title',sa.String, nullable= False))
    pass


def downgrade():
    op.drop_table("posts")
    pass
