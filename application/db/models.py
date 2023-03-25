import uuid

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, BigInteger, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True)
    user_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False, unique=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)


user_orm = User.__table__


class RefreshToken(Base):
    __tablename__ = 'RefreshToken'
    token_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    refresh_session = Column(UUID, nullable=False)
    expires_in = Column(BigInteger, nullable=False)
    time_created = Column(DateTime(timezone=False), nullable=False)


refresh_session_orm = RefreshToken.__table__
