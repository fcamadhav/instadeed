import os

with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """            conn = sqlite3.connect(DATABASE_FILE)
            conn.execute("BEGIN TRANSACTION")
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE orders SET status = 'PAID', updated_at = ? WHERE id = ?", (now, body.razorpay_order_id))
    else:"""

replacement = """            conn = sqlite3.connect(DATABASE_FILE)
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
            threading.Thread(target=sync_order_to_admin, args=(body.razorpay_order_id, "PAID", body.razorpay_payment_id)).start()
            return {"status": "success", "message": "Payment verified successfully!"}
        except razorpay.errors.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid Payment Signature. Potential Fraud.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:"""

if target in content:
    content = content.replace(target, replacement)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed!")
else:
    print("Target not found. Doing fallback search.")
    target_crlf = target.replace('\n', '\r\n')
    if target_crlf in content:
        content = content.replace(target_crlf, replacement.replace('\n', '\r\n'))
        with open('server.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Fixed CRLF!")
    else:
        print("Target really not found.")
