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
    """تهيئة البيانات التجريبية للنظام"""
    db = SessionLocal()
    try:
        print("🌱 بدء إضافة البيانات التجريبية...")
        
        # جلب قائمة الأدمن من البيئة
        root_admins = os.getenv('ROOT_ADMINS', '123456789').split(',')
        created_count = 0
        existing_count = 0
        
        # 1. إنشاء مستخدمين أدمن
        for admin_id in root_admins:
            if admin_id.strip():
                telegram_id = int(admin_id.strip())
                
                existing_user = db.query(User).filter(User.telegram_id == telegram_id).first()
                
                if not existing_user:
                    user = User(
                        telegram_id=telegram_id,
                        username=f"admin_{telegram_id}",
                        first_name="Admin",
                        role="admin"
                    )
                    db.add(user)
                    db.commit()
                    db.refresh(user)
                    
                    wallet = Wallet(user_id=user.id, balance=1000.0)
                    db.add(wallet)
                    db.commit()
                    
                    print(f"✅ تم إنشاء الأدمن: {telegram_id} مع محفظة برصيد 1000")
                    created_count += 1
                else:
                    print(f"⚠️  الأدمن موجود مسبقاً: {telegram_id}")
                    existing_count += 1
        
        # 2. إنشاء مستخدم عادي تجريبي
        test_user = db.query(User).filter(User.telegram_id == 111222333).first()
        if not test_user:
            user = User(
                telegram_id=111222333,
                username="test_user",
                first_name="Test User",
                role="user"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
            wallet = Wallet(user_id=user.id, balance=500.0)
            db.add(wallet)
            db.commit()
            print("✅ تم إنشاء مستخدم تجريبي: 111222333 مع محفظة برصيد 500")
            created_count += 1
        
        # 3. إنشاء مستخدم عادي إضافي
        additional_user = db.query(User).filter(User.telegram_id == 222333444).first()
        if not additional_user:
            user = User(
                telegram_id=222333444,
                username="regular_user",
                first_name="Regular User", 
                role="user"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
            wallet = Wallet(user_id=user.id, balance=250.0)
            db.add(wallet)
            db.commit()
            print("✅ تم إنشاء مستخدم عادي: 222333444 مع محفظة برصيد 250")
            created_count += 1
        
        # 4. عرض الإحصائيات النهائية
        user_count = db.query(User).count()
        wallet_count = db.query(Wallet).count()
        
        print("🎉 تم تهيئة البيانات التجريبية بنجاح!")
        print(f"📊 الإحصائيات النهائية:")
        print(f"   - إجمالي المستخدمين: {user_count}")
        print(f"   - إجمالي المحافظ: {wallet_count}")
        print(f"   - تم إنشاء: {created_count} مستخدم جديد")
        print(f"   - موجود مسبقاً: {existing_count} مستخدم")
                    
    except Exception as e:
        print(f"❌ خطأ في تهيئة البيانات: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_initial_data()