# backend/test_init.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv('.env.local')

from app.db.database import init_db, engine
from app.models.base import Base

print("🚀 بدء تهيئة قاعدة البيانات...")

try:
    # إنشاء جميع الجداول
    Base.metadata.create_all(bind=engine)
    print("✅ تم إنشاء الجداول بنجاح!")
    
    # تحقق من الجداول المنشأة
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"📊 الجداول المنشأة: {tables}")
    
except Exception as e:
    print(f"❌ خطأ في إنشاء الجداول: {e}")