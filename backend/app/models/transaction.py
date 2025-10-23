from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime
from sqlalchemy.sql import func
from .base import Base

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    to_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    amount = Column(Numeric(12,2), nullable=False)
    type = Column(String, nullable=False)  # 'topup', 'transfer', 'purchase'
    note = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
