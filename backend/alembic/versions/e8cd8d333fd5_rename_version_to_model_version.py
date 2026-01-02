"""rename version to model_version

Revision ID: e8cd8d333fd5
Revises: c5275c62e092
Create Date: 2026-01-02 09:16:45.913021

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'e8cd8d333fd5'
down_revision: Union[str, Sequence[str], None] = 'c5275c62e092'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
  op.add_column('ai_models', sa.Column('model_version', sa.Text(), nullable=True))
  op.drop_column('ai_models', 'version')

def downgrade() -> None:
  op.add_column('ai_models', sa.Column('version', sa.TEXT(), autoincrement=False, nullable=True))
  op.drop_column('ai_models', 'model_version')

