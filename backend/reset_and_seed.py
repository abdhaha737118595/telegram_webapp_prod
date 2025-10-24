# backend/reset_db.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv('.env.local')

from app.db.database import engine
from app.models.base import Base

print("🔄 إعادة إنشاء قاعدة البيانات...")

# إسقاط جميع الجداول
Base.metadata.drop_all(bind=engine)
print("✅ تم إسقاط الجداول")

# إنشاء الجداول الجديدة
Base.metadata.create_all(bind=engine)
print("✅ تم إنشاء الجداول الجديدة")

print("🎉 جاهز لاختبار العلاقات!")