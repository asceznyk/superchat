import uuid
from sqlalchemy import (
  Column,
  Text,
  TIMESTAMP,
  func,
)
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

class User(Base):
  __tablename__ = "users"
  user_id = Column(
    UUID(as_uuid=True),
    primary_key=True,
    server_default=func.gen_random_uuid(),
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



