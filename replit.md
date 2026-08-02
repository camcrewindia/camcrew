# CamCrew

A marketplace web app for creative professionals — photographers, videographers, designers, organizers, caterers, and more. Customers can browse services, book professionals, manage orders, and handle rentals/sales. Professionals get a dashboard to manage their profile and bookings. Admins have a separate dashboard for user management and verification.

## Stack

- **Backend**: Python / Flask (`app.py`)
- **Database**: PostgreSQL (via `psycopg2`)
- **Frontend**: Multi-page HTML/CSS/JS (Tailwind CSS via CDN)
- **Auth**: Session-based (Flask sessions)

## Running the app

The workflow `Start application` runs `python app.py`, which starts the Flask server on port 5000.

```
python app.py
```

## Environment variables / secrets

| Key | Purpose |
|-----|---------|
| `SESSION_SECRET` | Flask session signing key |
| `RENDER_DATABASE_URL` | PostgreSQL external connection URL |

## Database

The app calls `init_db()` on startup, which creates all tables with `CREATE TABLE IF NOT EXISTS` — safe to run on an existing database.

## Key pages

- `/` — Homepage (`index.html`)
- `/signin.html` — Customer/professional sign-in
- `/admindashboard.html` — Admin dashboard
- `/professional-dashboard.html` — Professional dashboard

## User preferences
