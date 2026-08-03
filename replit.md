# CamCrew

A Flask web platform connecting customers with photography/videography professionals, studios, caterers, designers, and other creative service providers.

## Stack
- **Backend**: Python / Flask (`app.py`)
- **Database**: PostgreSQL (via `psycopg2`)
- **Frontend**: Plain HTML/CSS/JS (multi-page, served as static files by Flask)

## Key features
- Customer & professional registration/login (with Aadhaar verification flow)
- Service browsing (photographers, videographers, studios, caterers, designers, etc.)
- Booking, cart, and checkout
- Professional dashboards, portfolio, and public profiles
- Admin dashboard (login at `/adminlogin.html`)
- Subscription management, order tracking, inventory

## Running the app

1. Set the `RENDER_DATABASE_URL` secret to your PostgreSQL connection string.
2. Set `SESSION_SECRET` to a random secret string.
3. Start the workflow: `python app.py` (serves on port 5000).

## Environment secrets required
| Secret | Purpose |
|--------|---------|
| `RENDER_DATABASE_URL` | PostgreSQL connection string |
| `SESSION_SECRET` | Flask session signing key |

## User preferences
