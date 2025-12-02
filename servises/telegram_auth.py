import hashlib
import hmac
from typing import Dict

from config import settings


def verify_telegram_auth(auth_data: Dict) -> bool:
    check_hash = auth_data.pop("hash", None)
    if not check_hash:
        return False

    data_check_arr = [f"{k}={v}" for k, v in sorted(auth_data.items())]
    data_check_string = "\n".join(data_check_arr)

    secret_key = hashlib.sha256(settings.bot.token.encode()).digest()
    hmac_hash = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    return hmac_hash == check_hash
