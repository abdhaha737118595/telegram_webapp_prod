import os, hashlib, hmac

def get_root_admins():
    s = os.getenv('ROOT_ADMINS', '')
    if not s:
        return []
    return [int(x.strip()) for x in s.split(',') if x.strip()]

def is_root_admin(telegram_id: int) -> bool:
    return telegram_id in get_root_admins()

def verify_telegram_webapp_hash(data: dict, bot_token: str) -> bool:
    check_hash = data.get('hash')
    if not check_hash:
        return False
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    data_check_arr = [f"{k}={v}" for k, v in sorted(data.items()) if k != 'hash']
    data_check_string = '\n'.join(data_check_arr)
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return hmac_hash == check_hash
