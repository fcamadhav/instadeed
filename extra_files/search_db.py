import sqlite3

term = "regrentdata"
found = False

try:
    conn = sqlite3.connect("madhav_crm.db")
    cursor = conn.cursor()
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cursor.fetchall()]
    
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [c[1] for c in cursor.fetchall()]
        
        # We can search in all rows
        cursor.execute(f"SELECT * FROM {table};")
        rows = cursor.fetchall()
        for row_idx, row in enumerate(rows):
            for col_idx, val in enumerate(row):
                if val and term in str(val).lower():
                    found = True
                    print(f"Found in table '{table}', row {row_idx}, column '{columns[col_idx]}':")
                    print("  Value:", str(val)[:200])
except Exception as e:
    print(f"Error reading DB: {e}")

if not found:
    print("Not found in database.")
