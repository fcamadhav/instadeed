import sqlite3
import json
import uuid
import datetime
import time
import logging
import os
import hashlib
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
import razorpay
import jwt
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# --- Configuration ---
JWT_SECRET = os.environ.get("JWT_SECRET", "instadeed-dev-secret-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24
DATABASE_FILE = "madhav_crm.db"
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))

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

# --- Rate Limiter ---
limiter = Limiter(key_func=get_remote_address)

# --- Razorpay ---
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "rzp_test_YOUR_KEY_HERE")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "YOUR_SECRET_HERE")
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
@limiter.limit("20/minute")
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
        conn.close()
        return {
            "total_orders": total_orders,
            "today_orders": today_orders,
            "total_revenue": total_revenue,
            "status_breakdown": status_breakdown,
            "agreement_breakdown": agreement_breakdown,
            "source_breakdown": source_breakdown,
            "agreement_details": agreement_details
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

# === Health Check ===

@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "2.0.0", "timestamp": datetime.datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Instadeed Backend v2.0.0 on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
