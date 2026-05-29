import urllib.request
import json

def test_api(url, method='GET', data=None, headers=None):
    if headers is None:
        headers = {}
    req = urllib.request.Request(url, method=method, headers=headers)
    if data:
        req.data = json.dumps(data).encode('utf-8')
        req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as response:
            res_data = response.read().decode('utf-8')
            return response.status, json.loads(res_data)
    except Exception as e:
        print(f"Error on {method} {url}: {e}")
        return None, None

def run_tests():
    print("Testing create offline order...")
    status, data = test_api(
        'http://localhost:8000/create-offline-order',
        method='POST',
        data={
            "customer_name": "Test Offline Client",
            "customer_phone": "9999999999",
            "customer_email": "test@offline.com",
            "agreement_type": "RENT",
            "amount": 0.0,
            "status": "COMPLETED",
            "form_data": {"type": "RENT", "payload": {"tenantName": "John Doe"}}
        }
    )
    print(f"Create offline order status: {status}")
    print(f"Response: {data}")
    
    if status == 200:
        order_id = data.get("order_id")
        
        print("\nTesting list orders...")
        status, orders = test_api('http://localhost:8000/orders')
        print(f"List orders status: {status}")
        print(f"Orders count: {len(orders) if orders else 0}")
        if orders:
            print(f"First order: ID={orders[0]['id']}, Name={orders[0]['customer_name']}, Source={orders[0]['source']}")
            
        print("\nTesting update status...")
        status, update_res = test_api(
            f'http://localhost:8000/orders/{order_id}/status',
            method='PUT',
            data={"status": "SIGNED"}
        )
        print(f"Update status status: {status}")
        print(f"Response: {update_res}")
        
        print("\nTesting analytics...")
        status, analytics = test_api('http://localhost:8000/analytics')
        print(f"Analytics status: {status}")
        print(f"Response: {analytics}")

if __name__ == '__main__':
    run_tests()
