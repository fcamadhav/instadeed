# Deployment Guide

## Prerequisites

- Python 3.11+
- Node.js 20+ (for frontend builds)
- A Render account (or any Docker host)
- A Hostinger account (for custom domain)

## Environment Variables

Copy `.env.example` to `.env` and set all required values:

```bash
cp .env.example .env
# Edit .env with your production values
```

**REQUIRED:**
- `JWT_SECRET` - Long random string (min 32 chars)
- `RAZORPAY_KEY_ID` - Live Razorpay key ID
- `RAZORPAY_KEY_SECRET` - Live Razorpay key secret

**RECOMMENDED:**
- `ADMIN_EMAIL` - Admin login email
- `ADMIN_PASSWORD` - Strong admin password
- `LEEGALITY_AUTH_TOKEN` - Leegality API token
- `ALLOWED_ORIGINS` - Comma-separated allowed CORS origins

## Deploying to Render (Current)

1. Connect your GitHub repository to Render
2. Set the build command: `pip install -r requirements.txt && python build.py`
3. Set the start command: `uvicorn server:app --host 0.0.0.0 --port 8000 --proxy-headers`
4. Add all environment variables in Render dashboard
5. Enable Auto-Deploy from GitHub

## Deploying with Docker

```bash
docker compose build
docker compose up -d
docker compose logs -f
```

## Deploying Manually

```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Build frontend
python build.py

# Run server
python server.py
# Or with uvicorn directly:
uvicorn server:app --host 0.0.0.0 --port 8000
```

## Health Check

After deployment, verify:
```bash
curl https://instadeed.io/api/health
# → {"status":"ok","version":"2.0.0","timestamp":"..."}
```

## Database Backups

SQLite database is stored in `madhav_crm.db`. Back up regularly:

```bash
cp madhav_crm.db backups/madhav_crm_$(date +%Y%m%d).db
```

For PostgreSQL (future), set `DATABASE_URL` env var.
