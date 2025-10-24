from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class AdminAction(Base):
    __tablename__ = 'admin_actions'
    
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action = Column(String, nullable=False)
    target_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    details = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # ✅ العلاقات المحسنة
    admin_user = relationship("User", foreign_keys=[admin_id], back_populates="admin_actions")
    target_user = relationship("User", foreign_keys=[target_user_id])
    
    def __repr__(self):
        return f"<AdminAction(id={self.id}, action='{self.action}', admin_id={self.admin_id})>"