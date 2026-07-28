# Camcrew Studio

A static multi-page digital marketplace for cinematic creators (photographers, videographers, designers, organizers, etc.) with a Python Flask authentication backend.

## Stack

- **Frontend**: Plain HTML + Tailwind CSS (CDN)
- **Backend**: Python Flask
- **Database**: SQLite (`camcrew.db`, auto-created on first run)
- **Auth**: Flask sessions + Werkzeug password hashing

## Running

```bash
python app.py
```

The app runs on port 5000.

## Auth API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register` | Register a new user. Body: `{ email, password, role }` |
| POST | `/api/login` | Log in. Body: `{ email, password }` |
| POST | `/api/logout` | Log out (clears session) |
| GET | `/api/me` | Returns current session user |

### Roles
- `customer` — default
- `professional` — photographers, videographers, designers, etc.
- `studio` — studio accounts (redirected to admin panel)

## Project Structure

```
app.py           # Flask app — auth API + static file serving
camcrew.db       # SQLite database (auto-created)
signin.html      # Auth portal (wired to Flask API)
admin.html       # Studio/admin landing page
index.html       # Main homepage
*.html           # Other marketplace pages
```

## User Preferences

- Backend must be strictly Python Flask only (no other frameworks).
