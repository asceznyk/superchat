"""create messages and others

Revision ID: c5275c62e092
Revises: 2c9d05b6a715
Create Date: 2026-01-01 15:06:08.843859

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'c5275c62e092'
down_revision: Union[str, Sequence[str], None] = '2c9d05b6a715'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
  op.create_table('actors',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('role', sa.Text(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
  )
  op.create_table('threads',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('thread_id', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('thread_title', sa.Text(), nullable=False),
    sa.Column('is_pinned', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('thread_id')
  )
  op.create_table('ai_models',
    sa.Column('model_id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('actor_id', sa.UUID(), nullable=False),
    sa.Column('model_name', sa.Text(), nullable=False),
    sa.Column('version', sa.Text(), nullable=True),
    sa.Column('provider', sa.Text(), nullable=False),
    sa.Column('capabilities', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('model_id')
  )
  op.create_table('messages',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('actor_id', sa.UUID(), nullable=False),
    sa.Column('thread_id', sa.Text(), nullable=False),
    sa.Column('branched_from_id', sa.UUID(), nullable=True),
    sa.Column('msg_type', sa.Text(), nullable=False),
    sa.Column('msg_content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
  )
  op.add_column('users', sa.Column('actor_id', sa.UUID(), nullable=False))
  op.create_foreign_key(None, 'users', 'actors', ['actor_id'], ['id'], ondelete='CASCADE')

def downgrade() -> None:
  op.drop_constraint(None, 'users', type_='foreignkey')
  op.drop_column('users', 'actor_id')
  op.drop_table('messages')
  op.drop_table('ai_models')
  op.drop_table('threads')
  op.drop_table('actors')

