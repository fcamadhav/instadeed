# Architecture

## System Overview

```
┌─────────────────────────────────────────────────────┐
│                   Client (Browser)                   │
│  React SPA ←→ Tailwind CDN ←→ Razorpay Checkout      │
└──────────────────────┬──────────────────────────────┘
                       │ HTTPS
                       ▼
┌─────────────────────────────────────────────────────┐
│            Render / Docker Host                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │              FastAPI (Uvicorn)                    │ │
│  │  ┌──────────┐ ┌────────┐ ┌───────────────────┐  │ │
│  │  │ Static   │ │ Auth   │ │ Admin Panel       │  │ │
│  │  │ Files    │ │ Module │ │ (Staff/Coupons/   │  │ │
│  │  │ (SPA)    │ │        │ │  Invoices/Reports)│  │ │
│  │  └──────────┘ └────────┘ └───────────────────┘  │ │
│  │  ┌──────────┐ ┌────────┐ ┌───────────────────┐  │ │
│  │  │ Orders   │ │Analytics│ │ Leegality eSign   │  │ │
│  │  │ & Drafts │ │ Engine │ │ Integration       │  │ │
│  │  └──────────┘ └────────┘ └───────────────────┘  │ │
│  └─────────────────────────────────────────────────┘ │
│                       │                               │
│                       ▼                               │
│  ┌─────────────────────────────────────────────────┐ │
│  │              SQLite / PostgreSQL                  │ │
│  │  11 tables: orders, users, api_keys,             │ │
│  │  page_events, activity_log, login_history,       │ │
│  │  order_notes, assignments, versions,             │ │
│  │  refunds, coupons, notifications, invoices       │ │
│  └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

## Key Design Decisions

### Why SQLite (Current)
- Zero configuration, no external service needed
- Sufficient for 1,000-10,000 concurrent users
- WAL mode for concurrent reads

### Why FastAPI
- Async-native, high performance
- Built-in Pydantic validation
- Automatic OpenAPI docs at /docs

### Why Single-File Frontend
- Early-stage simplicity
- No build tooling beyond Babel
- Tailwind CDN eliminates CSS pipeline

### Why FPDF
- Pure Python, no system dependencies
- Sufficient for simple document generation
- No LaTeX or Chromium needed

## API Design

RESTful endpoints organized by domain:
- `/api/auth/*` - Authentication
- `/api/admin/*` - Admin operations
- `/api/sign/*` - e-Sign integration
- `/api/analytics/*` - Business analytics
- `/api/drafts/*` - Draft save/resume
- `/api/...` - User-facing operations

## Data Flow: Payment

1. User fills form → frontend calls `POST /create-order`
2. Backend creates Razorpay order → returns `order_id`
3. Frontend opens Razorpay Checkout with `order_id`
4. Razorpay calls `callback` → frontend sends to `POST /verify-payment`
5. Backend verifies signature → updates order to `PAID`

## Data Flow: e-Sign

1. Admin clicks "Send for e-Sign" → frontend calls `POST /api/sign/leegality/send`
2. Backend generates PDF → base64 encodes → sends to Leegality API
3. Leegality sends email/SMS to signee with signing link
4. Signee signs → Leegality calls `POST /api/sign/leegality/webhook`
5. Backend marks order as `SIGNED`
