# backend/scripts/seed_data.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv('.env.local')

from app.db.database import SessionLocal
from app.models.user import User
from app.models.wallet import Wallet

def seed_initial_data():
    db = SessionLocal()
    try:
        # جلب قائمة الأدمن من البيئة
        root_admins = os.getenv('ROOT_ADMINS', '123456789').split(',')
        
        for admin_id in root_admins:
            if admin_id.strip():
                telegram_id = int(admin_id.strip())
                
                # تحقق إذا كان المستخدم موجود
                existing_user = db.query(User).filter(User.telegram_id == telegram_id).first()
                
                if not existing_user:
                    # إنشاء مستخدم أدمن جديد
                    user = User(
                        telegram_id=telegram_id,
                        username=f"admin_{telegram_id}",
                        first_name="Admin",
                        role="admin"
                    )
                    db.add(user)
                    db.commit()
                    db.refresh(user)
                    
                    # إنشاء محفظة للمستخدم
                    wallet = Wallet(user_id=user.id, balance=1000.0)  # رصيد ابتدائي
                    db.add(wallet)
                    db.commit()
                    
                    print(f"✅ تم إنشاء الأدمن: {telegram_id} مع محفظة برصيد 1000")
                else:
                    print(f"⚠️  الأدمن موجود مسبقاً: {telegram_id}")
        
        print("🎉 تم تهيئة البيانات التجريبية بنجاح!")
                    
    except Exception as e:
        print(f"❌ خطأ في تهيئة البيانات: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_initial_data()