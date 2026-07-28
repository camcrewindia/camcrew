import os
import sqlite3
from flask import (
    Flask, request, session, jsonify,
    send_from_directory, abort
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-change-me")

# Only these extensions may be served as static files.
ALLOWED_EXTENSIONS = {
    ".html", ".css", ".js", ".ico", ".png", ".jpg", ".jpeg",
    ".gif", ".svg", ".webp", ".woff", ".woff2", ".ttf", ".otf",
    ".json", ".map", ".txt",
}

DB_PATH = "camcrew.db"

# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                email        TEXT    NOT NULL UNIQUE,
                password     TEXT    NOT NULL,
                role         TEXT    NOT NULL DEFAULT 'customer',
                display_name TEXT,
                created_at   TEXT    DEFAULT (datetime('now'))
            )
        """)
        # Migrate: add display_name if it doesn't exist yet
        try:
            conn.execute("ALTER TABLE users ADD COLUMN display_name TEXT")
        except Exception:
            pass
        conn.commit()


init_db()

# ---------------------------------------------------------------------------
# Static page routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    # Block any path that escapes the root or targets hidden/sensitive files
    if ".." in filename or filename.startswith("."):
        abort(403)

    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        abort(403)

    return send_from_directory(".", filename)

# ---------------------------------------------------------------------------
# Auth API
# ---------------------------------------------------------------------------

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(force=True)
    email    = (data.get("email")    or "").strip().lower()
    password = (data.get("password") or "").strip()
    role     = (data.get("role")     or "customer").strip().lower()

    if not email or not password:
        return jsonify({"ok": False, "error": "Email and password are required."}), 400

    if len(password) < 6:
        return jsonify({"ok": False, "error": "Password must be at least 6 characters."}), 400

    if role not in ("customer", "professional", "studio", "admin"):
        role = "customer"

    hashed = generate_password_hash(password)
    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
                (email, hashed, role),
            )
            conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"ok": False, "error": "An account with that email already exists."}), 409

    # Log the user in immediately after registration
    with get_db() as conn:
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

    session["user_id"] = row["id"]
    session["email"]   = row["email"]
    session["role"]    = row["role"]

    return jsonify({"ok": True, "user": {"email": row["email"], "role": row["role"]}})


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    email    = (data.get("email")    or "").strip().lower()
    password = (data.get("password") or "").strip()

    if not email or not password:
        return jsonify({"ok": False, "error": "Email and password are required."}), 400

    with get_db() as conn:
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

    if not row or not check_password_hash(row["password"], password):
        return jsonify({"ok": False, "error": "Invalid email or password."}), 401

    session["user_id"] = row["id"]
    session["email"]   = row["email"]
    session["role"]    = row["role"]

    return jsonify({"ok": True, "user": {"email": row["email"], "role": row["role"]}})


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/me", methods=["GET"])
def me():
    if "user_id" not in session:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    return jsonify({
        "ok": True,
        "user": {
            "email": session["email"],
            "role":  session["role"],
        }
    })


@app.route("/api/profile", methods=["GET"])
def get_profile():
    if "user_id" not in session:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    with get_db() as conn:
        row = conn.execute(
            "SELECT email, role, display_name, created_at FROM users WHERE id = ?",
            (session["user_id"],)
        ).fetchone()
    if not row:
        return jsonify({"ok": False, "error": "User not found."}), 404
    return jsonify({
        "ok": True,
        "profile": {
            "email":        row["email"],
            "role":         row["role"],
            "display_name": row["display_name"] or "",
            "created_at":   row["created_at"],
        }
    })


@app.route("/api/profile", methods=["PATCH"])
def update_profile():
    if "user_id" not in session:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    data = request.get_json(force=True)
    display_name = (data.get("display_name") or "").strip()
    if len(display_name) > 60:
        return jsonify({"ok": False, "error": "Display name must be 60 characters or fewer."}), 400
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET display_name = ? WHERE id = ?",
            (display_name, session["user_id"])
        )
        conn.commit()
    return jsonify({"ok": True, "display_name": display_name})


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug)
