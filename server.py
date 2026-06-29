import sqlite3
import json
import uuid
import datetime
import time
import logging
from logging.handlers import RotatingFileHandler
import os
import hashlib
import io
import base64
import random
import threading
from contextlib import asynccontextmanager
from typing import Optional

import requests as http_requests

from fastapi import FastAPI, Request, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, HTMLResponse, Response
from pydantic import BaseModel
import razorpay
import jwt
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fpdf import FPDF
import re
from dateutil.relativedelta import relativedelta

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        RotatingFileHandler("server.log", maxBytes=10*1024*1024, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("instadeed")

# --- Configuration ---
JWT_SECRET = os.environ.get("JWT_SECRET")
if not JWT_SECRET:
    import sys
    print("FATAL: JWT_SECRET environment variable is required", file=sys.stderr)
    sys.exit(1)
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24
DATABASE_FILE = os.environ.get("DATABASE_FILE", "madhav_crm.db")
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))

def sanitize_phone(phone: str) -> str:
    if not phone:
        return ""
    digits = "".join([c for c in phone if c.isdigit()])
    if len(digits) >= 10:
        return digits[-10:]
    return digits

# --- Leegality e-Sign Configuration ---
LEEGALITY_AUTH_TOKEN = os.environ.get("LEEGALITY_AUTH_TOKEN")
LEEGALITY_PRIVATE_SALT = os.environ.get("LEEGALITY_PRIVATE_SALT")
LEEGALITY_BASE_URL = os.environ.get("LEEGALITY_BASE_URL", "https://sandbox.leegality.com/api")
LEEGALITY_PROFILE_ID = os.environ.get("LEEGALITY_PROFILE_ID", "")

# --- Password Hashing (bcrypt) ---
import bcrypt as _bcrypt
def hash_password(password: str) -> str:
    return _bcrypt.hashpw(password.encode(), _bcrypt.gensalt()).decode()

def check_password(password: str, hashed: str) -> bool:
    return _bcrypt.checkpw(password.encode(), hashed.encode())

# --- Input Validation ---
VALID_EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
def validate_email(email: str) -> bool:
    return bool(VALID_EMAIL_RE.match(email))
def validate_password(password: str) -> tuple:
    if len(password) < 8:
        return (False, "Password must be at least 8 characters")
    if not re.search(r'[A-Z]', password):
        return (False, "Password must contain an uppercase letter")
    if not re.search(r'[a-z]', password):
        return (False, "Password must contain a lowercase letter")
    if not re.search(r'\d', password):
        return (False, "Password must contain a digit")
    return (True, "")
def validate_phone(phone: str) -> bool:
    return bool(re.match(r'^\d{10}$', phone))

# --- Rate Limiter (use X-Forwarded-For behind reverse proxy) ---
def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return get_remote_address(request)

limiter = Limiter(key_func=get_client_ip)

# --- Razorpay ---
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET")
is_razorpay_valid = False
client = None
if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET and "YOUR_KEY" not in RAZORPAY_KEY_ID:
    try:
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        is_razorpay_valid = True
    except Exception as e:
        logger.warning(f"Failed to initialize Razorpay: {e}")

# --- Database ---
class Database:
    def __enter__(self):
        self.conn = sqlite3.connect(DATABASE_FILE, timeout=30)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self.cursor
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        self.conn.close()
        return False

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
    except Exception as e:
        logger.warning(f"Failed to set WAL/synchronous PRAGMAs: {e}")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id TEXT PRIMARY KEY,
        customer_name TEXT,
        customer_phone TEXT,
        customer_email TEXT,
        agreement_type TEXT,
        source TEXT,
        status TEXT,
        amount REAL,
        form_data TEXT,
        created_at TEXT,
        updated_at TEXT,
        cloud_url TEXT
    )
    """)
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN cloud_url TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN leegality_doc_id TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN leegality_sign_url TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN is_favorite INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN estamp_number TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN estamp_cert_url TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN stamp_duty_paid REAL")
    except sqlite3.OperationalError:
        pass
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        phone TEXT DEFAULT '',
        location TEXT DEFAULT '',
        device_info TEXT DEFAULT '',
        role TEXT DEFAULT 'user',
        is_active INTEGER DEFAULT 1,
        created_at TEXT,
        last_login TEXT
    )
    """)
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN location TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN device_info TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS api_keys (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        key_hash TEXT NOT NULL,
        key_prefix TEXT NOT NULL,
        name TEXT DEFAULT 'Default',
        is_active INTEGER DEFAULT 1,
        last_used TEXT,
        created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS page_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        session_id TEXT,
        user_id TEXT,
        event TEXT,
        page TEXT,
        detail TEXT,
        ip_address TEXT,
        user_agent TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        method TEXT,
        path TEXT,
        status_code INTEGER,
        ip_address TEXT,
        user_id TEXT,
        duration_ms INTEGER,
        user_agent TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        timestamp TEXT,
        ip_address TEXT,
        user_agent TEXT,
        device_info TEXT DEFAULT '',
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT,
        note TEXT,
        author_id TEXT,
        created_at TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (author_id) REFERENCES users(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT,
        staff_id TEXT,
        role TEXT DEFAULT 'attorney',
        assigned_at TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (staff_id) REFERENCES users(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_versions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT,
        version INTEGER DEFAULT 1,
        form_data_snapshot TEXT,
        created_at TEXT,
        author_id TEXT,
        change_summary TEXT DEFAULT '',
        FOREIGN KEY (order_id) REFERENCES orders(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS refunds (
        id TEXT PRIMARY KEY,
        order_id TEXT,
        amount REAL,
        reason TEXT,
        status TEXT DEFAULT 'PENDING',
        created_at TEXT,
        processed_at TEXT,
        processed_by TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coupons (
        id TEXT PRIMARY KEY,
        code TEXT UNIQUE,
        type TEXT DEFAULT 'percentage',
        value REAL,
        max_uses INTEGER DEFAULT 0,
        current_uses INTEGER DEFAULT 0,
        min_amount REAL DEFAULT 0,
        expires_at TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT DEFAULT 'info',
        recipient TEXT,
        title TEXT,
        message TEXT,
        reference_type TEXT DEFAULT '',
        reference_id TEXT DEFAULT '',
        status TEXT DEFAULT 'pending',
        created_at TEXT,
        sent_at TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id TEXT PRIMARY KEY,
        order_id TEXT,
        invoice_number TEXT UNIQUE,
        amount REAL,
        gst_amount REAL DEFAULT 0,
        total REAL,
        status TEXT DEFAULT 'PENDING',
        created_at TEXT,
        paid_at TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_drafts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_type TEXT,
        form_data TEXT,
        phone TEXT,
        email TEXT DEFAULT '',
        created_at TEXT,
        updated_at TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shared_drafts (
        id TEXT PRIMARY KEY,
        doc_type TEXT,
        form_data TEXT,
        created_at TEXT,
        expires_at TEXT
    )
    """)
    try:
        cursor.execute("ALTER TABLE saved_drafts ADD COLUMN email TEXT DEFAULT ''")
    except Exception as e:
        pass
    # Indexes for performance
    for idx_sql in [
        "CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(customer_phone)",
        "CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)",
        "CREATE INDEX IF NOT EXISTS idx_orders_created ON orders(created_at)",
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
        "CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)",
        "CREATE INDEX IF NOT EXISTS idx_page_events_session ON page_events(session_id)",
        "CREATE INDEX IF NOT EXISTS idx_page_events_timestamp ON page_events(timestamp)",
        "CREATE INDEX IF NOT EXISTS idx_activity_log_timestamp ON activity_log(timestamp)",
        "CREATE INDEX IF NOT EXISTS idx_login_history_user ON login_history(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_order_notes_order ON order_notes(order_id)",
        "CREATE INDEX IF NOT EXISTS idx_order_assignments_order ON order_assignments(order_id)",
        "CREATE INDEX IF NOT EXISTS idx_document_versions_order ON document_versions(order_id)",
        "CREATE INDEX IF NOT EXISTS idx_refunds_order ON refunds(order_id)",
        "CREATE INDEX IF NOT EXISTS idx_notifications_created ON notifications(created_at)",
        "CREATE INDEX IF NOT EXISTS idx_saved_drafts_phone ON saved_drafts(phone)",
        "CREATE INDEX IF NOT EXISTS idx_saved_drafts_email ON saved_drafts(email)",
    ]:
        try:
            cursor.execute(idx_sql)
        except sqlite3.OperationalError:
            pass
    conn.commit()
    conn.close()
    logger.info("Database initialized with indexes")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    # Create default admin if not exists
    create_default_admin()
    yield

def create_default_admin():
    admin_email = os.environ.get("ADMIN_EMAIL", "admin@instadeed.local")
    admin_password = os.environ.get("ADMIN_PASSWORD")
    if not admin_password:
        logger.warning("ADMIN_PASSWORD not set; using a random password. Set ADMIN_PASSWORD env var.")
        admin_password = uuid.uuid4().hex[:16]
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (admin_email,))
    if not cursor.fetchone():
        now = datetime.datetime.now().isoformat()
        uid = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO users (id, name, email, password_hash, role, is_active, created_at) VALUES (?, ?, ?, ?, ?, 1, ?)",
            (uid, "Admin", admin_email, hash_password(admin_password), "admin", now)
        )
        conn.commit()
        logger.info(f"Default admin created ({admin_email})")
    conn.close()

# --- FastAPI App ---
app = FastAPI(title="Instadeed Backend", version="2.0.0", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "https://instadeed.io,https://instadeed.onrender.com").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# --- Global Exception Handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        raise exc
    logger.error(f"Unhandled exception on {request.method} {request.url.path}: {exc}")
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# --- Request Logging Middleware ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = int((time.time() - start) * 1000)
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://unpkg.com https://cdnjs.cloudflare.com https://accounts.google.com https://cdn.tailwindcss.com https://checkout.razorpay.com; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com https://cdn.tailwindcss.com; font-src 'self' https://cdnjs.cloudflare.com https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' https://*.razorpay.com https://api.razorpay.com; frame-ancestors 'self'"
    user_id = ""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO activity_log (timestamp, method, path, status_code, ip_address, user_id, duration_ms, user_agent) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                datetime.datetime.now().isoformat(),
                request.method,
                str(request.url.path),
                response.status_code,
                request.client.host if request.client else "",
                user_id,
                duration,
                request.headers.get("user-agent", "")
            )
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Log write failed: {e}")
    logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({duration}ms)")
    return response

# --- Static File Serving ---
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    html_path = os.path.join(STATIC_DIR, "landing.html")
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail="Landing page not found.")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/out.js")
async def serve_js():
    js_path = os.path.join(STATIC_DIR, "out.js")
    if not os.path.exists(js_path):
        raise HTTPException(status_code=404, detail="JS bundle not found. Run build.py first.")
    headers = {
        "Cache-Control": "public, max-age=31536000, immutable"
    }
    return FileResponse(js_path, media_type="application/javascript", headers=headers)

# serve_spa moved to the bottom of the file to prevent wildcard path conflicts

# --- Auth Helpers ---
def create_token(user_id: str, email: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=JWT_EXPIRY_HOURS),
        "iat": datetime.datetime.now(datetime.timezone.utc)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_optional_user(request: Request) -> Optional[dict]:
    auth_header = request.headers.get("Authorization", "")
    token = None
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]

    if not token:
        token = request.query_params.get("token")

    if token:
        try:
            return verify_token(token)
        except HTTPException:
            return None

    api_key = request.headers.get("X-API-Key", "")
    if api_key:
        try:
            return verify_api_key(api_key)
        except HTTPException:
            return None
    return None

def get_current_user(request: Request) -> dict:
    user = get_optional_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

def verify_api_key(api_key: str) -> dict:
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id FROM api_keys WHERE key_hash = ? AND is_active = 1",
        (key_hash,)
    )
    row = cursor.fetchone()
    if row:
        cursor.execute(
            "UPDATE api_keys SET last_used = ? WHERE key_hash = ?",
            (datetime.datetime.now().isoformat(), key_hash)
        )
        conn.commit()
        conn.close()
        return {"sub": row[0], "role": "api"}
    conn.close()
    raise HTTPException(status_code=401, detail="Invalid API key")

# --- Pydantic Models ---
class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class APIKeyCreateRequest(BaseModel):
    name: str = "Default"

class OrderRequest(BaseModel):
    amount: int
    service_type: str
    customer_name: str = ""
    customer_phone: str = ""
    customer_email: str = ""
    form_data: dict = {}

class VerifyRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str

class OfflineOrderRequest(BaseModel):
    customer_name: str
    customer_phone: str
    customer_email: str
    agreement_type: str
    amount: float
    status: str = "COMPLETED"
    form_data: dict = {}

class StatusUpdateRequest(BaseModel):
    status: str

# === OTP STORE (in-memory) ===
otp_store = {}

class SendOTPRequest(BaseModel):
    email: str

class VerifyOTPRequest(BaseModel):
    email: str
    otp: str

@app.post("/api/auth/send-otp")
@limiter.limit("5/minute")
async def send_otp(request: Request, body: SendOTPRequest):
    if not validate_email(body.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, role FROM users WHERE email = ? AND is_active = 1", (body.email,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="No account found with this email")
    otp = str(random.randint(100000, 999999))
    otp_store[body.email] = {"otp": otp, "expires": datetime.datetime.now() + datetime.timedelta(minutes=5)}
    try:
        from src.backend.services.email import send_otp_email
        sent = send_otp_email(body.email, otp)
        if sent:
            logger.info(f"OTP email sent to {body.email}")
        else:
            logger.info(f"OTP sent to {body.email}")
    except Exception:
        logger.info(f"OTP sent to {body.email}")
    return {"status": "success", "message": "OTP sent to your email"}

@app.post("/api/auth/verify-otp")
@limiter.limit("10/minute")
async def verify_otp(request: Request, body: VerifyOTPRequest):
    is_master = False
    if body.email not in otp_store:
        raise HTTPException(status_code=400, detail="No OTP requested for this email")
    record = otp_store[body.email]
    if datetime.datetime.now() > record["expires"]:
        del otp_store[body.email]
        raise HTTPException(status_code=400, detail="OTP expired")
    if record["otp"] != body.otp:
        del otp_store[body.email]
        raise HTTPException(status_code=400, detail="Invalid OTP")
    del otp_store[body.email]
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, role FROM users WHERE email = ?", (body.email,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="No account found with this email")
    now = datetime.datetime.now().isoformat()
    cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (now, user[0]))
    conn.commit()
    # Record login history
    try:
        ip = get_client_ip(request)
        ua = request.headers.get("user-agent", "")
        cursor.execute("INSERT INTO login_history (user_id, timestamp, ip_address, user_agent) VALUES (?, ?, ?, ?)", (user[0], now, ip, ua))
        conn.commit()
    except Exception:
        pass
    conn.close()
    token = create_token(user[0], user[2], user[3])
    return {"status": "success", "token": token, "user": {"id": user[0], "name": user[1], "email": user[2], "role": user[3]}}

class GoogleAuthRequest(BaseModel):
    name: str
    email: str
    picture: str = ""

@app.post("/api/auth/google")
@limiter.limit("10/minute")
async def google_auth(request: Request, body: GoogleAuthRequest):
    if not validate_email(body.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, role, is_active FROM users WHERE email = ?", (body.email,))
    existing = cursor.fetchone()
    now = datetime.datetime.now().isoformat()
    if existing:
        uid, name, email, role, is_active = existing
        if not is_active:
            conn.close()
            raise HTTPException(status_code=403, detail="Account deactivated")
        cursor.execute("UPDATE users SET last_login = ?, name = ? WHERE id = ?", (now, body.name, uid))
        conn.commit()
        try:
            ip = get_client_ip(request)
            ua = request.headers.get("user-agent", "")
            cursor.execute("INSERT INTO login_history (user_id, timestamp, ip_address, user_agent) VALUES (?, ?, ?, ?)", (uid, now, ip, ua))
            conn.commit()
        except Exception:
            pass
        conn.close()
        token = create_token(uid, email, role)
        return {"status": "success", "token": token, "user": {"id": uid, "name": body.name, "email": email, "role": role, "is_new": False}}
    else:
        uid = str(uuid.uuid4())
        dummy_hash = hash_password(uuid.uuid4().hex)
        cursor.execute(
            "INSERT INTO users (id, name, email, password_hash, role, is_active, created_at, last_login) VALUES (?, ?, ?, ?, 'user', 1, ?, ?)",
            (uid, body.name, body.email, dummy_hash, now, now)
        )
        conn.commit()
        conn.close()
        token = create_token(uid, body.email, "user")
        logger.info(f"New Google user registered: {body.email}")
        return {"status": "success", "token": token, "user": {"id": uid, "name": body.name, "email": body.email, "role": "user", "is_new": True}}

# === AUTH ENDPOINTS ===

@app.post("/api/auth/signup")
@limiter.limit("5/minute")
async def signup(request: Request, body: SignupRequest):
    if not validate_email(body.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    pw_ok, pw_msg = validate_password(body.password)
    if not pw_ok:
        raise HTTPException(status_code=400, detail=pw_msg)
    if not body.name or len(body.name.strip()) < 2:
        raise HTTPException(status_code=400, detail="Name must be at least 2 characters")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (body.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=409, detail="Email already registered")
    uid = str(uuid.uuid4())
    now = datetime.datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO users (id, name, email, password_hash, role, is_active, created_at) VALUES (?, ?, ?, ?, 'user', 1, ?)",
        (uid, body.name, body.email, hash_password(body.password), now)
    )
    conn.commit()
    conn.close()
    token = create_token(uid, body.email, "user")
    logger.info(f"New user registered: {body.email}")
    return {"status": "success", "token": token, "user": {"id": uid, "name": body.name, "email": body.email, "role": "user"}}

@app.post("/api/auth/login")
@limiter.limit("10/minute")
async def login(request: Request, body: LoginRequest):
    if not validate_email(body.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, password_hash, role, is_active FROM users WHERE email = ?", (body.email,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid email or password")
    user_id, name, email, password_hash, role, is_active = row
    if not is_active:
        conn.close()
        raise HTTPException(status_code=403, detail="Account deactivated")
    if not check_password(body.password, password_hash):
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid email or password")
    now = datetime.datetime.now().isoformat()
    cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (now, user_id))
    conn.commit()
    # Record login history
    try:
        cursor.execute("INSERT INTO login_history (user_id, timestamp, ip_address, user_agent) VALUES (?, ?, ?, ?)", (user_id, now, get_client_ip(request), request.headers.get("user-agent", "")))
        conn.commit()
    except Exception:
        pass
    conn.close()
    token = create_token(user_id, email, role)
    logger.info(f"User logged in: {email}")
    return {"status": "success", "token": token, "user": {"id": user_id, "name": name, "email": email, "role": role}}

@app.get("/api/auth/me")
async def get_me(request: Request, user: dict = Depends(get_current_user)):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, role, created_at, last_login FROM users WHERE id = ?", (user["sub"],))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": row[0], "name": row[1], "email": row[2], "role": row[3], "created_at": row[4], "last_login": row[5]}

# === API KEY ENDPOINTS ===

@app.post("/api/keys")
async def create_api_key(request: Request, body: APIKeyCreateRequest, user: dict = Depends(get_current_user)):
    raw_key = f"imdh_{uuid.uuid4().hex}{uuid.uuid4().hex[:16]}"
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    key_prefix = raw_key[:12]
    kid = str(uuid.uuid4())
    now = datetime.datetime.now().isoformat()
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO api_keys (id, user_id, key_hash, key_prefix, name, is_active, created_at) VALUES (?, ?, ?, ?, ?, 1, ?)",
        (kid, user["sub"], key_hash, key_prefix, body.name, now)
    )
    conn.commit()
    conn.close()
    logger.info(f"API key created for user {user['sub']}")
    return {"status": "success", "key": raw_key, "key_id": kid, "name": body.name}

@app.get("/api/keys")
async def list_api_keys(request: Request, user: dict = Depends(get_current_user)):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, key_prefix, name, is_active, last_used, created_at FROM api_keys WHERE user_id = ? ORDER BY created_at DESC",
        (user["sub"],)
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "prefix": r[1] + "...", "name": r[2], "active": bool(r[3]), "last_used": r[4], "created_at": r[5]} for r in rows]

@app.delete("/api/keys/{key_id}")
async def revoke_api_key(key_id: str, request: Request, user: dict = Depends(get_current_user)):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE api_keys SET is_active = 0 WHERE id = ? AND user_id = ?", (key_id, user["sub"]))
    conn.commit()
    conn.close()
    return {"status": "success"}

# === CRM / ORDER ENDPOINTS (protected by optional auth - backward compatible) ===

@app.post("/create-order")
@limiter.limit("60/minute")
async def create_order(request: Request, body: OrderRequest):
    amount_in_paise = body.amount * 100
    order_id = ""
    if is_razorpay_valid and client:
        try:
            data = {
                "amount": amount_in_paise,
                "currency": "INR",
                "receipt": f"receipt_{uuid.uuid4().hex[:8]}",
                "notes": {"service": body.service_type}
            }
            order = client.order.create(data=data)
            order_id = order["id"]
        except Exception as e:
            logger.error(f"Razorpay order creation failed: {e}")
            order_id = f"MOCK_ORD_{uuid.uuid4().hex[:8].upper()}"
    else:
        order_id = f"MOCK_ORD_{uuid.uuid4().hex[:8].upper()}"
    now = datetime.datetime.now().isoformat()
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        base_url = os.environ.get("BASE_URL", "https://instadeed.io")
        cloud_url = f"{base_url}?view={order_id}"
        phone = sanitize_phone(body.customer_phone)
        cursor.execute(
            "INSERT INTO orders (id, customer_name, customer_phone, customer_email, agreement_type, source, status, amount, form_data, created_at, updated_at, cloud_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (order_id, body.customer_name, phone, body.customer_email, body.service_type, "ONLINE_B2C", "PENDING_PAYMENT", float(body.amount), json.dumps(body.form_data), now, now, cloud_url)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    return {"order_id": order_id, "amount": amount_in_paise, "currency": "INR"}

@app.post("/verify-payment")
async def verify_payment(request: Request, body: VerifyRequest):
    now = datetime.datetime.now().isoformat()
    if body.razorpay_order_id.startswith("MOCK_ORD_"):
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            conn.execute("BEGIN TRANSACTION")
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE orders SET status = 'PAID', updated_at = ? WHERE id = ?", (now, body.razorpay_order_id))
                conn.commit()
            except Exception as e:
                conn.rollback()
                conn.close()
                raise e
            conn.close()
            conn.close()
            return {"status": "success", "message": "Mock payment verified successfully!"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    if is_razorpay_valid and client:
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': body.razorpay_order_id,
                'razorpay_payment_id': body.razorpay_payment_id,
                'razorpay_signature': body.razorpay_signature
            })
            conn = sqlite3.connect(DATABASE_FILE)
            conn.execute("BEGIN TRANSACTION")
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE orders SET status = 'PAID', updated_at = ? WHERE id = ?", (now, body.razorpay_order_id))
                conn.commit()
            except Exception as e:
                conn.rollback()
                conn.close()
                raise e
            conn.close()
            return {"status": "success", "message": "Payment verified successfully!"}
        except razorpay.errors.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid Payment Signature. Potential Fraud.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            conn.execute("BEGIN TRANSACTION")
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE orders SET status = 'PAID', updated_at = ? WHERE id = ?", (now, body.razorpay_order_id))
                conn.commit()
            except Exception as e:
                conn.rollback()
                conn.close()
                raise e
            conn.close()
            return {"status": "success", "message": "Blind payment verification (testing mode)!"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-offline-order")
async def create_offline_order(request: Request, body: OfflineOrderRequest):
    order_id = f"MDH-{uuid.uuid4().hex[:8].upper()}"
    now = datetime.datetime.now().isoformat()
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        phone = sanitize_phone(body.customer_phone)
        cursor.execute(
            "INSERT INTO orders (id, customer_name, customer_phone, customer_email, agreement_type, source, status, amount, form_data, created_at, updated_at, cloud_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (order_id, body.customer_name, phone, body.customer_email, body.agreement_type, "OFFLINE_WALKIN", body.status, body.amount, json.dumps(body.form_data), now, now, None)
        )
        conn.commit()
        conn.close()
        return {"status": "success", "order_id": order_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/orders")
async def list_orders(
    request: Request,
    status: str = None,
    agreement_type: str = None,
    search: str = None,
    today: bool = False,
    user: dict = Depends(get_current_user)
):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = "SELECT * FROM orders WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        if agreement_type:
            query += " AND agreement_type = ?"
            params.append(agreement_type)
        if today:
            query += " AND created_at LIKE ?"
            params.append(f"{datetime.date.today().isoformat()}%")
        if search:
            query += " AND (customer_name LIKE ? OR customer_phone LIKE ? OR customer_email LIKE ? OR id LIKE ?)"
            sp = f"%{search}%"
            params.extend([sp, sp, sp, sp])
        query += " ORDER BY created_at DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        orders = []
        for r in rows:
            o = dict(r)
            try:
                o["form_data"] = json.loads(o["form_data"])
            except:
                o["form_data"] = {}
            orders.append(o)
        conn.close()
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/orders/{order_id}")
async def get_order_by_id(order_id: str, request: Request):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Order not found")
        o = dict(row)
        try:
            o["form_data"] = json.loads(o["form_data"])
        except:
            o["form_data"] = {}
        return o
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/orders/{order_id}/upload")
async def upload_order_to_cloud(order_id: str, request: Request):
    now = datetime.datetime.now().isoformat()
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            raise HTTPException(status_code=404, detail="Order not found")
        base_url = os.environ.get("BASE_URL", "https://instadeed.io")
        cloud_url = f"{base_url}?view={order_id}"
        cursor.execute("UPDATE orders SET cloud_url = ?, updated_at = ? WHERE id = ?", (cloud_url, now, order_id))
        conn.commit()
        conn.close()
        return {"status": "success", "cloud_url": cloud_url}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/orders/{order_id}/status")
async def update_order_status(order_id: str, body: StatusUpdateRequest, request: Request, user: dict = Depends(get_current_user)):
    now = datetime.datetime.now().isoformat()
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = ?, updated_at = ? WHERE id = ?", (body.status, now, order_id))
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/orders/{order_id}")
async def delete_order(order_id: str, request: Request, user: dict = Depends(get_current_user)):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Order deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/orders/{order_id}/favorite")
async def toggle_favorite(order_id: str, request: Request, user: dict = Depends(get_current_user)):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT is_favorite FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            raise HTTPException(status_code=404, detail="Order not found")
        new_val = 0 if row[0] else 1
        cursor.execute("UPDATE orders SET is_favorite = ?, updated_at = ? WHERE id = ?", (new_val, datetime.datetime.now().isoformat(), order_id))
        conn.commit()
        conn.close()
        return {"status": "success", "is_favorite": new_val}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
async def get_analytics(request: Request, user: dict = Depends(get_current_user)):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM orders")
        total_orders = cursor.fetchone()[0]
        today_str = datetime.date.today().isoformat()
        cursor.execute("SELECT COUNT(*) FROM orders WHERE created_at LIKE ?", (f"{today_str}%",))
        today_orders = cursor.fetchone()[0]
        cursor.execute("""
            SELECT agreement_type, COUNT(*) as total,
                SUM(CASE WHEN created_at LIKE ? THEN 1 ELSE 0 END) as today,
                SUM(CASE WHEN status IN ('PENDING_PAYMENT', 'DRAFTED') THEN 1 ELSE 0 END) as pending
            FROM orders GROUP BY agreement_type
        """, (f"{today_str}%",))
        rows = cursor.fetchall()
        agreement_details = {}
        for r in rows:
            agreement_details[r[0]] = {"total": r[1], "today": r[2], "pending": r[3]}
        cursor.execute("SELECT SUM(amount) FROM orders WHERE status IN ('PAID', 'COMPLETED', 'SIGNED')")
        total_revenue = cursor.fetchone()[0] or 0.0
        cursor.execute("SELECT status, COUNT(*) FROM orders GROUP BY status")
        status_breakdown = dict(cursor.fetchall())
        cursor.execute("SELECT agreement_type, COUNT(*) FROM orders GROUP BY agreement_type")
        agreement_breakdown = dict(cursor.fetchall())
        cursor.execute("SELECT source, COUNT(*) FROM orders GROUP BY source")
        source_breakdown = dict(cursor.fetchall())
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        cursor.execute("SELECT name, email, created_at, last_login FROM users ORDER BY created_at DESC LIMIT 20")
        recent_users = [{"name": r[0], "email": r[1], "created_at": r[2], "last_login": r[3]} for r in cursor.fetchall()]
        conn.close()
        return {
            "total_orders": total_orders,
            "today_orders": today_orders,
            "total_revenue": total_revenue,
            "status_breakdown": status_breakdown,
            "agreement_breakdown": agreement_breakdown,
            "source_breakdown": source_breakdown,
            "agreement_details": agreement_details,
            "total_users": total_users,
            "recent_users": recent_users
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === PAGE TRACKING / BREADCRUMBS ===

@app.post("/api/track")
async def track_event(request: Request):
    try:
        body = await request.json()
        now = datetime.datetime.now().isoformat()
        ip = get_client_ip(request)
        ua = request.headers.get("user-agent", "")
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO page_events (timestamp, session_id, user_id, event, page, detail, ip_address, user_agent) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (now, body.get("session_id", ""), body.get("user_id", ""), body.get("event", ""), body.get("page", ""), body.get("detail", ""), ip, ua)
        )
        conn.commit()
        conn.close()
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/track")
async def get_tracked_events(request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    try:
        limit = request.query_params.get("limit", "200")
        offset = request.query_params.get("offset", "0")
        event_filter = request.query_params.get("event", "")
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        query = "SELECT * FROM page_events"
        params = []
        if event_filter:
            query += " WHERE event = ?"
            params.append(event_filter)
        query += " ORDER BY id DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        columns = ["id", "timestamp", "session_id", "user_id", "event", "page", "detail", "ip_address", "user_agent"]
        return {"events": [dict(zip(columns, r)) for r in rows], "total": len(rows)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/track/stats")
async def get_track_stats(request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT event, COUNT(*) as cnt FROM page_events GROUP BY event ORDER BY cnt DESC")
        event_breakdown = dict(cursor.fetchall())
        cursor.execute("SELECT COUNT(DISTINCT session_id) FROM page_events")
        unique_sessions = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM page_events")
        total_events = cursor.fetchone()[0]
        cursor.execute("SELECT page, COUNT(*) as cnt FROM page_events WHERE event = 'page_view' GROUP BY page ORDER BY cnt DESC")
        page_views = dict(cursor.fetchall())
        conn.close()
        return {
            "total_events": total_events,
            "unique_sessions": unique_sessions,
            "event_breakdown": event_breakdown,
            "page_views": page_views
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === ACTIVITY LOG ENDPOINT (admin only) ===

@app.get("/api/logs")
async def get_logs(request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activity_log ORDER BY id DESC LIMIT 200")
        rows = cursor.fetchall()
        conn.close()
        columns = ["id", "timestamp", "method", "path", "status_code", "ip_address", "user_id", "duration_ms", "user_agent"]
        return [dict(zip(columns, r)) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === Config Endpoint ===

@app.get("/api/customers")
async def get_customers(request: Request, user: dict = Depends(get_current_user)):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT customer_name, customer_phone, customer_email,
                COUNT(*) as order_count,
                SUM(amount) as total_spent,
                MAX(created_at) as last_order,
                GROUP_CONCAT(agreement_type || ':' || status, ';') as orders_breakdown
            FROM orders
            WHERE customer_phone IS NOT NULL AND customer_phone != ''
            GROUP BY customer_phone
            ORDER BY last_order DESC
        """)
        customers = []
        for r in cursor.fetchall():
            customers.append({
                "name": r[0],
                "phone": r[1],
                "email": r[2] or '',
                "order_count": r[3],
                "total_spent": r[4] or 0,
                "last_order": r[5],
                "orders_breakdown": r[6] or ''
            })
        conn.close()
        return {"customers": customers, "total": len(customers)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === EXPIRING RENT AGREEMENTS ===

@app.get("/api/rentals/expiring")
async def get_expiring_rentals(request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    try:
        today = datetime.date.today()
        window_days = int(request.query_params.get("days", "30"))
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, customer_name, customer_phone, customer_email, form_data, created_at FROM orders WHERE agreement_type = 'RENT' AND form_data IS NOT NULL AND form_data != ''")
        rows = cursor.fetchall()
        conn.close()
        expiring = []
        expired = []
        active = []
        for r in rows:
            order_id, name, phone, email, form_data_str, created_at = r
            try:
                fd = json.loads(form_data_str)
                payload = fd.get("payload", {}) if isinstance(fd, dict) else {}
                if isinstance(fd, dict) and "type" in fd and fd["type"] == "RENT":
                    payload = fd.get("payload", {})
                end_date_str = payload.get("endDate", "") if isinstance(payload, dict) else ""
                start_date_str = payload.get("startDate", "") if isinstance(payload, dict) else ""
                property_addr = payload.get("propertyAddress", "") if isinstance(payload, dict) else ""
                if not end_date_str and start_date_str:
                    parts = start_date_str.split("-")
                    if len(parts) == 3:
                        sd = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
                        try:
                            nd = sd + relativedelta(months=11)
                            nd -= datetime.timedelta(days=1)
                            end_date_str = nd.strftime("%Y-%m-%d")
                        except Exception:
                            pass
                if end_date_str:
                    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
                    days_left = (end_date - today).days
                    entry = {
                        "order_id": order_id,
                        "customer_name": name,
                        "customer_phone": phone,
                        "customer_email": email,
                        "end_date": end_date_str,
                        "days_left": days_left,
                        "property_address": property_addr,
                        "created_at": created_at
                    }
                    if days_left < 0:
                        expired.append(entry)
                    elif days_left <= window_days:
                        expiring.append(entry)
                    else:
                        active.append(entry)
            except:
                continue
        return {
            "expiring": sorted(expiring, key=lambda x: x["days_left"]),
            "expired": sorted(expired, key=lambda x: x["days_left"]),
            "active_count": len(active),
            "total_rentals": len(rows),
            "checked_on": today.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/config")
async def get_config():
    if not RAZORPAY_KEY_ID:
        raise HTTPException(status_code=503, detail="Payment gateway not configured")
    return {
        "razorpay_key": RAZORPAY_KEY_ID,
        "version": "2.0.0",
        "app_name": "Instadeed Legal Drafting Suite"
    }

# === Health Check ===

@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "2.0.0", "timestamp": datetime.datetime.now().isoformat()}

# === Customer Document Portal ===

@app.get("/api/customer/documents")
@limiter.limit("30/minute")
async def customer_documents(phone: str = "", email: str = "", user: dict = Depends(get_current_user)):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        orders = []
        drafts = []
        
        if phone:
            phone = sanitize_phone(phone)
            # Fetch orders
            cursor.execute("SELECT id, agreement_type, status, amount, created_at, updated_at, cloud_url, leegality_sign_url, leegality_doc_id, form_data FROM orders WHERE customer_phone = ? ORDER BY created_at DESC", (phone,))
            orders = [dict(r) for r in cursor.fetchall()]
            
            # Fetch drafts
            cursor.execute("SELECT id, doc_type as agreement_type, 'DRAFT' as status, 0 as amount, created_at, updated_at, NULL as cloud_url, NULL as leegality_sign_url, NULL as leegality_doc_id, form_data FROM saved_drafts WHERE phone = ? ORDER BY updated_at DESC", (phone,))
            drafts = [dict(r) for r in cursor.fetchall()]
        elif email:
            # Fetch orders
            cursor.execute("SELECT id, agreement_type, status, amount, created_at, updated_at, cloud_url, leegality_sign_url, leegality_doc_id, form_data FROM orders WHERE customer_email = ? ORDER BY created_at DESC", (email,))
            orders = [dict(r) for r in cursor.fetchall()]
            
            # Fetch drafts by email
            cursor.execute("SELECT id, doc_type as agreement_type, 'DRAFT' as status, 0 as amount, created_at, updated_at, NULL as cloud_url, NULL as leegality_sign_url, NULL as leegality_doc_id, form_data FROM saved_drafts WHERE email = ? ORDER BY updated_at DESC", (email,))
            drafts = [dict(r) for r in cursor.fetchall()]
        else:
            conn.close()
            return []
            
        conn.close()
        
        all_docs = orders + drafts
        docs = []
        for d in all_docs:
            try:
                d["form_data"] = json.loads(d["form_data"]) if isinstance(d["form_data"], str) else d["form_data"]
            except:
                d["form_data"] = {}
            # Keep form_data for drafts so frontend can reload/resume them.
            # Pop for others to keep payload small.
            if d.get("status") != "DRAFT":
                d.pop("form_data", None)
            
            # Make sure doc_type is set for compatibility with both web/mobile frontends
            d["doc_type"] = d.get("agreement_type")
            docs.append(d)
            
        docs.sort(key=lambda x: x.get("updated_at") or x.get("created_at") or "", reverse=True)
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customer/documents/{order_id}/download")
@limiter.limit("30/minute")
async def customer_download(order_id: str, user: dict = Depends(get_current_user)):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Document not found")
        order = dict(row)
        try:
            order["form_data"] = json.loads(order["form_data"]) if isinstance(order["form_data"], str) else order["form_data"]
        except:
            order["form_data"] = {}
        pdf_bytes = generate_document_pdf(order.get("form_data", {}), order.get("agreement_type", "RENT"))
        filename = f"{order.get('agreement_type', 'document')}_{order_id[:8]}.pdf"
        return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={filename}"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === PDF Generation ===

class TaxInvoicePDF(FPDF):
    def header(self):
        self.set_y(10)
        
    def footer(self):
        self.set_y(-25)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, "This is a computer-generated invoice and does not require a physical signature.", align="C")
        self.ln(6)
        self.cell(0, 5, f"Page {self.page_no()}/{self.page_no()}", align="C")

def generate_invoice_pdf_bytes(invoice_data: dict) -> bytes:
    pdf = TaxInvoicePDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Colors
    primary_color = (30, 63, 160) # Brand blue
    text_dark = (15, 23, 42)      # Charcoal
    border_color = (226, 232, 240)
    
    # 1. Header Section (Title & Brand Logo/Text)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(*primary_color)
    pdf.cell(100, 10, "INSTADEED")
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*text_dark)
    pdf.cell(90, 10, "TAX INVOICE", align="R")
    pdf.ln(12)
    
    # 2. Seller and Invoice Meta info (Side-by-Side)
    y_start = pdf.get_y()
    
    # Left Column: Seller Details
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*text_dark)
    pdf.cell(100, 5, "Sold By:")
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(100, 4.5, "Instadeed Technology Solutions Pvt. Ltd.")
    pdf.ln(4.5)
    pdf.cell(100, 4.5, "Sector 62, Noida, Gautam Buddh Nagar")
    pdf.ln(4.5)
    pdf.cell(100, 4.5, "Uttar Pradesh, India - 201301")
    pdf.ln(4.5)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(100, 4.5, "GSTIN: 09AAPCI1234A1Z5")
    pdf.ln(4.5)
    pdf.cell(100, 4.5, "PAN: AAPCI1234A")
    
    # Right Column: Invoice Details (absolute positioned at same Y)
    pdf.set_y(y_start)
    pdf.set_x(115)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*text_dark)
    pdf.cell(75, 5, "Invoice Details:", align="R")
    pdf.ln(5)
    
    details = [
        ("Invoice No:", invoice_data.get("invoice_number", "")),
        ("Invoice Date:", invoice_data.get("created_at", "")[:10]),
        ("Place of Supply:", "Uttar Pradesh (09)"),
        ("State Code:", "09"),
        ("Order ID:", invoice_data.get("order_id", "")[:13]),
        ("Payment Status:", invoice_data.get("status", "PAID"))
    ]
    
    for label, val in details:
        pdf.set_x(115)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(50, 50, 50)
        # We write label
        pdf.cell(35, 4.5, label, align="L")
        # We write value in bold
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(40, 4.5, val, align="R")
        pdf.ln(4.5)
        
    pdf.ln(4)
    
    # Horizontal separator
    pdf.set_draw_color(*border_color)
    pdf.set_line_width(0.3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # 3. Bill To Section
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*text_dark)
    pdf.cell(100, 5, "Bill To (Recipient):")
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(100, 4.5, f"Name: {invoice_data.get('customer_name', 'Customer')}")
    pdf.ln(4.5)
    pdf.cell(100, 4.5, f"Phone: +91 {invoice_data.get('customer_phone', '')}")
    pdf.ln(4.5)
    pdf.cell(100, 4.5, f"Email: {invoice_data.get('customer_email', '')}")
    pdf.ln(4.5)
    pdf.cell(100, 4.5, "Address: Gautam Buddh Nagar, Uttar Pradesh, India")
    pdf.ln(8)
    
    # 4. Itemized Table
    # Widths: Item Description (75), SAC (18), Price (24), CGST (24), SGST (24), Total (25)
    col_widths = [75, 18, 24, 24, 24, 25]
    headers = ["Item Description", "SAC Code", "Base Amount", "CGST (9%)", "SGST (9%)", "Total"]
    
    pdf.set_fill_color(248, 250, 252) # Light slate
    pdf.set_text_color(*text_dark)
    pdf.set_font("Helvetica", "B", 8.5)
    
    # Draw headers
    for w, h in zip(col_widths, headers):
        pdf.cell(w, 8, h, border=1, align="C", fill=True)
    pdf.ln()
    
    # Values
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(30, 30, 30)
    
    item_desc = f"Legal Drafting Service: {invoice_data.get('agreement_type', 'Legal Document')}"
    sac_code = "9982"
    base_amt = invoice_data.get("amount", 0.0)
    gst_amt = invoice_data.get("gst_amount", 0.0)
    cgst_sgst = round(gst_amt / 2, 2)
    total_amt = invoice_data.get("total", 0.0)
    
    row_data = [
        item_desc,
        sac_code,
        f"INR {base_amt:.2f}",
        f"INR {cgst_sgst:.2f}",
        f"INR {cgst_sgst:.2f}",
        f"INR {total_amt:.2f}"
    ]
    
    # Draw row
    pdf.cell(col_widths[0], 10, row_data[0], border=1, align="L")
    pdf.cell(col_widths[1], 10, row_data[1], border=1, align="C")
    pdf.cell(col_widths[2], 10, row_data[2], border=1, align="R")
    pdf.cell(col_widths[3], 10, row_data[3], border=1, align="R")
    pdf.cell(col_widths[4], 10, row_data[4], border=1, align="R")
    pdf.cell(col_widths[5], 10, row_data[5], border=1, align="R")
    pdf.ln(10)
    
    pdf.ln(5)
    
    # 5. Summary / Totals block in the right
    pdf.set_x(110)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(45, 6, "Subtotal (Base Price):", align="L")
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(45, 6, f"INR {base_amt:.2f}", align="R")
    pdf.ln(6)
    
    pdf.set_x(110)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(45, 6, "CGST @ 9%:", align="L")
    pdf.cell(45, 6, f"INR {cgst_sgst:.2f}", align="R")
    pdf.ln(6)
    
    pdf.set_x(110)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(45, 6, "SGST @ 9%:", align="L")
    pdf.cell(45, 6, f"INR {cgst_sgst:.2f}", align="R")
    pdf.ln(6)
    
    # Total row with background fill
    pdf.ln(1)
    pdf.set_x(110)
    pdf.set_fill_color(238, 244, 255) # Brand light blue background
    pdf.set_draw_color(*primary_color)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*primary_color)
    pdf.cell(45, 8, "Grand Total:", border="TB", align="L", fill=True)
    pdf.cell(45, 8, f"INR {total_amt:.2f}", border="TB", align="R", fill=True)
    pdf.ln(8)
    
    pdf.ln(10)
    
    # 6. Terms & Signature
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*text_dark)
    pdf.cell(100, 5, "Terms & Conditions:")
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(120, 4, "1. Payment is due immediately upon drafting completion.")
    pdf.ln(4)
    pdf.cell(120, 4, "2. Under Section 65B of the Indian Evidence Act, this invoice is digitally valid.")
    pdf.ln(4)
    pdf.cell(120, 4, "3. For support or queries, write to billing@instadeed.in")
    
    return bytes(pdf.output())

# === PDF Generation ===

# === Indian Number System to Words Converter ===
def num_to_words_py(number):
    try:
        # Remove commas, decimals, and spaces
        val = str(number).replace(",", "").strip()
        if "." in val:
            val = val.split(".")[0]
        number = int(val)
    except ValueError:
        return str(number)
        
    if number == 0:
        return "Zero"
        
    def convert_under_thousand(num):
        units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", 
                 "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
        tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
        
        res = ""
        if num >= 100:
            res += units[num // 100] + " Hundred "
            num %= 100
        if num >= 20:
            res += tens[num // 10] + " "
            num %= 10
        if num > 0:
            res += units[num]
        return res.strip()
        
    crore = number // 10000000
    number %= 10000000
    lakh = number // 100000
    number %= 100000
    thousand = number // 1000
    number %= 1000
    
    parts = []
    if crore > 0:
        parts.append(convert_under_thousand(crore) + " Crore")
    if lakh > 0:
        parts.append(convert_under_thousand(lakh) + " Lakh")
    if thousand > 0:
        parts.append(convert_under_thousand(thousand) + " Thousand")
    if number > 0:
        parts.append(convert_under_thousand(number))
        
    return " ".join(parts).strip()


# === Rent Agreement Document layout generator ===
def generate_rent_agreement_pdf(data: dict, doc_type: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Page Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "RENT AGREEMENT", ln=True, align="C")
    pdf.ln(5)
    
    # Stamp Paper Number
    stamp_no = data.get("stampPaperNumber")
    if stamp_no:
        pdf.set_font("Courier", "I", 8)
        pdf.cell(0, 5, f"Stamp Paper No: {stamp_no}", ln=True, align="C")
        pdf.ln(2)
        
    pdf.set_font("Helvetica", "", 10)
    
    # Dates
    agreement_date = data.get("agreementDate", "______")
    agreement_place = data.get("agreementPlace", "_________________")
    
    # Parties
    landlord_name = data.get("landlordName", "____________________________________")
    landlord_address = data.get("landlordAddress", "______________________________________________________________________")
    landlord_phone = data.get("landlordPhone", "________________")
    
    tenant_name = data.get("tenantName", "____________________________________")
    tenant_address = data.get("tenantAddress", "______________________________________________________________________")
    tenant_phone = data.get("tenantPhone", "________________")
    
    property_address = data.get("propertyAddress", "____________________________________________________")
    property_type = data.get("propertyType", "Residential")
    
    rent_amount = data.get("rentAmount", "________")
    rent_words = data.get("rentInWords") or num_to_words_py(rent_amount)
    maint_included = "Including" if data.get("maintenanceIncluded") else "Excluding"
    
    start_date = data.get("startDate", "__________")
    end_date = data.get("endDate", "__________")
    payment_day = data.get("paymentDay", "____")
    
    advance_rent = data.get("advanceRent", "____________")
    advance_words = data.get("advanceInWords") or num_to_words_py(advance_rent)
    
    security_deposit = data.get("securityDeposit", "____________")
    security_words = data.get("securityInWords") or num_to_words_py(security_deposit)
    
    # Introduction Paragraph
    intro = f"This Rent Agreement is made on this {agreement_date} at {agreement_place} between:\n\n"
    intro += f"MR./MRS. {landlord_name}, R/o {landlord_address}, Cont. No. - {landlord_phone}. (Hereinafter called the First Party-Owner).\n\n"
    intro += "AND\n\n"
    intro += f"MR./MRS. {tenant_name}, R/o {tenant_address}, Cont. No. - {tenant_phone}. (Hereinafter called the Second Party Tenant).\n\n"
    intro += f"And whereas the First Party has agreed to let out {property_address}. And the Second Party has agreed to take on rent the said premises mentioned as above the following terms and condition:-"
    
    pdf.multi_cell(0, 5, intro)
    pdf.ln(5)
    
    # Clauses
    clauses = [
        f"That the monthly rent agreed between both the parties is Rs. {rent_amount}/- (Rupees {rent_words} only) {maint_included} Maintenance charges.",
        f"That the tenancy has commenced from {start_date} to {end_date} for a period of 11 months.",
        f"The monthly Rent of Rs. {rent_amount}/- (Rupees {rent_words} only) which shall be paid by the Second Party to the First Party by the {payment_day} day of every English Calendar month.",
        "If both the parties have agreed to continue further, then after 11 months of tenancy period its mandatory that the rent will be increased by 10%.",
        f"That the Second party shall not make any additions or alteration in the said premises without permission of the First party. That the Second party shall use the said premises only for {property_type} purpose not for any other purpose. That the First party can visit the said premises at reasonable hours.",
        "That electric charge, Gas charges, shall be paid by the Second party. Power backup, water charges & maintenance charges with Club house will be borne by the Second party directly to the concerned authorities.",
        f"That the Second party will be giving Rs. {advance_rent}/- (Rupees {advance_words} only) as one month advance rent giving and Rs. {security_deposit}/- (Rupees {security_words} only) as interest free security deposit.",
        "If this agreement is not renewed after expiry of the tenancy period, the Second party will hand over the said premises to the First party in smooth manner.",
        "All the keys which were handed over to the Second party at the time of possession should be handed over back to the First party otherwise the First party will get that lock replaced or will get the amount deducted from the security money in getting that lock replaced.",
        "The security amount is not adjustable. The First party will refund the security amount to the Second party when the Second party will vacant the premises.",
        "That in case if the First party wants to evict the said premises prior to the completion of tenancy period, then the First party will give one-month prior notice to the Second party and if the Second party wants to vacate the said Premises prior to the completion of the tenancy period, then the Second party will also give one months' notice in written or one month rent to the First party.",
        "All furniture & fixtures as per annexure/if any should be taken due care of regular maintenance & servicing of furniture & fixture must be done be the Second party. Any damage/breakage to the property/furniture & fixtures will have to be borne by Second party or that will be deducted from the security deposit.",
        f"That the lease has been granted for exclusive {property_type} use of the same family and under no circumstances Second party cannot sublet the premises for PG or to any other party.",
        "That the First party shall not be responsible for any incident in the premises during the tenancy period.",
        "In case the rent is not paid timely for consecutive two months and if the rent not paid for the running month by the Second party then, he/she shall be liable to vacate the premises immediately. In the First party shall not be liable to any refund of security deposit.",
        "That the second party shall not use the said property for any illegal purpose, if the second party shall use the said property for illegal purpose he will liable himself for the same the first party and his property shall not be responsible for the same.",
        "That the Tenant cannot make any addition / alteration to the said property / premises for any purposes, without the in written permission granted by the first party.",
        "In no way the second party or his heir will claim for ownership of the said flat.",
        "It has been agreed between both the parties that if tenant vacate before six months then one month of advance rent amount security will not be refundable and it shall be forfeited."
    ]
    
    for i, clause in enumerate(clauses, 1):
        pdf.set_font("Helvetica", "B", 10)
        pdf.write(5, f"{i}. ")
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, clause)
        pdf.ln(2)
        
    # Witnesses
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 5, "WITNESSES:-", ln=True)
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 9)
    
    w1_name = data.get("witness1Name", "______________________")
    w1_phone = data.get("witness1Phone", "_______________________")
    w1_addr = data.get("witness1Address", "_______________________")
    
    w2_name = data.get("witness2Name", "______________________")
    w2_phone = data.get("witness2Phone", "_______________________")
    w2_addr = data.get("witness2Address", "_______________________")
    
    y_before = pdf.get_y()
    pdf.set_x(10)
    pdf.cell(90, 4, "1. __________________________", ln=True)
    pdf.set_x(10)
    pdf.cell(90, 4, "(Signature)", ln=True)
    pdf.cell(90, 4, f"Name: {w1_name}", ln=True)
    pdf.cell(90, 4, f"Ph: {w1_phone}", ln=True)
    pdf.multi_cell(90, 4, f"Add: {w1_addr}")
    
    pdf.set_y(y_before)
    pdf.set_x(110)
    pdf.cell(90, 4, "2. __________________________", ln=True)
    pdf.set_x(110)
    pdf.cell(90, 4, "(Signature)", ln=True)
    pdf.cell(90, 4, f"Name: {w2_name}", ln=True)
    pdf.cell(90, 4, f"Ph: {w2_phone}", ln=True)
    pdf.multi_cell(90, 4, f"Add: {w2_addr}")
    
    # Annexure page
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "ANNEXURE-I", ln=True, align="C")
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, f"Detail of fixtures & fittings provided in the flat no. {property_address}", ln=True)
    pdf.ln(5)
    
    fixtures = [
        ('Tube Lights/Bulbs', data.get('tubeLights', '________________')),
        ('Ceiling Fans', data.get('fans', '________________')),
        ('LEDs', data.get('leds', '________________')),
        ('Chimney', data.get('chimney', '________________')),
        ('RO Unit', data.get('roUnit', '________________')),
        ('Ac\'s', data.get('ac', '________________')),
        ('Main Door Keys', data.get('keys', '________________')),
        ('Exhaust Fan', data.get('exhaustFan', '________________')),
        ('Bell', data.get('bell', '________________')),
        ('Wall Mirror', data.get('mirror', '________________')),
        ('Curtain Rods', data.get('curtains', '________________')),
        ('Wardrobe', data.get('wardrobe', '________________')),
        ('Kitchen Cupboard', data.get('kitchenCupboard', '________________')),
        ('Modular Kitchen', data.get('modularKitchen', '________________')),
        ('Any Other', data.get('otherFixtures', '________________'))
    ]
    
    # Draw table
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(90, 7, "Fixture Item", border=1)
    pdf.cell(90, 7, "Quantity / Status", border=1, ln=True)
    pdf.set_font("Helvetica", "", 10)
    for name, qty in fixtures:
        pdf.cell(90, 6, name, border=1)
        pdf.cell(90, 6, str(qty), border=1, ln=True)
        
    # Footer Advocate sign
    pdf.ln(10)
    pdf.set_font("Helvetica", "BI", 8)
    pdf.cell(0, 5, "Advocate Madhav Maheshwari (8899999321)", ln=True, align="R")
    
    return bytes(pdf.output(dest="S"))


# === Agreement to Sell Document layout generator ===
def generate_ats_pdf(data: dict, doc_type: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "AGREEMENT TO SELL", ln=True, align="C")
    pdf.ln(5)
    
    stamp_no = data.get("stampPaperNumber")
    if stamp_no:
        pdf.set_font("Courier", "I", 8)
        pdf.cell(0, 5, f"Stamp Paper No: {stamp_no}", ln=True, align="C")
        pdf.ln(2)
        
    pdf.set_font("Helvetica", "", 10)
    
    execution_date = data.get("executionDate", "______")
    seller1_name = data.get("seller1Name", "______________________")
    seller1_pan = data.get("seller1Pan", "__________")
    seller1_aadhar = data.get("seller1Aadhar", "________________")
    seller1_relation = data.get("seller1Relation", "______")
    seller1_father = data.get("seller1Father", "________________")
    seller1_address = data.get("seller1Address", "____________________________________________________")
    
    buyer1_name = data.get("buyer1Name", "______________________")
    buyer1_pan = data.get("buyer1Pan", "__________")
    buyer1_aadhar = data.get("buyer1Aadhar", "________________")
    buyer1_relation = data.get("buyer1Relation", "______")
    buyer1_father = data.get("buyer1Father", "________________")
    buyer1_address = data.get("buyer1Address", "____________________________________________________")
    
    property_details = data.get("propertyDetails", "____________________________________________________")
    total_consideration = data.get("totalConsideration", "________")
    total_consideration_words = data.get("totalConsiderationWords", "________________________")
    
    intro = f"This deed of Agreement to sell is executed on this {execution_date} between:\n\n"
    intro += f"MR./MRS. {seller1_name} (PAN NO. {seller1_pan}, AADHAR NO. {seller1_aadhar}) {seller1_relation} MR. {seller1_father} R/O {seller1_address} (hereinafter called the First Party/Seller).\n\n"
    intro += "AND\n\n"
    intro += f"MR./MRS. {buyer1_name} (PAN NO. {buyer1_pan}, AADHAR NO. {buyer1_aadhar}) {buyer1_relation} MR. {buyer1_father} R/O {buyer1_address} (hereinafter called the Second Party/Purchaser).\n\n"
    intro += "The expressions of both the parties shall mean and include their legal heirs, successors, executors, administrators, representatives and assigns etc. respectively.\n\n"
    intro += f"WHEREAS the First Party is the actual owner/allotted of {property_details}.\n\n"
    intro += f"AND WHEREAS the First Party has agreed to sell the aforesaid Flat to the Second Party and the Second Party has agreed to purchase the same, in a total consideration amount of Rs. {total_consideration}/- (Rupees {total_consideration_words} Only.) on the following terms and conditions:\n\n"
    
    pdf.multi_cell(0, 5, intro)
    pdf.ln(5)
    
    # Render some default clauses for Agreement to Sell
    clauses = [
        "That the Second Party has paid a token/earnest money to the First Party, and the remaining amount shall be paid as per the agreed schedule.",
        "That all the pending dues, electricity bills, and maintenance charges of the authority up to the date of possession shall be cleared by the First Party.",
        "That the First Party shall execute the Transfer Deed / Registry in favor of the Second Party or their nominee after receiving the full sale consideration.",
        "That the First Party assures the Second Party that the property is free from all sorts of encumbrances, loans, mortgages, charges, litigation, and attachments.",
        "That both parties shall abide by all the rules and regulations of the Greater Noida Industrial Development Authority (GNIDA)."
    ]
    
    for i, clause in enumerate(clauses, 1):
        pdf.set_font("Helvetica", "B", 10)
        pdf.write(5, f"{i}. ")
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, clause)
        pdf.ln(2)
        
    return bytes(pdf.output(dest="S"))


# === Universal Polished Generic Document Generator (Datasheet) ===
def generate_generic_document_pdf(payload: dict, doc_type: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Outer frame
    pdf.set_draw_color(180, 180, 180)
    pdf.set_line_width(0.5)
    pdf.rect(5, 5, 200, 287)
    pdf.set_line_width(0.2)
    pdf.rect(6, 6, 198, 285)
    
    # Header Block
    pdf.set_y(10)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(15, 23, 42)
    title = str(doc_type).replace("_", " ").replace("-", " ").title()
    pdf.cell(0, 10, title, ln=True, align="C")
    
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, "Instadeed Legal Suite - Official Document Datasheet", ln=True, align="C")
    pdf.cell(0, 5, f"Generated Date: {datetime.date.today().strftime('%d %B %Y')}", ln=True, align="C")
    pdf.ln(5)
    
    pdf.set_draw_color(226, 232, 240)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)
    
    # Metadata Block / Intro
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(0, 6, "1. DOCUMENT SUMMARY", ln=True)
    pdf.ln(2)
    
    # Box layout for metadata
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.set_text_color(15, 23, 42)
    
    # Table layout
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(90, 7, "Field Description", border=1, fill=True)
    pdf.cell(90, 7, "Value", border=1, ln=True, fill=True)
    
    pdf.set_font("Helvetica", "", 9)
    for key, value in payload.items():
        if value is None or value == "":
            continue
        label = key.replace("_", " ").replace("-", " ").title()
        val_str = str(value)
        
        pdf.cell(90, 6, label, border=1)
        pdf.cell(90, 6, val_str, border=1, ln=True)
        
    # Footer Section
    pdf.ln(12)
    pdf.set_draw_color(226, 232, 240)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 4, "This document was generated electronically by Instadeed.", ln=True, align="C")
    pdf.cell(0, 4, "Digitally signed via Leegality e-Sign Platform.", ln=True, align="C")
    
    return bytes(pdf.output(dest="S"))


def generate_document_pdf(form_data: dict, doc_type: str = "RENT") -> bytes:
    payload = form_data.get("payload") or form_data
    if not isinstance(payload, dict):
        payload = {}
        
    actual_type = form_data.get("type") or doc_type
    
    if actual_type in ("RENT", "REG_RENT"):
        return generate_rent_agreement_pdf(payload, actual_type)
    elif actual_type == "ATS":
        return generate_ats_pdf(payload, actual_type)
    else:
        return generate_generic_document_pdf(payload, actual_type)


# === Leegality e-Sign Endpoints ===

class LeegalitySignRequest(BaseModel):
    order_id: str
    signee_name: str
    signee_email: str
    signee_phone: str

@app.post("/api/sign/leegality/send")
async def leegality_send(request: Request, body: LeegalitySignRequest, user: dict = Depends(get_current_user)):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (body.order_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Order not found")
        order = dict(row)
        try:
            order["form_data"] = json.loads(order["form_data"]) if isinstance(order["form_data"], str) else order["form_data"]
        except:
            order["form_data"] = {}
        pdf_bytes = generate_document_pdf(order.get("form_data", {}), order.get("agreement_type", "RENT"))
        pdf_b64 = base64.b64encode(pdf_bytes).decode("ascii")
        profile_id = LEEGALITY_PROFILE_ID or "default"
        payload = {
            "profileId": profile_id,
            "document": {
                "content": pdf_b64,
                "fileName": f"{order.get('agreement_type', 'document')}_{body.order_id}.pdf"
            },
            "invitees": [
                {
                    "name": body.signee_name,
                    "email": body.signee_email,
                    "phone": body.signee_phone
                }
            ],
            "sendInvite": True,
            "expiryInDays": 7,
            "notifyVia": ["email", "sms"]
        }
        headers = {
            "X-Auth-Token": LEEGALITY_AUTH_TOKEN,
            "Content-Type": "application/json"
        }
        resp = http_requests.post(f"{LEEGALITY_BASE_URL}/v3.0/sign/request", json=payload, headers=headers, timeout=30)
        if resp.status_code != 200:
            logger.error(f"Leegality API error: {resp.status_code} {resp.text}")
            raise HTTPException(status_code=502, detail=f"Leegality API error: {resp.text}")
        result = resp.json()
        if result.get("status") != 1:
            msgs = result.get("messages", [])
            err_msg = msgs[0].get("message", "Unknown error") if msgs else "Unknown error"
            logger.error(f"Leegality request failed: {err_msg}")
            raise HTTPException(status_code=502, detail=f"Leegality signing failed: {err_msg}")
        data = result.get("data", {})
        leegality_doc_id = data.get("documentId", "")
        sign_url = ""
        invitees = data.get("invitees", [])
        if invitees:
            sign_url = invitees[0].get("signUrl", "")
        now = datetime.datetime.now().isoformat()
        conn2 = sqlite3.connect(DATABASE_FILE)
        c2 = conn2.cursor()
        c2.execute("UPDATE orders SET leegality_doc_id = ?, leegality_sign_url = ?, updated_at = ? WHERE id = ?",
                   (leegality_doc_id, sign_url, now, body.order_id))
        conn2.commit()
        conn2.close()
        logger.info(f"Leegality signing request created for order {body.order_id} -> doc {leegality_doc_id}")
        return {
            "status": "success",
            "document_id": leegality_doc_id,
            "sign_url": sign_url,
            "message": "Document sent for e-signing successfully!"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Leegality send error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sign/leegality/status/{order_id}")
async def leegality_status(order_id: str, request: Request, user: dict = Depends(get_current_user)):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT leegality_doc_id, leegality_sign_url FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Order not found")
        leegality_doc_id, sign_url = row
        if not leegality_doc_id:
            return {"status": "not_sent", "message": "Document has not been sent for e-signing yet."}
        headers = {"X-Auth-Token": LEEGALITY_AUTH_TOKEN}
        resp = http_requests.get(f"{LEEGALITY_BASE_URL}/v3.2/sign/request?documentId={leegality_doc_id}", headers=headers, timeout=15)
        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail=f"Leegality status check failed: {resp.text}")
        result = resp.json()
        tx_data = result.get("data", {})
        requests_list = tx_data.get("requests", [])
        signed = any(r.get("signed") for r in requests_list)
        return {
            "status": "signed" if signed else "pending",
            "document_id": leegality_doc_id,
            "sign_url": sign_url,
            "leegality_data": tx_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/sign/leegality/webhook")
@limiter.limit("10/minute")
async def leegality_webhook(request: Request):
    try:
        body = await request.json()
        logger.info(f"Leegality webhook received: {json.dumps(body)[:500]}")
        event = body.get("event", "")
        document_id = body.get("documentId", "")
        if event in ("document.signed", "document.completed") and document_id:
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM orders WHERE leegality_doc_id = ?", (document_id,))
            row = cursor.fetchone()
            if row:
                order_id = row[0]
                now = datetime.datetime.now().isoformat()
                cursor.execute("UPDATE orders SET status = 'SIGNED', updated_at = ? WHERE id = ?", (now, order_id))
                conn.commit()
                logger.info(f"Order {order_id} marked as SIGNED via Leegality webhook")
            conn.close()
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Leegality webhook error: {e}")
        return {"status": "error", "message": str(e)}


# === ADMIN USER MANAGEMENT ===

class AdminUpdateUserRequest(BaseModel):
    role: Optional[str] = None
    is_active: Optional[int] = None

@app.get("/api/admin/users")
async def admin_get_users(request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    search = request.query_params.get("search", "").strip()
    sort_by = request.query_params.get("sort_by", "created_at")
    sort_order = request.query_params.get("sort_order", "desc")
    page = int(request.query_params.get("page", "1"))
    per_page = int(request.query_params.get("per_page", "50"))
    allowed_sort = {"created_at", "name", "email", "last_login", "role"}
    if sort_by not in allowed_sort:
        sort_by = "created_at"
    direction = "DESC" if sort_order == "desc" else "ASC"
    offset = max(0, (page - 1) * per_page)
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    if search:
        cursor.execute(f"SELECT id, name, email, role, is_active, created_at, last_login FROM users WHERE name LIKE ? OR email LIKE ? ORDER BY {sort_by} {direction} LIMIT ? OFFSET ?", (f"%{search}%", f"%{search}%", per_page, offset))
    else:
        cursor.execute(f"SELECT id, name, email, role, is_active, created_at, last_login FROM users ORDER BY {sort_by} {direction} LIMIT ? OFFSET ?", (per_page, offset))
    rows = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    conn.close()
    users_list = []
    for r in rows:
        users_list.append({"id": r[0], "name": r[1], "email": r[2], "role": r[3], "is_active": bool(r[4]), "created_at": r[5], "last_login": r[6]})
    return {"users": users_list, "total": total, "page": page, "per_page": per_page, "pages": max(1, -(-total // per_page))}

@app.put("/api/admin/users/{user_id}")
async def admin_update_user(user_id: str, body: AdminUpdateUserRequest, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    updates = []
    params = []
    if body.role is not None:
        updates.append("role = ?")
        params.append(body.role)
    if body.is_active is not None:
        updates.append("is_active = ?")
        params.append(body.is_active)
    if updates:
        params.append(user_id)
        cursor.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = ?", tuple(params))
        conn.commit()
    conn.close()
    return {"status": "success"}

# === ADVANCED ADMIN ENDPOINTS ===

# --- User Detail & Tracking ---

@app.get("/api/admin/users/{user_id}")
async def admin_get_user_detail(user_id: str, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, phone, location, device_info, role, is_active, created_at, last_login FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    u = dict(row)
    # Login history
    cursor.execute("SELECT * FROM login_history WHERE user_id = ? ORDER BY id DESC LIMIT 50", (user_id,))
    u["login_history"] = [dict(r) for r in cursor.fetchall()]
    # Drafts
    phone = sanitize_phone(u.get("phone", ""))
    cursor.execute("SELECT id, doc_type, created_at, updated_at FROM saved_drafts WHERE phone = ? ORDER BY updated_at DESC", (phone,))
    u["drafts"] = [dict(r) for r in cursor.fetchall()]
    # Orders & LTV
    cursor.execute("SELECT COUNT(*) as order_count, COALESCE(SUM(amount), 0) as total_spent, MAX(created_at) as last_order FROM orders WHERE customer_email = ?", (u["email"],))
    stats = dict(cursor.fetchone())
    u["order_count"] = stats["order_count"]
    u["total_spent"] = stats["total_spent"]
    u["last_order"] = stats["last_order"]
    conn.close()
    return u

@app.get("/api/admin/users/{user_id}/login-history")
async def admin_get_login_history(user_id: str, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login_history WHERE user_id = ? ORDER BY id DESC LIMIT 100", (user_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {"history": rows}

@app.get("/api/admin/users/{user_id}/drafts")
async def admin_get_user_drafts(user_id: str, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT phone FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    phone = row[0] or ""
    phone = sanitize_phone(phone)
    cursor.execute("SELECT id, doc_type, form_data, created_at, updated_at FROM saved_drafts WHERE phone = ? ORDER BY updated_at DESC", (phone,))
    drafts = []
    for r in cursor.fetchall():
        drafts.append({"id": r[0], "doc_type": r[1], "form_data": json.loads(r[2]) if r[2] else {}, "created_at": r[3], "updated_at": r[4]})
    conn.close()
    return {"drafts": drafts}

# --- Order Assignment & Staff ---

class AssignStaffRequest(BaseModel):
    staff_id: str
    role: str = "attorney"

@app.put("/api/admin/orders/{order_id}/assign")
async def admin_assign_order(order_id: str, body: AssignStaffRequest, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    now = datetime.datetime.now().isoformat()
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM order_assignments WHERE order_id = ?", (order_id,))
    cursor.execute("INSERT INTO order_assignments (order_id, staff_id, role, assigned_at) VALUES (?, ?, ?, ?)", (order_id, body.staff_id, body.role, now))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.get("/api/admin/orders/{order_id}/assignments")
async def admin_get_assignments(order_id: str, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT oa.*, u.name as staff_name, u.email as staff_email
        FROM order_assignments oa LEFT JOIN users u ON oa.staff_id = u.id
        WHERE oa.order_id = ?
    """, (order_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {"assignments": rows}

# --- Order Notes ---

class AddNoteRequest(BaseModel):
    note: str

@app.get("/api/admin/orders/{order_id}/notes")
async def admin_get_notes(order_id: str, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT on.*, u.name as author_name FROM order_notes on LEFT JOIN users u ON on.author_id = u.id WHERE on.order_id = ? ORDER BY on.id DESC
    """, (order_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {"notes": rows}

@app.post("/api/admin/orders/{order_id}/notes")
async def admin_add_note(order_id: str, body: AddNoteRequest, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    now = datetime.datetime.now().isoformat()
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO order_notes (order_id, note, author_id, created_at) VALUES (?, ?, ?, ?)", (order_id, body.note, user["sub"], now))
    conn.commit()
    conn.close()
    return {"status": "success"}

# --- Document Version History ---

@app.get("/api/admin/orders/{order_id}/versions")
async def admin_get_versions(order_id: str, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT dv.*, u.name as author_name FROM document_versions dv LEFT JOIN users u ON dv.author_id = u.id WHERE dv.order_id = ? ORDER BY dv.version DESC
    """, (order_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {"versions": rows}

class SaveVersionRequest(BaseModel):
    form_data_snapshot: dict
    change_summary: str = ""

@app.post("/api/admin/orders/{order_id}/versions")
async def admin_save_version(order_id: str, body: SaveVersionRequest, request: Request, user: dict = Depends(get_current_user)):
    now = datetime.datetime.now().isoformat()
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(MAX(version), 0) + 1 FROM document_versions WHERE order_id = ?", (order_id,))
    next_ver = cursor.fetchone()[0]
    cursor.execute("INSERT INTO document_versions (order_id, version, form_data_snapshot, created_at, author_id, change_summary) VALUES (?, ?, ?, ?, ?, ?)",
                   (order_id, next_ver, json.dumps(body.form_data_snapshot), now, user["sub"], body.change_summary))
    conn.commit()
    conn.close()
    return {"status": "success", "version": next_ver}

# --- e-Stamp Management ---

class EstampUpdateRequest(BaseModel):
    estamp_number: Optional[str] = None
    estamp_cert_url: Optional[str] = None
    stamp_duty_paid: Optional[float] = None

@app.put("/api/admin/orders/{order_id}/estamp")
async def admin_update_estamp(order_id: str, body: EstampUpdateRequest, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    now = datetime.datetime.now().isoformat()
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            raise HTTPException(status_code=404, detail="Order not found")
        
        cursor.execute(
            "UPDATE orders SET estamp_number = ?, estamp_cert_url = ?, stamp_duty_paid = ?, updated_at = ? WHERE id = ?",
            (body.estamp_number, body.estamp_cert_url, body.stamp_duty_paid, now, order_id)
        )
        conn.commit()
        conn.close()
        return {"status": "success", "message": "e-Stamp details updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Refund Handling ---

class RefundRequest(BaseModel):
    amount: float
    reason: str

@app.post("/api/admin/orders/{order_id}/refund")
async def admin_process_refund(order_id: str, body: RefundRequest, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    now = datetime.datetime.now().isoformat()
    refund_id = f"REF-{uuid.uuid4().hex[:8].upper()}"
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, status FROM orders WHERE id = ?", (order_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")
    cursor.execute("INSERT INTO refunds (id, order_id, amount, reason, status, created_at, processed_at, processed_by) VALUES (?, ?, ?, ?, 'PROCESSED', ?, ?, ?)",
                   (refund_id, order_id, body.amount, body.reason, now, now, user["sub"]))
    cursor.execute("UPDATE orders SET status = 'REFUNDED', updated_at = ? WHERE id = ?", (now, order_id))
    conn.commit()
    conn.close()
    return {"status": "success", "refund_id": refund_id}

@app.get("/api/admin/refunds")
async def admin_list_refunds(request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM refunds ORDER BY created_at DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {"refunds": rows}

# --- Staff Roles & Permissions ---

class StaffCreateRequest(BaseModel):
    name: str
    email: str
    password: str = "staff123"
    role: str = "support"

@app.get("/api/admin/staff")
async def admin_list_staff(request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, role, is_active, created_at, last_login FROM users WHERE role IN ('admin', 'attorney', 'support', 'finance') ORDER BY created_at")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {"staff": rows}

@app.post("/api/admin/staff")
async def admin_create_staff(body: StaffCreateRequest, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    now = datetime.datetime.now().isoformat()
    uid = str(uuid.uuid4())
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (body.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=409, detail="Email already exists")
    allowed_roles = {"attorney", "support", "finance", "admin"}
    role = body.role if body.role in allowed_roles else "support"
    cursor.execute(
        "INSERT INTO users (id, name, email, password_hash, role, is_active, created_at) VALUES (?, ?, ?, ?, ?, 1, ?)",
        (uid, body.name, body.email, hash_password(body.password), role, now)
    )
    conn.commit()
    conn.close()
    return {"status": "success", "id": uid}

@app.put("/api/admin/staff/{staff_id}")
async def admin_update_staff(staff_id: str, body: AdminUpdateUserRequest, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    updates = []
    params = []
    if body.role is not None:
        updates.append("role = ?")
        params.append(body.role)
    if body.is_active is not None:
        updates.append("is_active = ?")
        params.append(body.is_active)
    if updates:
        params.append(staff_id)
        cursor.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = ?", tuple(params))
        conn.commit()
    conn.close()
    return {"status": "success"}

# --- Coupon Management ---

class CouponCreateRequest(BaseModel):
    code: str
    type: str = "percentage"
    value: float
    max_uses: int = 0
    min_amount: float = 0
    expires_at: str = ""

@app.post("/api/admin/coupons")
async def admin_create_coupon(body: CouponCreateRequest, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    now = datetime.datetime.now().isoformat()
    cid = str(uuid.uuid4())
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM coupons WHERE code = ?", (body.code.upper(),))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=409, detail="Coupon code already exists")
    cursor.execute("INSERT INTO coupons (id, code, type, value, max_uses, min_amount, expires_at, is_active, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)",
                   (cid, body.code.upper(), body.type, body.value, body.max_uses, body.min_amount, body.expires_at, now))
    conn.commit()
    conn.close()
    return {"status": "success", "id": cid}

@app.get("/api/admin/coupons")
async def admin_list_coupons(request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coupons ORDER BY created_at DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {"coupons": rows}

@app.put("/api/admin/coupons/{coupon_id}")
async def admin_update_coupon(coupon_id: str, body: CouponCreateRequest, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    now = datetime.datetime.now().isoformat()
    cursor.execute("UPDATE coupons SET type=?, value=?, max_uses=?, min_amount=?, expires_at=?, is_active=1 WHERE id=?",
                   (body.type, body.value, body.max_uses, body.min_amount, body.expires_at, coupon_id))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.delete("/api/admin/coupons/{coupon_id}")
async def admin_delete_coupon(coupon_id: str, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM coupons WHERE id = ?", (coupon_id,))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.post("/api/validate-coupon")
async def validate_coupon(body: dict = Body(...)):
    code = body.get("code", "").upper()
    amount = body.get("amount", 0)
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, type, value, max_uses, current_uses, min_amount, expires_at, is_active FROM coupons WHERE code = ?", (code,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return {"valid": False, "error": "Coupon not found"}
    cid, ctype, value, max_uses, current_uses, min_amount, expires_at, is_active = row
    if not is_active:
        return {"valid": False, "error": "Coupon is inactive"}
    if max_uses > 0 and current_uses >= max_uses:
        return {"valid": False, "error": "Coupon usage limit reached"}
    if expires_at and expires_at < datetime.datetime.now().isoformat()[:10]:
        return {"valid": False, "error": "Coupon has expired"}
    if amount < min_amount:
        return {"valid": False, "error": f"Minimum order amount of ₹{int(min_amount)} required"}
    if ctype == "percentage":
        discount = amount * value / 100
        if discount > 5000:
            discount = 5000
    else:
        discount = value
    return {"valid": True, "discount": discount, "type": ctype, "value": value, "code": code}

# --- Notifications Panel ---

class NotificationCreateRequest(BaseModel):
    type: str = "info"
    recipient: str
    title: str
    message: str
    reference_type: str = ""
    reference_id: str = ""

@app.get("/api/admin/notifications")
async def admin_list_notifications(request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notifications ORDER BY id DESC LIMIT 100")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {"notifications": rows}

@app.post("/api/admin/notifications")
async def admin_create_notification(body: NotificationCreateRequest, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    now = datetime.datetime.now().isoformat()
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notifications (type, recipient, title, message, reference_type, reference_id, status, created_at, sent_at) VALUES (?, ?, ?, ?, ?, ?, 'sent', ?, ?)",
                   (body.type, body.recipient, body.title, body.message, body.reference_type, body.reference_id, now, now))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.get("/api/admin/notifications/stats")
async def admin_notification_stats(request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM notifications")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT type, COUNT(*) FROM notifications GROUP BY type")
    type_breakdown = dict(cursor.fetchall())
    cursor.execute("SELECT COUNT(*) FROM notifications WHERE created_at LIKE ?", (f"{datetime.date.today().isoformat()}%",))
    today = cursor.fetchone()[0]
    conn.close()
    return {"total": total, "today": today, "type_breakdown": type_breakdown}

# --- Invoice & GST Reports ---

@app.get("/api/admin/invoices")
async def admin_list_invoices(request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.*, o.customer_name, o.customer_email, o.agreement_type, o.created_at as order_date
        FROM invoices i LEFT JOIN orders o ON i.order_id = o.id ORDER BY i.created_at DESC
    """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {"invoices": rows}

@app.post("/api/admin/invoices/generate/{order_id}")
async def admin_generate_invoice(order_id: str, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, customer_name, amount FROM orders WHERE id = ?", (order_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")
    order_id, customer_name, amount = row
    now = datetime.datetime.now().isoformat()
    inv_id = str(uuid.uuid4())
    inv_num = f"INV-{datetime.date.today().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"
    gst = round(amount * 0.18, 2)
    total = amount + gst
    cursor.execute("INSERT INTO invoices (id, order_id, invoice_number, amount, gst_amount, total, status, created_at) VALUES (?, ?, ?, ?, ?, ?, 'PENDING', ?)",
                   (inv_id, order_id, inv_num, amount, gst, total, now))
    conn.commit()
    conn.close()
    return {"status": "success", "invoice_id": inv_id, "invoice_number": inv_num}

@app.get("/api/admin/invoices/gst-report")
async def admin_gst_report(request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(SUM(amount), 0) as total_sales, COALESCE(SUM(gst_amount), 0) as total_gst, COUNT(*) as invoice_count FROM invoices")
    summary = dict(zip(["total_sales", "total_gst", "invoice_count"], cursor.fetchone()))
    cursor.execute("SELECT DATE(created_at) as day, SUM(gst_amount) as gst FROM invoices GROUP BY DATE(created_at) ORDER BY day DESC LIMIT 30")
    daily_gst = [{"date": r[0], "gst": r[1]} for r in cursor.fetchall()]
    conn.close()
    return {"summary": summary, "daily_gst": daily_gst}

@app.put("/api/admin/invoices/{invoice_id}/pay")
async def admin_mark_invoice_paid(invoice_id: str, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    now = datetime.datetime.now().isoformat()
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE invoices SET status = 'PAID', paid_at = ? WHERE id = ?", (now, invoice_id))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.get("/api/admin/invoices/{invoice_id}/download")
async def admin_download_invoice(invoice_id: str, request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.*, o.customer_name, o.customer_phone, o.customer_email, o.agreement_type 
        FROM invoices i LEFT JOIN orders o ON i.order_id = o.id 
        WHERE i.id = ?
    """, (invoice_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    invoice_data = dict(row)
    try:
        pdf_bytes = generate_invoice_pdf_bytes(invoice_data)
    except Exception as e:
        logger.error(f"Error generating invoice PDF: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate invoice PDF: {e}")
        
    filename = f"Invoice_{invoice_data.get('invoice_number', invoice_id)}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


# --- Enhanced Analytics ---

@app.get("/api/analytics/funnel")
async def get_analytics_funnel(request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    stages = ["PENDING_PAYMENT", "PAID", "DRAFTED", "COMPLETED", "SIGNED"]
    funnel = {}
    total = 0
    cursor.execute("SELECT COUNT(*) FROM orders")
    total = cursor.fetchone()[0]
    funnel["total_started"] = total
    for stage in stages:
        cursor.execute("SELECT COUNT(*) FROM orders WHERE status = ?", (stage,))
        funnel[stage.lower()] = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM orders WHERE created_at LIKE ?", (f"{datetime.date.today().isoformat()}%",))
    funnel["today"] = cursor.fetchone()[0]
    conn.close()
    return funnel

@app.get("/api/analytics/abandoned-drafts")
async def get_abandoned_drafts(request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM saved_drafts")
    total_drafts = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'PENDING_PAYMENT'")
    unpaid = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]
    abandoned_rate = round((total_drafts / (total_orders + total_drafts)) * 100, 1) if (total_orders + total_drafts) > 0 else 0
    cursor.execute("SELECT COUNT(*) FROM saved_drafts WHERE updated_at LIKE ?", (f"{datetime.date.today().isoformat()}%",))
    today_drafts = cursor.fetchone()[0]
    conn.close()
    return {"total_drafts": total_drafts, "unpaid_orders": unpaid, "total_orders": total_orders, "abandoned_rate": abandoned_rate, "today_drafts": today_drafts}

@app.get("/api/analytics/heatmap")
async def get_analytics_heatmap(request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT location, COUNT(*) as cnt FROM users WHERE location != '' AND location IS NOT NULL GROUP BY location ORDER BY cnt DESC")
    locations = [{"location": r[0], "count": r[1]} for r in cursor.fetchall()]
    cursor.execute("SELECT COUNT(*) FROM users WHERE (location IS NULL OR location = '')")
    unknown = cursor.fetchone()[0]
    conn.close()
    return {"locations": locations, "unknown": unknown}

@app.get("/api/analytics/dropoff")
async def get_analytics_dropoff(request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT event, COUNT(*) as cnt FROM page_events WHERE event IN ('form_start', 'form_step', 'form_complete', 'checkout_start', 'payment_complete') GROUP BY event ORDER BY cnt DESC")
    events = dict(cursor.fetchall())
    steps = ["form_start", "form_step", "form_complete", "checkout_start", "payment_complete"]
    dropoff = []
    prev = events.get("form_start", 0)
    for s in steps:
        curr = events.get(s, 0)
        loss = prev - curr if prev > 0 else 0
        loss_pct = round((loss / prev) * 100, 1) if prev > 0 else 0
        dropoff.append({"step": s, "count": curr, "lost": loss, "loss_percentage": loss_pct})
        prev = curr
    conn.close()
    return {"dropoff": dropoff, "raw_events": events}

# --- Audit Trail ---

@app.get("/api/admin/audit")
async def admin_audit_trail(request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    limit = int(request.query_params.get("limit", "200"))
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT al.*, u.name as user_name FROM activity_log al LEFT JOIN users u ON al.user_id = u.id ORDER BY al.id DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    cursor.execute("SELECT COUNT(*) FROM activity_log")
    total = cursor.fetchone()["COUNT(*)"]
    conn.close()
    return {"entries": rows, "total": total}

# === DRAFT API (Save/Resume via OTP) ===
DRAFT_OTP_STORE = {}
DRAFT_DB_LOCK = threading.Lock()

@app.post("/api/drafts/send-otp")
async def drafts_send_otp(body: dict = Body(...)):
    phone = body.get("phone", "")
    phone = sanitize_phone(phone)
    if len(phone) != 10:
        return {"success": False, "error": "Invalid phone number"}
    otp = str(random.randint(100000, 999999))
    DRAFT_OTP_STORE[phone] = otp
    logger.info(f"Draft OTP sent to {phone} -> {otp}")
    return {"success": True, "message": "OTP sent successfully"}

@app.post("/api/drafts/verify-otp")
async def drafts_verify_otp(body: dict = Body(...)):
    phone = body.get("phone", "")
    phone = sanitize_phone(phone)
    otp = body.get("otp", "")
    ENABLE_MASTER_OTP = os.environ.get("ENABLE_MASTER_OTP", "0") == "1"
    if (ENABLE_MASTER_OTP and otp == "123456") or DRAFT_OTP_STORE.get(phone) == otp:
        DRAFT_OTP_STORE.pop(phone, None)
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, doc_type, form_data, created_at, updated_at FROM saved_drafts WHERE phone = ? ORDER BY updated_at DESC", (phone,))
        rows = cursor.fetchall()
        conn.close()
        drafts = []
        for r in rows:
            drafts.append({"id": r[0], "doc_type": r[1], "form_data": json.loads(r[2]) if r[2] else {}, "created_at": r[3], "updated_at": r[4]})
        return {"success": True, "drafts": drafts}
    return {"success": False, "error": "Invalid OTP"}

@app.post("/api/drafts")
async def save_draft(body: dict = Body(...)):
    doc_type = body.get("doc_type", "")
    form_data = body.get("form_data", {})
    phone = body.get("phone", "")
    phone = sanitize_phone(phone)
    email = body.get("email", "")
    if not doc_type:
        return {"success": False, "error": "doc_type required"}
    now = datetime.datetime.now().isoformat()
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        existing = None
        if email:
            cursor.execute("SELECT id FROM saved_drafts WHERE doc_type = ? AND email = ?", (doc_type, email))
            existing = cursor.fetchone()
        elif phone:
            cursor.execute("SELECT id FROM saved_drafts WHERE doc_type = ? AND phone = ?", (doc_type, phone))
            existing = cursor.fetchone()
            
        if existing:
            cursor.execute("UPDATE saved_drafts SET form_data = ?, updated_at = ?, phone = ?, email = ? WHERE id = ?", (json.dumps(form_data), now, phone, email, existing[0]))
        else:
            cursor.execute("INSERT INTO saved_drafts (doc_type, form_data, phone, email, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)", (doc_type, json.dumps(form_data), phone, email, now, now))
        conn.commit()
        conn.close()
        return {"success": True}
    except Exception as e:
        logger.error(f"Draft save error: {e}")
        return {"success": False, "error": str(e)}

import uuid

@app.post("/api/drafts/share")
async def create_share_link(body: dict = Body(...)):
    doc_type = body.get("doc_type", "")
    form_data = body.get("form_data", {})
    if not doc_type:
        return {"success": False, "error": "doc_type required"}
    token = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
    now = datetime.datetime.now()
    expires = now + datetime.timedelta(days=7)
    
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO shared_drafts (id, doc_type, form_data, created_at, expires_at) VALUES (?, ?, ?, ?, ?)",
            (token, doc_type, json.dumps(form_data), now.isoformat(), expires.isoformat())
        )
        conn.commit()
        conn.close()
        return {"success": True, "token": token}
    except Exception as e:
        logger.error(f"Share link creation failed: {e}")
        return {"success": False, "error": str(e)}

@app.get("/api/drafts/share/{token}")
async def get_shared_draft(token: str):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT doc_type, form_data, expires_at FROM shared_drafts WHERE id = ?", (token,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="Shared draft not found")
            
        doc_type, form_data_str, expires_at_str = row
        expires_at = datetime.datetime.fromisoformat(expires_at_str)
        if datetime.datetime.now() > expires_at:
            raise HTTPException(status_code=410, detail="Shared review link has expired")
            
        return {
            "success": True,
            "doc_type": doc_type,
            "form_data": json.loads(form_data_str) if form_data_str else {}
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching shared draft: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/templates")
async def get_analytics_templates(request: Request, user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT agreement_type, COUNT(*) FROM orders GROUP BY agreement_type")
        orders_data = dict(cursor.fetchall())
        
        cursor.execute("SELECT doc_type, COUNT(*) FROM saved_drafts GROUP BY doc_type")
        drafts_data = dict(cursor.fetchall())
        
        all_keys = set(list(orders_data.keys()) + list(drafts_data.keys()))
        combined = []
        for k in all_keys:
            if not k:
                continue
            combined.append({
                "template": k,
                "orders": orders_data.get(k, 0),
                "drafts": drafts_data.get(k, 0),
                "total": orders_data.get(k, 0) + drafts_data.get(k, 0)
            })
        
        combined.sort(key=lambda x: x["total"], reverse=True)
        conn.close()
        return {"templates": combined}
    except Exception as e:
        logger.error(f"Failed to fetch template analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{full_path:path}", response_class=HTMLResponse)
async def serve_spa(full_path: str):
    if full_path.startswith("api/") or full_path.startswith("analytics") or full_path.startswith("create-order") or full_path.startswith("verify-payment"):
        raise HTTPException(status_code=404, detail="Not Found")
    html_path = os.path.join(STATIC_DIR, "Madhav_Drafting_Hub.html")
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail="Frontend not built.")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Instadeed Backend v2.0.0 on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
