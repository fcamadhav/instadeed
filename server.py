import sqlite3
import json
import uuid
import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import razorpay

app = FastAPI()

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite database path
DATABASE_FILE = "madhav_crm.db"

# Initialize database
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
    # Safe migration for existing DBs
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN cloud_url TEXT")
    except Exception:
        pass
    conn.commit()
    conn.close()

# Run database setup on startup
init_db()

# TODO: Replace with your actual Razorpay keys
RAZORPAY_KEY_ID = "rzp_test_YOUR_KEY_HERE"
RAZORPAY_KEY_SECRET = "YOUR_SECRET_HERE"

# Initialize Razorpay Client (with safe fallback for dummy keys)
is_razorpay_valid = not ("YOUR_KEY" in RAZORPAY_KEY_ID or RAZORPAY_KEY_ID == "")
client = None
if is_razorpay_valid:
    try:
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    except Exception as e:
        print(f"Failed to initialize Razorpay: {e}")
        is_razorpay_valid = False

class OrderRequest(BaseModel):
    amount: int  # Amount in INR (e.g. 499)
    service_type: str  # e.g., "rent_agreement"
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

@app.post("/create-order")
async def create_order(request: OrderRequest):
    # Razorpay amount is in paise (1 INR = 100 paise)
    amount_in_paise = request.amount * 100
    order_id = ""
    
    # Try to create order on Razorpay
    if is_razorpay_valid and client:
        try:
            data = {
                "amount": amount_in_paise,
                "currency": "INR",
                "receipt": f"receipt_{uuid.uuid4().hex[:8]}",
                "notes": {
                    "service": request.service_type
                }
            }
            order = client.order.create(data=data)
            order_id = order["id"]
        except Exception as e:
            # Rollback to dummy order if Razorpay fails
            print(f"Razorpay order creation failed: {e}")
            order_id = f"MOCK_ORD_{uuid.uuid4().hex[:8].upper()}"
    else:
        # Dummy order ID for testing when Razorpay is not configured
        order_id = f"MOCK_ORD_{uuid.uuid4().hex[:8].upper()}"
        
    now = datetime.datetime.now().isoformat()
    
    # Save the order with status PENDING_PAYMENT
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        # Online B2C is synced to cloud automatically
        cloud_url = f"http://localhost:8765/Madhav_Drafting_Hub.html?view={order_id}"
        cursor.execute(
            "INSERT INTO orders (id, customer_name, customer_phone, customer_email, agreement_type, source, status, amount, form_data, created_at, updated_at, cloud_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (order_id, request.customer_name, request.customer_phone, request.customer_email, request.service_type, "ONLINE_B2C", "PENDING_PAYMENT", float(request.amount), json.dumps(request.form_data), now, now, cloud_url)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    return {"order_id": order_id, "amount": amount_in_paise, "currency": "INR"}

@app.post("/verify-payment")
async def verify_payment(request: VerifyRequest):
    now = datetime.datetime.now().isoformat()
    
    # Handle mock orders
    if request.razorpay_order_id.startswith("MOCK_ORD_"):
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE orders SET status = 'PAID', updated_at = ? WHERE id = ?",
                (now, request.razorpay_order_id)
            )
            conn.commit()
            conn.close()
            return {"status": "success", "message": "Mock payment verified successfully!"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            
    # Real signature verification
    if is_razorpay_valid and client:
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': request.razorpay_order_id,
                'razorpay_payment_id': request.razorpay_payment_id,
                'razorpay_signature': request.razorpay_signature
            })
            
            # Update status in db
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE orders SET status = 'PAID', updated_at = ? WHERE id = ?",
                (now, request.razorpay_order_id)
            )
            conn.commit()
            conn.close()
            return {"status": "success", "message": "Payment verified successfully!"}
            
        except razorpay.errors.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid Payment Signature. Potential Fraud.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        # Fallback if Razorpay is not configured but a non-mock order ID came in (verify blindly for local testing)
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE orders SET status = 'PAID', updated_at = ? WHERE id = ?",
                (now, request.razorpay_order_id)
            )
            conn.commit()
            conn.close()
            return {"status": "success", "message": "Blind payment verification (testing mode)!"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-offline-order")
async def create_offline_order(request: OfflineOrderRequest):
    order_id = f"MDH-{uuid.uuid4().hex[:8].upper()}"
    now = datetime.datetime.now().isoformat()
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        # Offline walk-in orders start with no cloud URL until uploaded
        cursor.execute(
            "INSERT INTO orders (id, customer_name, customer_phone, customer_email, agreement_type, source, status, amount, form_data, created_at, updated_at, cloud_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (order_id, request.customer_name, request.customer_phone, request.customer_email, request.agreement_type, "OFFLINE_WALKIN", request.status, request.amount, json.dumps(request.form_data), now, now, None)
        )
        conn.commit()
        conn.close()
        return {"status": "success", "order_id": order_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/orders")
async def list_orders(status: str = None, agreement_type: str = None, search: str = None, today: bool = False):
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
            today_str = datetime.date.today().isoformat()
            query += " AND created_at LIKE ?"
            params.append(f"{today_str}%")
        if search:
            query += " AND (customer_name LIKE ? OR customer_phone LIKE ? OR customer_email LIKE ? OR id LIKE ?)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param, search_param])
            
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
async def get_order_by_id(order_id: str):
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
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/orders/{order_id}/upload")
async def upload_order_to_cloud(order_id: str):
    now = datetime.datetime.now().isoformat()
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        # Check if order exists
        cursor.execute("SELECT id FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            raise HTTPException(status_code=404, detail="Order not found")
            
        # Simulating cloud sync - generate public view-only sharing link
        cloud_url = f"http://localhost:8765/Madhav_Drafting_Hub.html?view={order_id}"
        
        cursor.execute(
            "UPDATE orders SET cloud_url = ?, updated_at = ? WHERE id = ?",
            (cloud_url, now, order_id)
        )
        conn.commit()
        conn.close()
        return {"status": "success", "cloud_url": cloud_url}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/orders/{order_id}/status")
async def update_order_status(order_id: str, request: StatusUpdateRequest):
    now = datetime.datetime.now().isoformat()
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE orders SET status = ?, updated_at = ? WHERE id = ?",
            (request.status, now, order_id)
        )
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
async def get_analytics():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        # Total count
        cursor.execute("SELECT COUNT(*) FROM orders")
        total_orders = cursor.fetchone()[0]
        
        # Today's count
        today_str = datetime.date.today().isoformat()
        cursor.execute("SELECT COUNT(*) FROM orders WHERE created_at LIKE ?", (f"{today_str}%",))
        today_orders = cursor.fetchone()[0]
        
        # Detailed breakdown per agreement type
        cursor.execute("""
            SELECT 
                agreement_type,
                COUNT(*) as total,
                SUM(CASE WHEN created_at LIKE ? THEN 1 ELSE 0 END) as today,
                SUM(CASE WHEN status IN ('PENDING_PAYMENT', 'DRAFTED') THEN 1 ELSE 0 END) as pending
            FROM orders
            GROUP BY agreement_type
        """, (f"{today_str}%",))
        rows = cursor.fetchall()
        agreement_details = {}
        for r in rows:
            agreement_details[r[0]] = {
                "total": r[1],
                "today": r[2],
                "pending": r[3]
            }
        
        # Total revenue (paid / completed)
        cursor.execute("SELECT SUM(amount) FROM orders WHERE status IN ('PAID', 'COMPLETED', 'SIGNED')")
        total_revenue = cursor.fetchone()[0] or 0.0
        
        # Status breakdown
        cursor.execute("SELECT status, COUNT(*) FROM orders GROUP BY status")
        status_breakdown = dict(cursor.fetchall())
        
        # Agreement type breakdown
        cursor.execute("SELECT agreement_type, COUNT(*) FROM orders GROUP BY agreement_type")
        agreement_breakdown = dict(cursor.fetchall())
        
        # Source breakdown
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

if __name__ == "__main__":
    import uvicorn
    # Runs the server on http://localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
