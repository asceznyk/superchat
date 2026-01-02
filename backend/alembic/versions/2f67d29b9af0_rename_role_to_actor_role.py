"""rename role to actor role

Revision ID: 2f67d29b9af0
Revises: e8cd8d333fd5
Create Date: 2026-01-02 09:22:34.857769

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '2f67d29b9af0'
down_revision: Union[str, Sequence[str], None] = 'e8cd8d333fd5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
  op.alter_column('actors', 'role', new_column_name='actor_role')

def downgrade() -> None:
  op.alter_column('actors', 'actor_role', new_column_name='role')

