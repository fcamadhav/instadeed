# Instadeed – Legal Drafting Suite

A web-based legal document drafting platform for Indian legal professionals. Draft, customize, and deliver legal documents including Registered Rent Agreements, TM-48 Trademark Authorizations, and GNIDA Registry forms.

## Features

- **Rent Agreement Generator** — Multi-party support, clause distribution, annexure tables, witness details, pagination-controlled (3-page hard lock)
- **TM-48 Trademark Authorization** — Exact replication of statutory form per the Trade Marks Act, 1999
- **GNIDA Registry Forms** — Integrated registry documentation
- **PDF Export & Print** — Hard-locked layouts for legal compliance
- **Payment Integration** — Razorpay checkout for paid document generation
- **Google Sign-In** — OAuth-based authentication
- **CRM Database** — SQLite-backed order management via FastAPI

## Tech Stack

- **Frontend**: HTML, Tailwind CSS, Vanilla JavaScript, Google Fonts, Font Awesome
- **Backend**: Python (FastAPI), SQLite
- **Payment**: Razorpay
- **Auth**: Google Identity Services (GSI)

## Getting Started

### Prerequisites

- Python 3.8+
- [Node.js](https://nodejs.org/) (for Tailwind CDN is used, but local dev may use npm)

### Setup

```bash
# Clone the repo
git clone https://github.com/fcamadhav/instadeed.git
cd instadeed

# Install Python dependencies
pip install fastapi uvicorn razorpay pydantic

# Start the backend server
python server.py
```

Open `Madhav_Drafting_Hub.html` in a browser (or serve via a local HTTP server for full functionality).

## Project Structure

| File | Description |
|------|-------------|
| `Madhav_Drafting_Hub.html` | Main application (all templates UI + logic) |
| `server.py` | FastAPI backend (payments, CRM, database API) |
| `madhav_crm.db` | SQLite database for orders |

## License

All rights reserved.
