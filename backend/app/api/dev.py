# backend/app/api/dev.py
from fastapi import APIRouter, Depends
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

@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": [
        {
            "id": user.id,
            "telegram_id": user.telegram_id,
            "username": user.username,
            "role": user.role
        } for user in users
    ]}

# في backend/app/api/dev.py، استبدل دالة get_all_wallets بهذا:

@router.get("/wallets")
def get_all_wallets(db: Session = Depends(get_db)):
    try:
        # الحل: جلب المحافظ والمستخدمين بشكل منفصل ثم دمجهم
        wallets = db.query(Wallet).all()
        users = db.query(User).all()
        
        # إنشاء mapping بين user_id والمستخدم
        user_map = {user.id: user for user in users}
        
        return {"wallets": [
            {
                "id": wallet.id,
                "user_id": wallet.user_id,
                "username": user_map.get(wallet.user_id, {}).username or "Unknown",
                "balance": float(wallet.balance)
            } for wallet in wallets
        ]}
    except Exception as e:
        return {"error": str(e)}

@router.get("/test-admin")
def test_admin():
    return {"message": "Admin endpoint works!"}

@router.post("/make-admin")
def make_admin(payload: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.telegram_id == payload['telegram_id']).first()
    if user:
        user.role = 'admin'
        db.commit()
        return {"status": "success", "message": f"User {user.telegram_id} is now admin"}
    return {"status": "error", "message": "User not found"}