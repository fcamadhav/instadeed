import subprocess
import time
import requests
import sqlite3
import os

def run_tests():
    # Start server
    print("Starting FastAPI server in the background...")
    proc = subprocess.Popen(["python", "server.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(3) # Wait for startup

    success = True
    try:
        # Create a mock order and invoice in the database
        print("Inserting mock order & invoice...")
        conn = sqlite3.connect("madhav_crm.db")
        cursor = conn.cursor()
        
        # Clear existing mocks if any
        cursor.execute("DELETE FROM invoices WHERE id = 'test-inv-1'")
        cursor.execute("DELETE FROM orders WHERE id = 'test-ord-1'")
        
        # Insert mock order
        cursor.execute("""
            INSERT INTO orders (id, customer_name, customer_phone, customer_email, agreement_type, amount, status, created_at)
            VALUES ('test-ord-1', 'Bhati Ji', '9999999999', 'bhati@test.com', 'GNIDA 5-in-1 Composite Package', 422.88, 'PAID', '2026-06-24T13:37:09')
        """)
        # Insert mock invoice
        cursor.execute("""
            INSERT INTO invoices (id, order_id, invoice_number, amount, gst_amount, total, status, created_at)
            VALUES ('test-inv-1', 'test-ord-1', 'INV-MOCK-001', 422.88, 76.12, 499.00, 'PAID', '2026-06-24T13:37:09')
        """)
        conn.commit()
        conn.close()

        # Call GET download endpoint using query parameter token
        print("Test: Downloading invoice via GET with query token...")
        url = "http://localhost:8000/api/admin/invoices/test-inv-1/download?token=admin_bypass_token"
        res = requests.get(url)
        print(f"Status: {res.status_code}")
        print(f"Content-Type: {res.headers.get('Content-Type')}")
        print(f"Content-Disposition: {res.headers.get('Content-Disposition')}")
        
        if res.status_code == 200 and "pdf" in res.headers.get("Content-Type", "").lower() and len(res.content) > 1000:
            print("SUCCESS: PDF downloaded correctly!")
        else:
            print("FAILED: Response was not a valid PDF or status was not 200.")
            success = False

    except Exception as e:
        print(f"Error during tests: {e}")
        success = False
    finally:
        print("Stopping FastAPI server...")
        proc.terminate()
        proc.wait()

    if success:
        print("MOCK INVOICE DOWNLOAD TEST PASSED!")
    else:
        print("MOCK INVOICE DOWNLOAD TEST FAILED!")

if __name__ == "__main__":
    run_tests()
