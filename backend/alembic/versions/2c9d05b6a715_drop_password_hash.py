"""drop password_hash

Revision ID: 2c9d05b6a715
Revises: 62d0ec2e2777
Create Date: 2025-12-29 14:35:47.193718

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '2c9d05b6a715'
down_revision: Union[str, Sequence[str], None] = '62d0ec2e2777'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
  op.drop_column('users', 'password_hash')

def downgrade() -> None:
  op.add_column('users', sa.Column('password_hash', sa.TEXT(), autoincrement=False, nullable=True))

