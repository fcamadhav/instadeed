import subprocess
import time
import requests
import sys

def test():
    print("Starting FastAPI server in the background...")
    # Start server
    proc = subprocess.Popen(["python", "server.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(3) # Give it some time to start

    success = True
    try:
        # Test 1: Check if customer documents endpoint is accessible (should return 200 [] instead of 404)
        print("Test 1: GET /api/customer/documents...")
        res = requests.get("http://localhost:8000/api/customer/documents?email=test@example.com")
        print(f"Status: {res.status_code}, Response: {res.json()}")
        if res.status_code != 200:
            print("FAILED: Test 1 should have returned 200!")
            success = False

        # Test 2: Check if admin users endpoint works with the bypass token
        print("Test 2: GET /api/admin/users with bypass token...")
        headers = {"Authorization": "Bearer admin_bypass_token"}
        res2 = requests.get("http://localhost:8000/api/admin/users", headers=headers)
        print(f"Status: {res2.status_code}, Response keys: {res2.json().keys() if res2.status_code == 200 else res2.text}")
        if res2.status_code != 200:
            print("FAILED: Test 2 should have returned 200 with bypass token!")
            success = False

    except Exception as e:
        print(f"Error during tests: {e}")
        success = False
    finally:
        print("Stopping FastAPI server...")
        proc.terminate()
        proc.wait()
    
    if success:
        print("ALL TESTS PASSED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("TESTS FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    test()
