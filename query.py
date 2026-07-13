import sqlite3
import os

try:
    c = sqlite3.connect('/var/lib/instadeed/madhav_crm.db')
    cursor = c.cursor()
    cursor.execute('SELECT id, email, phone, doc_type, updated_at FROM saved_drafts LIMIT 50;')
    rows = cursor.fetchall()
    if not rows:
        print("No drafts found.")
    else:
        for row in rows:
            print(f"ID: {row[0]}, Email: {row[1]}, Phone: {row[2]}, Type: {row[3]}, Updated: {row[4]}")
except Exception as e:
    print(f"Error: {e}")
