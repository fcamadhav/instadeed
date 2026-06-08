import jwt
import uuid
import hashlib
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
    logger.warning("bcrypt not installed; using SHA-256 fallback")
    def hash_password(password: str) -> str:
        salt = uuid.uuid4().hex[:16]
        return salt + ":" + hashlib.sha256((salt + password).encode()).hexdigest()
    def verify_password(password: str, stored: str) -> bool:
        if ":" not in stored:
            return False
        salt, expected = stored.split(":", 1)
        return hashlib.sha256((salt + password).encode()).hexdigest() == expected

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
