import os
from typing import List

class Settings:
    APP_NAME: str = "Instadeed Legal Suite"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = os.environ.get("DEBUG", "false").lower() == "true"

    JWT_SECRET: str = os.environ.get("JWT_SECRET", "")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: int = int(os.environ.get("JWT_EXPIRY_HOURS", "24"))

    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///madhav_crm.db")
    DATABASE_FILE: str = os.environ.get("DATABASE_FILE", "madhav_crm.db")
    DB_TYPE: str = "sqlite"
    if DATABASE_URL.startswith("postgres"):
        DB_TYPE = "postgres"

    STATIC_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    RAZORPAY_KEY_ID: str = os.environ.get("RAZORPAY_KEY_ID", "")
    RAZORPAY_KEY_SECRET: str = os.environ.get("RAZORPAY_KEY_SECRET", "")

    LEEGALITY_AUTH_TOKEN: str = os.environ.get("LEEGALITY_AUTH_TOKEN", "")
    LEEGALITY_PRIVATE_SALT: str = os.environ.get("LEEGALITY_PRIVATE_SALT", "")
    LEEGALITY_BASE_URL: str = os.environ.get("LEEGALITY_BASE_URL", "https://sandbox.leegality.com/api")
    LEEGALITY_PROFILE_ID: str = os.environ.get("LEEGALITY_PROFILE_ID", "")

    ALLOWED_ORIGINS: List[str] = os.environ.get("ALLOWED_ORIGINS", "https://instadeed.io,https://instadeed.onrender.com").split(",")

    ADMIN_EMAIL: str = os.environ.get("ADMIN_EMAIL", "admin@instadeed.local")
    ADMIN_PASSWORD: str = os.environ.get("ADMIN_PASSWORD", "")

    REDIS_URL: str = os.environ.get("REDIS_URL", "")
    SMTP_HOST: str = os.environ.get("SMTP_HOST", "")
    SMTP_PORT: int = int(os.environ.get("SMTP_PORT", "587"))
    SMTP_USER: str = os.environ.get("SMTP_USER", "")
    SMTP_PASS: str = os.environ.get("SMTP_PASS", "")
    SMTP_FROM: str = os.environ.get("SMTP_FROM", "noreply@instadeed.io")

    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
    SENTRY_DSN: str = os.environ.get("SENTRY_DSN", "")

    def validate(self):
        errors = []
        if not self.JWT_SECRET:
            errors.append("JWT_SECRET must be set")
        if not self.RAZORPAY_KEY_ID or not self.RAZORPAY_KEY_SECRET:
            errors.append("RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET must be set")
        return errors

settings = Settings()
