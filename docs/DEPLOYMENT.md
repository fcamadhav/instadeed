# Deployment Guide

## Current Architecture

- **VM**: GCP Compute Engine e2-small (us-central1-a, 2GB RAM + 2GB swap)
- **HTTPS**: Terminated at Cloudflare (not on VM)
- **Reverse Proxy**: nginx on port 80 → routes to Docker containers
- **Database**: SQLite (file on Docker volume, no separate DB process)

## Services

| Service | Container | Port | Route |
|---------|-----------|------|-------|
| Admin API | `admin_backend_1` | 4000 | `/api/` |
| Admin Panel | `admin_frontend_1` | 3000 | `/admin/` |
| Landing Page | `landing_frontend_1` | 5000 | `/` |
| Customer SPA | nginx static file | — | `/app/` |

## Environment Variables

**Required for backend:**
- `DATABASE_URL` — e.g. `file:./data/instadeed_admin.db`
- `JWT_SECRET` — 32+ random characters
- `NODE_ENV` — `production`

**Required for payments (production):**
- Set real Razorpay keys via admin panel at `/admin/payments`
- Without real keys, payment endpoints return 503 (fail-closed)

## Deploying to GCP VM

```bash
# SSH into the VM
gcloud compute ssh instadeed-server --zone us-central1-a

# Pull latest code and rebuild
cd /app/admin
git pull origin master
docker-compose up -d --build
```

## First-Time Setup

```bash
# Clone repo
git clone https://github.com/fcamadhav/instadeed.git /app
cd /app/admin

# Build and start
docker-compose build
docker-compose up -d

# Admin login
# Email: admin@instadeed.local
# Password: admin123  (change immediately in admin panel)
```

## Nginx Configuration

The nginx config lives at `/etc/nginx/sites-available/default` and routes:
- `/` → landing_frontend_1:5000
- `/admin/` → admin_frontend_1:3000
- `/app/` → static file: `/var/www/draft/index.html`
- `/api/` → admin_backend_1:4000

## Backups

Automated via `backup.sh` — daily cron at 3 AM IST:
- DB + document files compressed
- 7 daily + 4 weekly rotation
- Off-site upload to GCS via gsutil

Manual trigger available in Admin Panel → Settings → Backups.

## Health Check

```bash
curl https://instadeed.io/api/config
# → {"razorpay_key":"...","version":"2.0.0","app_name":"INSTADEED"}
```
