# Instadeed – Legal Drafting Suite

A production-ready legal document drafting platform for Indian legal professionals.
Draft, customize, and deliver legal documents including Rent Agreements, TM-48 Trademark Authorizations,
GNIDA Registry forms, and more — with integrated payments, e-Sign, and admin CRM.

## Tech Stack

- **Backend**: Python (FastAPI), SQLite/PostgreSQL, JWT auth
- **Frontend**: React + JSX (compiled via Babel), Tailwind CSS CDN
- **Payment**: Razorpay Checkout
- **e-Sign**: Leegality API
- **Auth**: Google Identity Services + OTP + Email/Password
- **Deploy**: Docker / Render

## Quick Start

```bash
# 1. Install dependencies
npm install
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your keys

# 3. Build frontend
python build.py

# 4. Run server
python server.py
# → http://localhost:8000
```

## Features

- **11 Document Types**: Rent Agreement, Agreement to Sell, Registered Rent, Mutation, GNIDA KYA, GNIDA Registry, GNIDA PTM, GNIDA 5-in-1 Package, Transfer Memo, TM-48 Trademark, NOIDA Transfer
- **Live Preview**: Real-time document preview with click-to-edit variable fields
- **Payment**: Razorpay checkout with order creation and signature verification
- **e-Sign**: Leegality digital signature integration for court-ready documents
- **Admin CRM**: Staff management, coupons, notifications, invoices, GST reports, Kanban pipeline
- **Analytics**: Conversion funnel, drop-off analysis, heatmaps, audit trail
- **Drafts**: OTP-based save/resume workflow
- **User Dashboard**: Order history, document download, e-Sign status

## API Overview

| Category | Endpoints |
|----------|-----------|
| Auth | `POST /api/auth/send-otp`, `verify-otp`, `google`, `signup`, `login`, `GET /api/auth/me` |
| Orders | `POST /create-order`, `POST /verify-payment`, `GET/PUT/DELETE /orders/{id}` |
| Admin | `GET/PUT /api/admin/users`, `GET/POST /api/admin/staff`, `CRUD /api/admin/coupons`, `GET/POST /api/admin/notifications`, `GET/POST /api/admin/invoices` |
| e-Sign | `POST /api/sign/leegality/send`, `GET /api/sign/leegality/status/{id}`, `POST /api/sign/leegality/webhook` |
| Analytics | `GET /api/analytics/funnel`, `abandoned-drafts`, `heatmap`, `dropoff`, `admin/audit` |
| Drafts | `POST /api/drafts/send-otp`, `verify-otp`, `POST /api/drafts` |

## Project Structure

```
├── server.py                  # FastAPI backend (single file, 2175 lines)
├── test_script.jsx             # React frontend source (11718 lines)
├── out.js                      # Compiled JS bundle
├── Madhav_Drafting_Hub.html    # Production HTML shell
├── build.py                    # Babel build script
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Multi-service setup
├── .env.example                # Environment template
├── src/
│   └── backend/                # Modular backend components
│       ├── config.py           # Settings & env vars
│       ├── database.py         # DB abstraction
│       ├── middleware/         # Security & logging middleware
│       └── services/          # Auth, email services
├── tests/                      # Test suite
├── docs/                       # Deployment, Security, Architecture docs
├── scripts/                    # Migration utilities
└── .github/workflows/          # CI/CD pipeline
```

## Security

See [docs/SECURITY.md](docs/SECURITY.md) for full security architecture.

- bcrypt password hashing
- JWT tokens with 24h expiry
- Rate limiting on all auth endpoints
- CORS restricted to allowed origins
- Security headers on all responses
- Input validation on all endpoints
- Parameterized SQL queries
- Global exception handler (no internal leakage)

## Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

## License

Proprietary — Instadeed Legal Suite
