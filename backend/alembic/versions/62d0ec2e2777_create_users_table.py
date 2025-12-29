"""create_users_table

Revision ID: 62d0ec2e2777
Revises:
Create Date: 2025-12-29 13:46:46.740789

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '62d0ec2e2777'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
  op.create_table(
    'users',
    sa.Column('user_id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('password_hash', sa.Text(), nullable=True),
    sa.Column('first_name', sa.Text(), nullable=True),
    sa.Column('last_name', sa.Text(), nullable=True),
    sa.Column('profile_pic', sa.Text(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_login_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('auth_type', sa.Text(), server_default='password', nullable=False),
    sa.Column('auth_provider', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
  )

def downgrade() -> None:
  op.drop_table('users')

