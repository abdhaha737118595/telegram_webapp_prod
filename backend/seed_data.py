# backend/seed_data.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv('.env.local')

from app.db.database import SessionLocal
from app.models.user import User
from app.models.wallet import Wallet

def seed_initial_data():
    db = SessionLocal()
    try:
        print("🌱 بدء إضافة البيانات التجريبية...")
        
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
                    wallet = Wallet(user_id=user.id, balance=1000.0)
                    db.add(wallet)
                    db.commit()
                    
                    print(f"✅ تم إنشاء الأدمن: {telegram_id} مع محفظة برصيد 1000")
                else:
                    print(f"⚠️  الأدمن موجود مسبقاً: {telegram_id}")
        
        # إنشاء مستخدم عادي تجريبي
        test_user = db.query(User).filter(User.telegram_id == 111222333).first()
        if not test_user:
            user = User(
                telegram_id=111222333,
                username="test_user",
                first_name="Test",
                role="user"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
            wallet = Wallet(user_id=user.id, balance=500.0)
            db.add(wallet)
            db.commit()
            print("✅ تم إنشاء مستخدم تجريبي: 111222333")
        
        print("🎉 تم تهيئة البيانات التجريبية بنجاح!")
        
        # عرض عدد المستخدمين
        user_count = db.query(User).count()
        wallet_count = db.query(Wallet).count()
        print(f"📊 إحصائيات: {user_count} مستخدم، {wallet_count} محفظة")
                    
    except Exception as e:
        print(f"❌ خطأ في تهيئة البيانات: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_initial_data()