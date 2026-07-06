import jwt
import hashlib
import hmac
import datetime
import logging
import os
from typing import Optional

logger = logging.getLogger("instadeed")

JWT_SECRET = os.environ.get("JWT_SECRET", "")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = int(os.environ.get("JWT_EXPIRY_HOURS", "24"))

try:
    import bcrypt as _bcrypt
    def hash_password(password: str) -> str:
        return _bcrypt.hashpw(password.encode(), _bcrypt.gensalt()).decode()
    def verify_password(password: str, stored: str) -> bool:
        return _bcrypt.checkpw(password.encode(), stored.encode())
except ImportError:
    logger.warning("bcrypt not installed; using PBKDF2 fallback")
    _PBKDF2_ITERATIONS = 310000
    def hash_password(password: str) -> str:
        salt = os.urandom(16)
        derived = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, _PBKDF2_ITERATIONS)
        return f"pbkdf2_sha256${_PBKDF2_ITERATIONS}${salt.hex()}${derived.hex()}"
    def verify_password(password: str, stored: str) -> bool:
        parts = stored.split("$", 3)
        if len(parts) != 4:
            return False
        scheme, iterations_str, salt_hex, expected_hex = parts
        if scheme != "pbkdf2_sha256":
            return False
        try:
            iterations = int(iterations_str)
            salt = bytes.fromhex(salt_hex)
            expected = bytes.fromhex(expected_hex)
        except (ValueError, TypeError):
            return False
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
        return hmac.compare_digest(actual, expected)

def create_token(user_id: str, email: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRY_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
