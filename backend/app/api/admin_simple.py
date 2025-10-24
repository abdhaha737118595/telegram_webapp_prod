# backend/app/api/admin_simple.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import SessionLocal
from ..models.user import User
from ..models.wallet import Wallet
from ..models.admin_action import AdminAction
from decimal import Decimal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/topup-simple')
def topup_simple(payload: dict, db: Session = Depends(get_db)):
    try:
        admin_id = int(payload.get('admin_telegram_id'))
        target_id = int(payload.get('target_telegram_id'))
        amount = float(payload.get('amount', 0))
        note = payload.get('note', '')
        
        print(f"🔍 محاولة شحن رصيد: أدمن {admin_id} -> مستخدم {target_id} مبلغ {amount}")
        
        # تحقق من الأدمن
        admin_user = db.query(User).filter(User.telegram_id == admin_id, User.role == 'admin').first()
        if not admin_user:
            raise HTTPException(status_code=403, detail="Not authorized as admin")
        
        # تحقق من المستخدم الهدف
        target_user = db.query(User).filter(User.telegram_id == target_id).first()
        if not target_user:
            raise HTTPException(status_code=404, detail="Target user not found")
        
        # احصل على محفظة المستخدم
        wallet = db.query(Wallet).filter(Wallet.user_id == target_user.id).first()
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        
        # تحديث الرصيد
        wallet.balance += Decimal(str(amount))
        db.commit()
        
        # ✅ تسجيل الإجراء مع الحقول الصحيحة
        action = AdminAction(
            admin_id=admin_user.id,
            action="topup",  # الحقل الصحيح هو 'action'
            target_user_id=target_user.id,
            details=f"شحن رصيد: {amount} - {note}"  # الحقل الصحيح هو 'details'
        )
        db.add(action)
        db.commit()
        
        print(f"✅ تم شحن الرصيد بنجاح. الرصيد الجديد: {wallet.balance}")
        
        return {
            'status': 'success',
            'new_balance': float(wallet.balance),
            'message': 'Top-up completed successfully with action log'
        }
        
    except Exception as e:
        db.rollback()
        print(f"❌ خطأ في topup-simple: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")