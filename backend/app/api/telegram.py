from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db.database import SessionLocal
from ..utils import verify_telegram_webapp_hash
from ..db.crud import ensure_user
import os

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/validate')
def validate(payload: dict, db: Session = Depends(get_db)):
    bot_token = os.getenv('BOT_TOKEN', '')
    if not bot_token:
        raise HTTPException(status_code=500, detail='BOT_TOKEN not configured')
    if not verify_telegram_webapp_hash(payload, bot_token):
        raise HTTPException(status_code=400, detail='Invalid init data hash')
    user = ensure_user(db, int(payload.get('id')), payload.get('username'), payload.get('first_name'))
    return { 'user_id': user.id, 'telegram_id': user.telegram_id, 'role': user.role }
