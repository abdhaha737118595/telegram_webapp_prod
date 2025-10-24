from sqlalchemy import Column, Integer, BigInteger, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    role = Column(String, default='user', nullable=False)  # 'user' or 'admin'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # ✅ العلاقات المحسنة
    wallet = relationship("Wallet", back_populates="user", uselist=False, cascade="all, delete-orphan")
    sent_transactions = relationship("Transaction", foreign_keys="Transaction.from_user_id", back_populates="from_user")
    received_transactions = relationship("Transaction", foreign_keys="Transaction.to_user_id", back_populates="to_user")
    admin_actions = relationship("AdminAction", foreign_keys="AdminAction.admin_id", back_populates="admin_user")
    
    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username='{self.username}')>"