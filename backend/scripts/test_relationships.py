# backend/scripts/test_relationships.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv('.env.local')

from app.db.database import SessionLocal
from app.models.user import User
from app.models.wallet import Wallet
from app.models.transaction import Transaction
from app.models.admin_action import AdminAction

def test_relationships():
    """اختبار العلاقات بين النماذج"""
    db = SessionLocal()
    try:
        print("🧪 بدء اختبار العلاقات بين النماذج...")
        
        # 1. إنشاء مستخدم اختبار
        test_user = User(
            telegram_id=999888777,
            username="test_user_relations",
            first_name="Test Relations",
            role="user"
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"✅ تم إنشاء مستخدم: {test_user}")

        # 2. إنشاء محفظة للمستخدم
        wallet = Wallet(user_id=test_user.id, balance=1000.0)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
        print(f"✅ تم إنشاء محفظة: {wallet}")

        # 3. التحقق من العلاقة User ↔ Wallet
        user_with_wallet = db.query(User).filter(User.id == test_user.id).first()
        if user_with_wallet.wallet:
            print(f"✅ العلاقة User ↔ Wallet تعمل: المستخدم لديه محفظة برصيد {user_with_wallet.wallet.balance}")
        else:
            print("❌ العلاقة User ↔ Wallet لا تعمل")

        # 4. إنشاء معاملة
        transaction = Transaction(
            from_user_id=test_user.id,
            to_user_id=test_user.id,  # نفس المستخدم للاختبار
            amount=500.0,
            type="transfer",
            note="اختبار العلاقات"
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        print(f"✅ تم إنشاء معاملة: {transaction}")

        # 5. التحقق من العلاقات في المعاملة
        transaction_with_relations = db.query(Transaction).filter(Transaction.id == transaction.id).first()
        if transaction_with_relations.from_user and transaction_with_relations.to_user:
            print("✅ العلاقات Transaction ↔ User تعمل")
        else:
            print("❌ العلاقات Transaction ↔ User لا تعمل")

        # 6. إنشاء إجراء أدمن
        admin_action = AdminAction(
            admin_id=test_user.id,
            action="test_action",
            target_user_id=test_user.id,
            details="اختبار علاقات الأدمن"
        )
        db.add(admin_action)
        db.commit()
        db.refresh(admin_action)
        print(f"✅ تم إنشاء إجراء أدمن: {admin_action}")

        # 7. التحقق من علاقات الأدمن
        admin_action_with_relations = db.query(AdminAction).filter(AdminAction.id == admin_action.id).first()
        if admin_action_with_relations.admin_user:
            print("✅ العلاقة AdminAction ↔ User (admin) تعمل")
        if admin_action_with_relations.target_user:
            print("✅ العلاقة AdminAction ↔ User (target) تعمل")

        # 8. اختبار العلاقات العكسية
        user_full = db.query(User).filter(User.id == test_user.id).first()
        print(f"📊 ملخص العلاقات للمستخدم {user_full.username}:")
        print(f"   - المحفظة: {user_full.wallet.balance if user_full.wallet else 'لا يوجد'}")
        print(f"   - عدد المعاملات المرسلة: {len(user_full.sent_transactions)}")
        print(f"   - عدد المعاملات المستلمة: {len(user_full.received_transactions)}")
        print(f"   - عدد إجراءات الأدمن: {len(user_full.admin_actions)}")

        print("🎉 جميع الاختبارات completed successfully!")

    except Exception as e:
        print(f"❌ خطأ في اختبار العلاقات: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # تنظيف البيانات الاختبارية
        try:
            db.query(AdminAction).filter(AdminAction.admin_id == test_user.id).delete()
            db.query(Transaction).filter(Transaction.from_user_id == test_user.id).delete()
            db.query(Wallet).filter(Wallet.user_id == test_user.id).delete()
            db.query(User).filter(User.id == test_user.id).delete()
            db.commit()
            print("🧹 تم تنظيف البيانات الاختبارية")
        except:
            db.rollback()
        finally:
            db.close()

if __name__ == "__main__":
    test_relationships()