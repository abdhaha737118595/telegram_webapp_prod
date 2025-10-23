from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class AdminAction(Base):
    __tablename__ = 'admin_actions'
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(BigInteger, nullable=False)
    action = Column(String, nullable=False)
    target_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    details = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
