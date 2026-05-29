import requests

BASE_URL = "http://localhost:8000"

def run_tests():
    print("1. Creating a test walk-in order...")
    payload = {
        "customer_name": "Cloud Test Client",
        "customer_phone": "9999988888",
        "customer_email": "cloudtest@example.com",
        "agreement_type": "RENT",
        "amount": 499.0,
        "status": "DRAFTED",
        "form_data": {"tenantName": "John Doe", "rentAmount": "15000"}
    }
    r = requests.post(f"{BASE_URL}/create-offline-order", json=payload)
    assert r.status_code == 200, f"Failed: {r.status_code}"
    order_id = r.json()["order_id"]
    print(f"Created: {order_id}")
    
    print("\n2. Fetching order details by ID...")
    r = requests.get(f"{BASE_URL}/orders/{order_id}")
    assert r.status_code == 200, f"Failed: {r.status_code}"
    order_data = r.json()
    assert order_data["customer_name"] == "Cloud Test Client"
    assert order_data["cloud_url"] is None
    print(f"Fetched successfully! cloud_url is initially {order_data['cloud_url']}")
    
    print("\n3. Syncing walk-in order to cloud...")
    r = requests.post(f"{BASE_URL}/orders/{order_id}/upload")
    assert r.status_code == 200, f"Failed: {r.status_code}"
    cloud_url = r.json()["cloud_url"]
    print(f"Synced successfully! cloud_url is: {cloud_url}")
    
    print("\n4. Re-fetching order details to verify cloud_url database persistence...")
    r = requests.get(f"{BASE_URL}/orders/{order_id}")
    assert r.status_code == 200, f"Failed: {r.status_code}"
    order_data = r.json()
    assert order_data["cloud_url"] == cloud_url
    print(f"Verified! Persisted cloud_url in database is: {order_data['cloud_url']}")
    
    print("\n5. Fetching all orders and checking list output...")
    r = requests.get(f"{BASE_URL}/orders")
    assert r.status_code == 200, f"Failed: {r.status_code}"
    orders = r.json()
    found_order = next((o for o in orders if o["id"] == order_id), None)
    assert found_order is not None
    assert found_order["cloud_url"] == cloud_url
    print("Verified! list output contains cloud_url.")
    
    print("\nALL CLOUD STORAGE & API ENDPOINT TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
