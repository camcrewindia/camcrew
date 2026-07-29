import os
import sqlite3
import secrets
from datetime import datetime, timedelta
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

        conn.execute("""
            CREATE TABLE IF NOT EXISTS password_reset_tokens (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL,
                token      TEXT    NOT NULL UNIQUE,
                expires_at TEXT    NOT NULL,
                used       INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id          INTEGER NOT NULL,
                order_ref        TEXT    NOT NULL,
                status           TEXT    NOT NULL DEFAULT 'processing',
                items_json       TEXT    NOT NULL DEFAULT '[]',
                total_amount     REAL    NOT NULL DEFAULT 0,
                tracking_number  TEXT,
                tracking_status  TEXT,
                created_at       TEXT    DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id           INTEGER NOT NULL,
                professional_name TEXT    NOT NULL,
                service           TEXT    NOT NULL,
                booking_date      TEXT    NOT NULL,
                status            TEXT    NOT NULL DEFAULT 'pending',
                amount            REAL    NOT NULL DEFAULT 0,
                note              TEXT,
                created_at        TEXT    DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS payment_methods (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL,
                type       TEXT    NOT NULL DEFAULT 'card',
                label      TEXT    NOT NULL,
                last4      TEXT,
                is_default INTEGER NOT NULL DEFAULT 0,
                created_at TEXT    DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS addresses (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL,
                label      TEXT    NOT NULL DEFAULT 'Home',
                full_name  TEXT    NOT NULL,
                line1      TEXT    NOT NULL,
                line2      TEXT,
                city       TEXT    NOT NULL,
                state      TEXT    NOT NULL,
                pincode    TEXT    NOT NULL,
                phone      TEXT,
                is_default INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS rewards (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                points  INTEGER NOT NULL DEFAULT 0,
                tier    TEXT    NOT NULL DEFAULT 'Bronze',
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS coupons (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id        INTEGER NOT NULL,
                code           TEXT    NOT NULL,
                discount_value REAL    NOT NULL,
                discount_type  TEXT    NOT NULL DEFAULT 'percent',
                min_order      REAL    NOT NULL DEFAULT 0,
                expires_at     TEXT,
                used           INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS refunds (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id   INTEGER,
                user_id    INTEGER NOT NULL,
                amount     REAL    NOT NULL,
                reason     TEXT,
                status     TEXT    NOT NULL DEFAULT 'pending',
                created_at TEXT    DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.commit()


def seed_demo_data(user_id):
    """Populate sample orders/bookings/rewards for a user that has none yet."""
    import json, random, string as _string
    with get_db() as conn:
        if conn.execute("SELECT COUNT(*) FROM orders WHERE user_id=?", (user_id,)).fetchone()[0]:
            return  # already seeded
        rnd = lambda n: ''.join(random.choices(_string.digits, k=n))
        orders = [
            (f"CC-{rnd(6)}", "delivered", json.dumps([
                {"name": "Canon EOS R5 Body", "qty": 1, "price": 12999},
                {"name": "EF 24-70mm f/2.8L Lens", "qty": 1, "price": 8499},
            ]), 21498, f"CCTK{rnd(8)}", "delivered"),
            (f"CC-{rnd(6)}", "processing", json.dumps([
                {"name": "DJI Ronin-S Gimbal", "qty": 1, "price": 15999},
            ]), 15999, f"CCTK{rnd(8)}", "in_transit"),
            (f"CC-{rnd(6)}", "cancelled", json.dumps([
                {"name": "LED Studio Light Kit", "qty": 2, "price": 3999},
            ]), 7998, None, None),
        ]
        for ref, status, items, total, trk_num, trk_status in orders:
            conn.execute(
                "INSERT INTO orders (user_id,order_ref,status,items_json,total_amount,tracking_number,tracking_status) VALUES (?,?,?,?,?,?,?)",
                (user_id, ref, status, items, total, trk_num, trk_status),
            )
        bookings = [
            ("Arjun Mehta", "Wedding Photography", "2026-08-15", "confirmed", 25000, "Looking forward to your big day!"),
            ("Studio Lumina", "Corporate Video Production", "2026-09-01", "pending", 45000, "Need a 2-minute brand film."),
            ("Priya Sharma", "Portrait Session", "2026-07-10", "completed", 8000, None),
        ]
        for prof, svc, date, status, amt, note in bookings:
            conn.execute(
                "INSERT INTO bookings (user_id,professional_name,service,booking_date,status,amount,note) VALUES (?,?,?,?,?,?,?)",
                (user_id, prof, svc, date, status, amt, note),
            )
        conn.execute("INSERT OR IGNORE INTO rewards (user_id,points,tier) VALUES (?,1250,'Silver')", (user_id,))
        for code, val, dtype, minord, exp in [
            ("CAMCREW10", 10, "percent", 1000, "2026-12-31"),
            ("SAVE500",  500, "flat",    5000, "2026-09-30"),
        ]:
            if not conn.execute("SELECT id FROM coupons WHERE user_id=? AND code=?", (user_id, code)).fetchone():
                conn.execute(
                    "INSERT INTO coupons (user_id,code,discount_value,discount_type,min_order,expires_at) VALUES (?,?,?,?,?,?)",
                    (user_id, code, val, dtype, minord, exp),
                )
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


@app.route("/api/forgot-password", methods=["POST"])
def forgot_password():
    data  = request.get_json(force=True)
    email = (data.get("email") or "").strip().lower()

    if not email:
        return jsonify({"ok": False, "error": "Email is required."}), 400

    with get_db() as conn:
        row = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()

    # Always return success to avoid leaking whether an account exists
    if not row:
        return jsonify({"ok": True, "message": "If that email is registered, a reset link has been sent."})

    token      = secrets.token_urlsafe(32)
    expires_at = (datetime.utcnow() + timedelta(hours=1)).isoformat()

    with get_db() as conn:
        # Invalidate any previous unused tokens for this user
        conn.execute(
            "UPDATE password_reset_tokens SET used = 1 WHERE user_id = ? AND used = 0",
            (row["id"],)
        )
        conn.execute(
            "INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES (?, ?, ?)",
            (row["id"], token, expires_at),
        )
        conn.commit()

    # In production, send token via email. Here we return it so the UI can
    # construct the reset link (dev/demo mode — replace with email delivery).
    return jsonify({
        "ok": True,
        "message": "If that email is registered, a reset link has been sent.",
        "reset_token": token,  # Remove this in production once email is wired up
    })


@app.route("/api/reset-password", methods=["POST"])
def reset_password():
    data     = request.get_json(force=True)
    token    = (data.get("token")    or "").strip()
    password = (data.get("password") or "").strip()

    if not token or not password:
        return jsonify({"ok": False, "error": "Token and new password are required."}), 400

    if len(password) < 6:
        return jsonify({"ok": False, "error": "Password must be at least 6 characters."}), 400

    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM password_reset_tokens WHERE token = ? AND used = 0",
            (token,)
        ).fetchone()

    if not row:
        return jsonify({"ok": False, "error": "This reset link is invalid or has already been used."}), 400

    if datetime.utcnow() > datetime.fromisoformat(row["expires_at"]):
        return jsonify({"ok": False, "error": "This reset link has expired. Please request a new one."}), 400

    hashed = generate_password_hash(password)
    with get_db() as conn:
        conn.execute("UPDATE users SET password = ? WHERE id = ?", (hashed, row["user_id"]))
        conn.execute("UPDATE password_reset_tokens SET used = 1 WHERE id = ?", (row["id"],))
        conn.commit()

    return jsonify({"ok": True, "message": "Password updated successfully. You can now sign in."})


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


# ---------------------------------------------------------------------------
# Customer dashboard API
# ---------------------------------------------------------------------------

def require_auth():
    """Return user_id from session or None."""
    return session.get("user_id")


@app.route("/api/customer/seed", methods=["POST"])
def customer_seed():
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    seed_demo_data(uid)
    return jsonify({"ok": True})


@app.route("/api/customer/overview", methods=["GET"])
def customer_overview():
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    with get_db() as conn:
        orders_count   = conn.execute("SELECT COUNT(*) FROM orders   WHERE user_id=?", (uid,)).fetchone()[0]
        bookings_count = conn.execute("SELECT COUNT(*) FROM bookings WHERE user_id=? AND status IN ('pending','confirmed')", (uid,)).fetchone()[0]
        addr_count     = conn.execute("SELECT COUNT(*) FROM addresses WHERE user_id=?", (uid,)).fetchone()[0]
        row            = conn.execute("SELECT points, tier FROM rewards WHERE user_id=?", (uid,)).fetchone()
        points = row["points"] if row else 0
        tier   = row["tier"]   if row else "Bronze"
    return jsonify({"ok": True, "overview": {
        "orders": orders_count, "active_bookings": bookings_count,
        "addresses": addr_count, "points": points, "tier": tier,
    }})


# ── Orders ─────────────────────────────────────────────────────────────────

@app.route("/api/customer/orders", methods=["GET"])
def customer_orders():
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    import json as _json
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM orders WHERE user_id=? ORDER BY created_at DESC", (uid,)
        ).fetchall()
    orders = []
    for r in rows:
        orders.append({
            "id": r["id"], "order_ref": r["order_ref"], "status": r["status"],
            "items": _json.loads(r["items_json"]), "total_amount": r["total_amount"],
            "tracking_number": r["tracking_number"], "tracking_status": r["tracking_status"],
            "created_at": r["created_at"],
        })
    return jsonify({"ok": True, "orders": orders})


@app.route("/api/customer/orders/<int:order_id>/cancel", methods=["POST"])
def cancel_order(order_id):
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    with get_db() as conn:
        row = conn.execute("SELECT * FROM orders WHERE id=? AND user_id=?", (order_id, uid)).fetchone()
        if not row:
            return jsonify({"ok": False, "error": "Order not found."}), 404
        if row["status"] not in ("processing", "confirmed"):
            return jsonify({"ok": False, "error": f"Cannot cancel an order with status '{row['status']}'."}), 400
        conn.execute("UPDATE orders SET status='cancelled', tracking_status=NULL WHERE id=?", (order_id,))
        conn.commit()
    return jsonify({"ok": True, "message": "Order cancelled."})


@app.route("/api/customer/orders/<int:order_id>/track", methods=["GET"])
def track_order(order_id):
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    with get_db() as conn:
        row = conn.execute("SELECT * FROM orders WHERE id=? AND user_id=?", (order_id, uid)).fetchone()
    if not row:
        return jsonify({"ok": False, "error": "Order not found."}), 404
    return jsonify({"ok": True, "tracking": {
        "order_ref": row["order_ref"], "tracking_number": row["tracking_number"],
        "tracking_status": row["tracking_status"], "order_status": row["status"],
    }})


# ── Bookings ────────────────────────────────────────────────────────────────

@app.route("/api/customer/bookings", methods=["GET"])
def customer_bookings():
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM bookings WHERE user_id=? ORDER BY booking_date DESC", (uid,)
        ).fetchall()
    return jsonify({"ok": True, "bookings": [dict(r) for r in rows]})


@app.route("/api/customer/bookings/<int:booking_id>/cancel", methods=["POST"])
def cancel_booking(booking_id):
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    with get_db() as conn:
        row = conn.execute("SELECT * FROM bookings WHERE id=? AND user_id=?", (booking_id, uid)).fetchone()
        if not row:
            return jsonify({"ok": False, "error": "Booking not found."}), 404
        if row["status"] in ("cancelled", "completed"):
            return jsonify({"ok": False, "error": f"Cannot cancel a booking with status '{row['status']}'."}), 400
        conn.execute("UPDATE bookings SET status='cancelled' WHERE id=?", (booking_id,))
        conn.commit()
    return jsonify({"ok": True, "message": "Booking cancelled."})


# ── Refunds ─────────────────────────────────────────────────────────────────

@app.route("/api/customer/refunds", methods=["GET"])
def customer_refunds():
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    with get_db() as conn:
        rows = conn.execute(
            "SELECT r.*, o.order_ref FROM refunds r LEFT JOIN orders o ON r.order_id=o.id WHERE r.user_id=? ORDER BY r.created_at DESC",
            (uid,)
        ).fetchall()
    return jsonify({"ok": True, "refunds": [dict(r) for r in rows]})


@app.route("/api/customer/refunds", methods=["POST"])
def request_refund():
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    data     = request.get_json(force=True)
    order_id = data.get("order_id")
    reason   = (data.get("reason") or "").strip()
    if not order_id:
        return jsonify({"ok": False, "error": "order_id is required."}), 400
    with get_db() as conn:
        order = conn.execute("SELECT * FROM orders WHERE id=? AND user_id=?", (order_id, uid)).fetchone()
        if not order:
            return jsonify({"ok": False, "error": "Order not found."}), 404
        if order["status"] not in ("cancelled", "delivered"):
            return jsonify({"ok": False, "error": "Refunds can only be requested for delivered or cancelled orders."}), 400
        existing = conn.execute("SELECT id FROM refunds WHERE order_id=? AND user_id=? AND status!='rejected'", (order_id, uid)).fetchone()
        if existing:
            return jsonify({"ok": False, "error": "A refund request already exists for this order."}), 409
        conn.execute(
            "INSERT INTO refunds (order_id,user_id,amount,reason,status) VALUES (?,?,?,?,'pending')",
            (order_id, uid, order["total_amount"], reason),
        )
        conn.commit()
    return jsonify({"ok": True, "message": "Refund request submitted."})


# ── Payment Methods ─────────────────────────────────────────────────────────

@app.route("/api/customer/payment-methods", methods=["GET"])
def get_payment_methods():
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM payment_methods WHERE user_id=? ORDER BY is_default DESC, created_at DESC", (uid,)).fetchall()
    return jsonify({"ok": True, "methods": [dict(r) for r in rows]})


@app.route("/api/customer/payment-methods", methods=["POST"])
def add_payment_method():
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    data  = request.get_json(force=True)
    mtype = (data.get("type")  or "card").strip().lower()
    label = (data.get("label") or "").strip()
    last4 = (data.get("last4") or "").strip()
    if not label:
        return jsonify({"ok": False, "error": "Label is required."}), 400
    with get_db() as conn:
        count = conn.execute("SELECT COUNT(*) FROM payment_methods WHERE user_id=?", (uid,)).fetchone()[0]
        is_default = 1 if count == 0 else 0
        conn.execute(
            "INSERT INTO payment_methods (user_id,type,label,last4,is_default) VALUES (?,?,?,?,?)",
            (uid, mtype, label, last4, is_default),
        )
        conn.commit()
    return jsonify({"ok": True, "message": "Payment method added."})


@app.route("/api/customer/payment-methods/<int:method_id>", methods=["DELETE"])
def delete_payment_method(method_id):
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    with get_db() as conn:
        row = conn.execute("SELECT * FROM payment_methods WHERE id=? AND user_id=?", (method_id, uid)).fetchone()
        if not row:
            return jsonify({"ok": False, "error": "Payment method not found."}), 404
        conn.execute("DELETE FROM payment_methods WHERE id=?", (method_id,))
        if row["is_default"]:
            conn.execute(
                "UPDATE payment_methods SET is_default=1 WHERE user_id=? ORDER BY created_at DESC LIMIT 1", (uid,)
            )
        conn.commit()
    return jsonify({"ok": True, "message": "Payment method removed."})


@app.route("/api/customer/payment-methods/<int:method_id>/default", methods=["PATCH"])
def set_default_payment(method_id):
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    with get_db() as conn:
        if not conn.execute("SELECT id FROM payment_methods WHERE id=? AND user_id=?", (method_id, uid)).fetchone():
            return jsonify({"ok": False, "error": "Payment method not found."}), 404
        conn.execute("UPDATE payment_methods SET is_default=0 WHERE user_id=?", (uid,))
        conn.execute("UPDATE payment_methods SET is_default=1 WHERE id=?", (method_id,))
        conn.commit()
    return jsonify({"ok": True})


# ── Addresses ───────────────────────────────────────────────────────────────

@app.route("/api/customer/addresses", methods=["GET"])
def get_addresses():
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM addresses WHERE user_id=? ORDER BY is_default DESC, id DESC", (uid,)).fetchall()
    return jsonify({"ok": True, "addresses": [dict(r) for r in rows]})


@app.route("/api/customer/addresses", methods=["POST"])
def add_address():
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    d = request.get_json(force=True)
    required = ["full_name", "line1", "city", "state", "pincode"]
    for f in required:
        if not (d.get(f) or "").strip():
            return jsonify({"ok": False, "error": f"'{f}' is required."}), 400
    with get_db() as conn:
        count = conn.execute("SELECT COUNT(*) FROM addresses WHERE user_id=?", (uid,)).fetchone()[0]
        is_default = 1 if count == 0 else int(bool(d.get("is_default")))
        if is_default:
            conn.execute("UPDATE addresses SET is_default=0 WHERE user_id=?", (uid,))
        conn.execute(
            "INSERT INTO addresses (user_id,label,full_name,line1,line2,city,state,pincode,phone,is_default) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (uid, (d.get("label") or "Home").strip(), d["full_name"].strip(),
             d["line1"].strip(), (d.get("line2") or "").strip(),
             d["city"].strip(), d["state"].strip(), d["pincode"].strip(),
             (d.get("phone") or "").strip(), is_default),
        )
        conn.commit()
    return jsonify({"ok": True, "message": "Address added."})


@app.route("/api/customer/addresses/<int:addr_id>", methods=["PATCH"])
def update_address(addr_id):
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    d = request.get_json(force=True)
    with get_db() as conn:
        if not conn.execute("SELECT id FROM addresses WHERE id=? AND user_id=?", (addr_id, uid)).fetchone():
            return jsonify({"ok": False, "error": "Address not found."}), 404
        conn.execute("""UPDATE addresses SET label=?,full_name=?,line1=?,line2=?,city=?,state=?,pincode=?,phone=? WHERE id=?""",
            ((d.get("label") or "Home").strip(), (d.get("full_name") or "").strip(),
             (d.get("line1") or "").strip(), (d.get("line2") or "").strip(),
             (d.get("city") or "").strip(), (d.get("state") or "").strip(),
             (d.get("pincode") or "").strip(), (d.get("phone") or "").strip(), addr_id))
        conn.commit()
    return jsonify({"ok": True, "message": "Address updated."})


@app.route("/api/customer/addresses/<int:addr_id>", methods=["DELETE"])
def delete_address(addr_id):
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    with get_db() as conn:
        if not conn.execute("SELECT id FROM addresses WHERE id=? AND user_id=?", (addr_id, uid)).fetchone():
            return jsonify({"ok": False, "error": "Address not found."}), 404
        conn.execute("DELETE FROM addresses WHERE id=?", (addr_id,))
        conn.commit()
    return jsonify({"ok": True, "message": "Address deleted."})


@app.route("/api/customer/addresses/<int:addr_id>/default", methods=["PATCH"])
def set_default_address(addr_id):
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    with get_db() as conn:
        if not conn.execute("SELECT id FROM addresses WHERE id=? AND user_id=?", (addr_id, uid)).fetchone():
            return jsonify({"ok": False, "error": "Address not found."}), 404
        conn.execute("UPDATE addresses SET is_default=0 WHERE user_id=?", (uid,))
        conn.execute("UPDATE addresses SET is_default=1 WHERE id=?", (addr_id,))
        conn.commit()
    return jsonify({"ok": True})


# ── Rewards & Coupons ───────────────────────────────────────────────────────

@app.route("/api/customer/rewards", methods=["GET"])
def customer_rewards():
    uid = require_auth()
    if not uid:
        return jsonify({"ok": False, "error": "Not authenticated."}), 401
    with get_db() as conn:
        rw  = conn.execute("SELECT * FROM rewards WHERE user_id=?", (uid,)).fetchone()
        cps = conn.execute("SELECT * FROM coupons WHERE user_id=? AND used=0 ORDER BY expires_at ASC", (uid,)).fetchall()
    points = rw["points"] if rw else 0
    tier   = rw["tier"]   if rw else "Bronze"
    tier_thresholds = {"Bronze": 0, "Silver": 1000, "Gold": 5000}
    next_tier = {"Bronze": ("Silver", 1000), "Silver": ("Gold", 5000), "Gold": (None, None)}
    nt_name, nt_pts = next_tier[tier]
    progress = 0
    if nt_pts:
        cur_floor = tier_thresholds[tier]
        progress = min(100, int((points - cur_floor) / (nt_pts - cur_floor) * 100))
    return jsonify({"ok": True, "rewards": {
        "points": points, "tier": tier,
        "next_tier": nt_name, "next_tier_points": nt_pts, "progress": progress,
        "coupons": [dict(c) for c in cps],
    }})


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug)
