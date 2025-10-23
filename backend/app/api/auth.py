from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db.database import SessionLocal
from ..db.crud import ensure_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/ensure')
def ensure(payload: dict, db: Session = Depends(get_db)):
    user = ensure_user(db, int(payload.get('telegram_id')), payload.get('username'), payload.get('first_name'))
    return { 'user_id': user.id, 'telegram_id': user.telegram_id, 'role': user.role }
