# Security Architecture

## Overview

Instadeed follows security best practices for a legal document SaaS platform handling PII and financial data.

## Security Layers

### 1. Transport Security
- HTTPS enforced at the Render/Hostinger reverse proxy level
- HSTS header: `max-age=31536000; includeSubDomains; preload`
- All API responses include security headers

### 2. Authentication
- **JWT Tokens**: HS256-signed tokens with 24h expiry
- **Password Storage**: bcrypt hashing (SHA-256 fallback)
- **OTP**: 6-digit random codes with 5-minute expiry (in-memory)
- **Google OAuth**: Token verification via Google Identity Services

### 3. Authorization
- Role-based access: `user`, `admin`, `attorney`, `support`, `finance`
- Admin endpoints require `role == "admin"` check
- API keys supported for programmatic access

### 4. API Security
- Rate limiting on auth endpoints (5-60 req/min depending on endpoint)
- CORS restricted to allowed origins
- All user input validated (email format, password strength, phone)
- SQL injection prevented via parameterized queries
- XSS prevented via `textContent` instead of `innerHTML`
- Global exception handler sanitizes 500 errors

### 5. Payment Security
- Razorpay signature verification on all payment callbacks
- No raw card data handled (Razorpay Checkout handles PCI DSS)
- Live keys only configurable via environment variables

### 6. Document Security
- PDFs generated server-side with FPDF
- e-Sign via Leegality (third-party KYC-compliant platform)
- Document access requires order ID + phone/email verification

### 7. Data Privacy
- SQLite database git-ignored
- Passwords never logged
- OTPs logged for debugging (in production, delivered via SMTP)
- Minimal PII collected (name, email, phone)

## Security Headers

All responses include:
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Content-Security-Policy: (restricted to known CDNs)
```

## OWASP Top 10 Coverage

| Risk | Status |
|------|--------|
| A01: Broken Access Control | ✅ RBAC implemented |
| A02: Cryptographic Failures | ✅ bcrypt + HS256 JWT |
| A03: Injection | ✅ Parameterized queries |
| A04: Insecure Design | ✅ Rate limited |
| A05: Security Misconfiguration | ✅ Env var based |
| A06: Vulnerable Components | ✅ Regular updates |
| A07: Auth Failures | ✅ OTP + JWT + OAuth |
| A08: Data Integrity Failures | ✅ Signature verification |
| A09: Logging Failures | ✅ Structured logging |
| A10: SSRF | ✅ No user-controlled URLs |
