# Instadeed – Legal Drafting Suite

A production-ready legal document drafting platform for Indian legal professionals.
Draft, customize, and deliver legal documents including Rent Agreements, TM-48 Trademark Authorizations,
GNIDA Registry forms, and more — with integrated payments and admin CRM.

## Tech Stack

- **Backend**: Node.js + Express + TypeScript, SQLite (Prisma ORM)
- **Admin Frontend**: Next.js 14 + React + Tailwind CSS
- **Landing Page**: Next.js 15 + Framer Motion + Tailwind v4
- **Customer SPA**: React compiled SPA (`Madhav_Drafting_Hub.html`)
- **Payment**: Razorpay
- **PDF**: pdfkit
- **Deploy**: Docker on GCP Compute Engine, nginx reverse proxy, Cloudflare HTTPS

## Quick Start

```bash
cd admin

# 1. Install dependencies
cd backend && npm install && npx prisma generate && cd ..
cd frontend && npm install && cd ..

# 2. Start in development
cd backend && npm run dev &    # → http://localhost:4000
cd frontend && npm run dev &   # → http://localhost:3000
```

## Production Deployment

```bash
cd admin

# Build and start with Docker
docker-compose build
docker-compose up -d
```

The server stack runs behind nginx:
- Landing: `https://instadeed.io/` (port 5000)
- Admin: `https://instadeed.io/admin/` (port 3000)
- Customer SPA: `https://instadeed.io/app/` (served directly by nginx)
- API: `https://instadeed.io/api/` (port 4000)

## Features

- **20+ Document Types**: Rent Agreement, Sale Deed, Mutation, GNIDA KYA, GNIDA Registry, GNIDA PTM, GNIDA 5-in-1 Package, Transfer Memo, TM-48, and more
- **Live Drafting**: Customer-facing SPA with real-time document form, document uploads, and payment
- **Payment**: Razorpay integration with order creation, signature verification, and webhook
- **Admin CRM**: Orders, customers, documents, invoices, GST reports, Kanban pipeline, audit trail, analytics
- **PDF Generation**: Automated PDF generation via pdfkit on payment verification
- **Backups**: Automated DB + document backups with rotation and off-site upload

## Project Structure

```
├── admin/
│   ├── backend/               # Express + TypeScript + Prisma API
│   │   ├── src/
│   │   │   ├── routes/        # API route handlers
│   │   │   ├── services/      # PDF generator, audit
│   │   │   ├── middleware/     # Auth, rate limiting
│   │   │   └── lib/           # Prisma client
│   │   ├── prisma/
│   │   │   ├── schema.prisma  # Database schema (SQLite)
│   │   │   └── data/          # SQLite DB file (mounted volume)
│   │   └── Dockerfile
│   ├── frontend/              # Next.js admin panel
│   │   ├── src/app/admin/     # Admin pages
│   │   └── Dockerfile
│   └── docker-compose.yml     # Backend + frontend services
├── landing/                   # Next.js landing page
├── Madhav_Drafting_Hub.html   # Customer-facing SPA
├── backup.sh                  # Backup script
└── .github/workflows/         # CI/CD pipeline
```

## API Overview

| Category | Endpoints |
|----------|-----------|
| Auth | `POST /api/admin/auth/login`, `/google`, `/register`, `/me`, `/forgot-password`, `/reset-password` |
| Payments | `POST /create-order`, `POST /verify-payment`, `GET /api/config`, `/api/admin/payment-gateways` |
| Admin | `CRUD /api/admin/orders`, `/documents`, `/users`, `/services`, `/categories`, `/customers` |
| Documents | `POST /api/applications/documents/upload`, `GET/DELETE /applications/documents/:id`, `GET /applications/:id/documents` |
| Reports | `GET /api/admin/reports/:type`, `/analytics`, `/audit` |

## Security

- bcrypt password hashing (12 rounds)
- JWT authentication with configurable expiry
- Google OAuth token server-side verification
- Rate limiting on all auth endpoints
- Path traversal protection (isPathSafe)
- Security headers on all responses (CSP, X-Frame-Options, etc.)
- Input validation via Zod on all endpoints
- Parameterized SQL queries (Prisma)

## Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

## License

Proprietary — Instadeed Legal Suite
