"""
Tests for Instadeed authentication system.
"""
import pytest
import os
import sys
import json

os.environ["JWT_SECRET"] = "test-secret-key-for-pytest"
os.environ["RAZORPAY_KEY_ID"] = "test_key"
os.environ["RAZORPAY_KEY_SECRET"] = "test_secret"

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.backend.services.auth import create_token, verify_token, hash_password, verify_password

class TestAuth:
    def test_hash_password(self):
        pw = "TestPass123"
        hashed = hash_password(pw)
        assert hashed != pw
        assert verify_password(pw, hashed)
        assert not verify_password("wrong", hashed)

    def test_create_token(self):
        token = create_token("user-1", "test@test.com", "user")
        assert token
        decoded = verify_token(token)
        assert decoded["sub"] == "user-1"
        assert decoded["email"] == "test@test.com"
        assert decoded["role"] == "user"

    def test_expired_token(self):
        import jwt
        import datetime
        expired = jwt.encode({
            "sub": "user-1",
            "exp": datetime.datetime.utcnow() - datetime.timedelta(hours=1)
        }, os.environ["JWT_SECRET"], algorithm="HS256")
        assert verify_token(expired) is None

    def test_invalid_token(self):
        assert verify_token("not-a-valid-token") is None


@pytest.mark.asyncio
class TestAPI:
    async def test_health_endpoint(self, client):
        resp = await client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"

    async def test_config_endpoint_no_key(self, client, monkeypatch):
        import server
        monkeypatch.setattr(server, "RAZORPAY_KEY_ID", "")
        resp = await client.get("/api/config")
        assert resp.status_code == 503

    async def test_send_otp_invalid_email(self, client):
        resp = await client.post("/api/auth/send-otp", json={"email": "not-an-email"})
        assert resp.status_code == 400

    async def test_signup_weak_password(self, client):
        resp = await client.post("/api/auth/signup", json={
            "name": "Test", "email": "test@test.com", "password": "123"
        })
        assert resp.status_code == 400
        assert "8 characters" in resp.json()["detail"]

    async def test_signup_missing_name(self, client):
        resp = await client.post("/api/auth/signup", json={
            "name": "", "email": "test@test.com", "password": "StrongPass1"
        })
        assert resp.status_code == 400
