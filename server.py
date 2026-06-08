import sqlite3
import json
import uuid
import datetime
import time
import logging
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
from fastapi.responses import FileResponse, HTMLResponse, Response
from pydantic import BaseModel
import razorpay
import jwt
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fpdf import FPDF

# --- Configuration ---
JWT_SECRET = os.environ.get("JWT_SECRET")
if not JWT_SECRET:
    JWT_SECRET = "dev-secret-change-in-production"
    logger.warning("JWT_SECRET not set — using insecure fallback. Set JWT_SECRET env var in production.")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24
DATABASE_FILE = "madhav_crm.db"
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Leegality e-Sign Configuration ---
LEEGALITY_AUTH_TOKEN = os.environ.get("LEEGALITY_AUTH_TOKEN")
LEEGALITY_PRIVATE_SALT = os.environ.get("LEEGALITY_PRIVATE_SALT")
LEEGALITY_BASE_URL = os.environ.get("LEEGALITY_BASE_URL", "https://sandbox.leegality.com/api")
LEEGALITY_PROFILE_ID = os.environ.get("LEEGALITY_PROFILE_ID", "")

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("instadeed")

# --- Password Hashing (bcrypt) ---
try:
    import bcrypt as _bcrypt
    def hash_password(password: str) -> str:
        return _bcrypt.hashpw(password.encode(), _bcrypt.gensalt()).decode()
    def verify_password(password: str, stored: str) -> bool:
        return _bcrypt.checkpw(password.encode(), stored.encode())
except ImportError:
    import hashlib
    logger.warning("bcrypt not installed; falling back to SHA-256. Install bcrypt for production.")
    def hash_password(password: str) -> str:
        salt = uuid.uuid4().hex[:16]
        return salt + ":" + hashlib.sha256((salt + password).encode()).hexdigest()
    def verify_password(password: str, stored: str) -> bool:
        if ":" not in stored:
            return False
        salt, expected = stored.split(":", 1)
        return hashlib.sha256((salt + password).encode()).hexdigest() == expected

# --- Input Validation ---
import re
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
        self.conn = sqlite3.connect(DATABASE_FILE)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        self.conn.close()
        return False

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
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
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN leegality_doc_id TEXT")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN leegality_sign_url TEXT")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN is_favorite INTEGER DEFAULT 0")
    except Exception:
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
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN location TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN device_info TEXT DEFAULT ''")
    except Exception:
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
    ]:
        try:
            cursor.execute(idx_sql)
        except Exception:
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

# --- Global Exception Handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        raise exc
    logger.error(f"Unhandled exception on {request.method} {request.url.path}: {exc}")
    raise HTTPException(status_code=500, detail="Internal server error")

# --- Request Logging Middleware ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = int((time.time() - start) * 1000)
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
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
    html_path = os.path.join(STATIC_DIR, "Madhav_Drafting_Hub.html")
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail="Frontend not built. Run build.py first.")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/out.js")
async def serve_js():
    js_path = os.path.join(STATIC_DIR, "out.js")
    if not os.path.exists(js_path):
        raise HTTPException(status_code=404, detail="JS bundle not found. Run build.py first.")
    return FileResponse(js_path, media_type="application/javascript")

@app.get("/{full_path:path}", response_class=HTMLResponse)
async def serve_spa(full_path: str):
    if full_path.startswith("api/") or full_path.startswith("analytics") or full_path.startswith("create-order") or full_path.startswith("verify-payment"):
        raise HTTPException(status_code=404, detail="Not Found")
    html_path = os.path.join(STATIC_DIR, "Madhav_Drafting_Hub.html")
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail="Frontend not built.")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# --- Auth Helpers ---
def create_token(user_id: str, email: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRY_HOURS),
        "iat": datetime.datetime.utcnow()
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
    if auth_header.startswith("Bearer "):
        try:
            return verify_token(auth_header[7:])
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
            logger.info(f"OTP for {body.email}: {otp} (email delivery not configured)")
    except Exception:
        logger.info(f"OTP for {body.email}: {otp} (email delivery not configured)")
    return {"status": "success", "message": "OTP sent to your email"}

@app.post("/api/auth/verify-otp")
@limiter.limit("10/minute")
async def verify_otp(request: Request, body: VerifyOTPRequest):
    if body.email not in otp_store:
        raise HTTPException(status_code=400, detail="No OTP requested for this email")
    record = otp_store[body.email]
    if datetime.datetime.now() > record["expires"]:
        del otp_store[body.email]
        raise HTTPException(status_code=400, detail="OTP expired")
    if record["otp"] != body.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    del otp_store[body.email]
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, role FROM users WHERE email = ?", (body.email,))
    user = cursor.fetchone()
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
    if not verify_password(body.password, password_hash):
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
        cursor.execute(
            "INSERT INTO orders (id, customer_name, customer_phone, customer_email, agreement_type, source, status, amount, form_data, created_at, updated_at, cloud_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (order_id, body.customer_name, body.customer_phone, body.customer_email, body.service_type, "ONLINE_B2C", "PENDING_PAYMENT", float(body.amount), json.dumps(body.form_data), now, now, cloud_url)
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
            cursor = conn.cursor()
            cursor.execute("UPDATE orders SET status = 'PAID', updated_at = ? WHERE id = ?", (now, body.razorpay_order_id))
            conn.commit()
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
            cursor = conn.cursor()
            cursor.execute("UPDATE orders SET status = 'PAID', updated_at = ? WHERE id = ?", (now, body.razorpay_order_id))
            conn.commit()
            conn.close()
            return {"status": "success", "message": "Payment verified successfully!"}
        except razorpay.errors.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid Payment Signature. Potential Fraud.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute("UPDATE orders SET status = 'PAID', updated_at = ? WHERE id = ?", (now, body.razorpay_order_id))
            conn.commit()
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
        cursor.execute(
            "INSERT INTO orders (id, customer_name, customer_phone, customer_email, agreement_type, source, status, amount, form_data, created_at, updated_at, cloud_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (order_id, body.customer_name, body.customer_phone, body.customer_email, body.agreement_type, "OFFLINE_WALKIN", body.status, body.amount, json.dumps(body.form_data), now, now, None)
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
async def update_order_status(order_id: str, body: StatusUpdateRequest, request: Request):
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
                        from datetime import datetime as dt_mod
                        sd = dt_mod.strptime(start_date_str, "%Y-%m-%d")
                        from dateutil.relativedelta import relativedelta
                        try:
                            from dateutil.relativedelta import relativedelta
                            nd = sd + relativedelta(months=11)
                            nd -= datetime.timedelta(days=1)
                            end_date_str = nd.strftime("%Y-%m-%d")
                        except:
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
async def customer_documents(phone: str = "", email: str = ""):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if phone:
            cursor.execute("SELECT id, agreement_type, status, amount, created_at, updated_at, cloud_url, leegality_sign_url, form_data FROM orders WHERE customer_phone = ? ORDER BY created_at DESC", (phone,))
        elif email:
            cursor.execute("SELECT id, agreement_type, status, amount, created_at, updated_at, cloud_url, leegality_sign_url, form_data FROM orders WHERE customer_email = ? ORDER BY created_at DESC", (email,))
        else:
            conn.close()
            return []
        rows = cursor.fetchall()
        conn.close()
        docs = []
        for r in rows:
            d = dict(r)
            try:
                d["form_data"] = json.loads(d["form_data"]) if isinstance(d["form_data"], str) else d["form_data"]
            except:
                d["form_data"] = {}
            d.pop("form_data", None)
            docs.append(d)
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customer/documents/{order_id}/download")
async def customer_download(order_id: str):
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
        pdf_bytes = generate_document_pdf(order.get("form_data", {}))
        filename = f"{order.get('agreement_type', 'document')}_{order_id[:8]}.pdf"
        return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={filename}"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === PDF Generation ===

def generate_document_pdf(form_data: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Courier", "B", 16)
    title = form_data.get("type", "Legal Document")
    pdf.cell(0, 10, str(title), ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Courier", "", 9)
    pdf.cell(0, 6, "Generated by Instadeed Legal Suite", ln=True, align="C")
    pdf.cell(0, 6, f"Date: {datetime.date.today().strftime('%d %B %Y')}", ln=True, align="C")
    pdf.ln(8)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)
    payload = form_data.get("payload") or form_data
    if isinstance(payload, dict):
        pdf.set_font("Courier", "B", 12)
        pdf.cell(0, 8, "Document Details", ln=True)
        pdf.ln(3)
        pdf.set_font("Courier", "", 10)
        for key, value in payload.items():
            if value is None or value == "":
                continue
            label = key.replace("_", " ").replace("-", " ").title()
            val_str = str(value)
            pdf.set_font("Courier", "B", 9)
            pdf.cell(60, 5, label + ":", ln=False)
            pdf.set_font("Courier", "", 9)
            pdf.multi_cell(0, 5, val_str)
            pdf.ln(1)
    pdf.ln(10)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    pdf.set_font("Courier", "", 7)
    pdf.cell(0, 4, "This document was generated electronically by Instadeed.", ln=True, align="C")
    pdf.cell(0, 4, "Digitally signed via Leegality e-Sign Platform.", ln=True, align="C")
    return bytes(pdf.output(dest="S"))


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
        pdf_bytes = generate_document_pdf(order.get("form_data", {}))
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
async def admin_update_user(user_id: str, body: AdminUpdateUserRequest, user: dict = Depends(get_current_user)):
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
    cursor.execute("SELECT id, doc_type, created_at, updated_at FROM saved_drafts WHERE phone = ? ORDER BY updated_at DESC", (u.get("phone", ""),))
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
    if len(phone) != 10:
        return {"success": False, "error": "Invalid phone number"}
    otp = os.environ.get("DEMO_OTP", str(random.randint(100000, 999999)))
    DRAFT_OTP_STORE[phone] = otp
    logger.info(f"Draft OTP for {phone}: {otp}")
    return {"success": True}

@app.post("/api/drafts/verify-otp")
async def drafts_verify_otp(body: dict = Body(...)):
    phone = body.get("phone", "")
    otp = body.get("otp", "")
    if DRAFT_OTP_STORE.get(phone) == otp:
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
    if not doc_type:
        return {"success": False, "error": "doc_type required"}
    now = datetime.datetime.now().isoformat()
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS saved_drafts (id INTEGER PRIMARY KEY AUTOINCREMENT, doc_type TEXT, form_data TEXT, phone TEXT, created_at TEXT, updated_at TEXT)")
        if phone:
            cursor.execute("SELECT id FROM saved_drafts WHERE doc_type = ? AND phone = ?", (doc_type, phone))
            existing = cursor.fetchone()
            if existing:
                cursor.execute("UPDATE saved_drafts SET form_data = ?, updated_at = ? WHERE id = ?", (json.dumps(form_data), now, existing[0]))
            else:
                cursor.execute("INSERT INTO saved_drafts (doc_type, form_data, phone, created_at, updated_at) VALUES (?, ?, ?, ?, ?)", (doc_type, json.dumps(form_data), phone, now, now))
        else:
            cursor.execute("INSERT INTO saved_drafts (doc_type, form_data, phone, created_at, updated_at) VALUES (?, ?, ?, ?, ?)", (doc_type, json.dumps(form_data), phone, now, now))
        conn.commit()
        conn.close()
        return {"success": True}
    except Exception as e:
        logger.error(f"Draft save error: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Instadeed Backend v2.0.0 on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
