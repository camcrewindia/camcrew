import os

# Set the environment variable for the database connection BEFORE importing app
os.environ["RENDER_DATABASE_URL"] = "postgresql://camcrewindia_user:OtYug8HJmROYnDqpCTF7v0bBGxwZeof3@dpg-d9k4lfbm8hqs73bl2jq0-a.oregon-postgres.render.com/camcrewindia"

from werkzeug.security import generate_password_hash
from app import get_db

email = "admin@cc.in"
password = "admin@cc.in"
hashed_password = generate_password_hash(password)

with get_db() as conn:
    try:
        # Check if user already exists
        row = conn.execute("SELECT * FROM users WHERE email=%s", (email,)).fetchone()
        if row:
            # Update password and role if already exists
            conn.execute("UPDATE users SET password=%s, role=%s WHERE email=%s", (hashed_password, 'admin', email))
            print("Admin user already existed and was updated successfully.")
        else:
            # Insert new user
            conn.execute(
                "INSERT INTO users (email, password, role, display_name) VALUES (%s, %s, %s, %s)",
                (email, hashed_password, 'admin', 'Admin')
            )
            print("Admin user created successfully.")
    except Exception as e:
        print(f"Error creating admin user: {e}")
