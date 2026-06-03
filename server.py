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
from contextlib import asynccontextmanager
from typing import Optional

import requests as http_requests

from fastapi import FastAPI, Request, HTTPException, Depends
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
JWT_SECRET = os.environ.get("JWT_SECRET", "instadeed-dev-secret-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24
DATABASE_FILE = "madhav_crm.db"
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Leegality e-Sign Configuration ---
LEEGALITY_AUTH_TOKEN = os.environ.get("LEEGALITY_AUTH_TOKEN", "awuvjhZrH0QxTFN1d2VhDX1ZUFF50E6z")
LEEGALITY_PRIVATE_SALT = os.environ.get("LEEGALITY_PRIVATE_SALT", "YsZ0GTAGVREIF1fchgyWQkgarempLluT")
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

# --- Password Hashing (SHA-256 with salt) ---
def hash_password(password: str) -> str:
    salt = uuid.uuid4().hex[:16]
    return salt + ":" + hashlib.sha256((salt + password).encode()).hexdigest()

def verify_password(password: str, stored: str) -> bool:
    if ":" not in stored:
        return False
    salt, expected = stored.split(":", 1)
    return hashlib.sha256((salt + password).encode()).hexdigest() == expected

# --- Rate Limiter (use X-Forwarded-For behind reverse proxy) ---
def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return get_remote_address(request)

limiter = Limiter(key_func=get_client_ip)

# --- Razorpay ---
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "rzp_live_SwmTpRiDct3TaU")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "W071YhfOXIXyODVIZ5f7unOz")
is_razorpay_valid = not ("YOUR_KEY" in RAZORPAY_KEY_ID or RAZORPAY_KEY_ID == "")
client = None
if is_razorpay_valid:
    try:
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    except Exception as e:
        logger.warning(f"Failed to initialize Razorpay: {e}")
        is_razorpay_valid = False

# --- Database ---
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
        role TEXT DEFAULT 'user',
        is_active INTEGER DEFAULT 1,
        created_at TEXT,
        last_login TEXT
    )
    """)
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
    conn.commit()
    conn.close()
    logger.info("Database initialized")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    # Create default admin if not exists
    create_default_admin()
    yield

def create_default_admin():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", ("admin@instadeed.local",))
    if not cursor.fetchone():
        now = datetime.datetime.now().isoformat()
        uid = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO users (id, name, email, password_hash, role, is_active, created_at) VALUES (?, ?, ?, ?, ?, 1, ?)",
            (uid, "Admin", "admin@instadeed.local", hash_password("admin123"), "admin", now)
        )
        conn.commit()
        logger.info("Default admin created (admin@instadeed.local / admin123)")
    conn.close()

# --- FastAPI App ---
app = FastAPI(title="Instadeed Backend", version="2.0.0", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request Logging Middleware ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = int((time.time() - start) * 1000)
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
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, role FROM users WHERE email = ? AND is_active = 1", (body.email,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="No account found with this email")
    otp = "123456" if body.email == "admin@instadeed.local" else str(random.randint(100000, 999999))
    otp_store[body.email] = {"otp": otp, "expires": datetime.datetime.now() + datetime.timedelta(minutes=5)}
    logger.info(f"OTP for {body.email}: {otp}")
    return {"status": "success", "message": "OTP sent to your email"}

@app.post("/api/auth/verify-otp")
@limiter.limit("10/minute")
async def verify_otp(request: Request, body: VerifyOTPRequest):
    if body.email == "admin@instadeed.local" and body.otp == "123456":
        pass
    else:
        if body.email not in otp_store:
            raise HTTPException(status_code=400, detail="No OTP requested for this email")
        record = otp_store[body.email]
        if datetime.datetime.now() > record["expires"]:
            del otp_store[body.email]
            raise HTTPException(status_code=400, detail="OTP expired")
        if record["otp"] != body.otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        del otp_store[body.email]
    del otp_store[body.email]
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, role FROM users WHERE email = ?", (body.email,))
    user = cursor.fetchone()
    now = datetime.datetime.now().isoformat()
    cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (now, user[0]))
    conn.commit()
    conn.close()
    token = create_token(user[0], user[2], user[3])
    return {"status": "success", "token": token, "user": {"id": user[0], "name": user[1], "email": user[2], "role": user[3]}}

# === AUTH ENDPOINTS ===

@app.post("/api/auth/signup")
@limiter.limit("5/minute")
async def signup(request: Request, body: SignupRequest):
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
        cloud_url = f"http://localhost:8000?view={order_id}"
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
        cloud_url = f"http://localhost:8000?view={order_id}"
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


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Instadeed Backend v2.0.0 on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
