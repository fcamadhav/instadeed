import sqlite3
import datetime
import logging
import os
from typing import Optional

logger = logging.getLogger("instadeed")

DATABASE_FILE = os.environ.get("DATABASE_FILE", "madhav_crm.db")

class Database:
    def __enter__(self):
        self.conn = sqlite3.connect(DATABASE_FILE)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA foreign_keys=ON")
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        self.conn.close()
        return False

def get_db():
    return Database()

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA foreign_keys=ON")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id TEXT PRIMARY KEY, customer_name TEXT, customer_phone TEXT,
        customer_email TEXT, agreement_type TEXT, source TEXT,
        status TEXT, amount REAL, form_data TEXT,
        created_at TEXT, updated_at TEXT, cloud_url TEXT,
        leegality_doc_id TEXT, leegality_sign_url TEXT,
        is_favorite INTEGER DEFAULT 0
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL, phone TEXT DEFAULT '',
        location TEXT DEFAULT '', device_info TEXT DEFAULT '',
        role TEXT DEFAULT 'user', is_active INTEGER DEFAULT 1,
        created_at TEXT, last_login TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS api_keys (
        id TEXT PRIMARY KEY, user_id TEXT NOT NULL,
        key_hash TEXT NOT NULL, key_prefix TEXT NOT NULL,
        name TEXT DEFAULT 'Default', is_active INTEGER DEFAULT 1,
        last_used TEXT, created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS page_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT,
        session_id TEXT, user_id TEXT, event TEXT, page TEXT,
        detail TEXT, ip_address TEXT, user_agent TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT,
        method TEXT, path TEXT, status_code INTEGER,
        ip_address TEXT, user_id TEXT, duration_ms INTEGER, user_agent TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT,
        timestamp TEXT, ip_address TEXT, user_agent TEXT,
        device_info TEXT DEFAULT '',
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, order_id TEXT,
        note TEXT, author_id TEXT, created_at TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (author_id) REFERENCES users(id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT, order_id TEXT,
        staff_id TEXT, role TEXT DEFAULT 'attorney', assigned_at TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (staff_id) REFERENCES users(id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_versions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, order_id TEXT,
        version INTEGER DEFAULT 1, form_data_snapshot TEXT,
        created_at TEXT, author_id TEXT, change_summary TEXT DEFAULT '',
        FOREIGN KEY (order_id) REFERENCES orders(id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS refunds (
        id TEXT PRIMARY KEY, order_id TEXT, amount REAL,
        reason TEXT, status TEXT DEFAULT 'PENDING',
        created_at TEXT, processed_at TEXT, processed_by TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coupons (
        id TEXT PRIMARY KEY, code TEXT UNIQUE, type TEXT DEFAULT 'percentage',
        value REAL, max_uses INTEGER DEFAULT 0, current_uses INTEGER DEFAULT 0,
        min_amount REAL DEFAULT 0, expires_at TEXT, is_active INTEGER DEFAULT 1,
        created_at TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT DEFAULT 'info',
        recipient TEXT, title TEXT, message TEXT,
        reference_type TEXT DEFAULT '', reference_id TEXT DEFAULT '',
        status TEXT DEFAULT 'pending', created_at TEXT, sent_at TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id TEXT PRIMARY KEY, order_id TEXT, invoice_number TEXT UNIQUE,
        amount REAL, gst_amount REAL DEFAULT 0, total REAL,
        status TEXT DEFAULT 'PENDING', created_at TEXT, paid_at TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(id)
    )""")

    for idx in [
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
    ]:
        try:
            cursor.execute(idx)
        except Exception:
            pass

    conn.commit()
    conn.close()
    logger.info("Database initialized with %d tables and indexes", 14)
