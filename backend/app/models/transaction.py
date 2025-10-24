from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    to_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    amount = Column(Numeric(12, 2), nullable=False)
    type = Column(String, nullable=False)  # 'topup', 'transfer', 'purchase'
    note = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # ✅ العلاقات المحسنة
    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="sent_transactions")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="received_transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, type='{self.type}')>"