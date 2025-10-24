# backend/app/db/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from ..models import base as models_base

# تأكد أن هذا السطر يقرأ من .env.local بشكل صحيح
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://telegram_user:telegram_pass@localhost:5432/telegram_wallet')

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    try:
        models_base.Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except OperationalError as e:
        print(f'❌ Database init failed: {e}')