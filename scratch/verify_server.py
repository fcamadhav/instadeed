import requests

try:
    res = requests.get("http://localhost:8000/")
    print(f"Status Code: {res.status_code}")
    print(f"Content length: {len(res.text)}")
    print(f"Contains INSTADEED: {'INSTADEED' in res.text}")
except Exception as e:
    print(f"Error connecting: {e}")
