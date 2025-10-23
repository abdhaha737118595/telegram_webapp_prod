import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from ..models import base as models_base

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost:5432/telegramapp')

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # create tables if they do not exist (safe to call)
    try:
        models_base.Base.metadata.create_all(bind=engine)
    except OperationalError as e:
        # in production with RDS, ensure networking (VPC) allows connection
        print('Database init failed:', e)
