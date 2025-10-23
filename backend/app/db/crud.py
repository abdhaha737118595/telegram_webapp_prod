from sqlalchemy.orm import Session
from ..models import User, Wallet, Transaction, AdminAction

def get_user_by_telegram_id(db: Session, telegram_id: int):
    return db.query(User).filter(User.telegram_id == telegram_id).first()

def create_user(db: Session, telegram_id: int, username: str = None, first_name: str = None):
    user = User(telegram_id=telegram_id, username=username, first_name=first_name)
    db.add(user); db.commit(); db.refresh(user)
    # create wallet
    w = Wallet(user_id=user.id, balance=0)
    db.add(w); db.commit()
    return user

def ensure_user(db: Session, telegram_id: int, username: str = None, first_name: str = None):
    user = get_user_by_telegram_id(db, telegram_id)
    if user:
        return user
    return create_user(db, telegram_id, username, first_name)

def add_balance(db: Session, admin_id: int, target_user_id: int, amount: float, note: str = None):
    w = db.query(Wallet).filter(Wallet.user_id == target_user_id).first()
    if not w:
        from ..models.wallet import Wallet as WalletModel
        w = WalletModel(user_id=target_user_id, balance=0)
        db.add(w); db.commit(); db.refresh(w)
    w.balance = w.balance + amount
    tx = Transaction(from_user_id=admin_id, to_user_id=target_user_id, amount=amount, type='topup', note=note)
    db.add(tx)
    aa = AdminAction(admin_id=admin_id, action='topup', target_user_id=target_user_id, details=note)
    db.add(aa)
    db.commit()
    return w
