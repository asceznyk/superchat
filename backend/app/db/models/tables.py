import uuid
from sqlalchemy import (
  Column,
  Text,
  Integer,
  Boolean,
  ForeignKey,
  TIMESTAMP,
  func,
)
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

class Actor(Base):
  __tablename__ = "actors"
  id = Column(
    UUID(as_uuid=True),
    primary_key=True,
    server_default=func.gen_random_uuid(),
  )
  actor_role = Column(Text, nullable=False)
  created_at = Column(
    TIMESTAMP(timezone=True),
    nullable=False,
    server_default=func.now()
  )

class User(Base):
  __tablename__ = "users"
  id = Column(
    UUID(as_uuid=True),
    primary_key=True,
    server_default=func.gen_random_uuid(),
  )
  actor_id = Column(
    ForeignKey("actors.id", ondelete="CASCADE"),
    nullable=False
  )
  username = Column(Text, nullable=False)
  email = Column(Text, nullable=False, unique=True)
  first_name = Column(Text)
  last_name = Column(Text)
  profile_pic = Column(Text)
  created_at = Column(
    TIMESTAMP(timezone=True),
    nullable=False,
    server_default=func.now(),
  )
  updated_at = Column(
    TIMESTAMP(timezone=True),
    nullable=False,
    server_default=func.now(),
  )
  last_login_at = Column(TIMESTAMP(timezone=True))
  auth_type = Column(
    Text,
    nullable=False,
    server_default="password",
  )
  auth_provider = Column(Text)

class AIModel(Base):
  __tablename__ = "ai_models"
  id = Column(
    UUID(as_uuid=True),
    primary_key=True,
    server_default=func.gen_random_uuid(),
  )
  actor_id = Column(
    ForeignKey("actors.id", ondelete="CASCADE"),
    nullable=False
  )
  model_name = Column(Text, nullable=False)
  model_version = Column(Text)
  provider = Column(Text, nullable=False)
  capabilities = Column(Text)

class Thread(Base):
  __tablename__ = "threads"
  id = Column(
    UUID(as_uuid=True),
    primary_key=True,
    server_default=func.gen_random_uuid(),
  )
  actor_id = Column(
    ForeignKey("actors.id", ondelete="CASCADE"),
    nullable=False
  )
  thread_title = Column(Text, nullable=False)
  is_pinned = Column(Boolean, nullable=False, server_default="false")
  created_at = Column(
    TIMESTAMP(timezone=True),
    nullable=False,
    server_default=func.now(),
  )
  updated_at = Column(
    TIMESTAMP(timezone=True),
    nullable=False,
    server_default=func.now(),
    onupdate=func.now(),
  )

class Message(Base):
  __tablename__ = "messages"
  id = Column(
    UUID(as_uuid=True),
    primary_key=True,
    server_default=func.gen_random_uuid(),
  )
  actor_id = Column(
    UUID(as_uuid=True),
    ForeignKey("actors.id", ondelete="CASCADE"),
    nullable=False,
  )
  thread_id = Column(
    UUID(as_uuid=True),
    ForeignKey("threads.id", ondelete="CASCADE"),
    nullable=False
  )
  branched_from_id = Column(
    UUID(as_uuid=True),
    ForeignKey("threads.id", ondelete="SET NULL"),
    nullable=True,
  )
  msg_type = Column(
    Text,
    nullable=False,
  )
  msg_content = Column(
    Text,
    nullable=False,
  )
  created_at = Column(
    TIMESTAMP(timezone=True),
    nullable=False,
    server_default=func.now(),
  )
  updated_at = Column(
    TIMESTAMP(timezone=True),
    nullable=False,
    server_default=func.now(),
    onupdate=func.now(),
  )


