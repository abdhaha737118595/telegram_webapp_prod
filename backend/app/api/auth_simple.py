# backend/app/api/auth_simple.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import SessionLocal
from ..models.user import User
from ..models.wallet import Wallet

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/ensure-simple')
def ensure_simple(payload: dict, db: Session = Depends(get_db)):
    try:
        telegram_id = int(payload.get('telegram_id'))
        username = payload.get('username', '')
        first_name = payload.get('first_name', '')
        
        print(f"🔍 محاولة إنشاء/تأكيد مستخدم: {telegram_id}, {username}")
        
        # تحقق إذا كان المستخدم موجود
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        
        if not user:
            # إنشاء مستخدم جديد
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                role="user"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
            # إنشاء محفظة
            wallet = Wallet(user_id=user.id, balance=0.0)
            db.add(wallet)
            db.commit()
            
            print(f"✅ تم إنشاء مستخدم جديد: {user.id}")
        else:
            print(f"✅ المستخدم موجود مسبقاً: {user.id}")
        
        return {
            'user_id': user.id,
            'telegram_id': user.telegram_id,
            'role': user.role,
            'username': user.username,
            'message': 'User ensured successfully'
        }
        
    except Exception as e:
        db.rollback()
        print(f"❌ خطأ في ensure-simple: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")