"""add user table

Revision ID: 78371551c55a
Revises: 466e29d75604
Create Date: 2022-05-09 14:56:33.406424

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78371551c55a'
down_revision = '466e29d75604'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
        sa.Column('id', sa.Integer, nullable = False), 
        sa.Column('email', sa.String, nullable = False), 
        sa.Column('password', sa.String, nullable = False), 
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default = sa.func.now(), nullable = False), 
        sa.PrimaryKeyConstraint('id'), 
        sa.UniqueConstraint("email"))
    pass


def downgrade():
    op.drop_table("users")
    pass
