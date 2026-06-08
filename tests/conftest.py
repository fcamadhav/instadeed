"""
Pytest configuration with async test client.
"""
import pytest
import os
import sys

os.environ["JWT_SECRET"] = "test-secret-key-for-pytest"
os.environ["RAZORPAY_KEY_ID"] = "test_key"
os.environ["RAZORPAY_KEY_SECRET"] = "test_secret"

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def client():
    from httpx import ASGITransport, AsyncClient
    from server import app
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")
