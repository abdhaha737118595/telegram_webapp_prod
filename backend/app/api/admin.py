from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import SessionLocal
from ..db.crud import get_user_by_telegram_id, add_balance
from ..utils import is_root_admin

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def require_admin(telegram_id: int, db: Session):
    if is_root_admin(telegram_id):
        return True
    user = get_user_by_telegram_id(db, telegram_id)
    if not user or user.role != 'admin':
        raise HTTPException(status_code=403, detail='Not authorized')
    return True

@router.post('/topup')
def topup(payload: dict, db: Session = Depends(get_db)):
    admin_id = int(payload.get('admin_telegram_id'))
    target_tid = int(payload.get('target_telegram_id'))
    amount = float(payload.get('amount'))
    note = payload.get('note')
    require_admin(admin_id, db)
    target = get_user_by_telegram_id(db, target_tid)
    if not target:
        raise HTTPException(status_code=404, detail='Target user not found')
    w = add_balance(db, admin_id, target.id, amount, note)
    return { 'status': 'ok', 'new_balance': str(w.balance) }
